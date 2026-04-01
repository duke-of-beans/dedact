"""
DEDACT Installation Verification Script
Checks all components and dependencies
"""

import sys
from pathlib import Path

print("="*70)
print("DEDACT v1.0.0 - INSTALLATION VERIFICATION")
print("="*70)
print()

# Track results
checks_passed = 0
checks_failed = 0
warnings = []

def check(description, test_func):
    """Run a verification check"""
    global checks_passed, checks_failed
    try:
        result = test_func()
        if result:
            print(f"✅ {description}")
            checks_passed += 1
            return True
        else:
            print(f"❌ {description}")
            checks_failed += 1
            return False
    except Exception as e:
        print(f"❌ {description}")
        print(f"   Error: {e}")
        checks_failed += 1
        return False

def warn(message):
    """Record a warning"""
    global warnings
    warnings.append(message)
    print(f"⚠️  {message}")

# ============================================================================
# SECTION 1: PYTHON VERSION
# ============================================================================
print("SECTION 1: Python Version")
print("-" * 70)

def check_python_version():
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print(f"   Python {version.major}.{version.minor}.{version.micro}")
        return True
    return False

check("Python 3.10+ installed", check_python_version)
print()

# ============================================================================
# SECTION 2: DIRECTORY STRUCTURE
# ============================================================================
print("SECTION 2: Directory Structure")
print("-" * 70)

base_dir = Path(__file__).parent

required_dirs = [
    'src',
    'src/ingestion',
    'src/detection', 
    'src/extraction',
    'src/analysis',
    'src/storage',
    'src/integration',
    'src/utils',
    'src/models',
    'src/cli',
    'config',
    'docs',
    'tests',
    'examples',
    'Logs'
]

for dir_path in required_dirs:
    full_path = base_dir / dir_path
    check(f"Directory exists: {dir_path}", lambda p=full_path: p.exists() and p.is_dir())

print()

# ============================================================================
# SECTION 3: CONFIGURATION FILES
# ============================================================================
print("SECTION 3: Configuration Files")
print("-" * 70)

required_files = [
    'DEDACT_DNA.yaml',
    'DEDACT_PROTOCOLS.md',
    'RESEARCH_INTEGRATION.md',
    'DEDACT_MANIFEST.yaml',
    'SYSTEM_ARCHITECTURE.md',
    'requirements.txt',
    'setup.py',
    'README.md',
    '.gitignore',
    'config/default.yaml',
    'config/crisis_capitalism.yaml',
    'config/epstein_corpus.yaml',
    'config/hirm.yaml'
]

for file_path in required_files:
    full_path = base_dir / file_path
    check(f"File exists: {file_path}", lambda p=full_path: p.exists() and p.is_file())

print()

# ============================================================================
# SECTION 4: CORE DEPENDENCIES
# ============================================================================
print("SECTION 4: Core Dependencies")
print("-" * 70)

dependencies = {
    'PyPDF2': 'PDF processing',
    'pdf2image': 'PDF to image conversion',
    'pytesseract': 'OCR engine',
    'PIL': 'Image processing (Pillow)',
    'cv2': 'Computer vision (OpenCV)',
    'spacy': 'NLP and entity recognition',
    'psycopg2': 'PostgreSQL connector',
    'neo4j': 'Neo4j graph database',
    'yaml': 'YAML configuration (PyYAML)',
    'click': 'CLI framework',
    'requests': 'HTTP requests',
    'tqdm': 'Progress bars',
    'fuzzywuzzy': 'Fuzzy string matching',
    'numpy': 'Numerical computing',
    'pandas': 'Data analysis'
}

for module, description in dependencies.items():
    def check_import(m=module, d=description):
        try:
            __import__(m)
            return True
        except ImportError:
            return False
    
    check(f"{module:20s} - {description}", check_import)

print()

# ============================================================================
# SECTION 5: DEDACT MODULES
# ============================================================================
print("SECTION 5: DEDACT Modules")
print("-" * 70)

# Add src to path
src_path = base_dir / 'src'
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

dedact_modules = [
    ('ingestion', 'FileDiscoverer'),
    ('ingestion', 'FileValidator'),
    ('ingestion', 'DuplicateDetector'),
    ('detection', 'VisualLayerAnalyzer'),
    ('detection', 'TextLayerAnalyzer'),
    ('detection', 'RedactionCorrelator'),
    ('detection', 'ConfidenceScorer'),
    ('extraction', 'DirectTextRecoverer'),
    ('extraction', 'OCRProcessor'),
    ('extraction', 'MetadataExtractor'),
    ('extraction', 'FragmentReconstructor'),
    ('analysis', 'EntityRecognizer'),
    ('analysis', 'PatternMatcher'),
    ('analysis', 'RelationshipMapper'),
    ('analysis', 'NetworkConstructor'),
    ('storage', 'PostgreSQLLoader'),
    ('storage', 'Neo4jLoader'),
    ('storage', 'ExportGenerator'),
    ('integration', 'MCPIntegrator'),
    ('integration', 'EntityResolver'),
    ('utils', 'setup_logging'),
    ('utils', 'DEDACTError'),
    ('utils', 'CheckpointManager'),
    ('models', 'ProcessingConfig')
]

