"""
Confidence Scoring Module
Multi-factor confidence calculation for redaction recovery
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional
from .redaction_correlation import ConfirmedRedaction, VulnerabilityType


class ConfidenceLevel(Enum):
    """Confidence level classifications"""
    VERY_LOW = "very_low"  # < 0.25
    LOW = "low"  # 0.25-0.49
    MEDIUM = "medium"  # 0.50-0.79
    HIGH = "high"  # 0.80-1.00


@dataclass
class ConfidenceScore:
    """Complete confidence assessment"""
    overall: float  # 0.0-1.0
    level: ConfidenceLevel
    method_confidence: float
    source_quality: float
    context_validation: float
    breakdown: Dict[str, float]
    recommendation: str


class ConfidenceScorer:
    """
    Calculate multi-factor confidence scores
    
    Factors:
    1. Method Confidence (extraction method reliability)
    2. Source Quality (document quality/resolution)
    3. Context Validation (linguistic coherence, document style)
    4. Multiple Method Agreement
    """
    
    def __init__(self):
        """Initialize confidence scorer"""
        pass
    
    def score(
        self,
        redaction: ConfirmedRedaction,
        extraction_method: Optional[str] = None,
        document_quality: Optional[str] = None,
        multiple_methods_agree: bool = False
    ) -> ConfidenceScore:
        """
        Calculate complete confidence score
        
        Args:
            redaction: Confirmed redaction to score
            extraction_method: Method used ('direct', 'ocr', 'metadata', 'fragment')
            document_quality: Quality assessment ('high', 'medium', 'low')
            multiple_methods_agree: Whether multiple extraction methods agree
            
        Returns:
            Complete confidence score
        """
        # Calculate component scores
        method_conf = self._score_extraction_method(
            redaction, 
            extraction_method
        )
        source_qual = self._score_source_quality(document_quality)
        context_val = self._score_context_validation(redaction)
        
        # Calculate overall (geometric mean for conservative estimate)
        overall = (method_conf * source_qual * context_val) ** (1/3)
        
        # Adjustment for multiple methods
        if multiple_methods_agree:
            overall = min(1.0, overall + 0.1)
        
        # Determine level
        level = self._determine_level(overall)
        
        # Generate recommendation
        recommendation = self._generate_recommendation(level, redaction)
        
        # Build breakdown
        breakdown = {
            'method_confidence': method_conf,
            'source_quality': source_qual,
            'context_validation': context_val,
            'multiple_methods_bonus': 0.1 if multiple_methods_agree else 0.0
        }
        
        return ConfidenceScore(
            overall=overall,
            level=level,
            method_confidence=method_conf,
            source_quality=source_qual,
            context_validation=context_val,
            breakdown=breakdown,
            recommendation=recommendation
        )
    
    def _score_extraction_method(
        self,
        redaction: ConfirmedRedaction,
        method: Optional[str]
    ) -> float:
        """
        Score based on extraction method reliability
        
        Args:
            redaction: Redaction with vulnerability type
            method: Extraction method
            
        Returns:
            Method confidence (0.0-1.0)
        """
        # Base score by vulnerability type
        if redaction.vulnerability_type == VulnerabilityType.TYPE_1_VISUAL_OVERLAY:
            base_score = 0.95  # Direct text extraction - very reliable
        elif redaction.vulnerability_type == VulnerabilityType.TYPE_4_FRAGMENT:
            base_score = 0.75  # Fragment reconstruction - moderate
        elif redaction.vulnerability_type == VulnerabilityType.TYPE_2_IMAGE_BASED:
            base_score = 0.60  # OCR - less reliable
        else:
            base_score = 0.50
        
        # Adjust by specific method if provided
        if method == 'direct_text':
            return min(1.0, base_score * 1.05)
        elif method == 'ocr_high_conf':
            return min(1.0, base_score * 0.95)
        elif method == 'ocr_low_conf':
            return min(1.0, base_score * 0.75)
        elif method == 'fragment_reconstruction':
            return min(1.0, base_score * 0.80)
        
        return base_score
    
    def _score_source_quality(self, quality: Optional[str]) -> float:
        """
        Score based on document source quality
        
        Args:
            quality: Quality assessment string
            
        Returns:
            Quality score (0.0-1.0)
        """
        if not quality:
            return 0.7  # Default moderate quality
        
        quality = quality.lower()
        
        if quality in ('high', 'excellent', 'pristine'):
            return 0.95
        elif quality in ('medium', 'good', 'acceptable'):
            return 0.80
        elif quality in ('low', 'poor', 'degraded'):
            return 0.50
        elif quality in ('very_low', 'damaged', 'corrupted'):
            return 0.30
        
        return 0.7
    
    def _score_context_validation(self, redaction: ConfirmedRedaction) -> float:
        """
        Score based on context validation
        
        Checks:
        - Linguistic coherence
        - Document style consistency
        - Text flow
        
        Args:
            redaction: Redaction with text content
            
        Returns:
            Context validation score (0.0-1.0)
        """
        if not redaction.text_content:
            return 0.5  # No text to validate
        
        score = 0.5  # Base score
        
        text = redaction.text_content.strip()
        
        # Length check (very short/long suspicious)
        if 10 <= len(text) <= 200:
            score += 0.2
        elif 5 <= len(text) < 10 or 200 < len(text) <= 500:
            score += 0.1
        
        # Printable characters check
        printable_ratio = sum(c.isprintable() for c in text) / len(text) if text else 0
        if printable_ratio > 0.95:
            score += 0.2
        elif printable_ratio > 0.85:
            score += 0.1
        
        # Word structure check (has spaces, not just gibberish)
        if ' ' in text and not text.isspace():
            score += 0.1
        
        return min(1.0, score)
    
    def _determine_level(self, overall: float) -> ConfidenceLevel:
        """
        Determine confidence level from overall score
        
        Args:
            overall: Overall confidence score
            
        Returns:
            Confidence level classification
        """
        if overall >= 0.80:
            return ConfidenceLevel.HIGH
        elif overall >= 0.50:
            return ConfidenceLevel.MEDIUM
        elif overall >= 0.25:
            return ConfidenceLevel.LOW
        else:
            return ConfidenceLevel.VERY_LOW
    
    def _generate_recommendation(
        self,
        level: ConfidenceLevel,
        redaction: ConfirmedRedaction
    ) -> str:
        """
        Generate usage recommendation based on confidence
        
        Args:
            level: Confidence level
            redaction: Redaction details
            
        Returns:
            Recommendation string
        """
        if level == ConfidenceLevel.HIGH:
            return "Include in primary analysis. High confidence recovery."
        elif level == ConfidenceLevel.MEDIUM:
            return "Include with caveat. Moderate confidence - verify if possible."
        elif level == ConfidenceLevel.LOW:
            return "Flag as 'possible'. Use with caution - manual review recommended."
        else:
            return "Exclude from analysis. Confidence too low for reliable use."
    
    def score_batch(
        self,
        redactions: list[ConfirmedRedaction],
        extraction_methods: Optional[Dict[int, str]] = None,
        document_quality: Optional[str] = None
    ) -> Dict[int, ConfidenceScore]:
        """
        Score multiple redactions efficiently
        
        Args:
            redactions: List of redactions to score
            extraction_methods: Dict mapping index to method
            document_quality: Quality for all redactions
            
        Returns:
            Dict mapping redaction index to confidence score
        """
        scores = {}
        
        for i, redaction in enumerate(redactions):
            method = extraction_methods.get(i) if extraction_methods else None
            score = self.score(
                redaction=redaction,
                extraction_method=method,
                document_quality=document_quality
            )
            scores[i] = score
        
        return scores
    
    def get_statistics(
        self,
        scores: Dict[int, ConfidenceScore]
    ) -> Dict[str, any]:
        """
        Calculate statistics across multiple scores
        
        Args:
            scores: Dict of confidence scores
            
        Returns:
            Statistics dictionary
        """
        if not scores:
            return {}
        
        overall_scores = [s.overall for s in scores.values()]
        levels = [s.level for s in scores.values()]
        
        return {
            'total_count': len(scores),
            'mean_confidence': sum(overall_scores) / len(overall_scores),
            'min_confidence': min(overall_scores),
            'max_confidence': max(overall_scores),
            'high_confidence_count': sum(1 for l in levels if l == ConfidenceLevel.HIGH),
            'medium_confidence_count': sum(1 for l in levels if l == ConfidenceLevel.MEDIUM),
            'low_confidence_count': sum(1 for l in levels if l == ConfidenceLevel.LOW),
            'very_low_confidence_count': sum(1 for l in levels if l == ConfidenceLevel.VERY_LOW)
        }
