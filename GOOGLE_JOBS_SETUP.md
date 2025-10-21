# Google Jobs Integration Setup Guide

This guide will walk you through setting up the Google Jobs integration for the AI Job Finder.

## What is Google Jobs?

Google Jobs is Google's job search feature that aggregates job listings from across the web, including:
- Company career pages
- Job boards (Indeed, LinkedIn, Monster, etc.)
- Staffing agencies
- Professional associations

By integrating with Google Jobs, the AI Job Finder can search through millions of job listings beyond the built-in job board sources.

## How It Works

The integration uses [SerpApi](https://serpapi.com/), a service that provides programmatic access to Google search results, including Google Jobs. SerpApi handles the complexity of scraping and parsing Google's results, providing a clean JSON API.

## Setup Instructions

### Step 1: Create a SerpApi Account

1. Go to https://serpapi.com/
2. Click "Sign Up" or "Get Started"
3. Create a free account (no credit card required for free tier)
4. Confirm your email address

### Step 2: Get Your API Key

1. Log in to your SerpApi dashboard
2. Navigate to https://serpapi.com/manage-api-key
3. Copy your API key

### Step 3: Configure the AI Job Finder

You have two options for configuring the API key:

#### Option A: Environment Variable (Recommended)

```bash
# On Linux/Mac
export SERPAPI_API_KEY='your_api_key_here'

# On Windows (Command Prompt)
set SERPAPI_API_KEY=your_api_key_here

# On Windows (PowerShell)
$env:SERPAPI_API_KEY='your_api_key_here'
```

#### Option B: .env File

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and add your API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   SERPAPI_API_KEY=your_serpapi_api_key_here
   ```

### Step 4: Test the Integration

Run the example script to verify everything is working:

```bash
python example_google_jobs.py
```

If successful, you should see job listings from Google Jobs!

### Step 5: Use with the Main Agent

Now you can use the main AI Job Finder with Google Jobs enabled:

```bash
python agent.py "software engineer in Amsterdam"
```

The agent will automatically include results from Google Jobs along with the traditional job board sources.

## Free Tier Limits

The free SerpApi tier includes:
- **100 searches per month**
- Access to all search engines (Google, Bing, etc.)
- JSON API responses
- No credit card required

Tips for managing your quota:
- Each agent query uses one Google Jobs search
- The system automatically disables Google Jobs if no API key is found
- Monitor your usage at https://serpapi.com/dashboard

## Paid Plans

If you need more searches, SerpApi offers paid plans:
- **Developer**: $50/month for 5,000 searches
- **Production**: $125/month for 15,000 searches
- **Enterprise**: Custom pricing for higher volumes

Learn more at https://serpapi.com/pricing

## Troubleshooting

### Google Jobs not returning results

1. **Check your API key**: Verify it's set correctly
   ```bash
   echo $SERPAPI_API_KEY
   ```

2. **Check your quota**: Log in to https://serpapi.com/dashboard to see remaining searches

3. **Verify internet connectivity**: The system needs internet access to reach SerpApi

### "GoogleJobsSource disabled" message

This is normal if you haven't set the SERPAPI_API_KEY. The system will work with other job sources only.

### API key not being recognized

Make sure you've either:
- Set the environment variable in the same terminal where you run the script
- Restarted your terminal after modifying `.env`
- Used `source .env` or `set -a; source .env; set +a` to load the `.env` file

## Privacy & Security

- Your API key should be kept private
- Never commit your API key to version control
- The `.env` file is already in `.gitignore` to prevent accidental commits
- SerpApi's privacy policy: https://serpapi.com/privacy-policy

## Alternative: Without Google Jobs

If you don't want to use Google Jobs, the AI Job Finder works perfectly fine without it:
- Simply don't set the SERPAPI_API_KEY
- The system will use Greenhouse, Lever, and Workable sources
- All features except Google Jobs search will work normally

## Support

For issues with:
- **SerpApi service**: Contact support@serpapi.com
- **AI Job Finder integration**: Open an issue on GitHub

## Additional Resources

- SerpApi Documentation: https://serpapi.com/docs
- Google Jobs API: https://serpapi.com/google-jobs-api
- Example API Response: https://serpapi.com/playground
