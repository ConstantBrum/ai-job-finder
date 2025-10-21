from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Optional

import yaml


@dataclass(slots=True)
class Credential:
    """Represents a credential that CUA can use during a browsing session."""

    name: str
    username: str
    password: str
    totp_secret: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Credential":
        return cls(
            name=data["name"],
            username=data["username"],
            password=data["password"],
            totp_secret=data.get("totp_secret"),
        )


@dataclass(slots=True)
class LoginProfile:
    """Describes how to log in to a specific site (e.g. LinkedIn)."""

    site_name: str
    login_url: str
    credential: Credential
    post_login_urls: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LoginProfile":
        return cls(
            site_name=data["site_name"],
            login_url=data["login_url"],
            credential=Credential.from_dict(data["credential"]),
            post_login_urls=list(data.get("post_login_urls", [])),
        )


@dataclass(slots=True)
class JobSearchPreferences:
    roles: Optional[list[str]] = None
    industries: Optional[list[str]] = None
    seniority: Optional[str] = None
    locations: Optional[list[str]] = None
    remote_ok: Optional[bool] = None
    onsite_ok: Optional[bool] = None
    hybrid_ok: Optional[bool] = None
    keywords_include: Optional[list[str]] = None
    keywords_exclude: Optional[list[str]] = None
    languages_required: Optional[list[str]] = None
    languages_forbidden: Optional[list[str]] = None
    salary_min_eur: Optional[int] = None
    employment_type: Optional[str] = None
    schedule_prefs: Optional[list[str]] = None
    company_include: Optional[list[str]] = None
    company_exclude: Optional[list[str]] = None

    def describe(self) -> str:
        """Create a human readable summary that can be sent to CUA."""

        def format_list(values: Iterable[str]) -> str:
            return ", ".join(values)

        lines: list[str] = []

        if self.roles:
            lines.append(f"Roles of interest: {format_list(self.roles)}.")
        if self.industries:
            lines.append(f"Target industries: {format_list(self.industries)}.")
        if self.seniority:
            lines.append(f"Desired seniority: {self.seniority} level roles.")
        if self.locations:
            lines.append(f"Search locations: {format_list(self.locations)}.")

        work_modes = [
            (self.remote_ok, "remote"),
            (self.onsite_ok, "onsite"),
            (self.hybrid_ok, "hybrid"),
        ]
        enabled_modes = [label for flag, label in work_modes if flag]
        disabled_modes = [label for flag, label in work_modes if flag is False]
        if enabled_modes:
            lines.append(f"Acceptable working modes: {format_list(enabled_modes)}.")
        if disabled_modes:
            lines.append(f"Avoid opportunities that are strictly {format_list(disabled_modes)}.")

        if self.keywords_include:
            lines.append(f"Include postings containing: {format_list(self.keywords_include)}.")
        if self.keywords_exclude:
            lines.append(f"Reject postings mentioning: {format_list(self.keywords_exclude)}.")
        if self.languages_required:
            lines.append(f"Roles must list languages: {format_list(self.languages_required)}.")
        if self.languages_forbidden:
            lines.append(
                f"Ignore postings that require: {format_list(self.languages_forbidden)}."
            )
        if self.salary_min_eur is not None:
            lines.append(
                f"Only consider opportunities with salary >= €{self.salary_min_eur:,}."
            )
        if self.employment_type:
            lines.append(f"Employment type preference: {self.employment_type} roles.")
        if self.schedule_prefs:
            lines.append(f"Preferred schedules: {format_list(self.schedule_prefs)}.")
        if self.company_include:
            lines.append(f"Prioritise employers: {format_list(self.company_include)}.")
        if self.company_exclude:
            lines.append(f"Exclude employers: {format_list(self.company_exclude)}.")

        if not lines:
            lines.append("No filters were provided; use your judgement to find promising roles.")

        return "\n".join(lines)


@dataclass(slots=True)
class CUASettings:
    base_url: str
    api_key: str
    workspace_id: Optional[str] = None
    persona_id: Optional[str] = None
    poll_interval: float = 2.0
    timeout_seconds: float = 180.0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CUASettings":
        return cls(
            base_url=data["base_url"],
            api_key=data["api_key"],
            workspace_id=data.get("workspace_id"),
            persona_id=data.get("persona_id"),
            poll_interval=float(data.get("poll_interval", 2.0)),
            timeout_seconds=float(data.get("timeout_seconds", 180.0)),
        )


@dataclass(slots=True)
class AppConfig:
    cua: CUASettings
    preferences: JobSearchPreferences
    logins: list[LoginProfile] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AppConfig":
        cua_settings = CUASettings.from_dict(data["cua"])
        preferences = JobSearchPreferences(**data.get("preferences", {}))
        logins = [LoginProfile.from_dict(item) for item in data.get("logins", [])]
        return cls(cua=cua_settings, preferences=preferences, logins=logins)


def _expand_env_vars(value: Any) -> Any:
    if isinstance(value, str):
        return os.path.expandvars(value)
    if isinstance(value, list):
        return [_expand_env_vars(item) for item in value]
    if isinstance(value, dict):
        return {key: _expand_env_vars(item) for key, item in value.items()}
    return value


def load_configuration(path: Path | str) -> AppConfig:
    """Load application configuration from a YAML file."""

    file_path = Path(path)
    with file_path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    data = _expand_env_vars(data)
    return AppConfig.from_dict(data)
