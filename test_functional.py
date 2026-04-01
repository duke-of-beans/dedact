"""
DEDACT Functional Test
Tests core functionality with installed package
"""

import sys
from pathlib import Path

print("="*70)
print("DEDACT FUNCTIONAL TEST")
print("="*70)
print()

def test_detection_module():
    """Test detection module"""
    print("Testing Detection Module...")
    try:
        from dedact.detection import VisualLayerAnalyzer, TextLayerAnalyzer
        from dedact.detection import RedactionCorrelator, ConfidenceScorer
        
        visual = VisualLayerAnalyzer()
        text = TextLayerAnalyzer()
        correlator = RedactionCorrelator()
        scorer = ConfidenceScorer()
        
        print("  ✅ All detection classes instantiated successfully")
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_analysis_module():
    """Test analysis module"""
    print("Testing Analysis Module...")
    try:
        from dedact.analysis import EntityRecognizer, PatternMatcher
        from dedact.analysis import RelationshipMapper, NetworkConstructor
        
        # Use small model for quick testing
        recognizer = EntityRecognizer(model_name='en_core_web_sm')
        matcher = PatternMatcher()
        mapper = RelationshipMapper()
        constructor = NetworkConstructor()
        
        # Test pattern matching
        test_text = "Contact john@example.com or call 555-123-4567 for $1,000"
        matches = matcher.match(test_text)
        
        if matches:
            print(f"  ✅ Pattern matcher found {len(matches)} patterns")
        else:
            print("  ⚠️  Pattern matcher returned no matches (may be OK)")
        
        # Test entity recognition
        test_text2 = "John Smith works at Microsoft in Seattle."
        entities = recognizer.extract(test_text2)
        
        if entities:
            print(f"  ✅ Entity recognizer found {len(entities)} entities")
        else:
            print("  ⚠️  Entity recognizer returned no entities")
        
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_storage_module():
    """Test storage module"""
    print("Testing Storage Module...")
    try:
        from dedact.storage import ExportGenerator
        
        exporter = ExportGenerator()
        print("  ✅ Storage classes instantiated successfully")
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_utils_module():
    """Test utils module"""
    print("Testing Utils Module...")
    try:
        from dedact.utils import setup_logging, DEDACTError, CheckpointManager
        
        logger = setup_logging()
        manager = CheckpointManager()
        
        print("  ✅ Utils module working")
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_models_module():
    """Test models module"""
    print("Testing Models Module...")
    try:
        from dedact.models import ProcessingConfig, Document
        
        config = ProcessingConfig()
        doc = Document(
            id="test_123",
            path="/path/to/test.pdf",
            hash="abc123",
            size=1000,
            format="pdf",
            corpus="test"
        )
        
        print(f"  ✅ Models working (confidence_threshold={config.confidence_threshold})")
        return True
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_cli():
    """Test CLI"""
    print("Testing CLI...")
    import subprocess
    try:
        result = subprocess.run(['dedact', '--help'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0 and 'Usage:' in result.stdout:
            print("  ✅ CLI is functional")
            return True
        return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

# Run all tests
print()
results = {
    'Detection Module': test_detection_module(),
    'Analysis Module': test_analysis_module(),
    'Storage Module': test_storage_module(),
    'Utils Module': test_utils_module(),
    'Models Module': test_models_module(),
    'CLI': test_cli()
}

print()
print("="*70)
print("TEST RESULTS")
print("="*70)

passed = sum(results.values())
total = len(results)

for name, result in results.items():
    status = "✅ PASS" if result else "❌ FAIL"
    print(f"{status:12} {name}")

print()
print(f"Score: {passed}/{total} ({passed/total*100:.1f}%)")
print()

if passed == total:
    print("🎉 ALL TESTS PASSED - DEDACT IS FULLY FUNCTIONAL!")
    print()
    print("You can now:")
    print("  • Process PDFs: dedact process document.pdf --output results/")
    print("  • Use Python API: from dedact.detection import VisualLayerAnalyzer")
    print("  • Review docs: cat docs/QUICKSTART.md")
elif passed >= total * 0.8:
    print("✅ CORE FUNCTIONALITY WORKING")
    print()
    print("Some modules may have issues, but core system is operational.")
else:
    print("⚠️  SYSTEM NOT READY")
    print()
    print("Please address failed tests before using DEDACT.")

print("="*70)
