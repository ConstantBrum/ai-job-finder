from __future__ import annotations

import argparse
import json
from pathlib import Path

from .automation import JobSearchAutomation
from .client import CUAClient, CUAClientError
from .config import AppConfig, load_configuration


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a CUA job search session.")
    parser.add_argument(
        "config",
        type=Path,
        help="Path to the YAML configuration file with CUA settings and filters.",
    )
    parser.add_argument(
        "--session-title",
        default="Job search session",
        help="Optional custom title for the CUA session.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Output the instructions that would be sent to CUA without executing them.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="If provided, persist the CUA session response to this JSON file.",
    )
    return parser.parse_args()


def run_job_search(
    config: AppConfig,
    *,
    session_title: str,
    dry_run: bool,
    output: Path | None,
) -> None:
    client = CUAClient(
        base_url=config.cua.base_url,
        api_key=config.cua.api_key,
        workspace_id=config.cua.workspace_id,
    )
    automation = JobSearchAutomation(client, logins=config.logins)
    if dry_run:
        print("System prompt:\n")
        print(automation.system_prompt)
        print("\nUser prompt:\n")
        print(automation.build_user_prompt(config.preferences))
        return

    try:
        result = automation.run(
            preferences=config.preferences,
            session_title=session_title,
            persona_id=config.cua.persona_id,
            poll_interval=config.cua.poll_interval,
            timeout_seconds=config.cua.timeout_seconds,
        )
    except (CUAClientError, TimeoutError) as exc:  # pragma: no cover - CLI surface
        raise SystemExit(str(exc)) from exc

    print(f"Session {result.session_id} finished with status: {result.status}")
    summary = result.data.get("summary")
    if summary:
        print("\nSummary:\n")
        print(summary)

    if output:
        output.write_text(json.dumps(result.data, indent=2), encoding="utf-8")
        print(f"\nFull response written to {output}")


def main() -> None:
    args = parse_args()
    config = load_configuration(args.config)
    run_job_search(
        config,
        session_title=args.session_title,
        dry_run=args.dry_run,
        output=args.output,
    )


if __name__ == "__main__":  # pragma: no cover
    main()
