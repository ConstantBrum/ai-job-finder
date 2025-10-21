"""Automation logic for searching jobs on LinkedIn using the control API."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Mapping, Sequence
from urllib.parse import urlencode

from .computer_control import ComputerControlAPI, UserConfirmation, UserConfirmationProvider


LINKEDIN_SEARCH_URL = "https://www.linkedin.com/jobs/search/"


@dataclass(slots=True)
class LinkedInJobSearchFilters:
    """Normalized representation of the supported LinkedIn search filters."""

    keywords: str | None = None
    location: str | None = None
    experience_level: Sequence[str] | None = None
    date_posted: str | None = None
    job_type: Sequence[str] | None = None

    def to_query_params(self) -> Mapping[str, str]:
        """Return LinkedIn job search query parameters for the configured filters."""

        params: dict[str, str] = {}
        if self.keywords:
            params["keywords"] = self.keywords
        if self.location:
            params["location"] = self.location
        if self.experience_level:
            params["f_E"] = ",".join(self.experience_level)
        if self.date_posted:
            params["f_TPR"] = self.date_posted
        if self.job_type:
            params["f_JT"] = ",".join(self.job_type)
        return params

    @classmethod
    def from_task(cls, filters: Mapping[str, object] | None) -> "LinkedInJobSearchFilters":
        """Instantiate filters from a JSON-like ``filters`` dictionary."""

        if not filters:
            return cls()

        def _str_sequence(value: object | None) -> Sequence[str] | None:
            if value is None:
                return None
            if isinstance(value, str):
                return (value,)
            if isinstance(value, Sequence):
                return tuple(str(v) for v in value)
            raise TypeError("Filter sequence values must be str or sequence of str")

        return cls(
            keywords=str(filters.get("keywords")) if filters.get("keywords") else None,
            location=str(filters.get("location")) if filters.get("location") else None,
            experience_level=_str_sequence(filters.get("experience_level")),
            date_posted=str(filters.get("date_posted")) if filters.get("date_posted") else None,
            job_type=_str_sequence(filters.get("job_type")),
        )


@dataclass(slots=True)
class JobPosting:
    """Structured representation of a LinkedIn job card."""

    job_id: str
    title: str
    company: str
    location: str
    listed_at: str
    job_url: str

    def to_dict(self) -> dict[str, str]:
        return {
            "job_id": self.job_id,
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "listed_at": self.listed_at,
            "job_url": self.job_url,
        }


@dataclass
class LinkedInJobSearchAgent:
    """Agent that orchestrates a LinkedIn job search via the control API."""

    control: ComputerControlAPI
    confirmation_provider: UserConfirmationProvider
    base_url: str = LINKEDIN_SEARCH_URL
    job_card_selector: str = "job-card-list"
    human_pause_seconds: float = 1.5
    _last_results: list[JobPosting] = field(default_factory=list, init=False)

    def run(self, goal: str, filters: Mapping[str, object] | None = None) -> list[dict[str, str]]:
        """Execute a job search and return deduplicated job postings."""

        self._validate_goal(goal)
        normalized_filters = LinkedInJobSearchFilters.from_task(filters)
        query_params = normalized_filters.to_query_params()

        self._load_search_results(goal, query_params)
        raw_results = self._collect_job_cards()
        unique_results = self._deduplicate_jobs(raw_results)
        self._last_results = unique_results
        return [job.to_dict() for job in unique_results]

    def _validate_goal(self, goal: str) -> None:
        if not goal:
            raise ValueError("A natural-language goal is required for the job search.")

    def _load_search_results(self, goal: str, query_params: Mapping[str, str]) -> None:
        params = {"keywords": goal, **query_params}
        query_string = urlencode(params)
        self.control.open_url(f"{self.base_url}?{query_string}")
        self.control.wait_for(self.job_card_selector, timeout=15)

    def _collect_job_cards(self) -> list[JobPosting]:
        card_count_raw = self.control.get_attr(self.job_card_selector, "data-card-count")
        try:
            card_count = int(card_count_raw) if card_count_raw else 0
        except ValueError:
            card_count = 0

        jobs: list[JobPosting] = []
        for index in range(card_count):
            job_id = self.control.get_attr(self._card_selector(index), "data-job-id") or str(index)
            title = self.control.get_text(self._card_field_selector(index, "title"))
            company = self.control.get_text(self._card_field_selector(index, "company"))
            location = self.control.get_text(self._card_field_selector(index, "location"))
            listed_at = self.control.get_text(self._card_field_selector(index, "listed_at"))
            job_url = self.control.get_attr(self._card_selector(index), "data-job-url") or ""
            jobs.append(
                JobPosting(
                    job_id=job_id.strip(),
                    title=title.strip(),
                    company=company.strip(),
                    location=location.strip(),
                    listed_at=listed_at.strip(),
                    job_url=job_url.strip(),
                )
            )
        return jobs

    def _card_selector(self, index: int) -> str:
        return f"{self.job_card_selector}[{index}]"

    def _card_field_selector(self, index: int, field: str) -> str:
        return f"{self.job_card_selector}[{index}].{field}"

    def _deduplicate_jobs(self, jobs: Iterable[JobPosting]) -> list[JobPosting]:
        seen_ids: set[str] = set()
        seen_identity: set[tuple[str, str, str]] = set()
        deduped: list[JobPosting] = []

        for job in jobs:
            job_id = job.job_id.strip()
            identity = (
                job.title.strip().lower(),
                job.company.strip().lower(),
                job.location.strip().lower(),
            )

            if job_id:
                if job_id in seen_ids:
                    continue
                seen_ids.add(job_id)

            if identity in seen_identity:
                continue

            seen_identity.add(identity)
            deduped.append(job)

        return deduped

    def request_irreversible_action(self, action_description: str) -> UserConfirmation:
        """Ask the user before triggering any irreversible behavior."""

        confirmation = self.confirmation_provider.confirm(action_description)
        if not confirmation.allowed:
            raise PermissionError(confirmation.reason or "Action not permitted by user")
        return confirmation

    @property
    def last_results(self) -> list[dict[str, str]]:
        return [job.to_dict() for job in self._last_results]
