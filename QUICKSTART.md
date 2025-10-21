# Quick Start Guide

Get up and running with AI Job Finder in minutes!

## Prerequisites

- Python 3.7 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Installation (30 seconds)

```bash
# 1. Clone the repository
git clone https://github.com/ConstantBrum/ai-job-finder.git
cd ai-job-finder

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your OpenAI API key
export OPENAI_API_KEY='your-api-key-here'
```

## Usage Examples

### Example 1: Basic Search
```bash
python agent.py "nurse in Utrecht, no Dutch required"
```

**What it does:**
- Searches for nursing positions in Utrecht
- Filters out jobs requiring Dutch language proficiency
- Returns jobs with English as the working language

**Expected Output:**
```
Searching for: nurse in Utrecht, no Dutch required
--------------------------------------------------------------------------------
Parsing query with AI...
Extracted filters: {
  "role": "nurse",
  "location": "Utrecht",
  "exclude_language": ["Dutch"]
}
--------------------------------------------------------------------------------
Fetching jobs from sources (Greenhouse, Lever, Workable)...
Found 150 total jobs from all sources
--------------------------------------------------------------------------------
Filtering jobs based on criteria...
Filtered to 12 matching jobs
--------------------------------------------------------------------------------
Removing duplicates...
Final result: 10 unique jobs
--------------------------------------------------------------------------------

================================================================================
FOUND 10 JOB(S)
================================================================================

1. Registered Nurse
   Company: Amsterdam Hospital
   Location: Utrecht, Netherlands
   Source: Greenhouse
   Apply: https://...
...
```

### Example 2: Tech Job Search
```bash
python agent.py "software engineer in Amsterdam, remote"
```

### Example 3: JSON Output
```bash
python agent.py "data scientist with Python" --format json
```

**Output:**
```json
[
  {
    "title": "Data Scientist",
    "company": "DataCorp",
    "location": "Amsterdam, Netherlands",
    "apply_url": "https://...",
    "source": "Lever"
  },
  ...
]
```

## Try It Without an API Key

Run our demo to see the filtering logic in action (no API key needed):

```bash
python demo.py
```

This shows how the system filters jobs based on role, location, and language requirements using mock data.

## Common Search Patterns

### Healthcare Jobs
```bash
python agent.py "nurse in Utrecht, no Dutch required"
python agent.py "doctor in Amsterdam, English speaking"
python agent.py "physiotherapist in Rotterdam"
```

### Tech Jobs
```bash
python agent.py "software engineer, remote, Python"
python agent.py "frontend developer in Amsterdam"
python agent.py "DevOps engineer in Berlin"
```

### Language Requirements
```bash
python agent.py "customer service in Munich, no German required"
python agent.py "marketing manager in Paris, English only"
```

### Salary Filters
```bash
python agent.py "product manager in London, minimum 80k"
python agent.py "senior engineer, 100k+ salary"
```

## Troubleshooting

### "OpenAI API key is required"
Make sure you've set your API key:
```bash
export OPENAI_API_KEY='sk-...'
```

Or create a `.env` file:
```bash
cp .env.example .env
# Edit .env and add your key
```

### "No jobs found"
Try:
- Broadening your search (remove location or specific requirements)
- Using more general role terms (e.g., "engineer" instead of "senior backend engineer")
- Running the demo to verify the system is working: `python demo.py`

### API Rate Limits
The job sources implement rate limiting. If you get connection errors, wait a moment and try again.

## Next Steps

1. **Extend Job Sources**: Add more companies to the lists in `job_sources.py`
2. **Add New Sources**: Implement additional job board integrations
3. **Customize Filters**: Modify filtering logic in `job_filter.py`
4. **Automate**: Set up cron jobs to run searches automatically

## Help & Support

- Read the full [README.md](README.md)
- Check [example.py](example.py) for programmatic usage
- Run tests: `python -m unittest test_agent`
- Open an issue on GitHub for bugs or feature requests

Happy job hunting! 🎯
