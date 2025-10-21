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
        # Allow the parser to work without an OpenAI API key by using a
        # lightweight local fallback parser. If an API key is provided or
        # available via env, we'll attempt to use the OpenAI client; otherwise
        # self.client will be None and parse_query will use the local parser.
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if self.api_key:
            try:
                self.client = OpenAI(api_key=self.api_key)
            except Exception:
                # If the OpenAI client fails to initialize, continue without it
                self.client = None
        else:
            self.client = None
    
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
        
        # If we have an OpenAI client, try using it first. If anything goes
        # wrong, or if the returned data is empty/incomplete, fall back to a
        # simple local parser that extracts role, location and language
        # negations from the query string.
        parsed_filters = None

        if self.client:
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

                # Some OpenAI SDKs return the structured object directly; if
                # it's a string, try to load JSON. Be defensive.
                raw = response.choices[0].message.content
                if isinstance(raw, (dict, list)):
                    parsed_filters = raw
                else:
                    try:
                        parsed_filters = json.loads(raw)
                    except Exception:
                        parsed_filters = None

            except Exception as e:
                print(f"Warning: OpenAI parsing failed, using local fallback: {e}")
                parsed_filters = None

        # Local heuristic fallback parser
        def local_parse(q: str) -> dict:
            q_lower = q.lower()
            result = {}

            # Extract excluded languages (e.g., "no Dutch required")
            exclude_langs = []
            import re
            for m in re.finditer(r'no\s+([a-zA-Z]+)\s+(?:required|needed|necessary)', q_lower):
                exclude_langs.append(m.group(1).title())

            # Also catch patterns like "no Dutch" or "without Dutch"
            for m in re.finditer(r'no\s+([a-zA-Z]+)\b', q_lower):
                lang = m.group(1).title()
                if lang not in exclude_langs and lang not in ['no', 'not']:
                    exclude_langs.append(lang)

            for m in re.finditer(r'without\s+([a-zA-Z]+)\b', q_lower):
                lang = m.group(1).title()
                if lang not in exclude_langs:
                    exclude_langs.append(lang)

            if exclude_langs:
                result['exclude_language'] = exclude_langs

            # Extract location using "in <location>" pattern
            loc = None
            m = re.search(r'\bin\s+([a-zA-Z\-\s]+?)(?:,|$)', q_lower)
            if m:
                loc = m.group(1).strip()
                # strip trailing words like 'remote' if matched
                loc = re.sub(r'\bremote\b', '', loc).strip()
                if loc:
                    result['location'] = loc.title()

            # Detect remote
            if 'remote' in q_lower or 'work from home' in q_lower or 'wfh' in q_lower:
                result['remote'] = True

            # Extract role: text before 'in <location>' or before comma
            role = None
            if m:
                role_part = q_lower[:m.start()].strip()
            else:
                # take up to first comma or end
                role_part = q_lower.split(',', 1)[0].strip()

            # Remove negations and noise
            role_part = re.sub(r'no\s+[a-zA-Z]+', '', role_part)
            role_part = role_part.replace('with', '').replace('but', '')
            role_part = role_part.strip()
            if role_part:
                # take the last word or phrase as role, but prefer short phrase
                role = role_part
                result['role'] = role.title()

            # Keywords: remaining words after removing role/location
            keywords = []
            # crude keywords: words like 'senior', 'junior', 'manager', etc.
            for kw in ['senior', 'junior', 'manager', 'specialist', 'engineer', 'nurse']:
                if kw in q_lower and (('role' not in result) or kw not in result.get('role','').lower()):
                    keywords.append(kw.title())
            if keywords:
                result['keywords'] = keywords

            return result

        heuristic = local_parse(query)

        # If parsed_filters is empty or missing critical fields, merge heuristic
        if not parsed_filters:
            return heuristic

        # Merge: prefer OpenAI fields but fill gaps from heuristic
        merged = dict(parsed_filters)
        for k, v in heuristic.items():
            if k not in merged or not merged.get(k):
                merged[k] = v

        return merged
