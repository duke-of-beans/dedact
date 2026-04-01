"""
Entity Recognition Module
Extract named entities from recovered content using spaCy
"""

from dataclasses import dataclass
from typing import List, Optional, Set
import re
try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False


@dataclass
class Entity:
    """Named entity with metadata"""
    text: str
    type: str
    start: int
    end: int
    confidence: float
    canonical_id: Optional[str]
    external_ids: dict


class EntityRecognizer:
    """
    Extract named entities from text
    
    Entity Types:
    - Standard: PERSON, ORG, GPE, DATE, MONEY, PERCENT
    - Custom: EMAIL, PHONE, SSN, STOCK_SYMBOL, CHEMICAL, DISEASE
    """
    
    def __init__(self, model_name: str = 'en_core_web_lg'):
        """
        Initialize entity recognizer
        
        Args:
            model_name: spaCy model to use
        """
        self.model_name = model_name
        self.nlp = None
        
        if SPACY_AVAILABLE:
            try:
                self.nlp = spacy.load(model_name)
            except OSError:
                # Model not installed - use fallback
                self.nlp = None
    
    def recognize(
        self,
        text: str,
        entity_types: Optional[List[str]] = None
    ) -> List[Entity]:
        """
        Extract entities from text
        
        Args:
            text: Text to analyze
            entity_types: Types to extract (None = all)
            
        Returns:
            List of extracted entities
        """
        entities = []
        
        # Standard entities with spaCy
        if self.nlp:
            entities.extend(self._extract_spacy_entities(text, entity_types))
        
        # Custom entity patterns
        entities.extend(self._extract_custom_entities(text, entity_types))
        
        # Remove duplicates and sort
        entities = self._deduplicate_entities(entities)
        entities.sort(key=lambda e: e.start)
        
        return entities
    
    def _extract_spacy_entities(
        self,
        text: str,
        entity_types: Optional[List[str]]
    ) -> List[Entity]:
        """Extract entities using spaCy NER"""
        if not self.nlp:
            return []
        
        entities = []
        doc = self.nlp(text)
        
        for ent in doc.ents:
            # Filter by type if specified
            if entity_types and ent.label_ not in entity_types:
                continue
            
            entities.append(Entity(
                text=ent.text,
                type=ent.label_,
                start=ent.start_char,
                end=ent.end_char,
                confidence=0.85,  # spaCy default confidence
                canonical_id=None,
                external_ids={}
            ))
        
        return entities
    
    def _extract_custom_entities(
        self,
        text: str,
        entity_types: Optional[List[str]]
    ) -> List[Entity]:
        """Extract custom entity types using regex"""
        entities = []
        
        # EMAIL
        if not entity_types or 'EMAIL' in entity_types:
            entities.extend(self._extract_emails(text))
        
        # PHONE
        if not entity_types or 'PHONE' in entity_types:
            entities.extend(self._extract_phones(text))
        
        # SSN (PROTECTED)
        if not entity_types or 'SSN' in entity_types:
            entities.extend(self._extract_ssns(text))
        
        # STOCK_SYMBOL
        if not entity_types or 'STOCK_SYMBOL' in entity_types:
            entities.extend(self._extract_stock_symbols(text))
        
        # URL
        if not entity_types or 'URL' in entity_types:
            entities.extend(self._extract_urls(text))
        
        return entities
    
    def _extract_emails(self, text: str) -> List[Entity]:
        """Extract email addresses"""
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        entities = []
        
        for match in re.finditer(pattern, text):
            entities.append(Entity(
                text=match.group(),
                type='EMAIL',
                start=match.start(),
                end=match.end(),
                confidence=0.95,
                canonical_id=None,
                external_ids={}
            ))
        
        return entities
    
    def _extract_phones(self, text: str) -> List[Entity]:
        """Extract phone numbers"""
        patterns = [
            r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # US format
            r'\+\d{1,3}[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}'  # International
        ]
        
        entities = []
        for pattern in patterns:
            for match in re.finditer(pattern, text):
                entities.append(Entity(
                    text=match.group(),
                    type='PHONE',
                    start=match.start(),
                    end=match.end(),
                    confidence=0.90,
                    canonical_id=None,
                    external_ids={}
                ))
        
        return entities
    
    def _extract_ssns(self, text: str) -> List[Entity]:
        """Extract SSNs (PROTECTED - auto-flag)"""
        pattern = r'\b\d{3}-\d{2}-\d{4}\b'
        entities = []
        
        for match in re.finditer(pattern, text):
            entities.append(Entity(
                text='[SSN-REDACTED]',  # Don't store actual SSN
                type='SSN',
                start=match.start(),
                end=match.end(),
                confidence=0.85,
                canonical_id=None,
                external_ids={'protected': True}
            ))
        
        return entities
    
    def _extract_stock_symbols(self, text: str) -> List[Entity]:
        """Extract stock symbols"""
        pattern = r'\b[A-Z]{1,5}\b(?=\s|$|,|\.)'
        entities = []
        
        # Common words to exclude
        exclude = {'THE', 'AND', 'FOR', 'ARE', 'WAS', 'THIS', 'THAT', 'WITH'}
        
        for match in re.finditer(pattern, text):
            symbol = match.group()
            if symbol not in exclude and len(symbol) <= 4:
                entities.append(Entity(
                    text=symbol,
                    type='STOCK_SYMBOL',
                    start=match.start(),
                    end=match.end(),
                    confidence=0.60,  # Lower confidence - many false positives
                    canonical_id=None,
                    external_ids={}
                ))
        
        return entities
    
    def _extract_urls(self, text: str) -> List[Entity]:
        """Extract URLs"""
        pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        entities = []
        
        for match in re.finditer(pattern, text):
            entities.append(Entity(
                text=match.group(),
                type='URL',
                start=match.start(),
                end=match.end(),
                confidence=0.95,
                canonical_id=None,
                external_ids={}
            ))
        
        return entities
    
    def _deduplicate_entities(self, entities: List[Entity]) -> List[Entity]:
        """Remove duplicate entities (same text at same position)"""
        seen = set()
        unique = []
        
        for entity in entities:
            key = (entity.text, entity.start, entity.end)
            if key not in seen:
                seen.add(key)
                unique.append(entity)
        
        return unique
    
    def get_entity_counts(self, entities: List[Entity]) -> dict:
        """Get count of entities by type"""
        counts = {}
        for entity in entities:
            counts[entity.type] = counts.get(entity.type, 0) + 1
        return counts
    
    def filter_by_confidence(
        self,
        entities: List[Entity],
        min_confidence: float = 0.6
    ) -> List[Entity]:
        """Filter entities by confidence threshold"""
        return [e for e in entities if e.confidence >= min_confidence]
    
    def batch_recognize(
        self,
        texts: List[str],
        entity_types: Optional[List[str]] = None
    ) -> List[List[Entity]]:
        """Process multiple texts efficiently"""
        return [self.recognize(text, entity_types) for text in texts]
