"""
OpenAI integration module for parsing natural language job search queries.
"""

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class JobQueryParser:
    """Parse natural language queries into structured job search filters."""
    
    def __init__(self, api_key=None):
        """
        Initialize the parser with OpenAI API key.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        self.client = OpenAI(api_key=self.api_key)
    
    def parse_query(self, query):
        """
        Parse natural language query into structured filters.
        
        Args:
            query: Natural language job search query
            
        Returns:
            dict: Structured filters with keys like role, location, language_required, etc.
        """
        system_prompt = """You are a job search query parser. Extract structured information from natural language job queries.
        
Return a JSON object with the following fields (all optional):
- role: job title or role (string)
- location: city, country, or region (string)
- language_required: languages required for the job (list of strings, e.g., ["Dutch", "English"])
- exclude_language: languages to exclude jobs requiring (list of strings)
- salary_min: minimum salary (number)
- salary_max: maximum salary (number)
- remote: whether remote work is mentioned (boolean)
- keywords: other important keywords (list of strings)

If language requirement is explicitly negated (e.g., "no Dutch required"), add that language to exclude_language.
Be flexible with location names and job titles.
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Parse this job search query: {query}"}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            parsed_filters = json.loads(response.choices[0].message.content)
            return parsed_filters
            
        except Exception as e:
            print(f"Error parsing query with OpenAI: {e}")
            return {}
