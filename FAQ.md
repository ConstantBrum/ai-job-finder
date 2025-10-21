# Frequently Asked Questions (FAQ)

Common questions and answers about the LinkedIn Job Finder Agent.

## General Questions

### What is this tool?

The LinkedIn Job Finder Agent is an AI-powered automation tool that helps you search for jobs on LinkedIn. It uses computer-control APIs to interact with LinkedIn's job search in a safe, controlled manner.

### Is this tool safe to use?

Yes! The tool is designed with safety as a top priority:
- ✅ No credential harvesting
- ✅ Operates only in your logged-in session
- ✅ Asks for confirmation before irreversible actions
- ✅ All data stays local on your machine
- ✅ Complete transparency through action logging

### Is this legal?

This tool is designed for **personal use only**. You must:
- Use it only for your own job search
- Respect LinkedIn's Terms of Service
- Not use it for commercial purposes
- Not share or resell the data

Always review and comply with LinkedIn's current Terms of Service.

### Do I need to pay for this?

No! This is a free, open-source tool under the ISC license.

## Installation & Setup

### What do I need to install?

Just Node.js 16.0 or higher. The core tool has no dependencies.

```bash
node --version  # Check your version
```

### Why do I see "placeholder implementations"?

The current version includes placeholder implementations for the computer-control API. This is intentional - you need to integrate with an actual browser automation tool (like Playwright or Puppeteer) to get real results.

See `API.md` for integration instructions.

### How do I integrate with a real browser?

