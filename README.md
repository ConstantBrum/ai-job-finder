# AI Job Finder

This repository provides a small command line tool that orchestrates a [CUA](https://docs.cua.ai)
workflow to search job portals (Google Jobs, LinkedIn, …) with rich filters. It generates
structured prompts from your requirements and, if necessary, performs logins before launching
the search.

## Features

- Expressive configuration file that mirrors typical job search filters.
- Optional login instructions so the agent can authenticate with providers such as LinkedIn.
- Dry-run mode for previewing the generated instructions before running a paid CUA session.
- Minimal Python package with a CLI entry point: `ai-job-finder`.

## Getting started

1. **Install dependencies**

   ```bash
   python -m pip install -e .
   ```

2. **Create a configuration file**

   Copy `example.config.yaml` and update it with your preferences. Environment variables
   inside the YAML file (e.g. `${CUA_API_KEY}`) are expanded automatically when the
   configuration is loaded.

   ```bash
   cp example.config.yaml my.config.yaml
   $EDITOR my.config.yaml
   ```

3. **Preview the instructions (optional)**

   ```bash
   ai-job-finder my.config.yaml --dry-run
   ```

4. **Run the automation**

   ```bash
   ai-job-finder my.config.yaml --output session.json
   ```

   The tool will create a new browser session via the CUA API, submit the job-search instructions,
   and wait for completion. When finished the summary (if provided) is printed and the raw response
   is persisted to `session.json`.

## Configuration reference

The YAML configuration file has three top-level keys:

- `cua`: connection settings for the API (base URL, API key, workspace/persona IDs, polling).
- `preferences`: the job search filters, matching the fields described in the initial request.
- `logins`: optional list of login steps the agent can perform before searching.

See `src/ai_job_finder/config.py` for the complete schema and `example.config.yaml` for a practical
example.

## Security considerations

- Store credentials securely. When possible rely on environment variables rather than hard-coding
  sensitive values inside the YAML file.
- Rotate API keys and site passwords periodically.
- When sharing output logs, redact personal information as the JSON may contain raw HTML captured
  during the CUA session.

## Limitations

- The HTTP endpoints used here follow the public CUA deployment as of April 2024. If the API
  surface changes you may need to adjust `src/ai_job_finder/client.py`.
- This project does not bundle automated tests because the workflow requires a live CUA backend.
  Use the `--dry-run` flag to validate your configuration without making network calls.
