"""
Demo script showing filtering capabilities without API calls.

This demonstrates the filtering logic using mock data.
"""

from job_filter import JobFilter


def main():
    """Demonstrate job filtering with mock data."""
    
    print("=" * 80)
    print("AI Job Finder - Filtering Demo")
    print("=" * 80)
    print()
    
    # Create mock job data
    mock_jobs = [
        {
            "id": "1",
            "title": "Senior Nurse",
            "company": "Utrecht Medical Center",
            "location": "Utrecht, Netherlands",
            "description": "Looking for an experienced nurse. Dutch language required.",
            "url": "https://example.com/job1"
        },
        {
            "id": "2",
            "title": "Registered Nurse",
            "company": "Amsterdam Hospital",
            "location": "Amsterdam, Netherlands",
            "description": "International team, English speaking environment. No Dutch required.",
            "url": "https://example.com/job2"
        },
        {
            "id": "3",
            "title": "Nurse Practitioner",
            "company": "Rotterdam Clinic",
            "location": "Utrecht, Netherlands",
            "description": "Join our diverse team. English is our working language.",
            "url": "https://example.com/job3"
        },
        {
            "id": "4",
            "title": "Software Engineer",
            "company": "TechCorp",
            "location": "Utrecht, Netherlands",
            "description": "Python developer needed. Remote work available.",
            "url": "https://example.com/job4"
        },
        {
            "id": "5",
            "title": "Nurse Manager",
            "company": "Utrecht Medical Center",
            "location": "Utrecht, Netherlands",
            "description": "Fluent in Dutch and English required for patient communication.",
            "url": "https://example.com/job5"
        },
        {
            "id": "6",
            "title": "Clinical Nurse",
            "company": "Den Haag Hospital",
            "location": "Den Haag, Netherlands",
            "description": "Seeking dedicated nurse for our international ward.",
            "url": "https://example.com/job6"
        }
    ]
    
    print(f"Starting with {len(mock_jobs)} total jobs")
    print("-" * 80)
    
    # Example 1: Filter for "nurse in Utrecht, no Dutch required"
    print("\nExample 1: 'nurse in Utrecht, no Dutch required'")
    print("-" * 80)
    
    filters = {
        "role": "nurse",
        "location": "Utrecht",
        "exclude_language": ["Dutch"]
    }
    
    print(f"Filters: {filters}")
    print()
    
    filtered = JobFilter.filter_jobs(mock_jobs, filters)
    
    print(f"Found {len(filtered)} matching jobs:")
    for i, job in enumerate(filtered, 1):
        print(f"\n{i}. {job['title']}")
        print(f"   Company: {job['company']}")
        print(f"   Location: {job['location']}")
        print(f"   URL: {job['url']}")
    
    # Example 2: Just location filter
    print("\n" + "=" * 80)
    print("Example 2: 'jobs in Utrecht'")
    print("-" * 80)
    
    filters = {
        "location": "Utrecht"
    }
    
    print(f"Filters: {filters}")
    print()
    
    filtered = JobFilter.filter_jobs(mock_jobs, filters)
    
    print(f"Found {len(filtered)} matching jobs:")
    for i, job in enumerate(filtered, 1):
        print(f"\n{i}. {job['title']}")
        print(f"   Company: {job['company']}")
        print(f"   Location: {job['location']}")
    
    # Example 3: Deduplication
    print("\n" + "=" * 80)
    print("Example 3: Deduplication")
    print("-" * 80)
    
    # Create jobs with duplicates
    jobs_with_dupes = [
        {"title": "Software Engineer", "company": "TechCo", "location": "Amsterdam"},
        {"title": "Software Engineer", "company": "TechCo", "location": "Amsterdam"},
        {"title": "Data Scientist", "company": "DataCorp", "location": "Utrecht"}
    ]
    
    print(f"Before deduplication: {len(jobs_with_dupes)} jobs")
    unique = JobFilter.deduplicate_jobs(jobs_with_dupes)
    print(f"After deduplication: {len(unique)} unique jobs")
    
    print("\n" + "=" * 80)
    print("Demo Complete!")
    print("=" * 80)
    print("\nTo use with real job sources and AI parsing:")
    print("  1. Set OPENAI_API_KEY environment variable")
    print("  2. Run: python agent.py 'nurse in Utrecht, no Dutch required'")


if __name__ == "__main__":
    main()
