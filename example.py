"""
Example usage script for AI Job Finder.

This demonstrates how to use the AI Job Finder programmatically.
Note: Requires OPENAI_API_KEY environment variable to be set.
"""

from agent import AIJobFinder
import os


def main():
    """Run example searches."""
    
    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("=" * 80)
        print("DEMO MODE - API Key Not Set")
        print("=" * 80)
        print("\nTo run this example with real API calls, set your OpenAI API key:")
        print("  export OPENAI_API_KEY='your-api-key'")
        print("\nFor now, showing example usage without making actual API calls...")
        print("=" * 80)
        print()
        
        # Show example queries
        example_queries = [
            "nurse in Utrecht, no Dutch required",
            "software engineer in Amsterdam, remote",
            "data scientist with Python experience",
            "product manager in Berlin, minimum 80k salary",
            "frontend developer, React experience, no German required"
        ]
        
        print("Example Queries You Can Try:")
        print("-" * 80)
        for i, query in enumerate(example_queries, 1):
            print(f"{i}. python agent.py \"{query}\"")
        print()
        
        print("Example with JSON output:")
        print("-" * 80)
        print(f"python agent.py \"{example_queries[0]}\" --format json")
        print()
        
        print("Programmatic Usage:")
        print("-" * 80)
        print("""
from agent import AIJobFinder

# Initialize the finder
finder = AIJobFinder()

# Search for jobs
jobs = finder.search("nurse in Utrecht, no Dutch required")

# Process results
for job in jobs:
    print(f"{job['title']} at {job['company']}")
    print(f"Location: {job['location']}")
    print(f"Apply: {job['url']}")
    print()
        """)
        
        return
    
    # If API key is set, run actual examples
    print("=" * 80)
    print("Running Example Searches")
    print("=" * 80)
    print()
    
    try:
        finder = AIJobFinder()
        
        # Example 1: Basic search
        print("\n" + "=" * 80)
        print("Example 1: Basic Search")
        print("=" * 80)
        jobs = finder.search("software engineer in Amsterdam", output_format="cli")
        
        # Example 2: With language exclusion
        print("\n" + "=" * 80)
        print("Example 2: With Language Exclusion")
        print("=" * 80)
        jobs = finder.search("nurse in Utrecht, no Dutch required", output_format="cli")
        
        # Example 3: JSON output
        print("\n" + "=" * 80)
        print("Example 3: JSON Output")
        print("=" * 80)
        jobs = finder.search("data scientist", output_format="json")
        
    except Exception as e:
        print(f"Error running examples: {e}")


if __name__ == "__main__":
    main()
