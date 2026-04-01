# DEDACT Quick Start Guide

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_lg

# Install DEDACT
pip install -e .
```

## Basic Usage

### Process Single Document

```bash
dedact process document.pdf --output results/
```

### Process Directory

```bash
dedact process /path/to/pdfs/ --output results/ --parallel 8
```

### Using Configuration

```bash
# Crisis Capitalism research
dedact process docs/ --config config/crisis_capitalism.yaml

# Epstein corpus (victim protection enabled)
dedact process docs/ --config config/epstein_corpus.yaml

# HIRM medical research
dedact process docs/ --config config/hirm.yaml
```

## Python API

```python
from pathlib import Path
from dedact import (
    FileDiscoverer,
    VisualLayerAnalyzer,
    TextLayerAnalyzer,
    RedactionCorrelator,
    DirectTextRecoverer,
    OCRProcessor
)

# Discover PDFs
discoverer = FileDiscoverer()
files = list(discoverer.discover(Path('documents/')))

# Detect redactions
visual = VisualLayerAnalyzer()
text = TextLayerAnalyzer()
correlator = RedactionCorrelator()

visual_candidates = visual.analyze(files[0].path)
text_positions, text_gaps = text.analyze(files[0].path)
redactions = correlator.correlate(visual_candidates, text_positions, text_gaps)

# Extract content
recoverer = DirectTextRecoverer()
for redaction in redactions:
    if redaction.extractable:
        content = recoverer.extract(files[0].path, redaction)
        print(f"Recovered: {content.text}")
```

## Next Steps

- See MODULE_SPECIFICATIONS.md for detailed API
- See VULNERABILITY_TYPES.md for redaction types  
- See ETHICAL_GUIDELINES.md for usage policy
