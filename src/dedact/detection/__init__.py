"""
Detection Module
Redaction detection and classification
"""

from .visual_layer_analysis import VisualLayerAnalyzer, BoundingBox, RedactionCandidate
from .text_layer_analysis import TextLayerAnalyzer, TextPosition, TextGap
from .redaction_correlation import RedactionCorrelator, ConfirmedRedaction, VulnerabilityType
from .confidence_scoring import ConfidenceScorer, ConfidenceLevel

__all__ = [
    'VisualLayerAnalyzer',
    'BoundingBox',
    'RedactionCandidate',
    'TextLayerAnalyzer',
    'TextPosition',
    'TextGap',
    'RedactionCorrelator',
    'ConfirmedRedaction',
    'VulnerabilityType',
    'ConfidenceScorer',
    'ConfidenceLevel'
]
