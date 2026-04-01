"""Tests for Ingestion Module"""

import pytest
from pathlib import Path
from src.ingestion import FileDiscoverer, QualityAssessor


class TestFileDiscoverer:
    """Test file discovery functionality"""
    
    def test_discover_pdfs(self, tmp_path):
        """Test PDF discovery"""
        # Create test PDFs
        (tmp_path / 'test1.pdf').touch()
        (tmp_path / 'test2.pdf').touch()
        
        discoverer = FileDiscoverer()
        files = list(discoverer.discover(tmp_path))
        
        assert len(files) == 2
        assert all(f.format == '.pdf' for f in files)
    
    def test_hash_calculation(self, tmp_path):
        """Test file hashing"""
        test_file = tmp_path / 'test.pdf'
        test_file.write_bytes(b'test content')
        
        discoverer = FileDiscoverer()
        files = list(discoverer.discover(tmp_path))
        
        assert len(files) == 1
        assert len(files[0].hash) == 64  # SHA256 hex length


class TestQualityAssessor:
    """Test quality assessment"""
    
    def test_strategy_selection(self):
        """Test processing strategy selection"""
        assessor = QualityAssessor()
        
        # Should select appropriate strategy based on file characteristics
        # This would need actual PDF files to test properly
        pass
