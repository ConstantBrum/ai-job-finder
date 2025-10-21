# AI Job Finder

An intelligent Python-based AI agent that searches for jobs across multiple public job boards using natural language queries. Powered by OpenAI's GPT models for query parsing.

## Features

- **Natural Language Processing**: Uses OpenAI API to parse job search queries like "nurse in Utrecht, no Dutch required"
- **Multi-Source Search**: Queries public job boards (Greenhouse, Lever, Workable) and Google Jobs
- **Google Jobs Integration**: Search through Google's job listings for comprehensive results (optional, requires SerpApi key)
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

3. Set up your API keys:
```bash
# Option 1: Environment variables
export OPENAI_API_KEY='your-openai-api-key-here'
export SERPAPI_API_KEY='your-serpapi-api-key-here'  # Optional, for Google Jobs

# Option 2: Create .env file
cp .env.example .env
# Edit .env and add your API keys
```

**API Keys:**
- **OpenAI API Key** (Required): Get from https://platform.openai.com/api-keys
- **SerpApi API Key** (Optional): Get from https://serpapi.com/ - Free tier includes 100 searches/month for Google Jobs integration

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

2. **Job Fetching**: The agent queries multiple job sources:
   - **Google Jobs** (via SerpApi): Comprehensive job search across the web
   - **Greenhouse boards**: airbnb, gitlab, doordash, etc.
   - **Lever boards**: netflix, spotify, databricks, etc.
   - **Workable boards**: various companies

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

## Google Jobs Integration

The Google Jobs integration provides access to millions of job listings across the web. It uses SerpApi to programmatically search Google Jobs.

### Setup
1. Sign up for a free SerpApi account at https://serpapi.com/
2. Get your API key from the dashboard
3. Add it to your `.env` file:
   ```
   SERPAPI_API_KEY=your_serpapi_api_key_here
   ```

### Features
- Searches across all job boards indexed by Google
- Finds jobs from company websites, job boards, and aggregators
- Free tier includes 100 searches per month
- Automatically enabled when API key is present

### Disabling Google Jobs
If you don't want to use Google Jobs (e.g., to avoid API costs), simply don't set the `SERPAPI_API_KEY`. The system will work with other job sources only.

## Limitations

- **API Dependencies**: Relies on public APIs which may change or have rate limits
- **Company Coverage**: Traditional sources (Greenhouse, Lever, Workable) only search companies explicitly configured in the source lists
- **Google Jobs Rate Limits**: Free SerpApi tier limited to 100 searches/month
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