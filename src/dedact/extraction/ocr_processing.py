"""
OCR Processing Module
Extract text from images using Tesseract OCR with preprocessing
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy as np
from pdf2image import convert_from_path
from ..detection.redaction_correlation import ConfirmedRedaction, BoundingBox


@dataclass
class OCRResult:
    """OCR extraction result"""
    text: str
    confidence: float
    word_confidences: list[float]
    method: str
    preprocessing_applied: str
    char_count: int


class OCRProcessor:
    """
    Extract text from images using OCR
    
    For Type 2 vulnerabilities (image-based redactions requiring OCR)
    
    Features:
    - Multiple preprocessing strategies
    - Confidence scoring
    - Fallback processing
    """
    
    def __init__(
        self,
        dpi: int = 300,
        tesseract_config: str = '--oem 3 --psm 6',
        confidence_threshold: float = 0.6
    ):
        """
        Initialize OCR processor
        
        Args:
            dpi: Resolution for PDF rendering
            tesseract_config: Tesseract configuration string
            confidence_threshold: Minimum acceptable confidence
        """
        self.dpi = dpi
        self.tesseract_config = tesseract_config
        self.confidence_threshold = confidence_threshold
        self.method_name = 'tesseract_ocr'
    
    def extract(
        self,
        pdf_path: Path,
        redaction: ConfirmedRedaction,
        preprocessing: str = 'standard'
    ) -> Optional[OCRResult]:
        """
        Extract text from redacted region using OCR
        
        Args:
            pdf_path: Path to PDF file
            redaction: Confirmed redaction
            preprocessing: Strategy ('standard', 'low_quality', 'high_contrast', 'degraded')
            
        Returns:
            OCRResult if successful
        """
        if not redaction.visual_bbox:
            return None
        
        try:
            # Render PDF page to image
            images = convert_from_path(
                str(pdf_path),
                dpi=self.dpi,
                first_page=redaction.page,
                last_page=redaction.page
            )
            
            if not images:
                return None
            
            page_image = images[0]
            
            # Crop to redaction region
            bbox = redaction.visual_bbox
            region = page_image.crop((bbox.x, bbox.y, bbox.x + bbox.width, bbox.y + bbox.height))
            
            # Apply preprocessing
            processed = self._preprocess_image(region, preprocessing)
            
            # Run OCR
            ocr_data = pytesseract.image_to_data(
                processed,
                config=self.tesseract_config,
                output_type=pytesseract.Output.DICT
            )
            
            # Extract text and confidence
            text, word_confs = self._extract_text_and_confidence(ocr_data)
            
            if not text or not text.strip():
                return None
            
            # Calculate overall confidence
            avg_conf = sum(word_confs) / len(word_confs) if word_confs else 0.0
            
            if avg_conf < self.confidence_threshold:
                # Try alternative preprocessing
                return self._try_alternative_preprocessing(
                    region,
                    preprocessing
                )
            
            return OCRResult(
                text=text.strip(),
                confidence=avg_conf / 100.0,  # Tesseract gives 0-100
                word_confidences=word_confs,
                method=self.method_name,
                preprocessing_applied=preprocessing,
                char_count=len(text.strip())
            )
        
        except Exception as e:
            return None
    
    def _preprocess_image(self, image: Image.Image, strategy: str) -> Image.Image:
        """
        Preprocess image for OCR
        
        Args:
            image: PIL Image
            strategy: Preprocessing strategy
            
        Returns:
            Preprocessed image
        """
        # Convert to numpy array
        img_array = np.array(image)
        
        if strategy == 'standard':
            return self._standard_preprocessing(img_array)
        elif strategy == 'low_quality':
            return self._low_quality_preprocessing(img_array)
        elif strategy == 'high_contrast':
            return self._high_contrast_preprocessing(img_array)
        elif strategy == 'degraded':
            return self._degraded_preprocessing(img_array)
        else:
            return image
    
    def _standard_preprocessing(self, img: np.ndarray) -> Image.Image:
        """Standard preprocessing pipeline"""
        # Grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        
        # CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        
        # Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(enhanced, (3, 3), 0)
        
        # Otsu's thresholding
        _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return Image.fromarray(binary)
    
    def _low_quality_preprocessing(self, img: np.ndarray) -> Image.Image:
        """Preprocessing for low-quality scans"""
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        
        # Aggressive noise reduction
        denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
        
        # Edge enhancement
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        enhanced = cv2.filter2D(denoised, -1, kernel)
        
        # Adaptive thresholding
        binary = cv2.adaptiveThreshold(
            enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
        
        return Image.fromarray(binary)
    
    def _high_contrast_preprocessing(self, img: np.ndarray) -> Image.Image:
        """Preprocessing for high-contrast images"""
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        
        # Adaptive thresholding
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY, 15, 10
        )
        
        # Morphological operations
        kernel = np.ones((2,2), np.uint8)
        morphed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        
        return Image.fromarray(morphed)
    
    def _degraded_preprocessing(self, img: np.ndarray) -> Image.Image:
        """Preprocessing for degraded/damaged documents"""
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        
        # Non-local means denoising (slow but effective)
        denoised = cv2.fastNlMeansDenoising(gray, None, 15, 7, 21)
        
        # Contrast normalization
        normalized = cv2.normalize(denoised, None, 0, 255, cv2.NORM_MINMAX)
        
        # Sharpening
        kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
        sharpened = cv2.filter2D(normalized, -1, kernel)
        
        # Thresholding
        _, binary = cv2.threshold(sharpened, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return Image.fromarray(binary)
    
    def _extract_text_and_confidence(
        self,
        ocr_data: dict
    ) -> Tuple[str, list[float]]:
        """
        Extract text and confidence scores from Tesseract output
        
        Args:
            ocr_data: Tesseract data dictionary
            
        Returns:
            Tuple of (text, word_confidences)
        """
        words = []
        confidences = []
        
        for i, text in enumerate(ocr_data['text']):
            conf = float(ocr_data['conf'][i])
            
            # Filter out low-confidence or empty results
            if conf > 0 and text.strip():
                words.append(text)
                confidences.append(conf)
        
        return ' '.join(words), confidences
    
    def _try_alternative_preprocessing(
        self,
        image: Image.Image,
        current_strategy: str
    ) -> Optional[OCRResult]:
        """
        Try alternative preprocessing if first attempt failed
        
        Args:
            image: Original image region
            current_strategy: Strategy that failed
            
        Returns:
            OCRResult if successful with alternative
        """
        # Define alternative strategies
        alternatives = {
            'standard': ['high_contrast', 'low_quality'],
            'low_quality': ['degraded', 'standard'],
            'high_contrast': ['standard', 'degraded'],
            'degraded': ['low_quality', 'high_contrast']
        }
        
        for alt_strategy in alternatives.get(current_strategy, []):
            processed = self._preprocess_image(image, alt_strategy)
            
            try:
                ocr_data = pytesseract.image_to_data(
                    processed,
                    config=self.tesseract_config,
                    output_type=pytesseract.Output.DICT
                )
                
                text, word_confs = self._extract_text_and_confidence(ocr_data)
                
                if text and word_confs:
                    avg_conf = sum(word_confs) / len(word_confs)
                    
                    if avg_conf >= self.confidence_threshold:
                        return OCRResult(
                            text=text.strip(),
                            confidence=avg_conf / 100.0,
                            word_confidences=word_confs,
                            method=f"{self.method_name}_fallback",
                            preprocessing_applied=alt_strategy,
                            char_count=len(text.strip())
                        )
            except:
                continue
        
        return None
    
    def extract_batch(
        self,
        pdf_path: Path,
        redactions: list[ConfirmedRedaction],
        preprocessing: str = 'standard'
    ) -> list[Optional[OCRResult]]:
        """
        Process multiple redactions with OCR
        
        Args:
            pdf_path: Path to PDF
            redactions: List of redactions
            preprocessing: Preprocessing strategy
            
        Returns:
            List of OCR results
        """
        return [self.extract(pdf_path, r, preprocessing) for r in redactions]
