"""
External Database Connectors Module
Connect to external databases for entity verification
"""

import requests
from typing import Optional, Dict
import time


class ExternalDBConnector:
    """
    Connect to external databases
    
    Supported:
    - Wikidata
    - OpenCorporates
    - LittleSis
    """
    
    def __init__(self, rate_limit_delay: float = 1.0):
        """
        Initialize connector
        
        Args:
            rate_limit_delay: Delay between requests (seconds)
        """
        self.rate_limit_delay = rate_limit_delay
        self.cache = {}
    
    def query_wikidata(self, entity_name: str) -> Optional[Dict]:
        """
        Query Wikidata for entity
        
        Args:
            entity_name: Entity name to search
            
        Returns:
            Entity data or None
        """
        cache_key = f"wikidata:{entity_name}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            url = "https://www.wikidata.org/w/api.php"
            params = {
                'action': 'wbsearchentities',
                'search': entity_name,
                'language': 'en',
                'format': 'json'
            }
            
            time.sleep(self.rate_limit_delay)
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                result = data.get('search', [{}])[0] if data.get('search') else None
                self.cache[cache_key] = result
                return result
        except Exception:
            pass
        
        return None
    
    def query_opencorporates(self, company_name: str) -> Optional[Dict]:
        """
        Query OpenCorporates for company
        
        Args:
            company_name: Company name
            
        Returns:
            Company data or None
        """
        cache_key = f"opencorporates:{company_name}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            url = f"https://api.opencorporates.com/v0.4/companies/search"
            params = {'q': company_name}
            
            time.sleep(self.rate_limit_delay)
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                companies = data.get('results', {}).get('companies', [])
                result = companies[0] if companies else None
                self.cache[cache_key] = result
                return result
        except Exception:
            pass
        
        return None
