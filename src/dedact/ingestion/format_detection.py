"""
DEDACT Format Detection
Validate file formats using magic bytes
"""
from pathlib import Path
from typing import Optional


class FormatDetector:
    """
    Detect and validate file formats using magic bytes
    
    Verifies that files are actually the format their extension claims
    """
    
    # Magic byte signatures for supported formats
    MAGIC_BYTES = {
        'pdf': b'%PDF',
        'png': b'\x89PNG',
        'jpg': b'\xff\xd8\xff',
        'jpeg': b'\xff\xd8\xff',
    }
    
    def detect_format(self, file_path: Path) -> Optional[str]:
        """
        Detect file format using magic bytes
        
        Args:
            file_path: Path to file
            
        Returns:
            Format string (e.g., 'pdf') or None if unrecognized
        """
        try:
            with open(file_path, 'rb') as f:
                header = f.read(8)  # Read first 8 bytes
                
                for fmt, magic in self.MAGIC_BYTES.items():
                    if header.startswith(magic):
                        return fmt
                
                return None
        except Exception:
            return None
    
    def validate_format(self, file_path: Path, expected_format: str) -> bool:
        """
        Validate that file matches expected format
        
        Args:
            file_path: Path to file
            expected_format: Expected format (e.g., 'pdf')
            
        Returns:
            True if format matches, False otherwise
        """
        detected = self.detect_format(file_path)
        
        # Handle extension variations (jpg/jpeg)
        if expected_format in ['jpg', 'jpeg'] and detected in ['jpg', 'jpeg']:
            return True
        
        return detected == expected_format
    
    def get_pdf_version(self, file_path: Path) -> Optional[str]:
        """
        Extract PDF version from header
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            PDF version string (e.g., '1.7') or None
        """
        try:
            with open(file_path, 'rb') as f:
                header = f.read(16).decode('ascii', errors='ignore')
                
                if header.startswith('%PDF-'):
                    version = header[5:8]  # e.g., '1.7'
                    return version.strip()
                
                return None
        except Exception:
            return None
