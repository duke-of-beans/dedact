"""
Entity Resolution Module
Create canonical entities from multiple mentions
"""

from typing import List, Dict
from fuzzywuzzy import fuzz


class EntityResolver:
    """
    Create canonical entities from mentions
    
    Features:
    - Fuzzy matching for name variations
    - Context-based disambiguation  
    - Canonical name selection
    """
    
    def __init__(self, similarity_threshold: float = 0.85):
        """
        Initialize entity resolver
        
        Args:
            similarity_threshold: Minimum similarity for matching
        """
        self.similarity_threshold = similarity_threshold
    
    def resolve(self, entity_mentions: List[Dict]) -> List[Dict]:
        """
        Resolve entity mentions to canonical entities
        
        Args:
            entity_mentions: List of entity mentions
            
        Returns:
            List of canonical entities
        """
        if not entity_mentions:
            return []
        
        # Group by type first
        by_type = {}
        for mention in entity_mentions:
            entity_type = mention.get('type', 'UNKNOWN')
            if entity_type not in by_type:
                by_type[entity_type] = []
            by_type[entity_type].append(mention)
        
        # Resolve within each type
        canonical = []
        for entity_type, mentions in by_type.items():
            canonical.extend(self._resolve_mentions(mentions, entity_type))
        
        return canonical
    
    def _resolve_mentions(
        self,
        mentions: List[Dict],
        entity_type: str
    ) -> List[Dict]:
        """Resolve mentions of same type"""
        clusters = []
        
        for mention in mentions:
            # Find matching cluster
            matched = False
            for cluster in clusters:
                if self._matches_cluster(mention, cluster):
                    cluster.append(mention)
                    matched = True
                    break
            
            if not matched:
                clusters.append([mention])
        
        # Create canonical entities from clusters
        canonical = []
        for cluster in clusters:
            canonical.append(self._create_canonical(cluster, entity_type))
        
        return canonical
    
    def _matches_cluster(self, mention: Dict, cluster: List[Dict]) -> bool:
        """Check if mention matches existing cluster"""
        for existing in cluster:
            name1 = mention.get('text', '').lower()
            name2 = existing.get('text', '').lower()
            
            similarity = fuzz.ratio(name1, name2) / 100.0
            if similarity >= self.similarity_threshold:
                return True
        
        return False
    
    def _create_canonical(
        self,
        cluster: List[Dict],
        entity_type: str
    ) -> Dict:
        """Create canonical entity from cluster"""
        # Select most frequent name
        name_counts = {}
        for mention in cluster:
            name = mention.get('text', '')
            name_counts[name] = name_counts.get(name, 0) + 1
        
        canonical_name = max(name_counts.items(), key=lambda x: x[1])[0]
        
        return {
            'canonical_name': canonical_name,
            'type': entity_type,
            'aliases': list(name_counts.keys()),
            'mention_count': len(cluster),
            'confidence': sum(m.get('confidence', 0) for m in cluster) / len(cluster)
        }
