"""
Main AI Job Finder Agent - orchestrates the job search process.
"""

import json
import sys
from openai_parser import JobQueryParser
from job_sources import JobAggregator
from job_filter import JobFilter


class AIJobFinder:
    """Main agent that orchestrates the job search."""
    
    def __init__(self, api_key=None):
        """
        Initialize the AI Job Finder.
        
        Args:
            api_key: OpenAI API key (optional)
        """
        self.parser = JobQueryParser(api_key=api_key)
        self.aggregator = JobAggregator()
        self.filter = JobFilter()
    
    def search(self, query: str, output_format: str = "cli") -> list:
        """
        Search for jobs based on natural language query.
        
        Args:
            query: Natural language job search query
            output_format: Output format - "cli" or "json"
            
        Returns:
            List of matching jobs
        """
        print(f"Searching for: {query}")
        print("-" * 80)
        
        # Step 1: Parse the query using OpenAI
        print("Parsing query with AI...")
        filters = self.parser.parse_query(query)
        print(f"Extracted filters: {json.dumps(filters, indent=2)}")
        print("-" * 80)
        
        # Step 2: Fetch jobs from all sources
        print("Fetching jobs from sources (Greenhouse, Lever, Workable)...")
        all_jobs = self.aggregator.search_all_sources(filters)
        print(f"Found {len(all_jobs)} total jobs from all sources")
        print("-" * 80)
        
        # Step 3: Filter jobs based on criteria
        print("Filtering jobs based on criteria...")
        filtered_jobs = self.filter.filter_jobs(all_jobs, filters)
        print(f"Filtered to {len(filtered_jobs)} matching jobs")
        print("-" * 80)
        
        # Step 4: Deduplicate jobs
        print("Removing duplicates...")
        unique_jobs = self.filter.deduplicate_jobs(filtered_jobs)
        print(f"Final result: {len(unique_jobs)} unique jobs")
        print("-" * 80)
        
        # Step 5: Output results
        if output_format == "json":
            self._output_json(unique_jobs)
        else:
            self._output_cli(unique_jobs)
        
        return unique_jobs
    
    def _output_cli(self, jobs: list):
        """
        Output jobs in CLI-friendly format.
        
        Args:
            jobs: List of job dictionaries
        """
        if not jobs:
            print("\nNo jobs found matching your criteria.")
            return
        
        print("\n" + "=" * 80)
        print(f"FOUND {len(jobs)} JOB(S)")
        print("=" * 80 + "\n")
        
        for i, job in enumerate(jobs, 1):
            print(f"{i}. {job.get('title', 'N/A')}")
            print(f"   Company: {job.get('company', 'N/A')}")
            print(f"   Location: {job.get('location', 'N/A')}")
            print(f"   Source: {job.get('source', 'N/A')}")
            print(f"   Apply: {job.get('url', 'N/A')}")
            print()
    
    def _output_json(self, jobs: list):
        """
        Output jobs in JSON format.
        
        Args:
            jobs: List of job dictionaries
        """
        # Prepare simplified output
        output_jobs = []
        for job in jobs:
            output_jobs.append({
                "title": job.get("title", ""),
                "company": job.get("company", ""),
                "location": job.get("location", ""),
                "apply_url": job.get("url", ""),
                "source": job.get("source", "")
            })
        
        print(json.dumps(output_jobs, indent=2))


def main():
    """Main CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="AI Job Finder - Search jobs using natural language",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python agent.py "nurse in Utrecht, no Dutch required"
  python agent.py "software engineer in Amsterdam, remote" --format json
  python agent.py "data scientist with Python experience"
        """
    )
    
    parser.add_argument(
        "query",
        help="Natural language job search query"
    )
    
    parser.add_argument(
        "--format",
        choices=["cli", "json"],
        default="cli",
        help="Output format (default: cli)"
    )
    
    parser.add_argument(
        "--api-key",
        help="OpenAI API key (can also use OPENAI_API_KEY env var)"
    )
    
    args = parser.parse_args()
    
    try:
        finder = AIJobFinder(api_key=args.api_key)
        finder.search(args.query, output_format=args.format)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        print("\nPlease set your OpenAI API key:", file=sys.stderr)
        print("  export OPENAI_API_KEY='your-api-key'", file=sys.stderr)
        print("Or create a .env file with OPENAI_API_KEY=your-api-key", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
