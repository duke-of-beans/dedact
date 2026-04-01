"""
Relationship Mapping Module
Map relationships between entities
"""

from dataclasses import dataclass
from typing import List, Optional
from .entity_recognition import Entity


@dataclass
class Relationship:
    """Relationship between two entities"""
    entity1: Entity
    entity2: Entity
    relationship_type: str
    confidence: float
    evidence: str
    source_document: str


class RelationshipMapper:
    """
    Map relationships between entities
    
    Types: SPATIAL, TEMPORAL, HIERARCHICAL, TRANSACTIONAL, SOCIAL, LEGAL, GEOGRAPHIC
    """
    
    def __init__(self):
        """Initialize relationship mapper"""
        self.relationship_patterns = self._build_patterns()
    
    def _build_patterns(self) -> dict:
        """Build relationship detection patterns"""
        return {
            'EMPLOYS': ['{ORG} employs {PERSON}', '{PERSON} works at {ORG}'],
            'OWNS': ['{ORG} owns {ORG}', '{PERSON} owns {ORG}'],
            'PAYS': ['{entity} paid {entity}', '{entity} pays {entity}'],
            'LOCATED_IN': ['{ORG} in {GPE}', '{ORG} located in {GPE}']
        }
    
    def extract(
        self,
        entities: List[Entity],
        text: str,
        document_id: str
    ) -> List[Relationship]:
        """
        Extract relationships from entities and text
        
        Args:
            entities: List of entities
            text: Source text
            document_id: Document identifier
            
        Returns:
            List of relationships
        """
        relationships = []
        
        # Co-occurrence relationships
        for i, e1 in enumerate(entities):
            for e2 in entities[i+1:]:
                # Check if entities appear in same sentence
                if self._in_same_sentence(e1, e2, text):
                    rel = self._infer_relationship(e1, e2, text, document_id)
                    if rel:
                        relationships.append(rel)
        
        return relationships
    
    def _in_same_sentence(self, e1: Entity, e2: Entity, text: str) -> bool:
        """Check if entities are in same sentence"""
        # Simple sentence boundary detection
        min_pos = min(e1.start, e2.start)
        max_pos = max(e1.end, e2.end)
        
        # Check for period between entities
        between_text = text[min_pos:max_pos]
        return '.' not in between_text
    
    def _infer_relationship(
        self,
        e1: Entity,
        e2: Entity,
        text: str,
        document_id: str
    ) -> Optional[Relationship]:
        """Infer relationship type from context"""
        # Extract context between entities
        start = min(e1.start, e2.start)
        end = max(e1.end, e2.end)
        context = text[start:end]
        
        # Pattern-based detection
        if 'paid' in context.lower() or 'payment' in context.lower():
            return Relationship(
                entity1=e1,
                entity2=e2,
                relationship_type='PAYS',
                confidence=0.75,
                evidence=context,
                source_document=document_id
            )
        
        # Default co-occurrence
        return Relationship(
            entity1=e1,
            entity2=e2,
            relationship_type='CO_OCCURS',
            confidence=0.5,
            evidence=context,
            source_document=document_id
        )
