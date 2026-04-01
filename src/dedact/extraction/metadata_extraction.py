"""
Metadata Extraction Module
Extract metadata that may contain redacted content
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Any
import PyPDF2
import subprocess
import json
from datetime import datetime


@dataclass
class MetadataCollection:
    """Complete metadata from document"""
    standard: Dict[str, Any]
    custom: Dict[str, Any]
    comments: List[str]
    hidden_objects: List[str]
    relevance_scores: Dict[str, float]
    extraction_depth: str


class MetadataExtractor:
    """
    Extract metadata that might contain redacted information
    
    Extraction Levels:
    - BASIC: Standard properties only
    - COMPREHENSIVE: + custom properties, comments
    - FORENSIC: + hidden objects, internal structure
    """
    
    def __init__(self, extraction_depth: str = 'comprehensive'):
        """
        Initialize metadata extractor
        
        Args:
            extraction_depth: Level of extraction (basic/comprehensive/forensic)
        """
        self.extraction_depth = extraction_depth
        self.method_name = 'metadata_extraction'
    
    def extract(self, file_path: Path) -> MetadataCollection:
        """
        Extract metadata from file
        
        Args:
            file_path: Path to file
            
        Returns:
            Complete metadata collection
        """
        if file_path.suffix.lower() == '.pdf':
            return self._extract_pdf_metadata(file_path)
        else:
            # Future: Add support for DOCX, images, etc.
            return MetadataCollection(
                standard={},
                custom={},
                comments=[],
                hidden_objects=[],
                relevance_scores={},
                extraction_depth=self.extraction_depth
            )
    
    def _extract_pdf_metadata(self, pdf_path: Path) -> MetadataCollection:
        """
        Extract metadata from PDF
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Complete metadata collection
        """
        standard = {}
        custom = {}
        comments = []
        hidden_objects = []
        
        try:
            # Basic metadata with PyPDF2
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                # Standard metadata
                if reader.metadata:
                    for key, value in reader.metadata.items():
                        clean_key = key.replace('/', '')
                        standard[clean_key] = str(value)
                
                # File info
                standard['num_pages'] = len(reader.pages)
                standard['is_encrypted'] = reader.is_encrypted
                
                if self.extraction_depth in ('comprehensive', 'forensic'):
                    # Extract comments/annotations
                    comments = self._extract_annotations(reader)
                
                if self.extraction_depth == 'forensic':
                    # Extract hidden objects
                    hidden_objects = self._extract_hidden_objects(reader)
        
        except Exception as e:
            standard['extraction_error'] = str(e)
        
        # Calculate relevance scores
        relevance_scores = self._score_relevance(standard, custom, comments)
        
        return MetadataCollection(
            standard=standard,
            custom=custom,
            comments=comments,
            hidden_objects=hidden_objects,
            relevance_scores=relevance_scores,
            extraction_depth=self.extraction_depth
        )
    
    def _extract_annotations(self, reader: PyPDF2.PdfReader) -> List[str]:
        """
        Extract annotations/comments from PDF
        
        Args:
            reader: PDF reader object
            
        Returns:
            List of annotation texts
        """
        annotations = []
        
        try:
            for page in reader.pages:
                if '/Annots' in page:
                    annots = page['/Annots']
                    for annot in annots:
                        annot_obj = annot.get_object()
                        if '/Contents' in annot_obj:
                            content = annot_obj['/Contents']
                            annotations.append(str(content))
        except:
            pass  # Annotation extraction is best-effort
        
        return annotations
    
    def _extract_hidden_objects(self, reader: PyPDF2.PdfReader) -> List[str]:
        """
        Extract hidden PDF objects
        
        Args:
            reader: PDF reader object
            
        Returns:
            List of hidden object descriptions
        """
        hidden = []
        
        try:
            # Look for hidden layers (OCGs - Optional Content Groups)
            if '/OCProperties' in reader.trailer.get('/Root', {}):
                hidden.append("Document contains optional content groups (layers)")
            
            # Check for JavaScript
            for page in reader.pages:
                if '/AA' in page:  # Additional Actions
                    hidden.append(f"Page contains JavaScript/Actions")
            
            # Check for embedded files
            if '/Names' in reader.trailer.get('/Root', {}):
                names = reader.trailer['/Root']['/Names']
                if '/EmbeddedFiles' in names:
                    hidden.append("Document contains embedded files")
        except:
            pass
        
        return hidden
    
    def _score_relevance(
        self,
        standard: Dict,
        custom: Dict,
        comments: List[str]
    ) -> Dict[str, float]:
        """
        Score metadata relevance for redaction recovery
        
        Args:
            standard: Standard metadata
            custom: Custom properties
            comments: Annotation texts
            
        Returns:
            Dictionary of relevance scores
        """
        scores = {}
        
        # Author/creator names (HIGH relevance)
        for key in ['Author', 'Creator', 'Producer']:
            if key in standard and standard[key]:
                scores[key] = 0.9
        
        # Dates (MEDIUM relevance)
        for key in ['CreationDate', 'ModDate']:
            if key in standard:
                scores[key] = 0.5
        
        # Comments (HIGH relevance - may mention redacted topics)
        if comments:
            scores['comments'] = 0.9
        
        # Custom properties (varies)
        for key in custom:
            # Suspicious custom property names
            if any(word in key.lower() for word in ['redact', 'hidden', 'delete', 'remove']):
                scores[f'custom_{key}'] = 0.95
            else:
                scores[f'custom_{key}'] = 0.6
        
        return scores
    
    def extract_with_exiftool(self, file_path: Path) -> Optional[Dict]:
        """
        Extract comprehensive metadata using ExifTool
        
        Args:
            file_path: Path to file
            
        Returns:
            Dictionary of metadata or None if ExifTool unavailable
        """
        try:
            # Run ExifTool
            result = subprocess.run(
                ['exiftool', '-j', str(file_path)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return data[0] if data else None
        except (FileNotFoundError, subprocess.TimeoutExpired, json.JSONDecodeError):
            # ExifTool not available or failed
            return None
    
    def find_suspicious_metadata(
        self,
        metadata: MetadataCollection,
        keywords: Optional[List[str]] = None
    ) -> Dict[str, List[str]]:
        """
        Find metadata entries matching suspicious keywords
        
        Args:
            metadata: Metadata collection
            keywords: List of keywords to search for (default: common redaction terms)
            
        Returns:
            Dictionary mapping categories to matching entries
        """
        if keywords is None:
            keywords = [
                'redact', 'classified', 'confidential', 'secret',
                'delete', 'remove', 'hide', 'censor',
                'ssn', 'social security', 'credit card',
                'classified', 'top secret', 'attorney'
            ]
        
        matches = {
            'standard': [],
            'custom': [],
            'comments': [],
            'hidden': []
        }
        
        # Search standard metadata
        for key, value in metadata.standard.items():
            value_str = str(value).lower()
            if any(kw in value_str or kw in key.lower() for kw in keywords):
                matches['standard'].append(f"{key}: {value}")
        
        # Search custom metadata
        for key, value in metadata.custom.items():
            value_str = str(value).lower()
            if any(kw in value_str or kw in key.lower() for kw in keywords):
                matches['custom'].append(f"{key}: {value}")
        
        # Search comments
        for comment in metadata.comments:
            comment_lower = comment.lower()
            if any(kw in comment_lower for kw in keywords):
                matches['comments'].append(comment)
        
        # Hidden objects always flagged
        matches['hidden'] = metadata.hidden_objects
        
        return matches
    
    def export_metadata_report(
        self,
        metadata: MetadataCollection,
        output_path: Path
    ) -> None:
        """
        Export metadata to JSON file
        
        Args:
            metadata: Metadata to export
            output_path: Output file path
        """
        report = {
            'extraction_depth': metadata.extraction_depth,
            'standard_metadata': metadata.standard,
            'custom_metadata': metadata.custom,
            'comments': metadata.comments,
            'hidden_objects': metadata.hidden_objects,
            'relevance_scores': metadata.relevance_scores,
            'timestamp': datetime.now().isoformat()
        }
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
