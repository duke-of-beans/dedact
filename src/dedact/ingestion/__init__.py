"""
Ingestion Module
File discovery, validation, and preprocessing
"""

from .file_discovery import FileDiscoverer
from .format_detection import FormatDetector
from .deduplication import Deduplicator
from .quality_assessment import QualityAssessor

__all__ = [
    'FileDiscoverer',
    'FormatDetector',
    'Deduplicator',
    'QualityAssessor'
]
