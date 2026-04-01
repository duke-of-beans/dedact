"""
MCP Integration Module  
Integrate with Model Context Protocol servers
"""

from pathlib import Path
import json
from typing import Dict, List


class MCPIntegrator:
    """
    Integrate DEDACT results with MCP servers
    
    Features:
    - Generate JSON indices for MCP
    - Update corpus files with recovered content
    - Enable enhanced queries (include_recovered=True)
    """
    
    def __init__(self, corpus_path: Path):
        """
        Initialize MCP integrator
        
        Args:
            corpus_path: Path to corpus directory
        """
        self.corpus_path = Path(corpus_path)
    
    def generate_entity_index(
        self,
        entities: List[Dict],
        output_filename: str = 'entity_index.json'
    ) -> Path:
        """
        Generate entity index for MCP server
        
        Args:
            entities: List of canonical entities
            output_filename: Output filename
            
        Returns:
            Path to generated index
        """
        index = {}
        
        for entity in entities:
            canonical_name = entity.get('canonical_name')
            if canonical_name:
                index[canonical_name] = {
                    'id': entity.get('id'),
                    'type': entity.get('type'),
                    'aliases': entity.get('aliases', []),
                    'mentions': entity.get('mention_count', 0),
                    'confidence': entity.get('confidence', 0.0),
                    'source': 'dedact_recovered'
                }
        
        output_path = self.corpus_path / output_filename
        with open(output_path, 'w') as f:
            json.dump(index, f, indent=2)
        
        return output_path
    
    def generate_cross_reference_index(
        self,
        recovered_content: List[Dict],
        output_filename: str = 'cross_reference_index.json'
    ) -> Path:
        """
        Generate cross-reference index
        
        Args:
            recovered_content: List of recovered content items
            output_filename: Output filename
            
        Returns:
            Path to generated index
        """
        index = {}
        
        for item in recovered_content:
            text = item.get('text', '')
            words = text.lower().split()
            
            for word in words:
                if len(word) > 3:  # Filter short words
                    if word not in index:
                        index[word] = {'occurrences': []}
                    
                    index[word]['occurrences'].append({
                        'document': item.get('document_id'),
                        'page': item.get('page'),
                        'confidence': item.get('confidence'),
                        'source': 'recovered'
                    })
        
        output_path = self.corpus_path / output_filename
        with open(output_path, 'w') as f:
            json.dump(index, f, indent=2)
        
        return output_path
    
    def update_corpus_metadata(
        self,
        corpus_stats: Dict
    ) -> Path:
        """
        Update corpus metadata with DEDACT results
        
        Args:
            corpus_stats: Statistics from processing
            
        Returns:
            Path to metadata file
        """
        metadata_path = self.corpus_path / 'dedact_metadata.json'
        
        metadata = {
            'dedact_version': '1.0.0',
            'processing_complete': True,
            'statistics': corpus_stats,
            'indices': [
                'entity_index.json',
                'cross_reference_index.json'
            ]
        }
        
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return metadata_path
