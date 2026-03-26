"""Tests for the HumanAgent Python SDK."""

import unittest
from unittest.mock import patch, MagicMock
from humanagent import HumanAgent
from humanagent.exceptions import (
    AuthenticationError,
    CheckpointNotFoundError,
    CheckpointExpiredError,
    HumanAgentError,
)


class TestClientInit(unittest.TestCase):
    """Test client initialization and API key validation."""

    def test_valid_live_key(self):
        client = HumanAgent(api_key="ha_live_abc123")
        assert client.api_key == "ha_live_abc123"
        assert client.base_url == "https://humanagent.net"

    def test_valid_test_key(self):
        client = HumanAgent(api_key="ha_test_abc123")
        assert client.api_key == "ha_test_abc123"

    def test_invalid_key_raises(self):
        with self.assertRaises(AuthenticationError):
            HumanAgent(api_key="bad_key")

    def test_empty_key_raises(self):
        with self.assertRaises(AuthenticationError):
            HumanAgent(api_key="")

    def test_custom_base_url(self):
        client = HumanAgent(api_key="ha_live_abc123", base_url="http://localhost:3000")
        assert client.base_url == "http://localhost:3000"

    def test_repr_masks_key(self):
        client = HumanAgent(api_key="ha_live_abc123def456")
        r = repr(client)
        assert "ha_live_abc1..." in r
        assert "abc123def456" not in r


class TestCreateCheckpoint(unittest.TestCase):
    """Test checkpoint creation."""

    @patch("humanagent.client.requests.Session")
    def test_create_checkpoint_success(self, MockSession):
        mock_resp = MagicMock()
        mock_resp.status_code = 201
        mock_resp.ok = True
        mock_resp.json.return_value = {
            "checkpoint_id": "abc-123",
            "status": "pending",
            "expires_at": "2026-03-26T06:00:00Z",
            "poll_url": "/api/v1/checkpoint/abc-123",
        }
        MockSession.return_value.request.return_value = mock_resp

        client = HumanAgent(api_key="ha_live_test123")
        result = client.create_checkpoint(
            task="Review NDA",
            credential="bar_licensed:US",
            sla="30min",
            budget=25.00,
        )

        assert result["checkpoint_id"] == "abc-123"
        assert result["status"] == "pending"

    @patch("humanagent.client.requests.Session")
    def test_create_checkpoint_auth_error(self, MockSession):
        mock_resp = MagicMock()
        mock_resp.status_code = 401
        mock_resp.ok = False
        MockSession.return_value.request.return_value = mock_resp

        client = HumanAgent(api_key="ha_live_test123")
        with self.assertRaises(AuthenticationError):
            client.create_checkpoint(task="Review NDA")


class TestGetCheckpoint(unittest.TestCase):
    """Test checkpoint polling."""

    @patch("humanagent.client.requests.Session")
    def test_get_checkpoint_completed(self, MockSession):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.ok = True
        mock_resp.json.return_value = {
            "checkpoint_id": "abc-123",
            "status": "completed",
            "result": {"approved": True, "notes": "Looks good"},
            "audit_hash": "sha256:deadbeef",
        }
        MockSession.return_value.request.return_value = mock_resp

        client = HumanAgent(api_key="ha_live_test123")
        result = client.get_checkpoint("abc-123")

        assert result["status"] == "completed"
        assert result["result"]["approved"] is True

    @patch("humanagent.client.requests.Session")
    def test_get_checkpoint_not_found(self, MockSession):
        mock_resp = MagicMock()
        mock_resp.status_code = 404
        mock_resp.ok = False
        mock_resp.json.return_value = {"error": "Checkpoint not found"}
        MockSession.return_value.request.return_value = mock_resp

        client = HumanAgent(api_key="ha_live_test123")
        with self.assertRaises(CheckpointNotFoundError):
            client.get_checkpoint("nonexistent")


class TestCheckpointWait(unittest.TestCase):
    """Test checkpoint with wait/poll behavior."""

    @patch("humanagent.client.requests.Session")
    def test_checkpoint_no_wait(self, MockSession):
        mock_resp = MagicMock()
        mock_resp.status_code = 201
        mock_resp.ok = True
        mock_resp.json.return_value = {
            "checkpoint_id": "abc-123",
            "status": "pending",
        }
        MockSession.return_value.request.return_value = mock_resp

        client = HumanAgent(api_key="ha_live_test123")
        result = client.checkpoint(task="Review NDA", wait=False)

        assert result["status"] == "pending"
        # Should only call once (create), not poll
        MockSession.return_value.request.assert_called_once()


if __name__ == "__main__":
    unittest.main()