for module_name, class_name in dedact_modules:
    def check_class(mod=module_name, cls=class_name):
        try:
            module = __import__(module_name, fromlist=[cls])
            return hasattr(module, cls)
        except Exception as e:
            return False
    
    check(f"{module_name}.{class_name}", check_class)

print()

# ============================================================================
# SECTION 6: SPACY MODEL
# ============================================================================
print("SECTION 6: spaCy NLP Model")
print("-" * 70)

def check_spacy_model():
    try:
        import spacy
        nlp = spacy.load('en_core_web_lg')
        return True
    except OSError:
        warn("spaCy model 'en_core_web_lg' not found - run: python -m spacy download en_core_web_lg")
        return False
    except Exception as e:
        return False

check("spaCy en_core_web_lg model", check_spacy_model)
print()

# ============================================================================
# SECTION 7: OPTIONAL DEPENDENCIES
# ============================================================================
print("SECTION 7: Optional Dependencies (Database)")
print("-" * 70)

optional_deps = [
    ('PostgreSQL', lambda: __import__('psycopg2')),
    ('Neo4j Driver', lambda: __import__('neo4j'))
]

for name, test_func in optional_deps:
    try:
        test_func()
        print(f"✅ {name} driver installed")
    except ImportError:
        warn(f"{name} driver installed but database not configured (optional)")

print()

# ============================================================================
# SECTION 8: EXTERNAL TOOLS
# ============================================================================
print("SECTION 8: External Tools")
print("-" * 70)

def check_tesseract():
    import subprocess
    try:
        result = subprocess.run(['tesseract', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"   {version_line}")
            return True
        return False
    except FileNotFoundError:
        warn("Tesseract OCR not found - install from: https://github.com/UB-Mannheim/tesseract/wiki")
        return False
    except Exception:
        return False

check("Tesseract OCR installed", check_tesseract)
print()

# ============================================================================
# SECTION 9: BASIC FUNCTIONALITY TEST
# ============================================================================
print("SECTION 9: Basic Functionality Test")
print("-" * 70)

def test_basic_functionality():
    try:
        from ingestion import FileDiscoverer
        from detection import VisualLayerAnalyzer, ConfidenceScorer
        from extraction import DirectTextRecoverer
        from analysis import EntityRecognizer
        from utils import setup_logging
        
        # Test instantiation
        discoverer = FileDiscoverer()
        analyzer = VisualLayerAnalyzer()
        scorer = ConfidenceScorer()
        recoverer = DirectTextRecoverer()
        recognizer = EntityRecognizer(model_name='en_core_web_sm')  # Use small model for test
        
        # Test basic entity recognition
        text = "John Smith works at Microsoft in Seattle."
        entities = recognizer.extract(text)
        
        return len(entities) > 0
    except Exception as e:
        print(f"   Error: {e}")
        return False

check("Module instantiation and basic entity extraction", test_basic_functionality)
print()

# ============================================================================
# SECTION 10: CLI AVAILABILITY
# ============================================================================
print("SECTION 10: CLI Command")
print("-" * 70)

def check_cli():
    import subprocess
    try:
        result = subprocess.run(['dedact', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"   {result.stdout.strip()}")
            return True
        return False
    except FileNotFoundError:
        warn("'dedact' command not found - install with: pip install -e .")
        return False
    except Exception as e:
        return False

check("dedact CLI command available", check_cli)
print()

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("="*70)
print("VERIFICATION SUMMARY")
print("="*70)
print(f"✅ Checks Passed: {checks_passed}")
print(f"❌ Checks Failed: {checks_failed}")
print(f"⚠️  Warnings: {len(warnings)}")
print()

if warnings:
    print("WARNINGS:")
    for warning in warnings:
        print(f"  • {warning}")
    print()

total_checks = checks_passed + checks_failed
success_rate = (checks_passed / total_checks * 100) if total_checks > 0 else 0

print(f"Success Rate: {success_rate:.1f}%")
print()

if checks_failed == 0:
    print("🎉 ALL CHECKS PASSED - DEDACT IS FULLY OPERATIONAL!")
    print()
    print("Next Steps:")
    print("  1. Process a test document: dedact process sample.pdf --output results/")
    print("  2. Run example script: python examples/basic_usage.py")
    print("  3. Review documentation: docs/QUICKSTART.md")
elif success_rate >= 80:
    print("✅ DEDACT IS MOSTLY OPERATIONAL")
    print()
    print("Minor issues detected - review warnings above.")
    print("Core functionality should work, but some features may be limited.")
else:
    print("⚠️  INSTALLATION INCOMPLETE")
    print()
    print("Critical issues detected - please resolve failed checks above.")
    print("Installation may not work correctly until issues are resolved.")

print()
print("="*70)
