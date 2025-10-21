# AI Job Finder

An intelligent Python-based AI agent that searches for jobs across multiple public job boards using natural language queries. Powered by OpenAI's GPT models for query parsing.

## Features

- **Natural Language Processing**: Uses OpenAI API to parse job search queries like "nurse in Utrecht, no Dutch required"
- **Multi-Source Search**: Queries public job boards (Greenhouse, Lever, Workable)
- **Smart Filtering**: Automatically filters by role, location, language requirements, salary, remote work, etc.
- **Language Exclusion**: Excludes jobs requiring specific languages (e.g., "no Dutch required")
- **Deduplication**: Removes duplicate job listings
- **Multiple Output Formats**: CLI-friendly output or structured JSON
- **Easy to Extend**: Modular architecture makes it easy to add more job sources

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ConstantBrum/ai-job-finder.git
cd ai-job-finder
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
```bash
# Option 1: Environment variable
export OPENAI_API_KEY='your-api-key-here'

# Option 2: Create .env file
cp .env.example .env
# Edit .env and add your API key
```

## Usage

### Basic CLI Usage

```bash
# Search for jobs using natural language
python agent.py "nurse in Utrecht, no Dutch required"

# Search for software engineering jobs
python agent.py "software engineer in Amsterdam, remote"

# Search with specific requirements
python agent.py "data scientist with Python experience, minimum 80k salary"
```

### JSON Output

```bash
# Get results in JSON format for programmatic use
python agent.py "product manager in Berlin" --format json
```

### Python API

You can also use the agent programmatically:

```python
from agent import AIJobFinder

# Initialize the finder
finder = AIJobFinder()

# Search for jobs
jobs = finder.search("frontend developer in Utrecht, no Dutch required")

# jobs is a list of dictionaries with job details
for job in jobs:
    print(f"{job['title']} at {job['company']}")
    print(f"Location: {job['location']}")
    print(f"Apply: {job['url']}")
```

## How It Works

1. **Query Parsing**: The natural language query is sent to OpenAI's GPT model which extracts structured filters (role, location, language requirements, etc.)

2. **Job Fetching**: The agent queries multiple public job board APIs:
   - Greenhouse boards (airbnb, gitlab, doordash, etc.)
   - Lever boards (netflix, spotify, databricks, etc.)
   - Workable boards (various companies)

3. **Filtering**: Jobs are filtered based on:
   - Job title/role matching
   - Location matching
   - Language requirement exclusions
   - Required skills/keywords
   - Remote work preferences
   - Salary ranges (when available)

4. **Deduplication**: Duplicate listings are removed based on normalized job title and company name

5. **Output**: Results are formatted and displayed in CLI or JSON format

## Architecture

```
ai-job-finder/
├── agent.py           # Main orchestrator and CLI entry point
├── openai_parser.py   # OpenAI integration for NLP parsing
├── job_sources.py     # Job board API integrations
├── job_filter.py      # Filtering and deduplication logic
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Supported Query Formats

The AI can understand various natural language patterns:

- **Role + Location**: "software engineer in Amsterdam"
- **Language Exclusions**: "nurse in Utrecht, no Dutch required"
- **Remote Work**: "remote data analyst position"
- **Skills**: "Python developer with machine learning experience"
- **Salary**: "backend engineer, minimum 70k salary"
- **Combined**: "senior product manager in Berlin, remote, no German required"

## Extending the System

### Adding More Job Sources

To add a new job source, create a class in `job_sources.py`:

```python
class NewJobSource(JobSource):
    def search_jobs(self, filters: Dict) -> List[Dict]:
        # Implement API calls
        # Return list of job dictionaries
        pass
```

Then add it to the `JobAggregator`:

```python
def __init__(self):
    self.sources = [
        GreenhouseSource(),
        LeverSource(),
        WorkableSource(),
        NewJobSource()  # Add here
    ]
```

### Adding More Companies

Edit the company lists in `job_sources.py`:

```python
# For Greenhouse
greenhouse_companies = [
    "airbnb",
    "gitlab",
    "your-company-name"  # Add here
]

# For Lever
lever_companies = [
    "netflix",
    "spotify",
    "your-company-name"  # Add here
]
```

## Limitations

- **API Dependencies**: Relies on public APIs which may change or have rate limits
- **Company Coverage**: Only searches companies explicitly configured in the source lists
- **Language Detection**: Language requirement detection is pattern-based and may not catch all variations
- **OpenAI Costs**: Each query uses OpenAI API credits (typically a few cents per query)

## Requirements

- Python 3.7+
- OpenAI API key
- Internet connection

## License

MIT License - Feel free to use and modify as needed.

## Contributing

Contributions are welcome! Please feel free to submit pull requests to:
- Add more job board integrations
- Improve filtering logic
- Enhance language detection
- Add more company boards
- Improve documentation

## Support

For issues or questions, please open an issue on GitHub.