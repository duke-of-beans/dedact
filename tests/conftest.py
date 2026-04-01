"""
Test Suite for DEDACT
Run with: pytest tests/
"""

import pytest
from pathlib import Path

# Test data directory
TEST_DATA_DIR = Path(__file__).parent / 'test_data'

@pytest.fixture
def sample_pdf_path():
    """Fixture for sample PDF path"""
    return TEST_DATA_DIR / 'sample.pdf'

@pytest.fixture
def test_config():
    """Fixture for test configuration"""
    return {
        'confidence_threshold': 0.6,
        'ocr_enabled': True,
        'parallel_workers': 2
    }
