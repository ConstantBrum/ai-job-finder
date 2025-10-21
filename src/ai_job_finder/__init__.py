"""Automation helpers for running job searches through CUA."""

from .config import JobSearchPreferences, CUASettings, Credential, LoginProfile, load_configuration
from .automation import JobSearchAutomation, SessionResult

__all__ = [
    "JobSearchPreferences",
    "CUASettings",
    "Credential",
    "LoginProfile",
    "load_configuration",
    "JobSearchAutomation",
    "SessionResult",
]
