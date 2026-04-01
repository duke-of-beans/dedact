"""
Cross-Corpus Integration Module
Integrate findings across multiple corpuses
"""

from typing import List, Dict
from fuzzywuzzy import fuzz


class CrossCorpusIntegrator:
    """
    Integrate entities and relationships across corpuses
    
    Features:
    - Entity resolution (fuzzy matching)
    - Relationship merging
    - Conflict detection
    """
    
    def __init__(self, similarity_threshold: float = 0.85):
        """
        Initialize cross-corpus integrator
        
        Args:
            similarity_threshold: Minimum similarity for entity matching
        """
        self.similarity_threshold = similarity_threshold
    
    def resolve_entities(
        self,
        entities_a: List[Dict],
        entities_b: List[Dict]
    ) -> Dict[str, List[Dict]]:
        """
        Resolve entities across corpuses
        
        Args:
            entities_a: Entities from corpus A
            entities_b: Entities from corpus B
            
        Returns:
            Dictionary with 'matched', 'only_a', 'only_b'
        """
        matched = []
        unmatched_a = list(entities_a)
        unmatched_b = list(entities_b)
        
        for ent_a in entities_a:
            for ent_b in entities_b:
                if self._entities_match(ent_a, ent_b):
                    matched.append({
                        'canonical': ent_a,
                        'from_a': ent_a,
                        'from_b': ent_b,
                        'similarity': self._calculate_similarity(ent_a, ent_b)
                    })
                    if ent_a in unmatched_a:
                        unmatched_a.remove(ent_a)
                    if ent_b in unmatched_b:
                        unmatched_b.remove(ent_b)
                    break
        
        return {
            'matched': matched,
            'only_a': unmatched_a,
            'only_b': unmatched_b
        }
    
    def _entities_match(self, ent_a: Dict, ent_b: Dict) -> bool:
        """Check if two entities match"""
        # Type must match
        if ent_a.get('type') != ent_b.get('type'):
            return False
        
        # Fuzzy name matching
        name_a = ent_a.get('canonical_name', '').lower()
        name_b = ent_b.get('canonical_name', '').lower()
        
        similarity = fuzz.ratio(name_a, name_b) / 100.0
        
        return similarity >= self.similarity_threshold
    
    def _calculate_similarity(self, ent_a: Dict, ent_b: Dict) -> float:
        """Calculate similarity score between entities"""
        name_a = ent_a.get('canonical_name', '').lower()
        name_b = ent_b.get('canonical_name', '').lower()
        
        return fuzz.ratio(name_a, name_b) / 100.0
    
    def merge_relationships(
        self,
        rels_a: List[Dict],
        rels_b: List[Dict],
        entity_mapping: Dict[str, str]
    ) -> List[Dict]:
        """
        Merge relationships from multiple corpuses
        
        Args:
            rels_a: Relationships from corpus A
            rels_b: Relationships from corpus B
            entity_mapping: Mapping of entity IDs across corpuses
            
        Returns:
            Merged relationships
        """
        merged = list(rels_a)
        
        for rel_b in rels_b:
            # Map entity IDs
            from_id = entity_mapping.get(rel_b['from'], rel_b['from'])
            to_id = entity_mapping.get(rel_b['to'], rel_b['to'])
            
            # Check if relationship already exists
            existing = next((r for r in merged 
                           if r['from'] == from_id 
                           and r['to'] == to_id 
                           and r['type'] == rel_b['type']), None)
            
            if existing:
                # Merge evidence
                existing['weight'] += rel_b.get('weight', 1)
                existing['evidence'].extend(rel_b.get('evidence', []))
            else:
                merged.append({
                    **rel_b,
                    'from': from_id,
                    'to': to_id
                })
        
        return merged