See the [Integration Guide](API.md#integration-guide) in the API documentation. Example:

```javascript
import { chromium } from 'playwright';
import { LinkedInJobAgent } from './src/linkedin-job-agent.js';

// Create your custom API that extends ComputerControlAPI
// Then use it with the agent
```

## Usage Questions

### How do I search for jobs?

Three ways:

1. **Command line:**
   ```bash
   node src/index.js --keywords "engineer" --location "SF"
   ```

2. **JSON file:**
   ```bash
   node src/index.js my-search.json
   ```

3. **Use examples:**
   ```bash
   node src/index.js examples/task-basic.json
   ```

### What filters are supported?

- Keywords (job title, skills)
- Location (city, state, country)
- Job type (full-time, part-time, contract, etc.)
- Experience level (entry, mid, senior, etc.)
- Remote type (on-site, remote, hybrid)
- Date posted (today, past week, past month)
- Easy Apply (true/false)
- Company name
- Industry

See the [Filter Reference](API.md#filter-reference) for details.

### Where are results saved?

Results are saved to `/tmp/linkedin-jobs-[timestamp].json`

To view:
```bash
ls -lt /tmp/linkedin-jobs-*.json | head -1
cat /tmp/linkedin-jobs-*.json | jq  # with jq for pretty print
```

### Can I search for multiple things at once?

Not in parallel, but you can run multiple searches sequentially:

```bash
node src/index.js examples/task-basic.json
node src/index.js examples/task-remote.json
node src/index.js examples/task-entry-level.json
```

### How many jobs will I get?

Typically 10-50 jobs per search, depending on:
- Your search filters
- Available jobs on LinkedIn
- How many times the agent scrolls
- The current placeholder implementation

## Features & Functionality

### Does it apply to jobs automatically?

**No!** The agent will **never** apply to jobs without your explicit confirmation. Safety is a core principle.

If you want to apply, you must:
1. Confirm the action when prompted
2. Or manually apply using the job URLs in the results

### Can it save jobs for me?

The `saveJob()` method exists but requires confirmation. In the current placeholder implementation, it simulates saving. With real browser integration, it would actually save jobs on LinkedIn.

### Does it work with LinkedIn Premium?

Yes, it works with both free and Premium LinkedIn accounts. It operates in whatever account you're logged into.

### Can I schedule automatic searches?

Not built-in, but you can use system scheduling tools:

```bash
# Linux/Mac cron
0 9 * * * cd /path/to/ai-job-finder && node src/index.js daily-search.json

# Windows Task Scheduler
# Create a task that runs: node C:\path\to\ai-job-finder\src\index.js
```

### Does it support other job sites?

Currently only LinkedIn. Support for other job sites would require:
1. Creating a new agent class
2. Implementing site-specific search logic
3. Mapping filters to that site's parameters

## Troubleshooting

### "Cannot find module"

Make sure you're in the project directory:
```bash
cd /path/to/ai-job-finder
node src/index.js --help
```

### Results show mock/placeholder data

This is expected! The current version uses placeholders. To get real data:
1. Integrate with Playwright, Puppeteer, or similar
2. Replace placeholder methods in `computer-control-api.js`
3. Implement actual DOM parsing

### "Permission denied" error

The file might need execute permissions:
```bash
chmod +x src/index.js
```

### Slow performance

The agent includes human-like delays to respect LinkedIn's usage policies:
- 50-150ms between keystrokes
- 500-1500ms between clicks
- 300-800ms between scrolls

This is intentional and should not be disabled.

### Action log is too verbose

The action log provides transparency. You can redirect output:
```bash
node src/index.js ... 2>&1 | grep "✅"  # Only show success messages
```

## Security & Privacy

### Does this steal my LinkedIn password?

**No!** The tool never accesses, stores, or transmits credentials. It operates in your already-logged-in browser session.

### Where is my data stored?

All data is stored locally on your machine in `/tmp/`. No cloud storage, no external transmission.

### Can others see my searches?

No. Everything happens on your local machine. No data is sent anywhere.

### Is my action log private?

Yes. The action log is stored in memory during execution and can be saved to a local file. It never leaves your machine.

### What data is collected?

Only job listing data from LinkedIn:
- Job titles
- Company names
- Locations
- Job descriptions
- URLs
- Posted dates

No personal data, no credentials, no browsing history.

## Development & Customization

### Can I modify the code?

Yes! This is open source. You can:
- Fork the repository
- Modify for your needs
- Submit improvements via pull requests

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### How do I add a new filter?

1. Add mapping function in `linkedin-job-agent.js`
2. Update `buildSearchURL()` to include the filter
3. Update documentation
4. Test thoroughly

See [ARCHITECTURE.md](ARCHITECTURE.md) for details.

### How do I add a new export format?

Add a method to `LinkedInJobAgent`:

```javascript
convertToXML(jobs) {
  // Your XML conversion logic
  return xmlString;
}

async exportResults(jobs, format) {
  if (format === 'xml') {
    content = this.convertToXML(jobs);
  }
  // ... existing code
}
```

### Can I use this in my own app?

Yes! Import and use the classes:

```javascript
import { LinkedInJobAgent } from './src/linkedin-job-agent.js';

const agent = new LinkedInJobAgent();
const results = await agent.searchJobs({
  filters: { keywords: 'engineer' }
});
```

See [API.md](API.md) for full API documentation.

### How do I contribute?

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines.

## Comparison with Other Tools

### How is this different from LinkedIn's own search?

This tool automates the search process and:
- Saves results locally
- Supports batch processing
- Provides programmatic access
- Deduplicates results
- Exports to multiple formats

### How is this different from web scrapers?

This tool is designed to be:
- **Safer**: Respects rate limits with human-like pacing
- **More ethical**: Requires user login, no credential theft
- **More transparent**: Complete action logging
- **More focused**: Specifically for personal job searching

### Why not just use LinkedIn's API?

LinkedIn's official API has:
- Limited job search capabilities
- Requires approval process
- May have usage costs
- Doesn't support all filters

This tool provides more flexibility for personal use.

## Best Practices

### How often should I search?

Recommendation:
- **Daily**: For active job hunting
- **Weekly**: For passive browsing
- **After applications**: To track new postings

Always respect LinkedIn's usage policies.

### Should I review results manually?

**Yes!** Always review job listings before:
- Applying
- Saving
- Sharing with others

The agent finds jobs; you make the decisions.

### How do I stay compliant?

1. Use for personal job search only
2. Don't share or resell data
3. Respect rate limits (built into the tool)
4. Don't automate applications without review
5. Review LinkedIn's Terms of Service regularly

### What should I do with the results?

Suggested workflow:
1. Run search
2. Review JSON results
3. Visit interesting jobs on LinkedIn
4. Apply manually or with Easy Apply
5. Track applications separately

## Getting Help

### Where can I get help?

1. **Documentation**: Start with README.md
2. **Examples**: Check the examples/ directory
3. **Issues**: Search existing GitHub issues
4. **New Issue**: Open a new issue with details

### What information should I include in bug reports?

- Your Node.js version
- Operating system
- Command you ran
- Error message (full text)
- Expected vs actual behavior
- Relevant logs

### Is there a community?

Check the GitHub repository for:
- Discussions
- Issues
- Pull requests
- Contributors

### Can I request features?

Yes! Open an issue with:
- Clear description
- Use case
- Expected behavior
- Potential implementation approach

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Future Plans

### What features are planned?

- Real browser automation integration
- More job sites support
- GUI interface
- Advanced filtering
- Job application tracking
- Resume matching
- Email notifications

### When will real browser automation be added?

This depends on community contributions. The architecture is ready - integration examples are provided in the API documentation.

### Will there be a web version?

Possibly! This could be:
- Browser extension
- Electron app
- Web service (with security considerations)

### Can I help build new features?

Absolutely! We welcome contributions. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Additional Resources

- [Quick Start Guide](QUICKSTART.md)
- [Full Documentation](README.md)
- [API Reference](API.md)
- [Architecture Details](ARCHITECTURE.md)
- [Security Policy](SECURITY.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

---

**Still have questions?**

Open an issue on GitHub or check the documentation files listed above.

**Last Updated**: 2025-10-21
