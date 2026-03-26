import pytest
from humanagent import HumanAgent
from humanagent.exceptions import AuthenticationError


def test_client_init():
    client = HumanAgent(api_key="ha_test_abc123", base_url="http://localhost:3000")
    assert client.api_key == "ha_test_abc123"
    assert client.base_url == "http://localhost:3000"


def test_client_init_live_key():
    client = HumanAgent(api_key="ha_live_abc123")
    assert client.base_url == "https://humanagent.net"


def test_client_invalid_key_no_prefix():
    with pytest.raises(AuthenticationError):
        HumanAgent(api_key="invalid_no_prefix")


def test_client_invalid_key_empty():
    with pytest.raises(AuthenticationError):
        HumanAgent(api_key="")


def test_client_repr():
    client = HumanAgent(api_key="ha_test_abc123")
    assert "ha_test_abc1..." in repr(client)
    assert "humanagent.net" in repr(client)


def test_client_default_base_url():
    client = HumanAgent(api_key="ha_live_abc123")
    assert client.base_url == "https://humanagent.net"


def test_client_custom_base_url():
    client = HumanAgent(api_key="ha_test_abc123", base_url="http://localhost:3000/")
    assert client.base_url == "http://localhost:3000"  # trailing slash stripped


def test_client_custom_timeout():
    client = HumanAgent(api_key="ha_test_abc123", timeout=60)
    assert client.timeout == 60


def test_client_session_headers():
    client = HumanAgent(api_key="ha_test_abc123")
    assert client.session.headers["Authorization"] == "Bearer ha_test_abc123"
    assert client.session.headers["Content-Type"] == "application/json"


def test_client_default_timeout():
    client = HumanAgent(api_key="ha_test_abc123")
    assert client.timeout == 30


def test_client_none_key():
    with pytest.raises(AuthenticationError):
        HumanAgent(api_key=None)
