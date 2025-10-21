"""
Unit tests for AI Job Finder components.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from job_filter import JobFilter
from job_sources import JobAggregator


class TestJobFilter(unittest.TestCase):
    """Test job filtering logic."""
    
    def test_filter_by_role(self):
        """Test filtering by job role."""
        jobs = [
            {"title": "Software Engineer", "company": "TechCo", "location": "Amsterdam", "description": "Python developer"},
            {"title": "Nurse", "company": "Hospital", "location": "Utrecht", "description": "Healthcare professional"},
            {"title": "Data Scientist", "company": "DataCorp", "location": "Rotterdam", "description": "ML expert"}
        ]
        
        filters = {"role": "engineer"}
        filtered = JobFilter.filter_jobs(jobs, filters)
        
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["title"], "Software Engineer")
    
    def test_filter_by_location(self):
        """Test filtering by location."""
        jobs = [
            {"title": "Engineer", "company": "Co1", "location": "Amsterdam", "description": "Job 1"},
            {"title": "Engineer", "company": "Co2", "location": "Utrecht", "description": "Job 2"},
            {"title": "Engineer", "company": "Co3", "location": "Berlin", "description": "Job 3"}
        ]
        
        filters = {"location": "Utrecht"}
        filtered = JobFilter.filter_jobs(jobs, filters)
        
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["location"], "Utrecht")
    
    def test_exclude_language(self):
        """Test excluding jobs requiring specific language."""
        jobs = [
            {"title": "Job 1", "company": "Co1", "location": "NL", "description": "Dutch required for this role"},
            {"title": "Job 2", "company": "Co2", "location": "NL", "description": "English only position"},
            {"title": "Job 3", "company": "Co3", "location": "NL", "description": "Fluent in Dutch needed"}
        ]
        
        filters = {"exclude_language": ["Dutch"]}
        filtered = JobFilter.filter_jobs(jobs, filters)
        
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["title"], "Job 2")
    
    def test_deduplicate_jobs(self):
        """Test job deduplication."""
        jobs = [
            {"title": "Software Engineer", "company": "TechCo", "location": "Amsterdam", "url": "url1"},
            {"title": "Software Engineer", "company": "TechCo", "location": "Amsterdam", "url": "url2"},  # Duplicate
            {"title": "Data Scientist", "company": "DataCorp", "location": "Utrecht", "url": "url3"}
        ]
        
        unique = JobFilter.deduplicate_jobs(jobs)
        
        self.assertEqual(len(unique), 2)
    
    def test_normalize_text(self):
        """Test text normalization."""
        text1 = "Software Engineer"
        text2 = "software engineer"
        text3 = "Software  Engineer  "
        
        norm1 = JobFilter._normalize_text(text1)
        norm2 = JobFilter._normalize_text(text2)
        norm3 = JobFilter._normalize_text(text3)
        
        # All should normalize to the same lowercase, single-spaced text
        self.assertEqual(norm1, "software engineer")
        self.assertEqual(norm1, norm2)
        self.assertEqual(norm1, norm3)


class TestJobSources(unittest.TestCase):
    """Test job source integrations."""
    
    def test_aggregator_initialization(self):
        """Test job aggregator initializes all sources."""
        aggregator = JobAggregator()
        
        # Should have 3 base sources (Greenhouse, Lever, Workable)
        # Google Jobs is only added if API key is present
        self.assertGreaterEqual(len(aggregator.sources), 3)
    
    def test_google_jobs_without_api_key(self):
        """Test Google Jobs source without API key."""
        from job_sources import GoogleJobsSource
        
        source = GoogleJobsSource()
        self.assertFalse(source.enabled)
        
        # Should return empty list when disabled
        jobs = source.search_jobs({"role": "engineer"})
        self.assertEqual(len(jobs), 0)
    
    @patch('job_sources.requests.get')
    def test_greenhouse_search(self, mock_get):
        """Test Greenhouse API search."""
        from job_sources import GreenhouseSource
        
        # Mock API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "jobs": [
                {
                    "id": 123,
                    "title": "Test Job",
                    "location": {"name": "Amsterdam"},
                    "absolute_url": "https://example.com/job",
                    "content": "Job description"
                }
            ]
        }
        mock_get.return_value = mock_response
        
        source = GreenhouseSource()
        jobs = source.search_jobs({})
        
        # Should have made API calls and returned jobs
        self.assertGreater(len(jobs), 0)
        self.assertTrue(mock_get.called)


class TestOpenAIParser(unittest.TestCase):
    """Test OpenAI query parser."""
    
    @patch('openai_parser.OpenAI')
    def test_parser_initialization(self, mock_openai):
        """Test parser initializes with API key."""
        from openai_parser import JobQueryParser
        
        # Mock OpenAI client
        mock_openai.return_value = MagicMock()
        
        parser = JobQueryParser(api_key="test-key")
        self.assertEqual(parser.api_key, "test-key")
    
    def test_parser_requires_api_key(self):
        """Test parser raises error without API key."""
        from openai_parser import JobQueryParser
        
        with patch.dict('os.environ', {}, clear=True):
            with self.assertRaises(ValueError):
                JobQueryParser()
    
    @patch('openai_parser.OpenAI')
    def test_parse_query(self, mock_openai_class):
        """Test query parsing."""
        from openai_parser import JobQueryParser
        
        # Mock OpenAI client and response
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"role": "nurse", "location": "Utrecht", "exclude_language": ["Dutch"]}'
        mock_client.chat.completions.create.return_value = mock_response
        
        parser = JobQueryParser(api_key="test-key")
        filters = parser.parse_query("nurse in Utrecht, no Dutch required")
        
        self.assertEqual(filters.get("role"), "nurse")
        self.assertEqual(filters.get("location"), "Utrecht")
        self.assertIn("Dutch", filters.get("exclude_language", []))


if __name__ == "__main__":
    unittest.main()
