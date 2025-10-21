# Quick Start Guide

Get started with the LinkedIn Job Finder Agent in 5 minutes!

## Prerequisites

- Node.js 16.0 or higher installed
- An active LinkedIn account (you must be logged in)
- Basic command line knowledge

## Installation

```bash
# Clone the repository
git clone https://github.com/ConstantBrum/ai-job-finder.git
cd ai-job-finder
```

That's it! No dependencies to install for the basic version.

## Your First Job Search

### Option 1: Command Line (Easiest)

Search for software engineering jobs:

```bash
node src/index.js --keywords "software engineer" --location "San Francisco, CA"
```

Search for remote jobs:

```bash
node src/index.js --keywords "developer" --remote "remote"
```

### Option 2: JSON Task File

Create a file called `my-search.json`:

```json
{
  "goal": "Find my ideal job",
  "filters": {
    "keywords": "software engineer",
    "location": "San Francisco, CA",
    "jobType": "full-time",
    "remote": "hybrid"
  }
}
```

Run the search:

```bash
node src/index.js my-search.json
```

### Option 3: Use Examples

We've included example searches you can use right away:

```bash
# Basic software engineering jobs
node src/index.js examples/task-basic.json

# Remote senior developer positions
node src/index.js examples/task-remote.json

# Entry-level positions
node src/index.js examples/task-entry-level.json
```

## Understanding the Output

The agent will:

1. 🔍 Parse your search criteria
2. 📍 Navigate to LinkedIn jobs
3. 🔐 Verify you're logged in
4. 📋 Extract job listings
5. 📜 Scroll to load more jobs
6. 🔄 Remove duplicates
7. 💾 Save results to `/tmp/linkedin-jobs-*.json`

Example output:

```
🤖 LinkedIn Job Finder Agent
============================================

🔍 LinkedIn Job Search Agent Starting...

Goal: Find software engineering jobs
Filters: {
  "keywords": "software engineer",
  "location": "San Francisco, CA",
  ...
}

✅ Search complete!
Found 25 unique job listings

💾 Results saved to: /tmp/linkedin-jobs-2025-10-21T18-43-00.json
```

## Common Filters

| What you want | Command |
|---------------|---------|
| Specific keywords | `--keywords "data scientist"` |
| Location | `--location "New York, NY"` |
| Remote only | `--remote "remote"` |
| Full-time jobs | `--job-type "full-time"` |
| Senior level | `--experience "senior"` |
| Recent jobs | `--date-posted "past week"` |
| Easy Apply | `--easy-apply` |

## Combine Multiple Filters

```bash
node src/index.js \
  --keywords "senior developer" \
  --remote "remote" \
  --experience "senior" \
  --date-posted "past week" \
  --easy-apply
```

## View Results

Results are saved as JSON files in `/tmp/`:

```bash
# View the latest results
cat /tmp/linkedin-jobs-*.json | less

# Or use jq for pretty formatting
cat /tmp/linkedin-jobs-*.json | jq
```

Each job includes:
- Job ID
- Title
- Company
- Location
- Description (placeholder)
- URL
- Posted date
- Easy Apply status

## Tips & Tricks

### 1. Start Broad, Then Narrow

```bash
# First search: broad
node src/index.js --keywords "engineer"

# Then narrow down
node src/index.js --keywords "software engineer" --experience "mid"
```

### 2. Save Your Common Searches

Create JSON files for searches you run often:

```bash
# daily-remote-search.json
{
  "filters": {
    "keywords": "developer",
    "remote": "remote",
    "datePosted": "today"
  }
}
```

Then just run:

```bash
node src/index.js daily-remote-search.json
```

### 3. Check the Help

```bash
node src/index.js --help
```

## What's Next?

1. **Read the full README**: `cat README.md`
2. **Check the API docs**: `cat API.md`
3. **Review security**: `cat SECURITY.md`
4. **Explore examples**: `ls examples/`

## Troubleshooting

### "Module not found"
Make sure you're running from the project root directory:
```bash
cd /path/to/ai-job-finder
node src/index.js --help
```

### "Permission denied"
The script might need execute permissions:
```bash
chmod +x src/index.js
```

### Results look empty
This version uses placeholder implementations. To get real results, you'll need to:
1. Integrate with a browser automation tool (see API.md)
2. Replace placeholder functions in `src/computer-control-api.js`

### Need more help?
- Read the full documentation
- Check existing GitHub issues
- Open a new issue with details

## Important Notes

⚠️ **This is for personal use only**
- Respect LinkedIn's Terms of Service
- Don't use for commercial purposes
- Don't share or resell data

🔒 **Your data stays local**
- No cloud storage
- No external transmission
- You control everything

✅ **Safe by design**
- No credential access
- Confirmation for actions
- Complete transparency

## Next Steps

- **Customize your searches**: Edit the example JSON files
- **Learn the API**: Read `API.md` for programmatic usage
- **Integrate**: Connect with actual browser automation (Playwright, Puppeteer)
- **Contribute**: Help improve the project!

Happy job hunting! 🎯
