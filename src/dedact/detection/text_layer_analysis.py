"""
Text Layer Analysis Module
Analyzes PDF text layer to identify gaps and missing content
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Tuple, Set
import PyPDF2
from collections import defaultdict


@dataclass
class TextPosition:
    """Position of text in PDF coordinate system"""
    x: float
    y: float
    width: float
    height: float
    text: str
    page: int
    font_size: float = 0.0


@dataclass
class TextGap:
    """Gap in text layer that might indicate redaction"""
    x: float
    y: float
    width: float
    height: float
    page: int
    surrounding_text: str
    confidence: float


class TextLayerAnalyzer:
    """
    Analyze PDF text layer to find gaps and missing content
    
    Strategy:
    1. Extract all text with positions
    2. Build spatial index of text locations
    3. Identify gaps in text flow
    4. Calculate text density map
    5. Score gaps by size and context
    """
    
    def __init__(
        self,
        min_gap_size: int = 100,
        grid_resolution: int = 50,
        context_window: int = 100
    ):
        """
        Initialize analyzer
        
        Args:
            min_gap_size: Minimum gap area in PDF units
            grid_resolution: Grid cell size for density map
            context_window: Characters of context around gaps
        """
        self.min_gap_size = min_gap_size
        self.grid_resolution = grid_resolution
        self.context_window = context_window
    
    def analyze(self, pdf_path: Path) -> Tuple[List[TextPosition], List[TextGap]]:
        """
        Analyze PDF text layer
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Tuple of (text_positions, text_gaps)
        """
        # Extract text with positions
        text_positions = self._extract_text_positions(pdf_path)
        
        # Find gaps in text
        text_gaps = self._find_text_gaps(text_positions)
        
        return text_positions, text_gaps
    
    def _extract_text_positions(self, pdf_path: Path) -> List[TextPosition]:
        """
        Extract all text with position information
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            List of TextPosition objects
        """
        positions = []
        
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                for page_num, page in enumerate(reader.pages, start=1):
                    # Extract text (basic approach - more advanced parsing possible)
                    try:
                        text = page.extract_text()
                        if text:
                            # Simple position estimation (real implementation would use
                            # more advanced PDF parsing to get actual positions)
                            positions.append(TextPosition(
                                x=0,
                                y=0,
                                width=page.mediabox.width,
                                height=page.mediabox.height,
                                text=text,
                                page=page_num
                            ))
                    except Exception as e:
                        # Handle extraction errors gracefully
                        continue
        
        except Exception as e:
            # Handle file read errors
            raise RuntimeError(f"Failed to read PDF: {e}")
        
        return positions
    
    def _find_text_gaps(self, positions: List[TextPosition]) -> List[TextGap]:
        """
        Identify gaps in text layer
        
        Args:
            positions: List of text positions
            
        Returns:
            List of identified gaps
        """
        gaps = []
        
        # Group by page
        pages: Dict[int, List[TextPosition]] = defaultdict(list)
        for pos in positions:
            pages[pos.page].append(pos)
        
        # Analyze each page
        for page_num, page_positions in pages.items():
            page_gaps = self._analyze_page_gaps(page_num, page_positions)
            gaps.extend(page_gaps)
        
        return gaps
    
    def _analyze_page_gaps(
        self, 
        page_num: int, 
        positions: List[TextPosition]
    ) -> List[TextGap]:
        """
        Analyze gaps on a single page
        
        Args:
            page_num: Page number
            positions: Text positions on this page
            
        Returns:
            List of gaps found on page
        """
        if not positions:
            return []
        
        gaps = []
        
        # Simple gap detection: look for large Y-coordinate jumps
        # (Real implementation would build proper spatial index)
        sorted_positions = sorted(positions, key=lambda p: (p.y, p.x))
        
        for i in range(len(sorted_positions) - 1):
            curr = sorted_positions[i]
            next_pos = sorted_positions[i + 1]
            
            # Calculate vertical gap
            gap_height = next_pos.y - (curr.y + curr.height)
            
            if gap_height > self.min_gap_size:
                # Found a significant gap
                gap = TextGap(
                    x=curr.x,
                    y=curr.y + curr.height,
                    width=curr.width,
                    height=gap_height,
                    page=page_num,
                    surrounding_text=self._get_context(curr, next_pos),
                    confidence=self._calculate_gap_confidence(gap_height, curr, next_pos)
                )
                gaps.append(gap)
        
        return gaps
    
    def _get_context(self, before: TextPosition, after: TextPosition) -> str:
        """
        Get surrounding text context for a gap
        
        Args:
            before: Text position before gap
            after: Text position after gap
            
        Returns:
            Context string
        """
        before_text = before.text[-self.context_window:] if before.text else ""
        after_text = after.text[:self.context_window] if after.text else ""
        
        return f"{before_text}[GAP]{after_text}"
    
    def _calculate_gap_confidence(
        self,
        gap_height: float,
        before: TextPosition,
        after: TextPosition
    ) -> float:
        """
        Calculate confidence that gap indicates redaction
        
        Args:
            gap_height: Height of gap
            before: Text before gap
            after: Text after gap
            
        Returns:
            Confidence score (0.0-1.0)
        """
        confidence = 0.0
        
        # Size factor (larger gaps more suspicious)
        if gap_height > 200:
            confidence += 0.4
        elif gap_height > 100:
            confidence += 0.3
        else:
            confidence += 0.2
        
        # Context factor (mid-sentence gaps more suspicious)
        before_text = before.text.strip() if before.text else ""
        after_text = after.text.strip() if after.text else ""
        
        # Check if gap is mid-sentence (not at paragraph boundary)
        if before_text and not before_text.endswith(('.', '!', '?')):
            confidence += 0.3
        
        if after_text and not after_text[0].isupper():
            confidence += 0.2
        
        return min(1.0, confidence)
    
    def build_density_map(
        self, 
        positions: List[TextPosition], 
        page_width: float, 
        page_height: float
    ) -> Dict[Tuple[int, int], int]:
        """
        Build text density map for visualization
        
        Args:
            positions: List of text positions
            page_width: Page width in PDF units
            page_height: Page height in PDF units
            
        Returns:
            Dictionary mapping (grid_x, grid_y) to text count
        """
        density_map = defaultdict(int)
        
        for pos in positions:
            # Calculate grid cell
            grid_x = int(pos.x / self.grid_resolution)
            grid_y = int(pos.y / self.grid_resolution)
            
            # Increment density
            density_map[(grid_x, grid_y)] += len(pos.text)
        
        return dict(density_map)
    
    def get_suspicious_gaps(
        self, 
        gaps: List[TextGap], 
        min_confidence: float = 0.6
    ) -> List[TextGap]:
        """
        Filter gaps by confidence threshold
        
        Args:
            gaps: All identified gaps
            min_confidence: Minimum confidence threshold
            
        Returns:
            List of high-confidence gaps
        """
        return [gap for gap in gaps if gap.confidence >= min_confidence]
