"""
DEDACT File Discovery
Recursively scan directories for documents to process
"""
from pathlib import Path
from typing import Generator, List
import hashlib
from datetime import datetime

from ..models.data_models import DiscoveredFile


class FileDiscoverer:
    """
    Recursively discover files in a directory
    
    Generates file metadata including hash, size, modification time
    Uses generator pattern for memory efficiency with large corpuses
    """
    
    def __init__(self, extensions: List[str] = None):
        """
        Initialize file discoverer
        
        Args:
            extensions: List of file extensions to process (e.g., ['.pdf'])
                       If None, defaults to ['.pdf']
        """
        self.extensions = extensions or ['.pdf']
    
    def discover(self, path: Path | str) -> Generator[DiscoveredFile, None, None]:
        """
        Discover files in directory or single file
        
        Args:
            path: Directory or file path
            
        Yields:
            DiscoveredFile objects with metadata
            
        Example:
            discoverer = FileDiscoverer()
            for file in discoverer.discover("/path/to/corpus"):
                print(file.path, file.hash)
        """
        path = Path(path)
        
        if path.is_file():
            if self._should_process(path):
                yield self._create_file_metadata(path)
        elif path.is_dir():
            yield from self._discover_recursive(path)
        else:
            raise ValueError(f"Path does not exist: {path}")
    
    def _discover_recursive(self, directory: Path) -> Generator[DiscoveredFile, None, None]:
        """Recursively discover files in directory"""
        for item in directory.rglob('*'):
            if item.is_file() and self._should_process(item):
                yield self._create_file_metadata(item)
    
    def _should_process(self, file_path: Path) -> bool:
        """Check if file should be processed based on extension"""
        return file_path.suffix.lower() in self.extensions
    
    def _create_file_metadata(self, file_path: Path) -> DiscoveredFile:
        """
        Create DiscoveredFile with complete metadata
        
        Args:
            file_path: Path to file
            
        Returns:
            DiscoveredFile with hash, size, timestamps
        """
        stat = file_path.stat()
        
        return DiscoveredFile(
            path=file_path,
            size=stat.st_size,
            hash=self._calculate_hash(file_path),
            modified=datetime.fromtimestamp(stat.st_mtime),
            format=file_path.suffix.lower()
        )
    
    def _calculate_hash(self, file_path: Path, chunk_size: int = 8192) -> str:
        """
        Calculate SHA256 hash of file
        
        Uses streaming to handle large files efficiently
        
        Args:
            file_path: Path to file
            chunk_size: Bytes to read per iteration
            
        Returns:
            Hexadecimal SHA256 hash
        """
        sha256 = hashlib.sha256()
        
        with open(file_path, 'rb') as f:
            while chunk := f.read(chunk_size):
                sha256.update(chunk)
        
        return sha256.hexdigest()
