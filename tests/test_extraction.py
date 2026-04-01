"""
Tests for Extraction Module
"""

import pytest
from dedact.extraction import (
    DirectTextRecoverer,
    OCRProcessor,
    MetadataExtractor,
    FragmentReconstructor
)


class TestDirectTextRecoverer:
    """Test direct text recovery"""
    
    def test_initialization(self):
        """Test recoverer initialization"""
        recoverer = DirectTextRecoverer()
        assert recoverer is not None


class TestOCRProcessor:
    """Test OCR processing"""
    
    def test_initialization(self):
        """Test processor initialization"""
        processor = OCRProcessor()
        assert processor is not None
    
    def test_preprocessing_strategies(self):
        """Test that all preprocessing strategies are available"""
        processor = OCRProcessor()
        strategies = ['standard', 'low_quality', 'high_contrast', 'degraded']
        assert all(s in processor.preprocessing_strategies for s in strategies)


class TestMetadataExtractor:
    """Test metadata extraction"""
    
    def test_initialization(self):
        """Test extractor initialization"""
        extractor = MetadataExtractor()
        assert extractor is not None


class TestFragmentReconstructor:
    """Test fragment reconstruction"""
    
    def test_initialization(self):
        """Test reconstructor initialization"""
        reconstructor = FragmentReconstructor()
        assert reconstructor is not None
