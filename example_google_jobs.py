"""
Example script showing Google Jobs integration.

This demonstrates how to use the Google Jobs search feature.
Requires SERPAPI_API_KEY to be set.
"""

import os
from job_sources import GoogleJobsSource

def main():
    """Demonstrate Google Jobs integration."""
    
    print("=" * 80)
    print("AI Job Finder - Google Jobs Integration Example")
    print("=" * 80)
    print()
    
    # Check if API key is set
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        print("❌ SERPAPI_API_KEY not set!")
        print()
        print("To use Google Jobs integration:")
        print("1. Sign up for free at https://serpapi.com/")
        print("2. Get your API key from the dashboard")
        print("3. Set it as an environment variable:")
        print("   export SERPAPI_API_KEY='your_api_key_here'")
        print()
        print("Or add it to your .env file:")
        print("   SERPAPI_API_KEY=your_api_key_here")
        return
    
    print("✓ SERPAPI_API_KEY found")
    print()
    
    # Create Google Jobs source
    source = GoogleJobsSource(api_key=api_key)
    
    if not source.enabled:
        print("❌ Google Jobs source is not enabled")
        return
    
    print("✓ Google Jobs source enabled")
    print()
    
    # Example 1: Search for software engineer jobs
    print("Example 1: Searching for 'software engineer in Amsterdam'")
    print("-" * 80)
    
    filters = {
        "role": "software engineer",
        "location": "Amsterdam"
    }
    
    jobs = source.search_jobs(filters)
    
    if jobs:
        print(f"Found {len(jobs)} jobs from Google Jobs:")
        print()
        
        # Show first 5 results
        for i, job in enumerate(jobs[:5], 1):
            print(f"{i}. {job['title']}")
            print(f"   Company: {job['company']}")
            print(f"   Location: {job['location']}")
            print(f"   URL: {job['url']}")
            print()
    else:
        print("No jobs found")
    
    print()
    
    # Example 2: Search for nurse jobs
    print("=" * 80)
    print("Example 2: Searching for 'nurse in Utrecht'")
    print("-" * 80)
    
    filters = {
        "role": "nurse",
        "location": "Utrecht"
    }
    
    jobs = source.search_jobs(filters)
    
    if jobs:
        print(f"Found {len(jobs)} jobs from Google Jobs:")
        print()
        
        # Show first 5 results
        for i, job in enumerate(jobs[:5], 1):
            print(f"{i}. {job['title']}")
            print(f"   Company: {job['company']}")
            print(f"   Location: {job['location']}")
            print(f"   URL: {job['url']}")
            print()
    else:
        print("No jobs found")
    
    print()
    print("=" * 80)
    print("Example Complete!")
    print("=" * 80)
    print()
    print("Note: Free SerpApi tier includes 100 searches/month")
    print("Check your usage at: https://serpapi.com/dashboard")


if __name__ == "__main__":
    main()
