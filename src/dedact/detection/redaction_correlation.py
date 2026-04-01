"""
Redaction Correlation Module
Correlates visual and text layer findings to confirm vulnerabilities
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional
from .visual_layer_analysis import RedactionCandidate, BoundingBox
from .text_layer_analysis import TextGap, TextPosition


class VulnerabilityType(Enum):
    """Types of redaction vulnerabilities"""
    TYPE_1_VISUAL_OVERLAY = "visual_overlay"  # Black box over readable text
    TYPE_2_IMAGE_BASED = "image_based"  # Requires OCR
    TYPE_3_METADATA = "metadata_leak"  # Not spatial
    TYPE_4_FRAGMENT = "text_fragment"  # Partial content remains
    PROPER_REDACTION = "properly_redacted"  # Actual redaction


@dataclass
class ConfirmedRedaction:
    """Confirmed redaction with vulnerability assessment"""
    visual_bbox: Optional[BoundingBox]
    text_gap: Optional[TextGap]
    vulnerability_type: VulnerabilityType
    correlation_score: float
    text_content: Optional[str]
    confidence: float
    page: int
    extractable: bool


class RedactionCorrelator:
    """
    Correlate visual and text layer findings
    
    Strategy:
    1. Match visual redactions with text gaps
    2. Identify mismatches (visual but no text gap = Type 1 vulnerability)
    3. Score correlation strength
    4. Classify vulnerability types
    """
    
    def __init__(
        self,
        correlation_threshold: float = 0.7,
        position_tolerance: float = 20.0
    ):
        """
        Initialize correlator
        
        Args:
            correlation_threshold: Minimum correlation for confirmation
            position_tolerance: Maximum position difference in PDF units
        """
        self.correlation_threshold = correlation_threshold
        self.position_tolerance = position_tolerance
    
    def correlate(
        self,
        visual_candidates: List[RedactionCandidate],
        text_positions: List[TextPosition],
        text_gaps: List[TextGap]
    ) -> List[ConfirmedRedaction]:
        """
        Correlate visual and text findings
        
        Args:
            visual_candidates: Detected visual redactions
            text_positions: All text positions
            text_gaps: Detected text gaps
            
        Returns:
            List of confirmed redactions with vulnerability types
        """
        confirmed = []
        
        # Process each visual candidate
        for visual in visual_candidates:
            text_in_region = self._find_text_in_region(
                visual.bbox, 
                text_positions
            )
            
            if text_in_region:
                # TYPE 1 VULNERABILITY: Visual overlay with readable text
                confirmed.append(ConfirmedRedaction(
                    visual_bbox=visual.bbox,
                    text_gap=None,
                    vulnerability_type=VulnerabilityType.TYPE_1_VISUAL_OVERLAY,
                    correlation_score=1.0,
                    text_content=text_in_region,
                    confidence=0.9,  # High confidence for Type 1
                    page=visual.bbox.page,
                    extractable=True
                ))
            else:
                # Might be proper redaction or Type 2 (needs OCR)
                matching_gap = self._find_matching_gap(visual.bbox, text_gaps)
                
                if matching_gap:
                    # Text layer properly removed - possible Type 2
                    confirmed.append(ConfirmedRedaction(
                        visual_bbox=visual.bbox,
                        text_gap=matching_gap,
                        vulnerability_type=VulnerabilityType.TYPE_2_IMAGE_BASED,
                        correlation_score=self._calculate_correlation(
                            visual.bbox, 
                            matching_gap
                        ),
                        text_content=None,
                        confidence=0.6,  # Medium confidence - needs OCR verification
                        page=visual.bbox.page,
                        extractable=False  # Requires OCR
                    ))
                else:
                    # Likely proper redaction
                    confirmed.append(ConfirmedRedaction(
                        visual_bbox=visual.bbox,
                        text_gap=None,
                        vulnerability_type=VulnerabilityType.PROPER_REDACTION,
                        correlation_score=0.5,
                        text_content=None,
                        confidence=0.3,  # Low confidence - might still be Type 2
                        page=visual.bbox.page,
                        extractable=False
                    ))
        
        # Check text gaps without visual redactions (Type 4 - Fragments)
        for gap in text_gaps:
            if not self._has_visual_match(gap, visual_candidates):
                confirmed.append(ConfirmedRedaction(
                    visual_bbox=None,
                    text_gap=gap,
                    vulnerability_type=VulnerabilityType.TYPE_4_FRAGMENT,
                    correlation_score=0.0,
                    text_content=gap.surrounding_text,
                    confidence=gap.confidence,
                    page=gap.page,
                    extractable=True
                ))
        
        return confirmed
    
    def _find_text_in_region(
        self,
        bbox: BoundingBox,
        text_positions: List[TextPosition]
    ) -> Optional[str]:
        """
        Find text within bounding box region
        
        Args:
            bbox: Bounding box to check
            text_positions: All text positions
            
        Returns:
            Text content if found, else None
        """
        for pos in text_positions:
            if pos.page != bbox.page:
                continue
            
            # Check if text position overlaps with bbox
            if self._regions_overlap(bbox, pos):
                return pos.text
        
        return None
    
    def _find_matching_gap(
        self,
        bbox: BoundingBox,
        text_gaps: List[TextGap]
    ) -> Optional[TextGap]:
        """
        Find text gap matching visual redaction
        
        Args:
            bbox: Visual redaction bounding box
            text_gaps: List of text gaps
            
        Returns:
            Matching gap if found
        """
        for gap in text_gaps:
            if gap.page != bbox.page:
                continue
            
            # Check position proximity
            if abs(gap.x - bbox.x) <= self.position_tolerance and \
               abs(gap.y - bbox.y) <= self.position_tolerance:
                return gap
        
        return None
    
    def _regions_overlap(
        self,
        bbox: BoundingBox,
        pos: TextPosition
    ) -> bool:
        """
        Check if bounding box and text position overlap
        
        Args:
            bbox: Visual redaction bbox
            pos: Text position
            
        Returns:
            True if overlap detected
        """
        # Simple rectangle intersection
        return not (
            bbox.x + bbox.width < pos.x or
            pos.x + pos.width < bbox.x or
            bbox.y + bbox.height < pos.y or
            pos.y + pos.height < bbox.y
        )
    
    def _calculate_correlation(
        self,
        bbox: BoundingBox,
        gap: TextGap
    ) -> float:
        """
        Calculate correlation score between visual and text layer
        
        Args:
            bbox: Visual redaction
            gap: Text gap
            
        Returns:
            Correlation score (0.0-1.0)
        """
        # Position similarity
        x_diff = abs(bbox.x - gap.x)
        y_diff = abs(bbox.y - gap.y)
        position_score = max(0, 1.0 - (x_diff + y_diff) / (2 * self.position_tolerance))
        
        # Size similarity
        width_diff = abs(bbox.width - gap.width)
        height_diff = abs(bbox.height - gap.height)
        size_score = max(0, 1.0 - (width_diff + height_diff) / (bbox.width + bbox.height))
        
        # Combined score
        return (position_score * 0.6 + size_score * 0.4)
    
    def _has_visual_match(
        self,
        gap: TextGap,
        visual_candidates: List[RedactionCandidate]
    ) -> bool:
        """
        Check if text gap has corresponding visual redaction
        
        Args:
            gap: Text gap
            visual_candidates: Visual redaction candidates
            
        Returns:
            True if match found
        """
        for visual in visual_candidates:
            if visual.bbox.page != gap.page:
                continue
            
            if abs(visual.bbox.x - gap.x) <= self.position_tolerance and \
               abs(visual.bbox.y - gap.y) <= self.position_tolerance:
                return True
        
        return False
    
    def get_extractable_redactions(
        self,
        confirmed: List[ConfirmedRedaction],
        min_confidence: float = 0.6
    ) -> List[ConfirmedRedaction]:
        """
        Filter for high-confidence extractable redactions
        
        Args:
            confirmed: All confirmed redactions
            min_confidence: Minimum confidence threshold
            
        Returns:
            List of extractable redactions
        """
        return [
            r for r in confirmed 
            if r.extractable and r.confidence >= min_confidence
        ]
    
    def get_ocr_candidates(
        self,
        confirmed: List[ConfirmedRedaction]
    ) -> List[ConfirmedRedaction]:
        """
        Get redactions requiring OCR processing
        
        Args:
            confirmed: All confirmed redactions
            
        Returns:
            List of Type 2 (image-based) redactions
        """
        return [
            r for r in confirmed 
            if r.vulnerability_type == VulnerabilityType.TYPE_2_IMAGE_BASED
        ]
