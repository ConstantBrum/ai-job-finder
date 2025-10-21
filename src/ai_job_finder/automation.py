from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Sequence

from .client import CUAClient, Message
from .config import JobSearchPreferences, LoginProfile


_DEFAULT_SYSTEM_PROMPT = (
    "You are an expert job search assistant. Use the provided browser to gather "
    "relevant job opportunities from sites like Google Jobs, LinkedIn, and other "
    "reputable sources. Always respect the user's filters and report your "
    "findings in a concise, structured summary."
)


@dataclass(slots=True)
class SessionResult:
    session_id: str
    status: str
    data: dict[str, Any]


class JobSearchAutomation:
    """High level helper that wires the configuration with the CUA API."""

    def __init__(
        self,
        client: CUAClient,
        *,
        system_prompt: str = _DEFAULT_SYSTEM_PROMPT,
        logins: Sequence[LoginProfile] | None = None,
    ) -> None:
        self.client = client
        self.system_prompt = system_prompt
        self.logins = list(logins or [])

    def build_user_prompt(self, preferences: JobSearchPreferences) -> str:
        """Create the instruction block sent to CUA for execution."""

        lines = [
            "Objective: find active job postings that match the filters below.",
            preferences.describe(),
            "If a login is required, use the provided credentials and confirm the login succeeded before searching.",
            "Capture the job title, company, location, salary information, and the URL for each promising listing.",
            "Return your findings as structured bullet points grouped by platform.",
        ]
        if self.logins:
            lines.append("Login instructions:")
            for login in self.logins:
                credential = login.credential
                lines.append(
                    f"- {login.site_name}: navigate to {login.login_url}, "
                    f"sign in as {credential.username} using the stored password."
                )
                if credential.totp_secret:
                    lines.append(
                        "  Use the stored TOTP secret if a two-factor token is requested."
                    )
                if login.post_login_urls:
                    lines.append(
                        "  After logging in, visit these pages before searching: "
                        + ", ".join(login.post_login_urls)
                    )

        return "\n".join(lines)

    def run(
        self,
        *,
        preferences: JobSearchPreferences,
        session_title: str = "Job search session",
        persona_id: str | None = None,
        poll_interval: float = 2.0,
        timeout_seconds: float = 180.0,
    ) -> SessionResult:
        session = self.client.create_session(title=session_title, persona_id=persona_id)
        session_id = session["id"]
        messages: Iterable[Message] = (
            Message(role="system", content=self.system_prompt),
            Message(role="user", content=self.build_user_prompt(preferences)),
        )
        self.client.post_messages(session_id, messages)
        data = self.client.wait_for_completion(
            session_id,
            poll_interval=poll_interval,
            timeout=timeout_seconds,
        )
        return SessionResult(session_id=session_id, status=data.get("status", "unknown"), data=data)
