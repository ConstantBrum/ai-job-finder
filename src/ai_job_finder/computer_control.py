"""Abstractions for the computer-control API used by the LinkedIn agent.

This module defines a protocol for the browser automation API described in the
project brief.  By relying on a protocol rather than concrete implementations we
can unit test the agent easily by providing lightweight fakes while the real
runtime injects production bindings.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Protocol

try:  # pragma: no cover - optional dependency import
    import httpx
except Exception:  # pragma: no cover - httpx remains optional for test doubles
    httpx = None  # type: ignore[assignment]


class ComputerControlAPI(Protocol):
    """Protocol that mirrors the computer-control API available at runtime."""

    def open_url(self, url: str) -> None:
        """Navigate the active browser tab to ``url``."""

    def wait_for(self, target: str, timeout: float | None = None) -> None:
        """Block until ``target`` is present in the DOM or timeout expires."""

    def click(self, target: str) -> None:
        """Click on the element identified by ``target``."""

    def type(self, text: str, into: str) -> None:
        """Type ``text`` into the element referenced by ``into``."""

    def press_key(self, key: str) -> None:
        """Send a single key press such as ``"Enter"``."""

    def scroll(self, amount: int | None = None, to: str | None = None) -> None:
        """Scroll by a pixel ``amount`` or to a special position like ``"end"``."""

    def select(self, option: str, in_: str) -> None:
        """Select an ``option`` within a select element referenced by ``in_``."""

    def hover(self, target: str) -> None:
        """Hover over the element referenced by ``target``."""

    def get_text(self, target: str) -> str:
        """Return the ``innerText`` for ``target``."""

    def get_attr(self, target: str, attr: str) -> str | None:
        """Return an attribute value from ``target`` if it exists."""

    def screenshot(self, area: str | None = None, full: bool = False) -> str:
        """Capture a screenshot and return a path to the saved artifact."""

    def copy_to_clipboard(self, text: str) -> None:
        """Copy ``text`` to the system clipboard."""

    def save_file(self, path: str, content: str) -> None:
        """Persist ``content`` to ``path`` on the local filesystem."""


class LocalDockerComputerControl(ComputerControlAPI):
    """Implementation that targets a locally hosted CUA computer container.

    The local Docker runtime exposes the same REST API surface area as the cloud
    Computers service.  By default the container listens on ``http://127.0.0.1:11400``
    and identifies itself using the computer id ``local``.  The implementation
    delegates to ``httpx`` when available, but a custom ``transport`` callable can
    be supplied for testing without network access.
    """

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:11400",
        computer_id: str = "local",
        *,
        transport: Callable[[str, dict], dict] | None = None,
    ) -> None:
        if transport is None and httpx is None:  # pragma: no cover - exercised in runtime
            raise RuntimeError(
                "httpx is required to use LocalDockerComputerControl. Install with "
                "`pip install httpx`."
            )
        self.base_url = base_url.rstrip("/")
        self.computer_id = computer_id
        self._transport = transport

    def _perform(self, action: dict) -> dict:
        payload = {"actions": [action]}
        endpoint = f"{self.base_url}/v1/computers/{self.computer_id}:perform"
        if self._transport is not None:
            response_data = self._transport(endpoint, payload)
        else:  # pragma: no cover - relies on networked httpx client
            with httpx.Client(timeout=30.0) as client:  # type: ignore[arg-type]
                response = client.post(endpoint, json=payload)
                response.raise_for_status()
                response_data = response.json()
        results = response_data.get("results", [])
        if not results:
            return {}
        return results[0]

    def open_url(self, url: str) -> None:
        self._perform({"type": "open_url", "url": url})

    def wait_for(self, target: str, timeout: float | None = None) -> None:
        action: dict[str, object] = {"type": "wait_for", "selector": target}
        if timeout is not None:
            action["timeout"] = timeout
        self._perform(action)

    def click(self, target: str) -> None:
        self._perform({"type": "click", "selector": target})

    def type(self, text: str, into: str) -> None:
        self._perform({"type": "type", "selector": into, "text": text})

    def press_key(self, key: str) -> None:
        self._perform({"type": "press_key", "key": key})

    def scroll(self, amount: int | None = None, to: str | None = None) -> None:
        action: dict[str, object] = {"type": "scroll"}
        if amount is not None:
            action["amount"] = amount
        if to is not None:
            action["to"] = to
        self._perform(action)

    def select(self, option: str, in_: str) -> None:
        self._perform({"type": "select", "selector": in_, "option": option})

    def hover(self, target: str) -> None:
        self._perform({"type": "hover", "selector": target})

    def get_text(self, target: str) -> str:
        result = self._perform({"type": "get_text", "selector": target})
        return str(result.get("text", ""))

    def get_attr(self, target: str, attr: str) -> str | None:
        result = self._perform({"type": "get_attribute", "selector": target, "attribute": attr})
        value = result.get("value")
        return None if value is None else str(value)

    def screenshot(self, area: str | None = None, full: bool = False) -> str:
        action: dict[str, object] = {"type": "screenshot", "full": full}
        if area is not None:
            action["selector"] = area
        result = self._perform(action)
        return str(result.get("path", ""))

    def copy_to_clipboard(self, text: str) -> None:
        self._perform({"type": "copy_to_clipboard", "text": text})

    def save_file(self, path: str, content: str) -> None:
        self._perform({"type": "save_file", "path": path, "content": content})


@dataclass(frozen=True)
class UserConfirmation:
    """Represent a reversible or irreversible action confirmation result."""

    allowed: bool
    reason: str | None = None


class UserConfirmationProvider(Protocol):
    """Protocol used by the agent to ask for confirmation before actions."""

    def confirm(self, prompt: str) -> UserConfirmation:
        """Return a confirmation response for ``prompt``."""
