"""
Job sources module to query public job boards.
"""

import requests
import time
import os
from typing import List, Dict
from serpapi import GoogleSearch


class JobSource:
    """Base class for job sources."""
    
    def search_jobs(self, filters: Dict) -> List[Dict]:
        """
        Search for jobs based on filters.
        
        Args:
            filters: Dictionary of search filters
            
        Returns:
            List of job dictionaries
        """
        raise NotImplementedError


class GreenhouseSource(JobSource):
    """Query Greenhouse job boards."""
    
    def search_jobs(self, filters: Dict) -> List[Dict]:
        """
        Search Greenhouse public job boards.
        
        Note: Greenhouse doesn't have a centralized API for all companies.
        This implementation searches multiple known company boards.
        """
        jobs = []
        
        # List of example Greenhouse company boards (can be expanded)
        greenhouse_companies = [
            "airbnb",
            "doordash", 
            "gitlab",
            "grammarly",
            "robinhood"
        ]
        
        for company in greenhouse_companies:
            try:
                url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    company_jobs = data.get("jobs", [])
                    
                    for job in company_jobs:
                        jobs.append({
                            "id": f"gh_{company}_{job.get('id')}",
                            "title": job.get("title", ""),
                            "company": company.title(),
                            "location": job.get("location", {}).get("name", ""),
                            "url": job.get("absolute_url", ""),
                            "source": "Greenhouse",
                            "description": job.get("content", "")
                        })
                
                # Rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Error fetching from Greenhouse ({company}): {e}")
                continue
        
        return jobs


class LeverSource(JobSource):
    """Query Lever job boards."""
    
    def search_jobs(self, filters: Dict) -> List[Dict]:
        """
        Search Lever public job boards.
        
        Note: Lever doesn't have a centralized API for all companies.
        This implementation searches multiple known company boards.
        """
        jobs = []
        
        # List of example Lever company identifiers (can be expanded)
        lever_companies = [
            "netflix",
            "spotify",
            "lyft",
            "databricks",
            "stripe"
        ]
        
        for company in lever_companies:
            try:
                url = f"https://api.lever.co/v0/postings/{company}"
                params = {"mode": "json"}
                response = requests.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    company_jobs = response.json()
                    
                    for job in company_jobs:
                        jobs.append({
                            "id": f"lever_{company}_{job.get('id')}",
                            "title": job.get("text", ""),
                            "company": company.title(),
                            "location": job.get("categories", {}).get("location", ""),
                            "url": job.get("hostedUrl", ""),
                            "source": "Lever",
                            "description": job.get("description", "")
                        })
                
                # Rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Error fetching from Lever ({company}): {e}")
                continue
        
        return jobs


class WorkableSource(JobSource):
    """Query Workable job boards."""
    
    def search_jobs(self, filters: Dict) -> List[Dict]:
        """
        Search Workable public job boards.
        
        Note: Workable uses company-specific subdomains.
        This implementation searches multiple known company boards.
        """
        jobs = []
        
        # List of example Workable company identifiers (can be expanded)
        workable_companies = [
            "signifyd",
            "omnipresent",
            "ometria"
        ]
        
        for company in workable_companies:
            try:
                url = f"https://apply.workable.com/api/v3/accounts/{company}/jobs"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    company_jobs = data.get("jobs", [])
                    
                    for job in company_jobs:
                        location_str = job.get("city", "")
                        if job.get("country"):
                            location_str += f", {job.get('country')}"
                        
                        jobs.append({
                            "id": f"workable_{company}_{job.get('shortcode')}",
                            "title": job.get("title", ""),
                            "company": company.title(),
                            "location": location_str,
                            "url": job.get("url", ""),
                            "source": "Workable",
                            "description": job.get("description", "")
                        })
                
                # Rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Error fetching from Workable ({company}): {e}")
                continue
        
        return jobs


class GoogleJobsSource(JobSource):
    """Search for jobs using Google Jobs via SerpApi."""
    
    def __init__(self, api_key=None):
        """
        Initialize Google Jobs source.
        
        Args:
            api_key: SerpApi API key (optional, defaults to SERPAPI_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("SERPAPI_API_KEY")
        self.enabled = bool(self.api_key)
        if not self.enabled:
            print("Warning: GoogleJobsSource disabled - no SerpApi API key found. Set SERPAPI_API_KEY env variable to enable.")
    
    def search_jobs(self, filters: Dict) -> List[Dict]:
        """
        Search Google Jobs using SerpApi.
        
        Note: Requires a SerpApi API key (https://serpapi.com/)
        Free tier: 100 searches/month
        """
        if not self.enabled:
            return []
        
        jobs = []
        
        try:
            # Build search query from filters
            query_parts = []
            if filters.get("role"):
                query_parts.append(filters["role"])
            else:
                query_parts.append("jobs")
            
            if filters.get("location"):
                query_parts.append(f"in {filters['location']}")
            
            query = " ".join(query_parts)
            
            # Set up SerpApi search parameters
            params = {
                "engine": "google_jobs",
                "q": query,
                "api_key": self.api_key,
                "hl": "en"
            }
            
            # Add location filter if available
            if filters.get("location"):
                params["location"] = filters["location"]
            
            # Execute search
            search = GoogleSearch(params)
            results = search.get_dict()
            
            # Parse job results
            if "jobs_results" in results:
                for job in results["jobs_results"]:
                    jobs.append({
                        "id": f"google_{job.get('job_id', '')}",
                        "title": job.get("title", ""),
                        "company": job.get("company_name", ""),
                        "location": job.get("location", ""),
                        "url": job.get("share_url", job.get("related_links", [{}])[0].get("link", "")),
                        "source": "Google Jobs",
                        "description": job.get("description", "")
                    })
            
            print(f"Found {len(jobs)} jobs from Google Jobs")
            
        except Exception as e:
            print(f"Error fetching from Google Jobs: {e}")
        
        return jobs


class JobAggregator:
    """Aggregate jobs from multiple sources."""
    
    def __init__(self, use_google_jobs=True):
        """
        Initialize all job sources.
        
        Args:
            use_google_jobs: Whether to include Google Jobs source (requires SerpApi key)
        """
        self.sources = [
            GreenhouseSource(),
            LeverSource(),
            WorkableSource()
        ]
        
        # Add Google Jobs source if enabled
        if use_google_jobs:
            google_source = GoogleJobsSource()
            if google_source.enabled:
                self.sources.append(google_source)
    
    def search_all_sources(self, filters: Dict) -> List[Dict]:
        """
        Search all configured job sources.
        
        Args:
            filters: Dictionary of search filters
            
        Returns:
            List of all jobs from all sources
        """
        all_jobs = []
        
        for source in self.sources:
            try:
                jobs = source.search_jobs(filters)
                all_jobs.extend(jobs)
            except Exception as e:
                print(f"Error fetching from source {source.__class__.__name__}: {e}")
                continue
        
        return all_jobs
