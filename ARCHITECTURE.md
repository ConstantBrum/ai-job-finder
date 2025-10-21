# System Architecture

## Component Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                          User Input                              │
│                   Natural Language Query                         │
│           "nurse in Utrecht, no Dutch required"                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       agent.py (AIJobFinder)                     │
│                     Main Orchestrator                            │
└────┬─────────────────────┬──────────────────┬──────────────────┘
     │                     │                  │
     │ 1. Parse Query      │ 2. Fetch Jobs    │ 3. Filter/Dedupe
     ▼                     ▼                  ▼
┌──────────────┐  ┌─────────────────┐  ┌────────────────┐
│ openai_      │  │  job_sources.py │  │ job_filter.py  │
│ parser.py    │  │                 │  │                │
│              │  │ ┌─────────────┐ │  │ - Filter jobs  │
│ - Parse NLP  │  │ │ Greenhouse  │ │  │ - Exclude lang │
│ - Extract    │  │ │   Source    │ │  │ - Deduplicate  │
│   filters    │  │ └─────────────┘ │  │                │
│              │  │                 │  │                │
│ Uses OpenAI  │  │ ┌─────────────┐ │  └────────────────┘
│ GPT-3.5      │  │ │   Lever     │ │
└──────────────┘  │ │   Source    │ │
                  │ └─────────────┘ │
                  │                 │
                  │ ┌─────────────┐ │
                  │ │  Workable   │ │
                  │ │   Source    │ │
                  │ └─────────────┘ │
                  └─────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Output (CLI or JSON)                        │
│  1. Software Engineer at TechCo - Utrecht - https://...         │
│  2. Nurse at Hospital - Utrecht - https://...                   │
│  ...                                                             │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Query Parsing Phase
```
User Query → OpenAI GPT-3.5 → Structured Filters
```

**Example:**
- Input: `"nurse in Utrecht, no Dutch required"`
- Output: 
```json
{
  "role": "nurse",
  "location": "Utrecht",
  "exclude_language": ["Dutch"]
}
```

### 2. Job Fetching Phase
```
Filters → Job Sources (Parallel) → Aggregated Jobs
```

**Process:**
- Each source (Greenhouse, Lever, Workable) is queried in parallel
- Results are aggregated into a unified format
- Rate limiting is applied (0.5s between requests per source)

**Job Format:**
```json
{
  "id": "unique_identifier",
  "title": "Job Title",
  "company": "Company Name",
  "location": "City, Country",
  "url": "https://apply-url",
  "source": "Greenhouse|Lever|Workable",
  "description": "Full job description"
}
```

### 3. Filtering Phase
```
All Jobs → Filter by Criteria → Deduplicate → Final Results
```

**Filtering Criteria:**
- Role matching (title and description)
- Location matching
- Language exclusions (pattern matching)
- Required languages
- Keywords
- Remote work preferences

**Deduplication:**
- Normalize job titles and company names
- Remove exact duplicates
- Keep first occurrence

### 4. Output Phase
```
Filtered Jobs → Format (CLI|JSON) → Display
```

## Module Responsibilities

### `agent.py` - Main Orchestrator
**Responsibilities:**
- CLI argument parsing
- Workflow orchestration
- Error handling
- Output formatting

**Key Methods:**
- `search(query, output_format)` - Main entry point
- `_output_cli(jobs)` - Format CLI output
- `_output_json(jobs)` - Format JSON output

### `openai_parser.py` - NLP Parser
**Responsibilities:**
- OpenAI API integration
- Natural language understanding
- Filter extraction

**Key Class:**
- `JobQueryParser`
  - `parse_query(query)` - Parse natural language to filters

**Dependencies:**
- OpenAI Python SDK
- dotenv for environment variables

### `job_sources.py` - Job Source Integrations
**Responsibilities:**
- API integrations with job boards
- Data fetching and normalization
- Rate limiting

**Key Classes:**
- `JobSource` (base class)
- `GreenhouseSource`
- `LeverSource`
- `WorkableSource`
- `JobAggregator` (coordinator)

**API Endpoints:**
- Greenhouse: `https://boards-api.greenhouse.io/v1/boards/{company}/jobs`
- Lever: `https://api.lever.co/v0/postings/{company}`
- Workable: `https://apply.workable.com/api/v3/accounts/{company}/jobs`

### `job_filter.py` - Filtering Logic
**Responsibilities:**
- Job filtering based on criteria
- Language requirement detection
- Deduplication

**Key Class:**
- `JobFilter`
  - `filter_jobs(jobs, filters)` - Apply all filters
  - `deduplicate_jobs(jobs)` - Remove duplicates
  - `_matches_filters(job, filters)` - Check single job
  - `_normalize_text(text)` - Normalize for comparison

## Configuration

### Environment Variables
```bash
OPENAI_API_KEY=sk-...    # Required for query parsing
```

### Extensibility Points

**Add More Job Sources:**
```python
class NewSource(JobSource):
    def search_jobs(self, filters):
        # Implementation
        return jobs
```

**Add More Companies:**
```python
# In job_sources.py
greenhouse_companies = [
    "existing-company",
    "new-company"  # Add here
]
```

**Customize Filtering:**
```python
# In job_filter.py, modify _matches_filters()
def _matches_filters(job, filters):
    # Add custom logic
    return matches
```

## Error Handling

### API Failures
- Individual source failures don't stop the entire search
- Errors are logged but execution continues
- Empty results returned if all sources fail

### Rate Limiting
- 0.5 second delay between requests to same source
- Prevents API rate limit issues
- Configurable in source classes

### OpenAI Errors
- Network errors return empty filter dict
- Invalid API key caught at initialization
- Parsing failures don't crash the system

## Testing Strategy

### Unit Tests (`test_agent.py`)
- Filter logic validation
- Deduplication testing
- Text normalization
- Source initialization
- Mock API responses

### Integration Points
- OpenAI API (mocked in tests)
- Job board APIs (mocked in tests)
- File system (environment variables)

### Manual Testing
- `demo.py` - Filtering without API calls
- `example.py` - Full system demo mode
- CLI commands with real searches

## Performance Considerations

### API Calls
- OpenAI: 1 call per search (~1-2 seconds)
- Job Sources: 3 sources × N companies = 3N API calls
- Total time: ~5-10 seconds for typical search

### Rate Limiting
- Built-in delays prevent API throttling
- Can be adjusted per source

### Optimization Opportunities
- Cache job listings (not implemented)
- Parallel API calls to different sources (partial)
- Background job fetching (not implemented)

## Security Considerations

### API Keys
- Never commit to repository
- Use environment variables or .env files
- .gitignore prevents accidental commits

### Input Validation
- Natural language input sanitized by OpenAI
- No SQL injection risk (no database)
- HTTP requests use timeout parameters

### External Dependencies
- All from PyPI (official repositories)
- Minimal dependency chain
- Regular updates recommended

## Deployment Options

### Local Development
```bash
pip install -r requirements.txt
export OPENAI_API_KEY=...
python agent.py "query"
```

### Script/Automation
```bash
#!/bin/bash
source .env
python agent.py "$1" --format json > results.json
```

### API Wrapper (Future)
Could wrap in Flask/FastAPI for HTTP API:
```python
@app.post("/search")
def search(query: str):
    finder = AIJobFinder()
    return finder.search(query)
```

## Monitoring & Observability

### Current Logging
- Console output for each stage
- Error messages for failures
- Progress indicators

### Metrics Available
- Total jobs fetched
- Filtered job count
- Unique job count
- Source success/failure rates

### Future Enhancements
- Structured logging (JSON)
- Performance metrics
- API call tracking
- Success rate monitoring
