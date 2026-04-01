"""
Network Construction Module
Build graph database from entities and relationships
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from .entity_recognition import Entity
from .relationship_mapping import Relationship


@dataclass
class NetworkGraph:
    """Complete network graph"""
    nodes: List[Dict]
    edges: List[Dict]
    statistics: Dict


class NetworkConstructor:
    """
    Build graph database from entities and relationships
    
    Creates:
    - Deduplicated nodes (canonical entities)
    - Weighted edges (relationships)
    - Graph statistics
    - Neo4j-compatible structure
    """
    
    def __init__(self):
        """Initialize network constructor"""
        self.node_id_counter = 0
        self.canonical_entities = {}
    
    def build(
        self,
        entities: List[Entity],
        relationships: List[Relationship],
        corpus_id: str
    ) -> NetworkGraph:
        """
        Build complete network graph
        
        Args:
            entities: List of entities
            relationships: List of relationships
            corpus_id: Corpus identifier
            
        Returns:
            Complete network graph
        """
        # Create canonical nodes
        nodes = self._create_nodes(entities, corpus_id)
        
        # Create edges
        edges = self._create_edges(relationships, corpus_id)
        
        # Calculate statistics
        stats = self._calculate_statistics(nodes, edges)
        
        return NetworkGraph(
            nodes=nodes,
            edges=edges,
            statistics=stats
        )
    
    def _create_nodes(self, entities: List[Entity], corpus_id: str) -> List[Dict]:
        """Create deduplicated nodes"""
        nodes = []
        entity_map = {}
        
        for entity in entities:
            # Create canonical key
            canonical_key = f"{entity.type}:{entity.text.lower()}"
            
            if canonical_key not in entity_map:
                node_id = self._generate_node_id()
                node = {
                    'id': node_id,
                    'canonical_name': entity.text,
                    'type': entity.type,
                    'corpus': corpus_id,
                    'mention_count': 1,
                    'confidence': entity.confidence,
                    'aliases': [entity.text]
                }
                nodes.append(node)
                entity_map[canonical_key] = node_id
                self.canonical_entities[canonical_key] = node_id
            else:
                # Update existing node
                node = next(n for n in nodes if n['id'] == entity_map[canonical_key])
                node['mention_count'] += 1
                if entity.text not in node['aliases']:
                    node['aliases'].append(entity.text)
        
        return nodes
    
    def _create_edges(self, relationships: List[Relationship], corpus_id: str) -> List[Dict]:
        """Create relationship edges"""
        edges = []
        edge_map = {}
        
        for rel in relationships:
            # Get node IDs
            key1 = f"{rel.entity1.type}:{rel.entity1.text.lower()}"
            key2 = f"{rel.entity2.type}:{rel.entity2.text.lower()}"
            
            node1_id = self.canonical_entities.get(key1)
            node2_id = self.canonical_entities.get(key2)
            
            if node1_id and node2_id:
                edge_key = f"{node1_id}:{rel.relationship_type}:{node2_id}"
                
                if edge_key not in edge_map:
                    edge = {
                        'from': node1_id,
                        'to': node2_id,
                        'type': rel.relationship_type,
                        'weight': 1,
                        'confidence': rel.confidence,
                        'evidence': [rel.evidence],
                        'documents': [rel.source_document]
                    }
                    edges.append(edge)
                    edge_map[edge_key] = len(edges) - 1
                else:
                    # Update existing edge
                    idx = edge_map[edge_key]
                    edges[idx]['weight'] += 1
                    edges[idx]['evidence'].append(rel.evidence)
                    if rel.source_document not in edges[idx]['documents']:
                        edges[idx]['documents'].append(rel.source_document)
        
        return edges
    
    def _generate_node_id(self) -> str:
        """Generate unique node ID"""
        self.node_id_counter += 1
        return f"node_{self.node_id_counter}"
    
    def _calculate_statistics(self, nodes: List[Dict], edges: List[Dict]) -> Dict:
        """Calculate graph statistics"""
        node_types = {}
        for node in nodes:
            node_types[node['type']] = node_types.get(node['type'], 0) + 1
        
        edge_types = {}
        for edge in edges:
            edge_types[edge['type']] = edge_types.get(edge['type'], 0) + 1
        
        return {
            'total_nodes': len(nodes),
            'total_edges': len(edges),
            'node_types': node_types,
            'edge_types': edge_types,
            'avg_degree': (2 * len(edges)) / len(nodes) if nodes else 0
        }
    
    def export_neo4j_cypher(self, graph: NetworkGraph) -> str:
        """Generate Neo4j Cypher script"""
        cypher = []
        
        # Create nodes
        for node in graph.nodes:
            props = ', '.join([f"{k}: '{v}'" if isinstance(v, str) else f"{k}: {v}" 
                              for k, v in node.items() if k != 'id'])
            cypher.append(f"CREATE (n:{node['type']} {{{props}}})")
        
        # Create relationships
        for edge in graph.edges:
            cypher.append(
                f"MATCH (a {{id: '{edge['from']}'}}), (b {{id: '{edge['to']}'}}) "
                f"CREATE (a)-[:{edge['type']} {{weight: {edge['weight']}}}]->(b)"
            )
        
        return '\n'.join(cypher)
