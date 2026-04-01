"""Test imports one by one to find the issue"""

print("Testing imports one by one...\n")

try:
    print("[1] Testing detection...")
    from dedact.detection import VisualLayerAnalyzer
    print("    [OK] VisualLayerAnalyzer")
    from dedact.detection import TextLayerAnalyzer
    print("    [OK] TextLayerAnalyzer")
    from dedact.detection import RedactionCorrelator
    print("    [OK] RedactionCorrelator")
    from dedact.detection import ConfidenceScorer
    print("    [OK] ConfidenceScorer")
except Exception as e:
    print(f"    [FAIL] {e}")
    import traceback
    traceback.print_exc()

try:
    print("\n[2] Testing extraction...")
    from dedact.extraction import DirectTextRecoverer
    print("    [OK] DirectTextRecoverer")
    from dedact.extraction import OCRProcessor
    print("    [OK] OCRProcessor")
    from dedact.extraction import MetadataExtractor
    print("    [OK] MetadataExtractor")
    from dedact.extraction import FragmentReconstructor
    print("    [OK] FragmentReconstructor")
except Exception as e:
    print(f"    [FAIL] {e}")
    import traceback
    traceback.print_exc()

try:
    print("\n[3] Testing analysis...")
    from dedact.analysis import EntityRecognizer
    print("    [OK] EntityRecognizer")
    from dedact.analysis import PatternMatcher
    print("    [OK] PatternMatcher")
    from dedact.analysis import RelationshipMapper
    print("    [OK] RelationshipMapper")
    from dedact.analysis import NetworkConstructor
    print("    [OK] NetworkConstructor")
except Exception as e:
    print(f"    [FAIL] {e}")
    import traceback
    traceback.print_exc()

print("\n[DONE] Import test complete")
