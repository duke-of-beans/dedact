"""
DEDACT Quality Assessment
Assess document quality and determine processing strategy
"""
from pathlib import Path
from typing import Optional
import PyPDF2

from ..models.data_models import (
    DiscoveredFile,
    QualityScore,
    ProcessingStrategy
)


class QualityAssessor:
    """
    Assess document quality and recommend processing strategy
    
    Checks for:
    - Text layer presence
    - Encryption
    - Corruption
    - OCR requirements
    """
    
    def assess(self, file: DiscoveredFile) -> QualityScore:
        """
        Assess file quality and recommend processing strategy
        
        Args:
            file: DiscoveredFile to assess
            
        Returns:
            QualityScore with recommendations
        """
        if file.format != '.pdf':
            return self._non_pdf_assessment(file)
        
        return self._assess_pdf(file.path)
    
    def _assess_pdf(self, path: Path) -> QualityScore:
        """
        Assess PDF quality
        
        Returns:
            QualityScore with strategy recommendation
        """
        try:
            with open(path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                
                # Check encryption
                if reader.is_encrypted:
                    return QualityScore(
                        readable=False,
                        has_text_layer=False,
                        ocr_required=False,
                        encrypted=True,
                        corrupted=False,
                        recommended_strategy=ProcessingStrategy.FAILED,
                        confidence=1.0
                    )
                
                # Check text layer
                has_text = self._has_text_layer(reader)
                
                # Determine strategy
                if has_text:
                    strategy = ProcessingStrategy.DIRECT
                    confidence = 0.9
                else:
                    strategy = ProcessingStrategy.OCR_PRIMARY
                    confidence = 0.7
                
                return QualityScore(
                    readable=True,
                    has_text_layer=has_text,
                    ocr_required=not has_text,
                    encrypted=False,
                    corrupted=False,
                    recommended_strategy=strategy,
                    confidence=confidence
                )
                
        except PyPDF2.errors.PdfReadError:
            return QualityScore(
                readable=False,
                has_text_layer=False,
                ocr_required=False,
                encrypted=False,
                corrupted=True,
                recommended_strategy=ProcessingStrategy.FAILED,
                confidence=1.0
            )
        except Exception as e:
            # Unknown error, mark as corrupted
            return QualityScore(
                readable=False,
                has_text_layer=False,
                ocr_required=False,
                encrypted=False,
                corrupted=True,
                recommended_strategy=ProcessingStrategy.FAILED,
                confidence=1.0
            )
    
    def _has_text_layer(self, reader: PyPDF2.PdfReader, sample_pages: int = 3) -> bool:
        """
        Check if PDF has extractable text layer
        
        Samples first N pages to determine if text is present
        
        Args:
            reader: PyPDF2 PdfReader object
            sample_pages: Number of pages to sample
            
        Returns:
            True if text layer detected
        """
        pages_to_check = min(sample_pages, len(reader.pages))
        
        for i in range(pages_to_check):
            try:
                text = reader.pages[i].extract_text()
                # If we get meaningful text (>50 chars), assume text layer exists
                if text and len(text.strip()) > 50:
                    return True
            except:
                continue
        
        return False
    
    def _non_pdf_assessment(self, file: DiscoveredFile) -> QualityScore:
        """Assessment for non-PDF files (future expansion)"""
        return QualityScore(
            readable=False,
            has_text_layer=False,
            ocr_required=False,
            encrypted=False,
            corrupted=False,
            recommended_strategy=ProcessingStrategy.FAILED,
            confidence=1.0
        )
