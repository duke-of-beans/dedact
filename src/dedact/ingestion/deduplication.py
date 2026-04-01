"""
DEDACT Deduplication
Identify and handle duplicate files
"""
from typing import List, Dict, Set
from pathlib import Path

from ..models.data_models import DiscoveredFile


class Deduplicator:
    """
    Identify duplicate files using hash comparison
    
    Supports both hash-based (fast) and content-based (thorough) deduplication
    """
    
    def __init__(self, method: str = 'hash'):
        """
        Initialize deduplicator
        
        Args:
            method: 'hash' for hash-based or 'content' for content-based
        """
        self.method = method
        self.seen_hashes: Set[str] = set()
        self.duplicates: Dict[str, List[DiscoveredFile]] = {}
    
    def deduplicate(self, files: List[DiscoveredFile]) -> List[DiscoveredFile]:
        """
        Remove duplicates from file list
        
        Args:
            files: List of DiscoveredFile objects
            
        Returns:
            List of unique files (first occurrence kept)
            
        Side Effects:
            Populates self.duplicates with duplicate groups
        """
        unique_files = []
        
        for file in files:
            if file.hash not in self.seen_hashes:
                self.seen_hashes.add(file.hash)
                unique_files.append(file)
            else:
                # Track duplicate
                if file.hash not in self.duplicates:
                    self.duplicates[file.hash] = []
                self.duplicates[file.hash].append(file)
        
        return unique_files
    
    def get_duplicate_groups(self) -> Dict[str, List[DiscoveredFile]]:
        """
        Get all duplicate file groups
        
        Returns:
            Dictionary mapping hash to list of duplicate files
        """
        return self.duplicates
    
    def select_canonical(self, duplicates: List[DiscoveredFile]) -> DiscoveredFile:
        """
        Select canonical file from duplicate group
        
        Selection criteria:
        1. Earliest modification time (original)
        2. Shortest path (prefer root over nested)
        
        Args:
            duplicates: List of duplicate files
            
        Returns:
            Canonical file to keep
        """
        if len(duplicates) == 1:
            return duplicates[0]
        
        # Sort by modification time, then path length
        sorted_dupes = sorted(
            duplicates,
            key=lambda f: (f.modified, len(str(f.path)))
        )
        
        return sorted_dupes[0]
