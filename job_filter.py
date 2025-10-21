"""
Job filtering and deduplication logic.
"""

from typing import List, Dict
import re


class JobFilter:
    """Filter jobs based on search criteria."""
    
    @staticmethod
    def filter_jobs(jobs: List[Dict], filters: Dict) -> List[Dict]:
        """
        Filter jobs based on parsed filters.
        
        Args:
            jobs: List of job dictionaries
            filters: Dictionary of search filters
            
        Returns:
            Filtered list of jobs
        """
        filtered_jobs = []
        
        for job in jobs:
            if JobFilter._matches_filters(job, filters):
                filtered_jobs.append(job)
        
        return filtered_jobs
    
    @staticmethod
    def _matches_filters(job: Dict, filters: Dict) -> bool:
        """
        Check if a job matches the given filters.
        
        Args:
            job: Job dictionary
            filters: Dictionary of search filters
            
        Returns:
            True if job matches all filters, False otherwise
        """
        # Filter by role
        if filters.get("role"):
            role_keywords = filters["role"].lower().split()
            title_lower = job.get("title", "").lower()
            description_lower = job.get("description", "").lower()
            
            # Check if any role keyword appears in title or description
            if not any(keyword in title_lower or keyword in description_lower 
                      for keyword in role_keywords):
                return False
        
        # Filter by location
        if filters.get("location"):
            location_filter = filters["location"].lower()
            job_location = job.get("location", "").lower()
            
            # Check if location filter appears in job location
            if location_filter not in job_location:
                return False
        
        # Exclude jobs requiring specific languages
        if filters.get("exclude_language"):
            description_lower = job.get("description", "").lower()
            title_lower = job.get("title", "").lower()
            
            for lang in filters["exclude_language"]:
                lang_lower = lang.lower()
                # Check for language requirements in description
                patterns = [
                    f"{lang_lower} required",
                    f"{lang_lower} proficiency",
                    f"fluent in {lang_lower}",
                    f"speak {lang_lower}",
                    f"native {lang_lower}",
                    f"{lang_lower} speaker",
                    f"{lang_lower} language"
                ]
                
                if any(pattern in description_lower or pattern in title_lower 
                      for pattern in patterns):
                    return False
        
        # Filter by required languages
        if filters.get("language_required"):
            description_lower = job.get("description", "").lower()
            
            for lang in filters["language_required"]:
                lang_lower = lang.lower()
                if lang_lower not in description_lower:
                    return False
        
        # Filter by keywords
        if filters.get("keywords"):
            description_lower = job.get("description", "").lower()
            title_lower = job.get("title", "").lower()
            
            for keyword in filters["keywords"]:
                keyword_lower = keyword.lower()
                if keyword_lower not in description_lower and keyword_lower not in title_lower:
                    return False
        
        # Filter by remote
        if filters.get("remote"):
            location_lower = job.get("location", "").lower()
            description_lower = job.get("description", "").lower()
            
            remote_keywords = ["remote", "work from home", "wfh", "distributed"]
            if not any(keyword in location_lower or keyword in description_lower 
                      for keyword in remote_keywords):
                return False
        
        return True
    
    @staticmethod
    def deduplicate_jobs(jobs: List[Dict]) -> List[Dict]:
        """
        Remove duplicate jobs based on title and company.
        
        Args:
            jobs: List of job dictionaries
            
        Returns:
            Deduplicated list of jobs
        """
        seen = set()
        unique_jobs = []
        
        for job in jobs:
            # Create a normalized key for deduplication
            title_normalized = JobFilter._normalize_text(job.get("title", ""))
            company_normalized = JobFilter._normalize_text(job.get("company", ""))
            key = (title_normalized, company_normalized)
            
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)
        
        return unique_jobs
    
    @staticmethod
    def _normalize_text(text: str) -> str:
        """
        Normalize text for comparison (lowercase, remove extra spaces).
        
        Args:
            text: Text to normalize
            
        Returns:
            Normalized text
        """
        # Convert to lowercase
        text = text.lower()
        # Remove special characters except spaces
        text = re.sub(r'[^a-z0-9\s]', '', text)
        # Remove extra spaces
        text = ' '.join(text.split())
        return text
