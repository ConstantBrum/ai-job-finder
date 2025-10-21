# AI Job Finder

Automation agent that performs LinkedIn job searches through a computer-control API.

## Local CUA computer

The agent can be run against the [CUA Computer SDK](https://www.cua.ai/docs/computer-sdk/computers)
in a fully local Docker container.  Launch the container and expose the default API
port by running:

```bash
docker run --rm -p 11400:11400 ghcr.io/cua/computer:latest
```

Point the agent at the local runtime by instantiating
`LocalDockerComputerControl(base_url="http://127.0.0.1:11400", computer_id="local")`
and pass the instance to `LinkedInJobSearchAgent`.

## Features

- Normalizes user-provided filters into LinkedIn query parameters.
- Drives a browser using the provided computer-control API to load search results.
- Collects job cards and returns clean, deduplicated results.
- Requests explicit user confirmation before irreversible actions such as applying or following companies.

## Development

Install development dependencies and run tests:

```bash
pip install -e .[develop]
pytest
```
