# DEDACT

Document Extraction, De-Redaction, and Analysis Capability Tool.

Forensic PDF analysis pipeline that detects improperly redacted content, extracts recoverable text, identifies entities, and maps relationships across document corpuses.

## What it does

DEDACT targets four classes of redaction vulnerability:

| Type | Vulnerability | Method |
|------|--------------|--------|
| 1 | Visual overlays with readable text layers underneath | Direct text extraction |
| 2 | Image-based redactions recoverable via OCR | Tesseract with 4 preprocessing strategies |
| 3 | Metadata leakage (author, revision history, comments) | Metadata extraction |
| 4 | Partial text fragments around redaction boundaries | Fragment reconstruction |

## Pipeline

```
Ingestion → Detection → Extraction → Analysis → Storage → Integration
   ↓           ↓            ↓            ↓          ↓          ↓
Discovery   Visual      Direct Text   Entities   PostgreSQL   External DBs
Quality     Text Layer  OCR           Patterns   Neo4j        Entity Resolution
Dedup       Correlation Metadata      Relations  Exports      Wikidata
Format      Confidence  Fragments     Network    Reports      OpenCorporates
```

## Usage

```bash
# Process a single document
dedact process document.pdf --output results/

# Process a directory
dedact process /path/to/pdfs/ --output results/ --parallel 8

# High confidence only
dedact process docs/ --confidence 0.80

# Custom config
dedact process docs/ --config config/default.yaml
```

### Python API

```python
from dedact.ingestion import FileDiscoverer
from dedact.detection import VisualLayerAnalyzer, TextLayerAnalyzer, RedactionCorrelator
from dedact.extraction import DirectTextRecoverer, OCRProcessor

discoverer = FileDiscoverer()
files = list(discoverer.discover(Path('documents/')))

visual_analyzer = VisualLayerAnalyzer()
text_analyzer = TextLayerAnalyzer()
correlator = RedactionCorrelator()

visual_candidates = visual_analyzer.analyze(files[0].path)
text_positions, text_gaps = text_analyzer.analyze(files[0].path)
redactions = correlator.correlate(visual_candidates, text_positions, text_gaps)

recoverer = DirectTextRecoverer()
for redaction in redactions:
    if redaction.extractable:
        content = recoverer.extract(files[0].path, redaction)
```

## Requirements

- Python 3.10+
- Tesseract OCR 5.0+
- PostgreSQL 14+ (optional — for structured storage)
- Neo4j Community 5.0+ (optional — for graph analysis)

## Install

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_lg
pip install -e .
```

## Entity recognition

Built-in spaCy NER (PERSON, ORG, GPE, DATE, MONEY) plus custom pattern matching for EMAIL, PHONE, SSN, and other structured identifiers. Extracted entities are linked via relationship mapping and can be exported to Neo4j for graph analysis or validated against external databases (Wikidata, OpenCorporates, LittleSis).

## Storage

```sql
-- PostgreSQL schema
documents       (id, path, hash, format, corpus, processed)
redactions      (id, document_id, page, bbox, type, confidence)
recovered_content (id, redaction_id, text, method, confidence)
entities        (id, content_id, canonical_id, text, type, confidence)
relationships   (id, entity1_id, entity2_id, type, confidence, evidence)
```

## Built with

PyPDF2, pdf2image, pdfminer.six, Tesseract OCR, OpenCV, Pillow, spaCy, PostgreSQL, Neo4j

## License

MIT