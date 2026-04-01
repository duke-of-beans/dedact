"""
Direct Text Recovery Module
Extract text directly from PDF text layer
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import PyPDF2
from ..detection.redaction_correlation import ConfirmedRedaction, BoundingBox


@dataclass
class RecoveredContent:
    """Recovered content with metadata"""
    text: str
    confidence: float
    method: str
    page: int
    bbox: Optional[BoundingBox]
    font_metadata: dict
    char_count: int


class DirectTextRecoverer:
    """
    Extract text directly from PDF text layer
    
    For Type 1 vulnerabilities (visual overlay with readable text layer)
    """
    
    def __init__(self):
        """Initialize text recoverer"""
        self.method_name = 'direct_text_extraction'
    
    def extract(
        self,
        pdf_path: Path,
        redaction: ConfirmedRedaction
    ) -> Optional[RecoveredContent]:
        """
        Extract text from redacted region
        
        Args:
            pdf_path: Path to PDF file
            redaction: Confirmed redaction to extract
            
        Returns:
            RecoveredContent if successful, None if failed
        """
        if not redaction.text_content:
            return None
        
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                if redaction.page > len(reader.pages):
                    return None
                
                page = reader.pages[redaction.page - 1]  # 0-indexed
                
                # Extract all text from page
                full_text = page.extract_text()
                
                if not full_text:
                    return None
                
                # For Type 1 vulnerabilities, we already have the text
                # from correlation analysis
                text = redaction.text_content
                
                # Validate extracted text
                if not self._validate_text(text):
                    return None
                
                # Calculate confidence based on text quality
                confidence = self._calculate_confidence(text, page)
                
                # Get font metadata (if available)
                font_metadata = self._extract_font_metadata(page)
                
                return RecoveredContent(
                    text=text,
                    confidence=confidence,
                    method=self.method_name,
                    page=redaction.page,
                    bbox=redaction.visual_bbox,
                    font_metadata=font_metadata,
                    char_count=len(text)
                )
        
        except Exception as e:
            # Handle extraction errors
            return None
    
    def _validate_text(self, text: str) -> bool:
        """
        Validate extracted text quality
        
        Args:
            text: Extracted text
            
        Returns:
            True if text appears valid
        """
        if not text or not text.strip():
            return False
        
        # Check for minimum length
        if len(text.strip()) < 2:
            return False
        
        # Check for reasonable printable character ratio
        printable_count = sum(1 for c in text if c.isprintable())
        ratio = printable_count / len(text) if text else 0
        
        if ratio < 0.7:  # At least 70% printable
            return False
        
        return True
    
    def _calculate_confidence(self, text: str, page: PyPDF2.PageObject) -> float:
        """
        Calculate extraction confidence
        
        Args:
            text: Extracted text
            page: PDF page object
            
        Returns:
            Confidence score (0.0-1.0)
        """
        confidence = 0.85  # Base confidence for direct extraction
        
        # Adjust for text quality
        printable_ratio = sum(1 for c in text if c.isprintable()) / len(text) if text else 0
        confidence += (printable_ratio - 0.85) * 0.3  # Bonus for high quality
        
        # Adjust for text length (very short or very long more suspicious)
        length = len(text.strip())
        if 10 <= length <= 200:
            confidence += 0.05
        elif length < 5 or length > 1000:
            confidence -= 0.10
        
        # Clamp to valid range
        return max(0.0, min(1.0, confidence))
    
    def _extract_font_metadata(self, page: PyPDF2.PageObject) -> dict:
        """
        Extract font metadata from page (if available)
        
        Args:
            page: PDF page object
            
        Returns:
            Dictionary of font metadata
        """
        metadata = {
            'fonts': [],
            'sizes': [],
            'encoding': None
        }
        
        try:
            # Attempt to extract font information
            # This is simplified - real implementation would parse PDF resources
            if hasattr(page, '/Resources') and page['/Resources']:
                resources = page['/Resources']
                if '/Font' in resources:
                    fonts = resources['/Font']
                    metadata['fonts'] = [str(f) for f in fonts.keys()]
        except:
            pass  # Font metadata extraction is optional
        
        return metadata
    
    def extract_batch(
        self,
        pdf_path: Path,
        redactions: list[ConfirmedRedaction]
    ) -> list[Optional[RecoveredContent]]:
        """
        Extract multiple redactions from same PDF
        
        Args:
            pdf_path: Path to PDF file
            redactions: List of redactions to extract
            
        Returns:
            List of recovered content (None for failures)
        """
        return [self.extract(pdf_path, r) for r in redactions]
    
    def get_statistics(
        self,
        results: list[Optional[RecoveredContent]]
    ) -> dict:
        """
        Calculate extraction statistics
        
        Args:
            results: List of extraction results
            
        Returns:
            Statistics dictionary
        """
        successful = [r for r in results if r is not None]
        
        if not successful:
            return {
                'total': len(results),
                'successful': 0,
                'failed': len(results),
                'success_rate': 0.0
            }
        
        return {
            'total': len(results),
            'successful': len(successful),
            'failed': len(results) - len(successful),
            'success_rate': len(successful) / len(results),
            'avg_confidence': sum(r.confidence for r in successful) / len(successful),
            'avg_length': sum(r.char_count for r in successful) / len(successful),
            'total_chars': sum(r.char_count for r in successful)
        }
