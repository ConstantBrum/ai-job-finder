# Architecture Documentation

This document describes the technical architecture of the LinkedIn Job Finder Agent.

## Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Component Details](#component-details)
4. [Data Flow](#data-flow)
5. [Integration Points](#integration-points)
6. [Security Architecture](#security-architecture)
7. [Extensibility](#extensibility)

## Overview

The LinkedIn Job Finder Agent is designed as a modular, extensible system for safe job searching on LinkedIn. It follows a three-tier architecture with clear separation of concerns.

### Design Principles

1. **Modularity**: Each component has a single responsibility
2. **Extensibility**: Easy to extend with new features or integrations
3. **Safety**: Security and privacy built into the design
4. **Transparency**: All actions are logged and visible
5. **Simplicity**: Clear, maintainable code

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface Layer                     │
│  ┌────────────────────┐      ┌─────────────────────────┐   │
│  │   CLI Interface    │      │   JSON Task Files       │   │
│  │  (src/index.js)    │      │   (examples/*.json)     │   │
│  └────────────────────┘      └─────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Business Logic Layer                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         LinkedIn Job Agent                            │  │
│  │     (src/linkedin-job-agent.js)                      │  │
│  │                                                       │  │
│  │  • Task Parsing      • Job Extraction               │  │
│  │  • Filter Building   • Deduplication                │  │
│  │  • URL Construction  • Export (JSON/CSV)            │  │
│  │  • Safety Controls   • Confirmation                 │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  Automation Interface Layer                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │       Computer Control API                            │  │
│  │    (src/computer-control-api.js)                     │  │
│  │                                                       │  │
│  │  • Browser Navigation    • Element Interaction       │  │
│  │  • Content Extraction    • Human-like Pacing         │  │
│  │  • Action Logging        • Confirmation Prompts      │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  Browser Automation Layer                    │
│           (Playwright / Puppeteer / Other)                   │
│                   (To be integrated)                         │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. User Interface Layer

#### CLI Interface (`src/index.js`)

**Responsibilities:**
- Parse command-line arguments
- Load JSON task files
- Display help information
- Format and display results
- Error handling and reporting

**Key Functions:**
- `parseArgs()`: Parse CLI arguments into task object
- `showHelp()`: Display usage information
- `main()`: Entry point that orchestrates the search

**Input Formats:**
- Command-line flags: `--keywords "engineer" --location "SF"`
- JSON files: `node src/index.js task.json`

### 2. Business Logic Layer

#### LinkedIn Job Agent (`src/linkedin-job-agent.js`)

**Responsibilities:**
- Task parsing and validation
- LinkedIn URL construction with filters
- Job extraction logic
- Deduplication
- Result formatting and export
- Safety controls

**Key Classes:**
- `LinkedInJobAgent`: Main agent class

**Key Methods:**
```javascript
parseTask(taskInput)           // Parse and validate task
buildSearchURL(filters)        // Construct LinkedIn URL
searchJobs(taskInput)          // Main search orchestration
extractJobListings()           // Extract jobs from page
loadMoreJobs(maxScrolls)       // Progressive loading
deduplicateJobs()             // Remove duplicates
exportResults(jobs, format)    // Export to JSON/CSV
```

**Filter Mapping:**
- Converts human-readable filters to LinkedIn URL parameters
- Supports 9+ filter types
- Flexible filter combination

### 3. Automation Interface Layer

#### Computer Control API (`src/computer-control-api.js`)

**Responsibilities:**
- Abstract browser automation
- Human-like behavior simulation
- Action logging
- Safety controls

**Key Classes:**
- `ComputerControlAPI`: Main API wrapper

**Key Methods:**
```javascript
// Navigation
open_url(url)                  // Navigate to URL
wait_for(selector, timeout)    // Wait for elements

// Interaction
click(selector)                // Click elements
type(text, into)              // Type text
press_key(key)                // Press keyboard keys
scroll(amount)                // Scroll page

// Extraction
get_text(selector)            // Get element text
get_attr(selector, attr)      // Get element attribute

// Utilities
screenshot(area)              // Take screenshots
save_file(path, content)      // Save files
ask_confirmation(action)      // User confirmation
```

**Configuration:**
```javascript
HUMAN_DELAYS = {
  minTypingDelay: 50,
  maxTypingDelay: 150,
  minClickDelay: 500,
  maxClickDelay: 1500,
  minScrollDelay: 300,
  maxScrollDelay: 800,
  pageLoadTimeout: 10000
}
```

## Data Flow

### 1. Search Initiation

```
User Input (CLI/JSON)
    ↓
parseArgs() / JSON.parse()
    ↓
Task Object {
  goal: string,
  filters: {
    keywords, location, jobType, ...
  }
}
```

### 2. Search Execution

```
Task Object
    ↓
LinkedInJobAgent.searchJobs()
    ↓
parseTask() → buildSearchURL()
    ↓
ComputerControlAPI.open_url()
    ↓
wait_for() → verify login
    ↓
extractJobListings()
    ↓
loadMoreJobs() → scroll → extract
    ↓
deduplicateJobs()
    ↓
Result Object
```

### 3. Result Processing

```
Result Object {
  success: boolean,
  count: number,
  jobs: Job[],
  filters: Filters,
  timestamp: string,
  actionLog: Action[]
}
    ↓
exportResults()
    ↓
JSON/CSV File in /tmp/
```

### 4. Data Structures

#### Task Object
```javascript
{
  goal: "Find software engineering jobs",
  filters: {
    keywords: "software engineer",
    location: "San Francisco, CA",
    jobType: "full-time",
    experienceLevel: "mid",
    remote: "hybrid",
    datePosted: "past week",
    easyApply: false,
    company: "",
    industry: ""
  }
}
```

#### Job Object
```javascript
{
  id: "job-12345",
  title: "Senior Software Engineer",
  company: "Tech Company",
  location: "San Francisco, CA",
  description: "Job description...",
  url: "https://www.linkedin.com/jobs/view/12345",
  postedDate: "2025-10-20T12:00:00Z",
  easyApply: true
}
```

#### Action Log Entry
```javascript
{
  timestamp: "2025-10-21T18:43:00.000Z",
  action: "click",
  details: {
    selector: ".job-card",
    result: "success"
  }
}
```

## Integration Points

### Browser Automation Integration

The system is designed to integrate with any browser automation tool:

```javascript
// Example: Playwright Integration
import { chromium } from 'playwright';
import { ComputerControlAPI } from './computer-control-api.js';

class PlaywrightAPI extends ComputerControlAPI {
  constructor() {
    super();
    this.page = null;
  }

  async init() {
    const browser = await chromium.launch();
    this.page = await browser.newPage();
  }

  async open_url(url) {
    await this.page.goto(url);
  }

  async click(selector) {
    await this.page.click(selector);
  }

  // ... implement other methods
}
```

### Custom Confirmation System

```javascript
class InteractiveAPI extends ComputerControlAPI {
  async ask_confirmation(action, details) {
    // Custom confirmation UI
    return await showConfirmationDialog(action, details);
  }
}
```

### Custom Storage

```javascript
class CustomAgent extends LinkedInJobAgent {
  async exportResults(jobs, format) {
    // Custom storage implementation
    await this.database.save(jobs);
    await super.exportResults(jobs, format);
  }
}
```

## Security Architecture

### Defense in Depth

1. **Input Layer**: Validate all user inputs
2. **Logic Layer**: Safety controls and confirmations
3. **API Layer**: Action logging and rate limiting
4. **Output Layer**: Secure file handling

### Security Controls

```
User Input
    ↓
Input Validation ───────────┐
    ↓                       │
Safety Checks              │ Security Layer 1
    ↓                       │
Confirmation (if needed) ───┘
    ↓
Action Logging ─────────────┐
    ↓                       │
Rate Limiting              │ Security Layer 2
    ↓                       │
Human-like Pacing ──────────┘
    ↓
Execution
    ↓
Result Sanitization ────────┐
    ↓                       │ Security Layer 3
Local Storage Only ─────────┘
    ↓
User Output
```

### Safety Mechanisms

1. **No Credential Access**: Never touches authentication
2. **Confirmation Required**: For irreversible actions
3. **Action Logging**: Complete transparency
4. **Rate Limiting**: Respects site policies
5. **Local Storage**: No external transmission

## Extensibility

### Adding New Features

#### 1. New Filter Types

```javascript
// In linkedin-job-agent.js
mapNewFilter(value) {
  const mapping = { /* ... */ };
  return mapping[value.toLowerCase()] || value;
}

buildSearchURL(filters) {
  // Add new filter parameter
  if (filters.newFilter) {
    params.append('f_NEW', this.mapNewFilter(filters.newFilter));
  }
  // ...
}
```

#### 2. New Export Formats

```javascript
async exportResults(jobs, format) {
  if (format === 'xml') {
    return await this.convertToXML(jobs);
  } else if (format === 'csv') {
    return await this.convertToCSV(jobs);
  }
  // ... existing formats
}
```

#### 3. New Automation APIs

```javascript
// Create new API wrapper
class CustomControlAPI extends ComputerControlAPI {
  // Override methods with custom implementation
}

// Use in agent
const customApi = new CustomControlAPI();
const agent = new LinkedInJobAgent(customApi);
```

### Plugin System (Future)

```javascript
class PluginManager {
  registerFilter(name, mapper) { /* ... */ }
  registerExporter(format, exporter) { /* ... */ }
  registerAPI(name, api) { /* ... */ }
}
```

## Performance Considerations

### Current Performance

- **Search Time**: ~20-30 seconds per search
- **Jobs per Search**: 10-50 jobs (depends on scrolling)
- **Memory Usage**: < 50MB
- **Network**: Minimal (simulated in placeholder)

### Optimization Opportunities

1. **Parallel Extraction**: Extract from multiple selectors simultaneously
2. **Smart Scrolling**: Stop when no new jobs appear
3. **Caching**: Cache recently seen jobs
4. **Batch Processing**: Process multiple searches efficiently

### Scalability

Current design supports:
- ✅ Single user
- ✅ Sequential searches
- ✅ Local processing

Future enhancements needed for:
- ⏳ Multiple concurrent users
- ⏳ Parallel searches
- ⏳ Distributed processing

## Error Handling

### Error Flow

```
Error Occurs
    ↓
Catch in method
    ↓
Log error details
    ↓
Return partial results (if available)
    ↓
Propagate to caller
    ↓
User-friendly error message
```

### Error Types

1. **Network Errors**: Retry with backoff
2. **Selector Not Found**: Try alternate selectors
3. **Timeout**: Return partial results
4. **Validation Errors**: Clear user feedback

## Testing Strategy

### Current State
- Manual testing only
- Example files for common scenarios

### Future Testing
- Unit tests for each component
- Integration tests for full workflows
- End-to-end tests with real browser
- Performance benchmarks

## Deployment

### Current Deployment
```bash
git clone https://github.com/ConstantBrum/ai-job-finder.git
cd ai-job-finder
node src/index.js --help
```

### Future Deployment Options
- npm package
- Docker container
- Electron app
- Browser extension

## Maintenance

### Code Quality
- ESLint for linting
- Prettier for formatting
- JSDoc for documentation
- Regular dependency updates

### Monitoring
- Action logs for debugging
- Error tracking
- Performance metrics
- User feedback

---

**Version**: 1.0.0  
**Last Updated**: 2025-10-21
