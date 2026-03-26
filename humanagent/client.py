"""
HumanAgent Python SDK
Human checkpoint infrastructure for AI workflows.

Usage:
    from humanagent import HumanAgent

    client = HumanAgent(api_key="ha_live_...")
    result = client.checkpoint(
        task="Review NDA for compliance gaps",
        credential="bar_licensed:US",
        sla="30min",
        budget=25.00
    )
"""

import time
import requests
from typing import Optional, Dict, Any
from .exceptions import (
    HumanAgentError,
    AuthenticationError,
    CheckpointNotFoundError,
    CheckpointExpiredError,
)


class HumanAgent:
    """Client for the HumanAgent API."""

    DEFAULT_BASE_URL = "https://humanagent.net"

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        timeout: int = 30,
    ):
        if not api_key or not api_key.startswith(("ha_live_", "ha_test_")):
            raise AuthenticationError("API key must start with 'ha_live_' or 'ha_test_'")

        self.api_key = api_key
        self.base_url = (base_url or self.DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        })

    def _request(self, method: str, path: str, **kwargs) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        kwargs.setdefault("timeout", self.timeout)

        resp = self.session.request(method, url, **kwargs)

        if resp.status_code == 401:
            raise AuthenticationError("Invalid API key")
        if resp.status_code == 404:
            raise CheckpointNotFoundError(resp.json().get("error", "Not found"))
        if resp.status_code == 410:
            raise CheckpointExpiredError(resp.json().get("error", "Expired"))
        if not resp.ok:
            error_msg = resp.json().get("error", resp.text) if resp.text else resp.reason
            raise HumanAgentError(f"API error ({resp.status_code}): {error_msg}")

        return resp.json()

    def create_checkpoint(
        self,
        task: str,
        credential: Optional[str] = None,
        sla: str = "1hr",
        budget: Optional[float] = None,
        priority: str = "standard",
        payload_url: Optional[str] = None,
        payload_meta: Optional[Dict] = None,
        callback_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a new checkpoint.

        Args:
            task: Description of what the human needs to do.
            credential: Required credential, e.g. "bar_licensed:US" or "cpa".
            sla: Time limit. "90s", "5min", "30min", "1hr", "4hr".
            budget: Maximum USD willing to pay.
            priority: "urgent", "standard", or "batch".
            payload_url: URL to a document/file the human needs to review.
            payload_meta: Additional context as a dict.
            callback_url: Webhook URL to receive the result.

        Returns:
            Dict with checkpoint_id, status, expires_at, poll_url.
        """
        body: Dict[str, Any] = {"task": task, "sla": sla, "priority": priority}
        if credential:
            body["credential"] = credential
        if budget is not None:
            body["budget"] = budget
        if payload_url:
            body["payload_url"] = payload_url
        if payload_meta:
            body["payload_meta"] = payload_meta
        if callback_url:
            body["callback_url"] = callback_url

        return self._request("POST", "/api/v1/checkpoint", json=body)

    def get_checkpoint(self, checkpoint_id: str) -> Dict[str, Any]:
        """
        Poll a checkpoint's status.

        Returns:
            Dict with status, sla_remaining, result (if completed), audit_hash, etc.
        """
        return self._request("GET", f"/api/v1/checkpoint/{checkpoint_id}")

    def checkpoint(
        self,
        task: str,
        credential: Optional[str] = None,
        sla: str = "1hr",
        budget: Optional[float] = None,
        priority: str = "standard",
        payload_url: Optional[str] = None,
        payload_meta: Optional[Dict] = None,
        callback_url: Optional[str] = None,
        wait: bool = True,
        poll_interval: int = 5,
        max_wait: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Create a checkpoint and optionally wait for the result.

        If wait=True (default), polls until completed or expired.
        If wait=False, returns immediately after creation.

        Args:
            ... (same as create_checkpoint)
            wait: Block until result. Default True.
            poll_interval: Seconds between polls. Default 5.
            max_wait: Maximum seconds to wait. Default None (wait until SLA expires).

        Returns:
            Dict with full checkpoint data including result if completed.
        """
        created = self.create_checkpoint(
            task=task,
            credential=credential,
            sla=sla,
            budget=budget,
            priority=priority,
            payload_url=payload_url,
            payload_meta=payload_meta,
            callback_url=callback_url,
        )

        if not wait:
            return created

        checkpoint_id = created["checkpoint_id"]
        start = time.time()

        while True:
            result = self.get_checkpoint(checkpoint_id)

            if result["status"] in ("completed", "expired", "rejected"):
                return result

            if max_wait and (time.time() - start) > max_wait:
                return result

            time.sleep(poll_interval)

    def __repr__(self):
        masked = self.api_key[:12] + "..."
        return f"HumanAgent(api_key='{masked}', base_url='{self.base_url}')"
