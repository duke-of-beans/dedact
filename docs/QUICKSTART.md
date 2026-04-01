# DEDACT Quick Start Guide

Get up and running with DEDACT in 10 minutes.

---

## Prerequisites

- Python 3.10+
- Tesseract OCR 5.0+
- 8GB RAM minimum (16GB recommended)
- PostgreSQL 14+ (optional)
- Neo4j Community 5.0+ (optional)

---

## Installation

### 1. Install Dependencies

```bash
# Navigate to DEDACT directory
cd D:/Dev/dedact

# Install Python dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_lg
```

### 2. Install Tesseract OCR

**Windows:**
Download from: https://github.com/UB-Mannheim/tesseract/wiki
Add to PATH: `C:\Program Files\Tesseract-OCR`

**Verify installation:**
```bash
tesseract --version
```

### 3. Install DEDACT

```bash
pip install -e .
```

---

## First Run

### Process Single Document

```bash
dedact process document.pdf --output results/
```

### Process Directory

```bash
dedact process D:/path/to/pdfs/ --output results/ --parallel 4
```

### With Custom Configuration

```bash
# Crisis Capitalism project
dedact process docs/ --config config/crisis_capitalism.yaml

# Epstein corpus (victim protection enabled)
dedact process docs/ --config config/epstein_corpus.yaml
```

---

## Python API Example

```python
from pathlib import Path
from dedact import (
    FileDiscoverer,
    VisualLayerAnalyzer,
    TextLayerAnalyzer,
    RedactionCorrelator,
    DirectTextRecoverer
)

# Discover PDFs
discoverer = FileDiscoverer()
files = list(discoverer.discover(Path('documents/')))

# Analyze first file
visual_analyzer = VisualLayerAnalyzer()
text_analyzer = TextLayerAnalyzer()
correlator = RedactionCorrelator()

visual_candidates = visual_analyzer.analyze(files[0].path)
text_positions, text_gaps = text_analyzer.analyze(files[0].path)
redactions = correlator.correlate(visual_candidates, text_positions, text_gaps)

# Extract content
recoverer = DirectTextRecoverer()
for redaction in redactions:
    if redaction.extractable:
        content = recoverer.extract(files[0].path, redaction)
        print(f"[{redaction.vulnerability_type.name}] Recovered: {content.text}")
        print(f"Confidence: {content.confidence:.2f}")
```

---

## Output Structure

```
results/
├── documents.json          # Document metadata
├── redactions.json         # All detected redactions
├── recovered_content.json  # Extracted content
├── entities.json          # Named entities
├── relationships.json     # Entity relationships
└── network_graph.cypher   # Neo4j import script
```

---

## Next Steps

1. **Configure for your project:** Edit `config/your_project.yaml`
2. **Review results:** Check `results/` directory
3. **Load to database:** Use PostgreSQL and Neo4j loaders
4. **Explore network:** Import Cypher script to Neo4j

---

## Common Issues

**Tesseract not found:**
```bash
# Add to PATH or set environment variable
export TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata
```

**spaCy model missing:**
```bash
python -m spacy download en_core_web_lg
```

**Memory errors:**
```bash
# Reduce parallel workers
dedact process docs/ --parallel 2
```

---

## Support

**Documentation:** `docs/`  
**Examples:** `examples/`  
**Issues:** Internal project - contact project lead
