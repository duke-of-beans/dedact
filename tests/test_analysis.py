"""
Tests for Analysis Module
"""

import pytest
from dedact.analysis import (
    EntityRecognizer,
    PatternMatcher,
    RelationshipMapper,
    NetworkConstructor
)


class TestEntityRecognizer:
    """Test entity recognition"""
    
    def test_initialization(self):
        """Test recognizer initialization"""
        recognizer = EntityRecognizer()
        assert recognizer is not None
    
    def test_extract_returns_entities(self):
        """Test that extract returns entity list"""
        recognizer = EntityRecognizer()
        text = "John Smith works at Microsoft in Seattle."
        entities = recognizer.extract(text)
        assert isinstance(entities, list)


class TestPatternMatcher:
    """Test pattern matching"""
    
    def test_initialization(self):
        """Test matcher initialization"""
        matcher = PatternMatcher()
        assert matcher is not None
    
    def test_match_email(self):
        """Test email pattern matching"""
        matcher = PatternMatcher()
        text = "Contact: john@example.com"
        matches = matcher.match(text, patterns=['EMAIL'])
        assert len(matches) > 0
        assert matches[0].pattern_type == 'EMAIL'


class TestRelationshipMapper:
    """Test relationship mapping"""
    
    def test_initialization(self):
        """Test mapper initialization"""
        mapper = RelationshipMapper()
        assert mapper is not None


class TestNetworkConstructor:
    """Test network construction"""
    
    def test_initialization(self):
        """Test constructor initialization"""
        constructor = NetworkConstructor()
        assert constructor is not None
