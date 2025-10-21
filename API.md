# API Documentation

This document describes how to integrate and use the LinkedIn Job Finder Agent programmatically.

## Table of Contents

- [Computer Control API](#computer-control-api)
- [LinkedIn Job Agent API](#linkedin-job-agent-api)
- [Integration Guide](#integration-guide)
- [Examples](#examples)

## Computer Control API

The `ComputerControlAPI` class provides methods for browser automation.

### Constructor

```javascript
import { ComputerControlAPI } from './src/computer-control-api.js';

const api = new ComputerControlAPI();
```

### Methods

#### `open_url(url)`
Navigate to a URL.

```javascript
await api.open_url('https://www.linkedin.com/jobs');
```

#### `wait_for(selectorOrText, timeout)`
Wait for an element or text to appear.

```javascript
await api.wait_for('.job-listing', 5000);
await api.wait_for('Login', 3000);
```

#### `click(selectorOrText)`
Click on an element.

```javascript
await api.click('.apply-button');
await api.click('Apply Now');
```

#### `type(text, into)`
Type text into an element.

```javascript
await api.type('software engineer', '.search-input');
```

#### `scroll(amountOrDestination)`
Scroll the page.

```javascript
await api.scroll('end');
await api.scroll(500);
```

#### `get_text(selector)`
Get text from an element.

```javascript
const result = await api.get_text('.job-title');
console.log(result.text);
```

#### `get_attr(selector, attr)`
Get an attribute from an element.

```javascript
const result = await api.get_attr('.job-link', 'href');
console.log(result.value);
```

#### `screenshot(areaOrFull)`
Take a screenshot.

```javascript
await api.screenshot('full');
await api.screenshot('.job-listing');
```

#### `save_file(path, content)`
Save content to a file.

```javascript
await api.save_file('/tmp/results.json', JSON.stringify(data));
```

#### `ask_confirmation(action, details)`
Ask for user confirmation.

```javascript
const confirmed = await api.ask_confirmation('Apply to Job', { jobId: '12345' });
if (confirmed) {
  // Proceed with action
}
```

### Configuration

Customize human-like delays:

```javascript
import { HUMAN_DELAYS } from './src/computer-control-api.js';

// View default delays
console.log(HUMAN_DELAYS);
```

## LinkedIn Job Agent API

The `LinkedInJobAgent` class provides job search functionality.

### Constructor

```javascript
import { LinkedInJobAgent } from './src/linkedin-job-agent.js';

// Use default API
const agent = new LinkedInJobAgent();

// Or provide custom API
const customApi = new ComputerControlAPI();
const agent = new LinkedInJobAgent(customApi);
```

### Methods

#### `searchJobs(taskInput)`
Search for jobs based on task input.

**Parameters:**
- `taskInput` (string | object): Natural language goal or task object

**Returns:** Promise<Result>

```javascript
// Natural language
const results = await agent.searchJobs('Find remote software engineer jobs');

// Structured task
const results = await agent.searchJobs({
  goal: 'Find engineering jobs',
  filters: {
    keywords: 'software engineer',
    location: 'San Francisco, CA',
    remote: 'hybrid'
  }
});
```

**Result Object:**
```javascript
{
  success: true,
  count: 25,
  jobs: [
    {
      id: 'job-12345',
      title: 'Senior Software Engineer',
      company: 'Tech Company',
      location: 'San Francisco, CA',
      description: 'Job description...',
      url: 'https://www.linkedin.com/jobs/view/12345',
      postedDate: '2025-10-20T12:00:00Z',
      easyApply: true
    }
  ],
  filters: { /* applied filters */ },
  timestamp: '2025-10-21T18:43:00Z',
  actionLog: [ /* all actions */ ]
}
```

#### `parseTask(taskInput)`
Parse task input and extract filters.

```javascript
const task = agent.parseTask({
  goal: 'Find jobs',
  filters: { keywords: 'developer' }
});
```

#### `buildSearchURL(filters)`
Build LinkedIn search URL with filters.

```javascript
const url = agent.buildSearchURL({
  keywords: 'software engineer',
  location: 'San Francisco',
  remote: 'hybrid'
});
```

#### `applyToJob(jobId)`
Apply to a job (requires confirmation).

```javascript
const result = await agent.applyToJob('job-12345');
```

#### `saveJob(jobId)`
Save a job for later (requires confirmation).

```javascript
const result = await agent.saveJob('job-12345');
```

#### `exportResults(jobs, format)`
Export results to a file.

**Parameters:**
- `jobs` (array): Array of job objects
- `format` (string): 'json' or 'csv'

```javascript
const filename = await agent.exportResults(results.jobs, 'json');
const csvFile = await agent.exportResults(results.jobs, 'csv');
```

## Integration Guide

### Step 1: Replace Placeholder Implementations

Replace the placeholder methods in `ComputerControlAPI` with your actual automation system:

```javascript
// Example with Playwright
import { chromium } from 'playwright';

class PlaywrightControlAPI extends ComputerControlAPI {
  constructor() {
    super();
    this.browser = null;
    this.page = null;
  }

  async init() {
    this.browser = await chromium.launch();
    this.page = await this.browser.newPage();
  }

  async open_url(url) {
    this.logAction('open_url', { url });
    await this.page.goto(url);
    return { success: true };
  }

  async click(selector) {
    this.logAction('click', { selector });
    await this.page.click(selector);
    return { success: true };
  }

  // ... implement other methods
}
```

### Step 2: Create Custom Agent

```javascript
import { LinkedInJobAgent } from './src/linkedin-job-agent.js';
import { PlaywrightControlAPI } from './custom-api.js';

async function main() {
  const api = new PlaywrightControlAPI();
  await api.init();

  const agent = new LinkedInJobAgent(api);
  
  const results = await agent.searchJobs({
    goal: 'Find senior developer jobs',
    filters: {
      keywords: 'senior developer',
      remote: 'remote',
      datePosted: 'past week'
    }
  });

  console.log(`Found ${results.count} jobs`);
  
  // Export results
  await agent.exportResults(results.jobs, 'json');
}

main();
```

### Step 3: Implement Confirmation System

```javascript
import readline from 'readline';

class InteractiveAPI extends ComputerControlAPI {
  async ask_confirmation(action, details) {
    console.log(`\n⚠️  Confirmation Required`);
    console.log(`Action: ${action}`);
    console.log(`Details: ${JSON.stringify(details, null, 2)}`);
    
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });

    return new Promise(resolve => {
      rl.question('Proceed? (yes/no): ', answer => {
        rl.close();
        resolve(answer.toLowerCase() === 'yes');
      });
    });
  }
}
```

## Examples

### Example 1: Basic Search

```javascript
import { LinkedInJobAgent } from './src/linkedin-job-agent.js';

const agent = new LinkedInJobAgent();
const results = await agent.searchJobs({
  filters: {
    keywords: 'software engineer',
    location: 'New York, NY'
  }
});

console.log(`Found ${results.count} jobs`);
```

### Example 2: Advanced Filters

```javascript
const results = await agent.searchJobs({
  goal: 'Find senior remote engineering roles',
  filters: {
    keywords: 'senior engineer',
    jobType: 'full-time',
    experienceLevel: 'senior',
    remote: 'remote',
    datePosted: 'past 24 hours',
    easyApply: true
  }
});
```

### Example 3: Custom Processing

```javascript
const results = await agent.searchJobs({ keywords: 'developer' });

// Filter by salary (if available)
const highPayingJobs = results.jobs.filter(job => {
  // Custom filtering logic
  return job.salary > 100000;
});

// Group by company
const byCompany = results.jobs.reduce((acc, job) => {
  acc[job.company] = acc[job.company] || [];
  acc[job.company].push(job);
  return acc;
}, {});

console.log('Jobs by company:', byCompany);
```

### Example 4: Batch Processing

```javascript
const searches = [
  { keywords: 'software engineer', location: 'San Francisco' },
  { keywords: 'data scientist', location: 'New York' },
  { keywords: 'product manager', location: 'Seattle' }
];

const allResults = [];

for (const search of searches) {
  const results = await agent.searchJobs({ filters: search });
  allResults.push(...results.jobs);
  
  // Delay between searches
  await new Promise(resolve => setTimeout(resolve, 5000));
}

console.log(`Total jobs found: ${allResults.length}`);
await agent.exportResults(allResults, 'json');
```

### Example 5: Error Handling

```javascript
try {
  const results = await agent.searchJobs({
    filters: { keywords: 'engineer' }
  });

  if (results.success) {
    console.log('Search successful');
    await agent.exportResults(results.jobs, 'json');
  } else {
    console.error('Search failed:', results.error);
    
    // Still export partial results
    if (results.jobs.length > 0) {
      await agent.exportResults(results.jobs, 'json');
    }
  }
} catch (error) {
  console.error('Fatal error:', error);
}
```

## Filter Reference

### Keywords
Type: `string`  
Description: Job title or skills to search for  
Example: `"software engineer"`, `"data scientist python"`

### Location
Type: `string`  
Description: City, state, or country  
Example: `"San Francisco, CA"`, `"New York"`, `"Remote"`

### Job Type
Type: `string`  
Options: `full-time`, `part-time`, `contract`, `temporary`, `volunteer`, `internship`  
Example: `"full-time"`

### Experience Level
Type: `string`  
Options: `internship`, `entry`, `associate`, `mid`, `senior`, `director`, `executive`  
Example: `"senior"`

### Remote
Type: `string`  
Options: `on-site`, `remote`, `hybrid`  
Example: `"remote"`

### Date Posted
Type: `string`  
Options: `today`, `past week`, `past month`, `any time`  
Example: `"past week"`

### Easy Apply
Type: `boolean`  
Description: Filter for jobs with Easy Apply option  
Example: `true`

### Company
Type: `string`  
Description: Company name  
Example: `"Google"`

## Best Practices

1. **Rate Limiting**: Add delays between multiple searches
2. **Error Handling**: Always handle errors gracefully
3. **Confirmation**: Implement proper confirmation for irreversible actions
4. **Logging**: Keep action logs for transparency
5. **Local Storage**: Store all data locally, never transmit
6. **Human-like Behavior**: Respect the built-in delays
7. **Session Management**: Operate only in logged-in sessions

## Security Notes

- Never store credentials in code
- Always validate user input
- Keep all data local
- Log all actions for transparency
- Require confirmation for irreversible actions
- Respect rate limits and site policies

## Support

For issues or questions about the API:
1. Check this documentation
2. Review the source code comments
3. Open an issue on GitHub
