from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest

from ai_job_finder.computer_control import (
    ComputerControlAPI,
    LocalDockerComputerControl,
    UserConfirmation,
    UserConfirmationProvider,
)
from ai_job_finder.linkedin_agent import (
    JobPosting,
    LinkedInJobSearchAgent,
    LinkedInJobSearchFilters,
)


@dataclass
class FakeConfirmationProvider(UserConfirmationProvider):
    allowed: bool = True
    reason: str | None = None

    def confirm(self, prompt: str) -> UserConfirmation:  # type: ignore[override]
        return UserConfirmation(allowed=self.allowed, reason=self.reason)


class FakeControl(ComputerControlAPI):
    def __init__(self, cards: list[JobPosting]):
        self.cards = cards
        self.opened_urls: list[str] = []
        self.waited_for: list[tuple[str, float | None]] = []

    def open_url(self, url: str) -> None:
        self.opened_urls.append(url)

    def wait_for(self, target: str, timeout: float | None = None) -> None:  # type: ignore[override]
        self.waited_for.append((target, timeout))

    def click(self, target: str) -> None:  # pragma: no cover - not used in tests
        raise NotImplementedError

    def type(self, text: str, into: str) -> None:  # pragma: no cover - not used in tests
        raise NotImplementedError

    def press_key(self, key: str) -> None:  # pragma: no cover - not used in tests
        raise NotImplementedError

    def scroll(self, amount: int | None = None, to: str | None = None) -> None:  # pragma: no cover
        raise NotImplementedError

    def select(self, option: str, in_: str) -> None:  # pragma: no cover - not used in tests
        raise NotImplementedError

    def hover(self, target: str) -> None:  # pragma: no cover - not used in tests
        raise NotImplementedError

    def get_text(self, target: str) -> str:
        index, field = self._parse_target(target)
        return getattr(self.cards[index], field)

    def get_attr(self, target: str, attr: str) -> str | None:
        if target == "job-card-list" and attr == "data-card-count":
            return str(len(self.cards))
        index, field = self._parse_target(target)
        mapping = {
            "data-job-id": self.cards[index].job_id,
            "data-job-url": self.cards[index].job_url,
        }
        return mapping.get(attr)

    def screenshot(self, area: str | None = None, full: bool = False) -> str:  # pragma: no cover
        raise NotImplementedError

    def copy_to_clipboard(self, text: str) -> None:  # pragma: no cover
        raise NotImplementedError

    def save_file(self, path: str, content: str) -> None:  # pragma: no cover
        raise NotImplementedError

    def _parse_target(self, target: str) -> tuple[int, str]:
        if "." not in target:
            index = int(target[target.find("[") + 1 : target.find("]")])
            return index, ""
        prefix, field = target.split(".")
        index = int(prefix[prefix.find("[") + 1 : prefix.find("]")])
        return index, field


def make_job(index: int, **overrides: Any) -> JobPosting:
    data = {
        "job_id": f"{1000 + index}",
        "title": f"Software Engineer {index}",
        "company": "OpenAI",
        "location": "Remote",
        "listed_at": "1 day ago",
        "job_url": f"https://www.linkedin.com/jobs/view/{1000 + index}/",
    }
    data.update(overrides)
    return JobPosting(**data)


def test_filters_from_task_normalizes_values() -> None:
    filters = LinkedInJobSearchFilters.from_task(
        {
            "keywords": "AI Engineer",
            "location": "San Francisco, CA",
            "experience_level": ["2", "3"],
            "job_type": "F",
        }
    )
    assert filters.to_query_params() == {
        "keywords": "AI Engineer",
        "location": "San Francisco, CA",
        "f_E": "2,3",
        "f_JT": "F",
    }


def test_agent_run_returns_deduplicated_results() -> None:
    cards = [
        make_job(1),
        make_job(2),
        make_job(2, job_id=""),
    ]
    control = FakeControl(cards)
    agent = LinkedInJobSearchAgent(control=control, confirmation_provider=FakeConfirmationProvider())

    results = agent.run("Search for machine learning roles", filters={"location": "Remote"})

    assert len(results) == 2
    assert control.opened_urls
    assert any("location=Remote" in url for url in control.opened_urls)


def test_request_irreversible_action_requires_confirmation() -> None:
    agent = LinkedInJobSearchAgent(
        control=FakeControl([make_job(1)]),
        confirmation_provider=FakeConfirmationProvider(allowed=False, reason="User declined"),
    )

    with pytest.raises(PermissionError, match="User declined"):
        agent.request_irreversible_action("Apply to job")


def test_local_docker_control_builds_requests() -> None:
    captured: list[tuple[str, dict]] = []

    def transport(url: str, payload: dict) -> dict:
        captured.append((url, payload))
        if payload["actions"][0]["type"] == "get_text":
            return {"results": [{"text": "Example"}]}
        if payload["actions"][0]["type"] == "get_attribute":
            return {"results": [{"value": "123"}]}
        return {"results": [{}]}

    control = LocalDockerComputerControl(
        base_url="http://localhost:9999",
        computer_id="demo",
        transport=transport,
    )

    control.open_url("https://example.com")
    control.wait_for(".result", timeout=5)
    control.click(".card")
    control.type("hello", into="#search")
    control.press_key("Enter")
    control.scroll(amount=100)
    control.select("Option", in_="#select")
    control.hover(".hover")
    assert control.get_text(".title") == "Example"
    assert control.get_attr(".card", "data-id") == "123"
    control.screenshot(full=True)
    control.copy_to_clipboard("text")
    control.save_file("/tmp/file.txt", "content")

    assert captured[0][0].endswith("/v1/computers/demo:perform")
    first_action = captured[0][1]["actions"][0]
    assert first_action == {"type": "open_url", "url": "https://example.com"}
