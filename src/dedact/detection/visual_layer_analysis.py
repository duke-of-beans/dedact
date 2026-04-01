"""
Visual Layer Analysis Module
Detects potential redactions by analyzing rendered PDF images
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple
import cv2
import numpy as np
from pdf2image import convert_from_path
from PIL import Image


@dataclass
class BoundingBox:
    """Rectangle coordinates for redaction regions"""
    x: int
    y: int
    width: int
    height: int
    page: int
    
    @property
    def area(self) -> int:
        """Calculate area of bounding box"""
        return self.width * self.height
    
    def overlaps(self, other: 'BoundingBox', threshold: float = 0.5) -> bool:
        """Check if this box overlaps with another"""
        if self.page != other.page:
            return False
        
        # Calculate intersection
        x_left = max(self.x, other.x)
        y_top = max(self.y, other.y)
        x_right = min(self.x + self.width, other.x + other.width)
        y_bottom = min(self.y + self.height, other.y + other.height)
        
        if x_right < x_left or y_bottom < y_top:
            return False
        
        intersection_area = (x_right - x_left) * (y_bottom - y_top)
        smaller_area = min(self.area, other.area)
        
        return (intersection_area / smaller_area) >= threshold


@dataclass
class RedactionCandidate:
    """Potential redaction with confidence score"""
    bbox: BoundingBox
    confidence: float
    detection_method: str
    color: Tuple[int, int, int]
    regularity_score: float


class VisualLayerAnalyzer:
    """
    Analyze PDF visual layer to detect potential redactions
    
    Strategy:
    1. Render PDF pages to images (300 DPI)
    2. Convert to grayscale
    3. Detect dark rectangular regions
    4. Filter by size, color, shape regularity
    5. Score confidence based on multiple factors
    """
    
    def __init__(
        self,
        dpi: int = 300,
        min_area: int = 100,
        max_area: int = 100000,
        black_threshold: int = 50,
        regularity_threshold: float = 0.85
    ):
        """
        Initialize analyzer
        
        Args:
            dpi: Resolution for PDF rendering
            min_area: Minimum redaction area in pixels
            max_area: Maximum redaction area in pixels
            black_threshold: Maximum brightness for "black" (0-255)
            regularity_threshold: Minimum shape regularity (0.0-1.0)
        """
        self.dpi = dpi
        self.min_area = min_area
        self.max_area = max_area
        self.black_threshold = black_threshold
        self.regularity_threshold = regularity_threshold
    
    def analyze(self, pdf_path: Path) -> List[RedactionCandidate]:
        """
        Analyze PDF for potential redactions
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            List of redaction candidates with confidence scores
        """
        candidates = []
        
        # Render PDF to images
        images = convert_from_path(str(pdf_path), dpi=self.dpi)
        
        # Process each page
        for page_num, image in enumerate(images, start=1):
            page_candidates = self._analyze_page(image, page_num)
            candidates.extend(page_candidates)
        
        return candidates
    
    def _analyze_page(self, image: Image.Image, page_num: int) -> List[RedactionCandidate]:
        """
        Analyze single page for redactions
        
        Args:
            image: PIL Image of page
            page_num: Page number (1-indexed)
            
        Returns:
            List of redaction candidates for this page
        """
        # Convert to numpy array and grayscale
        img_array = np.array(image)
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # Threshold to find dark regions
        _, binary = cv2.threshold(gray, self.black_threshold, 255, cv2.THRESH_BINARY_INV)
        
        # Find contours
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        candidates = []
        for contour in contours:
            candidate = self._evaluate_contour(contour, page_num, img_array)
            if candidate:
                candidates.append(candidate)
        
        return candidates
    
    def _evaluate_contour(
        self, 
        contour: np.ndarray, 
        page_num: int, 
        image: np.ndarray
    ) -> RedactionCandidate | None:
        """
        Evaluate if contour is likely a redaction
        
        Args:
            contour: OpenCV contour
            page_num: Page number
            image: Original image array
            
        Returns:
            RedactionCandidate if likely redaction, else None
        """
        # Get bounding rectangle
        x, y, w, h = cv2.boundingRect(contour)
        area = w * h
        
        # Filter by size
        if area < self.min_area or area > self.max_area:
            return None
        
        # Calculate shape regularity (how rectangular is it)
        contour_area = cv2.contourArea(contour)
        regularity = contour_area / area if area > 0 else 0
        
        if regularity < self.regularity_threshold:
            return None
        
        # Extract average color from region
        region = image[y:y+h, x:x+w]
        avg_color = tuple(region.mean(axis=(0, 1)).astype(int))
        
        # Calculate confidence
        confidence = self._calculate_confidence(
            area=area,
            regularity=regularity,
            color=avg_color,
            aspect_ratio=w/h if h > 0 else 0
        )
        
        bbox = BoundingBox(x=x, y=y, width=w, height=h, page=page_num)
        
        return RedactionCandidate(
            bbox=bbox,
            confidence=confidence,
            detection_method='contour_detection',
            color=avg_color,
            regularity_score=regularity
        )
    
    def _calculate_confidence(
        self,
        area: int,
        regularity: float,
        color: Tuple[int, int, int],
        aspect_ratio: float
    ) -> float:
        """
        Calculate confidence that this is a redaction
        
        Factors:
        - Color darkness (darker = higher confidence)
        - Shape regularity (more rectangular = higher)
        - Aspect ratio (typical redactions are 3:1 to 10:1)
        - Size (typical redactions are 1000-50000 px²)
        
        Args:
            area: Bounding box area in pixels
            regularity: Shape regularity score (0.0-1.0)
            color: Average RGB color
            aspect_ratio: Width/height ratio
            
        Returns:
            Confidence score (0.0-1.0)
        """
        confidence = 0.0
        
        # Color score (darker = more confident)
        brightness = sum(color) / 3
        color_score = max(0, (255 - brightness) / 255) * 0.3
        confidence += color_score
        
        # Regularity score
        regularity_score = regularity * 0.3
        confidence += regularity_score
        
        # Aspect ratio score (prefer 3:1 to 10:1)
        if 3.0 <= aspect_ratio <= 10.0:
            aspect_score = 0.2
        elif 2.0 <= aspect_ratio < 3.0 or 10.0 < aspect_ratio <= 15.0:
            aspect_score = 0.1
        else:
            aspect_score = 0.05
        confidence += aspect_score
        
        # Size score (prefer 1000-50000)
        if 1000 <= area <= 50000:
            size_score = 0.2
        elif 500 <= area < 1000 or 50000 < area <= 100000:
            size_score = 0.1
        else:
            size_score = 0.05
        confidence += size_score
        
        return min(1.0, confidence)
