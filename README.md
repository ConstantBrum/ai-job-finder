# LinkedIn Job Finder Agent

An AI-powered agent that searches for jobs on LinkedIn using computer-control API for safe, local job searching. This agent operates via your logged-in browser profile and respects all safety and compliance guidelines.

## 🎯 Features

- **Safe & Compliant**: Operates only in your logged-in browser profile
- **No Credential Harvesting**: Never stores or transmits credentials
- **Human-Like Behavior**: Adds realistic pacing to avoid detection
- **Confirmation Required**: Asks before any irreversible actions (apply, follow, save)
- **Local Results**: All data stays on your computer
- **Deduplication**: Automatically removes duplicate job listings
- **Flexible Filters**: Support for keywords, location, job type, experience level, remote work, and more
- **Transparent**: Complete action logging for full transparency

## 🔒 Safety & Compliance

This agent follows strict safety guidelines:

1. **User Control**: Operates only in the user's logged-in browser profile
2. **No Credential Harvesting**: Never attempts to access or store credentials
3. **Respectful Scraping**: Uses human-like pacing and respects site usage rules
4. **Confirmation Required**: Always asks before irreversible actions (Apply, Follow, Save)
5. **Immediate Execution**: Completes tasks in the current session, no background operations
6. **Local Storage**: All results stored locally, never transmitted

## 📋 Prerequisites

- Node.js 16.0 or higher
- An active LinkedIn account (you must be logged in)
- Computer-control API integration (placeholder implementations included)

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/ConstantBrum/ai-job-finder.git
cd ai-job-finder

# Install dependencies (if any are added later)
npm install
```

## 💻 Usage

### Command Line Interface

```bash
# Basic search with keywords
node src/index.js --keywords "software engineer" --location "San Francisco, CA"

# Search for remote senior-level jobs
node src/index.js --keywords "developer" --remote "remote" --experience "senior"

# Search with Easy Apply filter
node src/index.js --keywords "data scientist" --easy-apply

# Use a task JSON file
node src/index.js examples/task-basic.json

# Show help
node src/index.js --help
```

### Task JSON Format

Create a JSON file with your search criteria:

```json
{
  "goal": "Find software engineering jobs",
  "filters": {
    "keywords": "software engineer",
    "location": "San Francisco, CA",
    "jobType": "full-time",
    "experienceLevel": "mid",
    "remote": "hybrid",
    "datePosted": "past week",
    "easyApply": false,
    "company": "Google",
    "industry": "technology"
  }
}
```

### Supported Filters

| Filter | Description | Example Values |
|--------|-------------|----------------|
| `keywords` | Job search keywords | "software engineer", "data scientist" |
| `location` | Job location | "San Francisco, CA", "New York, NY" |
| `jobType` | Employment type | "full-time", "part-time", "contract", "internship" |
| `experienceLevel` | Experience level | "entry", "mid", "senior", "director", "executive" |
| `remote` | Remote work type | "on-site", "remote", "hybrid" |
| `datePosted` | Posting date range | "today", "past week", "past month" |
| `easyApply` | Easy Apply filter | `true` or `false` |
| `company` | Company name | "Google", "Microsoft" |
| `industry` | Industry filter | "technology", "finance" |

## 📂 Examples

The `examples/` directory contains sample task files:

- `task-basic.json` - Basic job search with common filters
- `task-remote.json` - Remote job search with Easy Apply
- `task-entry-level.json` - Entry-level positions for recent graduates

## 🏗️ Architecture

The project consists of three main components:

### 1. Computer Control API (`src/computer-control-api.js`)

Provides wrapper functions for browser automation:
- `open_url(url)` - Navigate to a URL
- `wait_for(selector, timeout)` - Wait for elements
- `click(selector)` - Click elements
- `type(text, into)` - Type text
- `scroll(amount)` - Scroll the page
- `get_text(selector)` - Extract text
- And more...

### 2. LinkedIn Job Agent (`src/linkedin-job-agent.js`)

Core agent functionality:
- Task parsing and filter handling
- LinkedIn URL construction
- Job extraction and deduplication
- Safety controls and confirmation prompts
- Result export (JSON, CSV)

### 3. Main Entry Point (`src/index.js`)

CLI interface:
- Command-line argument parsing
- Task file loading
- Agent execution
- Result reporting

## 🛡️ Security Considerations

### What This Agent Does

- ✅ Searches for jobs using your logged-in LinkedIn session
- ✅ Respects LinkedIn's usage policies with human-like pacing
- ✅ Stores all results locally on your machine
- ✅ Provides complete transparency via action logging
- ✅ Asks for confirmation before any irreversible actions

### What This Agent Does NOT Do

- ❌ Never attempts to harvest or store credentials
- ❌ Never performs aggressive scraping
- ❌ Never runs in the background without user knowledge
- ❌ Never transmits data to external services
- ❌ Never takes irreversible actions without confirmation

## 🔧 Integration with Computer-Control API

This implementation includes placeholder functions for the computer-control API. In a production environment, you would need to:

1. Replace the placeholder implementations in `src/computer-control-api.js`
2. Connect to your actual computer-control system (e.g., Playwright, Puppeteer, Selenium)
3. Implement the confirmation mechanism (e.g., CLI prompts, GUI dialogs)

Example integration points:

```javascript
// Replace placeholders with actual implementations
async open_url(url) {
  // Your computer-control API call here
  await yourBrowserAPI.navigate(url);
}

async click(selector) {
  // Your computer-control API call here
  await yourBrowserAPI.clickElement(selector);
}
```

## 📊 Output Format

Results are returned in the following structure:

```json
{
  "success": true,
  "count": 25,
  "jobs": [
    {
      "id": "job-12345",
      "title": "Senior Software Engineer",
      "company": "Tech Company",
      "location": "San Francisco, CA",
      "description": "Job description...",
      "url": "https://www.linkedin.com/jobs/view/12345",
      "postedDate": "2025-10-20T12:00:00Z",
      "easyApply": true
    }
  ],
  "filters": { /* applied filters */ },
  "timestamp": "2025-10-21T18:43:00Z",
  "actionLog": [ /* all actions taken */ ]
}
```

## 🤝 Contributing

Contributions are welcome! Please ensure that any changes:

1. Maintain the safety and compliance guidelines
2. Include appropriate documentation
3. Follow the existing code style
4. Add tests if applicable

## 📝 License

ISC License - See LICENSE file for details

## ⚠️ Disclaimer

This tool is for personal use only. Users are responsible for ensuring their use complies with LinkedIn's Terms of Service and any applicable laws and regulations. The authors are not responsible for any misuse of this tool.

## 🆘 Support

For issues, questions, or contributions, please open an issue on GitHub.