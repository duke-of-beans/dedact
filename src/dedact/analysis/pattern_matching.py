"""
Pattern Matching Module
Find structured data patterns using regex
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
import re


@dataclass
class PatternMatch:
    """Matched pattern with validation"""
    pattern_type: str
    matched_text: str
    start: int
    end: int
    validated: bool
    metadata: Dict[str, any]


class PatternMatcher:
    """
    Find structured data patterns
    
    Patterns:
    - PHONE, EMAIL, SSN, URL
    - ADDRESS, CREDIT_CARD, IP_ADDRESS
    - BITCOIN_ADDRESS, CASE_NUMBER
    - DOLLAR_AMOUNT, STOCK_SYMBOL
    """
    
    def __init__(self, validation_level: str = 'format_only'):
        """
        Initialize pattern matcher
        
        Args:
            validation_level: 'format_only', 'checksum', 'external_validation'
        """
        self.validation_level = validation_level
        self.patterns = self._build_patterns()
    
    def _build_patterns(self) -> Dict[str, str]:
        """Build comprehensive regex patterns"""
        return {
            'PHONE_US': r'\b(\+1[-.]?)?\(?\d{3}\)?[-.]?\d{3}[-.]?\d{4}\b',
            'EMAIL': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'SSN': r'\b\d{3}-\d{2}-\d{4}\b',
            'URL': r'https?://[^\s]+',
            'IP_ADDRESS': r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
            'DOLLAR': r'\$\d+(?:,\d{3})*(?:\.\d{2})?',
            'ZIP_CODE': r'\b\d{5}(?:-\d{4})?\b',
            'CREDIT_CARD': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
            'STOCK_SYMBOL': r'\b[A-Z]{1,5}\b(?=\s|$|,)',
            'CASE_NUMBER': r'\b\d{2}-[A-Z]{2}-\d{4,6}\b'
        }
    
    def match(self, text: str, patterns: Optional[List[str]] = None) -> List[PatternMatch]:
        """
        Find all pattern matches in text
        
        Args:
            text: Text to search
            patterns: Specific patterns to match (None = all)
            
        Returns:
            List of pattern matches
        """
        matches = []
        
        patterns_to_use = patterns or list(self.patterns.keys())
        
        for pattern_name in patterns_to_use:
            if pattern_name in self.patterns:
                pattern = self.patterns[pattern_name]
                for match in re.finditer(pattern, text):
                    validated = self._validate_match(pattern_name, match.group())
                    
                    matches.append(PatternMatch(
                        pattern_type=pattern_name,
                        matched_text=match.group(),
                        start=match.start(),
                        end=match.end(),
                        validated=validated,
                        metadata={'validation_level': self.validation_level}
                    ))
        
        return matches
    
    def _validate_match(self, pattern_type: str, text: str) -> bool:
        """
        Validate match based on validation level
        
        Args:
            pattern_type: Type of pattern
            text: Matched text
            
        Returns:
            True if validated
        """
        if self.validation_level == 'format_only':
            return True
        
        # Additional validation logic would go here
        return True
    
    def get_statistics(self, matches: List[PatternMatch]) -> Dict[str, int]:
        """Calculate pattern statistics"""
        stats = {}
        for match in matches:
            stats[match.pattern_type] = stats.get(match.pattern_type, 0) + 1
        return stats
