"""
Tests for Detection Module
"""

import pytest
from pathlib import Path
from dedact.detection import (
    VisualLayerAnalyzer,
    TextLayerAnalyzer,
    RedactionCorrelator,
    ConfidenceScorer
)


class TestVisualLayerAnalyzer:
    """Test visual layer analysis"""
    
    def test_initialization(self):
        """Test analyzer initialization"""
        analyzer = VisualLayerAnalyzer()
        assert analyzer is not None
    
    def test_analyze_returns_candidates(self, sample_pdf_path):
        """Test that analyze returns redaction candidates"""
        if not sample_pdf_path.exists():
            pytest.skip("Sample PDF not available")
        
        analyzer = VisualLayerAnalyzer()
        candidates = analyzer.analyze(sample_pdf_path, page=0)
        assert isinstance(candidates, list)


class TestTextLayerAnalyzer:
    """Test text layer analysis"""
    
    def test_initialization(self):
        """Test analyzer initialization"""
        analyzer = TextLayerAnalyzer()
        assert analyzer is not None
    
    def test_analyze_returns_positions_and_gaps(self, sample_pdf_path):
        """Test that analyze returns text positions and gaps"""
        if not sample_pdf_path.exists():
            pytest.skip("Sample PDF not available")
        
        analyzer = TextLayerAnalyzer()
        positions, gaps = analyzer.analyze(sample_pdf_path, page=0)
        assert isinstance(positions, list)
        assert isinstance(gaps, list)


class TestRedactionCorrelator:
    """Test redaction correlation"""
    
    def test_initialization(self):
        """Test correlator initialization"""
        correlator = RedactionCorrelator()
        assert correlator is not None


class TestConfidenceScorer:
    """Test confidence scoring"""
    
    def test_initialization(self):
        """Test scorer initialization"""
        scorer = ConfidenceScorer()
        assert scorer is not None
