# Security Policy

## Overview

The LinkedIn Job Finder Agent is designed with security and privacy as top priorities. This document outlines our security practices, policies, and guidelines.

## 🔒 Security Principles

### 1. No Credential Harvesting
- **Never** attempts to access, store, or transmit user credentials
- Operates only in the user's logged-in browser session
- No password prompts, no credential storage

### 2. Local Data Storage
- All job search results remain on the user's local machine
- No data transmission to external servers
- No cloud storage or external APIs

### 3. User Consent
- Requires explicit confirmation for irreversible actions
- Transparent action logging
- User has full control over all operations

### 4. Respectful Automation
- Human-like pacing to respect site policies
- No aggressive scraping or rate limit violations
- Reasonable delays between actions

### 5. Transparency
- Complete action logging
- Clear documentation of all operations
- Open source code for audit

## 🛡️ Security Features

### Action Logging
Every action is logged with:
- Timestamp
- Action type
- Parameters used
- Result status

Example log entry:
```json
{
  "timestamp": "2025-10-21T18:43:00Z",
  "action": "click",
  "details": {
    "selector": ".job-card"
  }
}
```

### Confirmation System
Irreversible actions require confirmation:
- Job applications
- Following companies
- Saving searches
- Sending messages

### Rate Limiting
Built-in delays between actions:
- Typing: 50-150ms per character
- Clicks: 500-1500ms between clicks
- Scrolls: 300-800ms between scrolls
- Page loads: up to 10 seconds

### Input Validation
All user inputs are validated:
- Task JSON structure
- Filter parameters
- File paths
- URLs

## 🚨 Reporting Security Issues

### Responsible Disclosure

If you discover a security vulnerability, please:

1. **Do NOT open a public issue**
2. Email the maintainers privately
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What Qualifies as a Security Issue

- Credential harvesting or storage
- Data exfiltration
- Unauthorized actions
- Bypass of confirmation mechanisms
- Privacy violations
- Injection vulnerabilities

### What is NOT a Security Issue

- Feature requests
- Performance issues
- UI/UX improvements
- Documentation errors

## ✅ Security Best Practices

### For Users

1. **Verify Source**: Only use official releases from trusted sources
2. **Review Code**: This is open source - audit the code before use
3. **Stay Updated**: Keep the tool updated with latest security patches
4. **Monitor Actions**: Review action logs after each run
5. **Use Confirmation**: Never disable the confirmation system
6. **Local Storage**: Ensure results are stored in secure locations

### For Developers

1. **Code Review**: All PRs must be reviewed for security
2. **No Secrets**: Never commit credentials or API keys
3. **Input Validation**: Validate all user inputs
4. **Safe APIs**: Use safe, well-tested libraries
5. **Error Handling**: Handle errors gracefully without exposing sensitive data
6. **Documentation**: Document security implications of changes

### For Integrators

1. **Custom API**: Secure your computer-control API implementation
2. **Confirmation**: Implement robust confirmation mechanisms
3. **Session Management**: Properly manage browser sessions
4. **Data Handling**: Secure storage and handling of job data
5. **Rate Limiting**: Respect site policies and rate limits

## 🔐 Data Privacy

### What Data is Collected

The agent collects:
- Job listings from LinkedIn
- Job metadata (title, company, location, etc.)
- Action logs (what the agent did)

### What Data is NOT Collected

The agent does NOT collect:
- User credentials
- Personal information
- Browsing history
- Cookies or session tokens
- Any data outside the job search scope

### Data Storage

- All data stored locally on user's machine
- No cloud storage
- No external transmission
- User controls all data

### Data Deletion

Users can delete all data by:
- Removing output files from `/tmp/` directory
- Clearing action logs
- Uninstalling the tool

## 🛠️ Security Controls

### Access Control
- Operates only in user's logged-in session
- No credential access
- No session hijacking

### Input Sanitization
- All inputs validated
- SQL injection: N/A (no database)
- XSS: N/A (no web interface)
- Command injection: Protected by input validation

### Output Encoding
- JSON output properly escaped
- CSV output properly quoted
- File paths validated

### Error Handling
- Errors logged without sensitive data
- Graceful degradation
- No stack traces in production

## 📋 Security Checklist

Before using the agent, verify:

- [ ] Code is from official repository
- [ ] No modifications to security features
- [ ] Confirmation system is enabled
- [ ] Action logging is enabled
- [ ] Results storage location is secure
- [ ] You're logged into LinkedIn
- [ ] You trust the computer-control API implementation

## 🔄 Security Updates

### Version Policy
- Security patches released immediately
- Users notified of critical issues
- Changelog includes security notes

### Update Procedure
```bash
# Pull latest changes
git pull origin main

# Review changelog
cat CHANGELOG.md

# Test in safe environment
node src/index.js --help
```

## 📚 Compliance

### LinkedIn Terms of Service
This tool is designed for personal use only. Users must:
- Comply with LinkedIn's Terms of Service
- Use the tool responsibly
- Not violate rate limits
- Not automate applications without review

### GDPR Compliance
- Data stored locally only
- User has full control
- No third-party data sharing
- Easy data deletion

### Accessibility
- Operates in user's own session
- No credential sharing
- Respects user consent

## 🚫 Prohibited Uses

This tool must NOT be used for:
- Credential harvesting
- Aggressive scraping
- Automated job applications without review
- Data reselling or redistribution
- Violating LinkedIn's Terms of Service
- Unauthorized access to accounts
- Spam or harassment

## 📞 Security Contacts

For security issues:
- **DO NOT** create public issues
- Email maintainers (see CONTRIBUTING.md)
- Allow time for response and fix

For general questions:
- Create public issue (non-security)
- Check documentation first
- Review existing issues

## 📜 Security Audit History

| Date | Auditor | Finding | Status |
|------|---------|---------|--------|
| Initial | Creator | Security design reviewed | ✅ Complete |

## 🎓 Security Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [LinkedIn Terms of Service](https://www.linkedin.com/legal/user-agreement)
- [Responsible Disclosure](https://en.wikipedia.org/wiki/Responsible_disclosure)

## 📄 License

This security policy is part of the project and covered under the ISC License.

---

**Last Updated**: 2025-10-21  
**Version**: 1.0.0
