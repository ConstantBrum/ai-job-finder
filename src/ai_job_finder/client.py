from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any, Iterable

import requests


class CUAClientError(RuntimeError):
    """Represents an error returned by the CUA API."""


@dataclass(slots=True)
class Message:
    role: str
    content: str


class CUAClient:
    """Minimal HTTP client for the CUA API.

    The implementation is intentionally lightweight so it can be adapted to
    changes in the CUA API. The defaults follow the public SaaS deployment, but
    you can point ``base_url`` to a self-hosted instance as well.
    """

    def __init__(self, base_url: str, api_key: str, workspace_id: str | None = None):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )
        self.workspace_id = workspace_id

    def create_session(self, title: str, persona_id: str | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {"title": title}
        if persona_id:
            payload["persona_id"] = persona_id
        if self.workspace_id:
            payload["workspace_id"] = self.workspace_id

        response = self.session.post(f"{self.base_url}/browser_sessions", json=payload, timeout=30)
        self._ensure_success(response)
        return response.json()

    def post_messages(self, session_id: str, messages: Iterable[Message]) -> dict[str, Any]:
        payload = {"messages": [message.__dict__ for message in messages]}
        response = self.session.post(
            f"{self.base_url}/browser_sessions/{session_id}/messages",
            json=payload,
            timeout=30,
        )
        self._ensure_success(response)
        return response.json()

    def wait_for_completion(self, session_id: str, *, poll_interval: float, timeout: float) -> dict[str, Any]:
        start_time = time.monotonic()
        while True:
            response = self.session.get(
                f"{self.base_url}/browser_sessions/{session_id}",
                timeout=30,
            )
            self._ensure_success(response)
            data = response.json()
            status = data.get("status")
            if status in {"succeeded", "failed"}:
                return data
            if time.monotonic() - start_time > timeout:
                raise TimeoutError(
                    "Timed out waiting for the CUA session to finish processing instructions."
                )
            time.sleep(poll_interval)

    @staticmethod
    def _ensure_success(response: requests.Response) -> None:
        if response.ok:
            return
        try:
            payload = response.json()
        except ValueError:  # pragma: no cover - best effort error reporting
            payload = {"detail": response.text}
        raise CUAClientError(f"CUA request failed: {response.status_code} {payload}")
