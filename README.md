# DEDACT
## Document Extraction, De-Redaction, and Analysis Capability Tool

Universal document forensics platform for recovering improperly redacted content from PDF corpuses.

**Version:** 1.0.0  
**Status:** Production Ready  
**License:** Private Research Tool

---

## Overview

DEDACT detects and recovers content from improperly redacted PDFs using multiple extraction methods:

- **Type 1 Vulnerabilities:** Visual overlays with readable text layers
- **Type 2 Vulnerabilities:** Image-based redactions recoverable via OCR
- **Type 3 Vulnerabilities:** Metadata leakage
- **Type 4 Vulnerabilities:** Partial text fragments

## Features

✅ **Complete PDF Analysis Pipeline**
- Visual layer analysis (OpenCV contour detection)
- Text layer extraction and gap detection
- Vulnerability correlation and classification
- Multi-factor confidence scoring

✅ **Advanced Extraction Methods**
- Direct text recovery (Type 1)
- OCR with 4 preprocessing strategies (Type 2)
- Comprehensive metadata extraction (Type 3)
- Fragment reconstruction (Type 4)

✅ **Entity Recognition & Network Analysis**
- spaCy NER (PERSON, ORG, GPE, DATE, MONEY, etc.)
- Custom pattern matching (EMAIL, PHONE, SSN, etc.)
- Relationship mapping
- Neo4j graph construction

✅ **Database Integration**
- PostgreSQL (structured data)
- Neo4j (graph database)
- External validation (Wikidata, OpenCorporates)
- MCP server integration

✅ **Multi-Project Support**
- Crisis Capitalism (congressional trading, defense contracts)
- Epstein Corpus (victim protection protocols)
- HIRM (medical research)

---

## Installation

### Requirements
- Python 3.10+
- Tesseract OCR 5.0+
- PostgreSQL 14+ (optional)
- Neo4j Community 5.0+ (optional)

### Quick Start

```bash
# Clone repository
git clone https://github.com/yourusername/dedact.git
cd dedact

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_lg

# Install DEDACT
pip install -e .
```

### Tesseract Installation

**Windows:**
```bash
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
# Add to PATH
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

---

## Usage

### Basic Processing

```bash
# Process single document
dedact process document.pdf --output results/

# Process directory
dedact process /path/to/pdfs/ --output results/ --parallel 8

# With custom configuration
dedact process documents/ --config config/crisis_capitalism.yaml
```

### Advanced Options

```bash
# High-confidence only
dedact process docs/ --confidence 0.80

# Verbose logging
dedact process docs/ -v

# Specific output format
dedact export results/ --format json
```

### Python API

```python
from dedact.ingestion import FileDiscoverer
from dedact.detection import VisualLayerAnalyzer, TextLayerAnalyzer, RedactionCorrelator
from dedact.extraction import DirectTextRecoverer, OCRProcessor

# Discover PDFs
discoverer = FileDiscoverer()
files = list(discoverer.discover(Path('documents/')))

# Detect redactions
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
        print(f"Recovered: {content.text}")
```

---

## Project Configurations

### Crisis Capitalism
```yaml
corpus_id: crisis_capitalism
focus_areas:
  - congressional_trading
  - defense_contracts
  - healthcare_mergers
confidence_threshold: 0.60
```

### Epstein Corpus
```yaml
corpus_id: epstein_corpus
victim_protection:
  enabled: true
  manual_review_required: true
  pseudonymization: true
confidence_threshold: 0.70
```

### HIRM (Medical Research)
```yaml
corpus_id: hirm
focus_areas:
  - clinical_trial_funding
  - researcher_conflicts
confidence_threshold: 0.65
```

---

## Architecture

```
Ingestion → Detection → Extraction → Analysis → Storage → Integration
    ↓           ↓           ↓           ↓          ↓           ↓
Discovery   Visual     Direct Text   Entities   PostgreSQL   MCP
Quality     Text       OCR           Patterns   Neo4j        External DBs
Dedup       Correlation Metadata     Relations  Exports      Entity Resolution
Format      Confidence  Fragments    Network    Reports
```

---

## Database Schemas

### PostgreSQL
```sql
documents (id, path, hash, format, corpus, processed)
redactions (id, document_id, page, bbox, type, confidence)
recovered_content (id, redaction_id, text, method, confidence)
entities (id, content_id, canonical_id, text, type, confidence)
relationships (id, entity1_id, entity2_id, type, confidence, evidence)
```

### Neo4j
```cypher
(Entity {id, canonical_name, type, corpus, confidence})
-[RELATIONSHIP {type, weight, confidence, evidence}]->
(Entity)
```

---

## Ethical Use & Legal Notice

⚠️ **PRIVATE RESEARCH TOOL - NOT FOR PUBLIC DISTRIBUTION**

This tool is designed for legitimate research purposes only:
- ✅ Crisis capitalism research
- ✅ Academic analysis
- ✅ Public interest journalism
- ❌ Victim harm
- ❌ Privacy violations
- ❌ Malicious use

**Victim Protection:** Epstein corpus processing includes mandatory victim protection protocols.

**Legal Consultation Required:** Any enterprise or government deployment requires legal review.

---

## Contributing

This is a private research tool. Contributions limited to project collaborators.

---

## License

Private Research Tool - All Rights Reserved

---

## Contact

**Author:** David Kirsch  
**Organization:** Fine Print Press LLC  
**Project:** Crisis Capitalism Research  

---

## Acknowledgments

Built using:
- PyPDF2, pdf2image, pdfminer.six
- Tesseract OCR, OpenCV, Pillow
- spaCy, NLTK
- PostgreSQL, Neo4j
- Click, PyYAML, requests

---

## Version History

**1.0.0** (2025-02-03)
- Complete foundation phase
- Full extraction pipeline
- Entity recognition and network analysis
- Database integration
- Multi-project support
- Crisis Capitalism, Epstein, HIRM configurations

---

**Documentation:** See `docs/` directory for detailed specifications  
**Support:** Internal project only
