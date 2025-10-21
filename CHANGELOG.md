# Changelog

## [Unreleased] - Google Jobs Integration

### Added
- **Google Jobs Integration**: Search through millions of jobs via Google Jobs using SerpApi
  - New `GoogleJobsSource` class for querying Google Jobs
  - Automatic integration with existing job aggregator
  - Optional feature - works without it
  - Free tier: 100 searches/month from SerpApi

### Changed
- Updated `JobAggregator` to support Google Jobs source
- Enhanced `requirements.txt` with SerpApi and BeautifulSoup dependencies
- Expanded `.env.example` with `SERPAPI_API_KEY` configuration

### Documentation
- Added `GOOGLE_JOBS_SETUP.md` - Comprehensive setup guide for Google Jobs
- Added `example_google_jobs.py` - Example script demonstrating Google Jobs integration
- Updated `README.md` with Google Jobs information and quick setup instructions
- Added new test cases for Google Jobs functionality

### Technical Details
- Uses SerpApi's Google Jobs API for web-wide job search
- Gracefully handles missing API key (disables feature, doesn't break)
- Maintains backward compatibility with existing functionality
- All existing tests continue to pass

### Benefits
- Significantly expands job search coverage beyond built-in boards
- Searches across company websites, job boards, and aggregators
- Simple opt-in configuration
- Free tier suitable for individual use
- Paid tiers available for higher volume

### Files Modified
- `job_sources.py` - Added GoogleJobsSource class and updated JobAggregator
- `requirements.txt` - Added google-search-results and beautifulsoup4
- `.env.example` - Added SERPAPI_API_KEY configuration
- `README.md` - Updated with Google Jobs documentation
- `test_agent.py` - Added tests for Google Jobs source

### Files Added
- `GOOGLE_JOBS_SETUP.md` - Complete setup guide
- `example_google_jobs.py` - Working example script
- `CHANGELOG.md` - This file
