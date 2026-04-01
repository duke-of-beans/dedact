"""
Data Models Module
Core data classes for DEDACT
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime
from pathlib import Path


@dataclass
class DiscoveredFile:
    """File discovered during ingestion"""
    path: Path
    size: int
    hash: str
    modified: datetime
    format: str


@dataclass
class QualityScore:
    """Quality assessment score for a document"""
    score: float  # 0.0-1.0
    has_text_layer: bool
    page_count: int
    average_dpi: Optional[int]
    is_scanned: bool
    is_encrypted: bool
    

@dataclass
class ProcessingStrategy:
    """Recommended processing strategy based on quality"""
    use_ocr: bool
    confidence_threshold: float
    extraction_methods: List[str]
    priority: str  # 'high', 'medium', 'low'


@dataclass
class ProcessingConfig:
    """Configuration for processing"""
    confidence_threshold: float = 0.6
    ocr_enabled: bool = True
    parallel_workers: int = 4
    extraction_depth: str = 'comprehensive'
    entity_types: List[str] = field(default_factory=lambda: ['PERSON', 'ORG', 'MONEY', 'DATE'])


@dataclass
class Document:
    """Document metadata"""
    id: str
    path: Path
    hash: str
    size: int
    format: str
    corpus: str
    processed: Optional[datetime] = None
    status: str = 'pending'


@dataclass
class ProcessingResult:
    """Complete processing result for document"""
    document_id: str
    success: bool
    redactions_found: int
    content_recovered: int
    entities_extracted: int
    confidence_distribution: Dict[str, int]
    processing_time: float
    errors: List[str] = field(default_factory=list)


@dataclass
class CorpusStatistics:
    """Statistics for entire corpus"""
    total_documents: int
    documents_processed: int
    total_redactions: int
    high_confidence_recoveries: int
    medium_confidence_recoveries: int
    low_confidence_recoveries: int
    total_entities: int
    total_relationships: int
    processing_time: float
    timestamp: datetime = field(default_factory=datetime.now)
