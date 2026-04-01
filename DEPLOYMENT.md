# DEDACT Deployment Guide
## Production Deployment Instructions

**Version:** 1.0.0  
**Status:** PRODUCTION READY  
**Date:** 2025-02-03

---

## PRE-DEPLOYMENT CHECKLIST

### System Requirements
- [ ] Python 3.10 or higher installed
- [ ] Tesseract OCR 5.0+ installed and in PATH
- [ ] Git installed (for cloning)
- [ ] 8GB+ RAM (16GB recommended for large corpuses)
- [ ] 50GB+ free disk space

### Optional Components
- [ ] PostgreSQL 14+ (for structured storage)
- [ ] Neo4j Community 5.0+ (for graph analysis)
- [ ] Virtual environment tool (venv/conda)

---

## INSTALLATION STEPS

### 1. Clone Repository

```bash
cd D:\Dev
# Repository already exists at D:\Dev\dedact
cd dedact
```

### 2. Create Virtual Environment (Recommended)

```bash
# Using venv
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install all requirements
pip install -r requirements.txt

# Download spaCy language model
python -m spacy download en_core_web_lg

# Install DEDACT package
pip install -e .
```

### 4. Verify Tesseract Installation

```bash
# Check Tesseract is in PATH
tesseract --version

# Should output: tesseract 5.x.x
```

**If not installed:**
- Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
- Linux: `sudo apt-get install tesseract-ocr`
- Mac: `brew install tesseract`

### 5. Test Installation

```bash
# Run CLI help
dedact --version
dedact --help

# Should output: DEDACT v1.0.0
```

---

## CONFIGURATION

### Project Configurations Available

**Crisis Capitalism** (`config/crisis_capitalism.yaml`)
- Congressional trading, defense contracts
- 8 parallel workers
- Confidence threshold: 0.60
- MCP integration: ENABLED

**Epstein Corpus** (`config/epstein_corpus.yaml`)
- Victim protection protocols
- 4 parallel workers (quality over speed)
- Confidence threshold: 0.70
- Manual review: REQUIRED
- MCP integration: DISABLED

**HIRM Medical** (`config/hirm.yaml`)
- Clinical trials, researcher conflicts
- 6 parallel workers
- Confidence threshold: 0.65
- MCP integration: ENABLED

### Customize Configuration

Create custom config file:

```yaml
# config/my_project.yaml
corpus_id: "my_project"
corpus_path: "/path/to/documents/"

processing:
  confidence_threshold: 0.60
  ocr_enabled: true
  parallel_workers: 4
  extraction_depth: "comprehensive"

entity_types:
  - PERSON
  - ORG
  - MONEY
  - DATE

output:
  formats:
    - json
    - csv
  directory: "output/my_project"
```

---

## BASIC USAGE

### Process Single Document

```bash
dedact process document.pdf --output results/
```

### Process Directory

```bash
dedact process /path/to/pdfs/ --output results/
```

### With Configuration

```bash
# Crisis Capitalism
dedact process "D:\Research\FINE PRINT\crisis capitalism\sample\" \
  --config config/crisis_capitalism.yaml

# Epstein Corpus (victim protection)
dedact process "D:\Research\FINE PRINT\epstein_documents\" \
  --config config/epstein_corpus.yaml

# HIRM
dedact process "D:\Research\HIRM\documents\" \
  --config config/hirm.yaml
```

### Advanced Options

```bash
# High confidence only
dedact process docs/ --confidence 0.80

# More parallel workers
dedact process docs/ --parallel 16

# Verbose logging
dedact process docs/ --verbose
```

---

## DATABASE SETUP (OPTIONAL)

### PostgreSQL Setup

```bash
# Install PostgreSQL 14+
# Create database
createdb dedact

# Create schema (automatic on first run)
# Or manually:
psql dedact < schema/postgresql_schema.sql
```

**Connection String:**
```python
postgresql://username:password@localhost:5432/dedact
```

### Neo4j Setup

```bash
# Install Neo4j Community Edition
# Start Neo4j
neo4j start

# Default connection:
# URI: bolt://localhost:7687
# User: neo4j
# Password: (set on first login)
```

---

## TESTING

### Run Test Suite

```bash
# All tests
pytest

# With coverage
pytest --cov=src tests/

# Specific module
pytest tests/test_ingestion.py
```

### Process Test Document

```bash
# Create test directory
mkdir -p data/sample_pdfs

# Place test PDF in data/sample_pdfs/

# Run example
python examples/basic_workflow.py
```

---

## PRODUCTION DEPLOYMENT

### For Crisis Capitalism Research

```bash
# 1. Configure paths
CORPUS_PATH="D:\Research\FINE PRINT\crisis capitalism"
OUTPUT_PATH="D:\Research\FINE PRINT\dedact_output"

# 2. Initial test run (10 documents)
dedact process "$CORPUS_PATH\sample\" \
  --config config/crisis_capitalism.yaml \
  --output "$OUTPUT_PATH\test_run\"

# 3. Validate results
# Check output/test_run/ for quality

# 4. Full corpus processing
dedact process "$CORPUS_PATH" \
  --config config/crisis_capitalism.yaml \
  --output "$OUTPUT_PATH\full_run\" \
  --parallel 8
```

### For Epstein Corpus (HIGH PRIORITY)

```bash
# CRITICAL: Victim protection protocols active

# 1. Phase 1 only (datasets 5-7)
EPSTEIN_PATH="D:\Research\FINE PRINT\epstein_documents\yung_megafone"

# 2. Process with protection
dedact process "$EPSTEIN_PATH\dataset_5" \
  --config config/epstein_corpus.yaml \
  --output "output/epstein/phase1" \
  --parallel 4

# 3. MANDATORY manual review before any use
# Review output/epstein/phase1/recovered_content.json

# 4. Never publish victim information
# Pseudonymization required for any analysis
```

### For HIRM Research

```bash
# Medical research corpus
HIRM_PATH="D:\Research\HIRM\documents"

dedact process "$HIRM_PATH" \
  --config config/hirm.yaml \
  --output "output/hirm" \
  --parallel 6
```

---

## MCP INTEGRATION

### Generate MCP Indices

```python
from pathlib import Path
from src.integration import MCPIntegrator

# Initialize
integrator = MCPIntegrator(Path('D:/Research/FINE PRINT/crisis capitalism'))

# Generate entity index
integrator.generate_entity_index(entities, 'entity_index.json')

# Generate cross-reference index
integrator.generate_cross_reference_index(recovered, 'cross_ref_index.json')

# Update corpus metadata
integrator.update_corpus_metadata(stats)
```

### Enable in MCP Server

Add to MCP server configuration:
```json
{
  "dedact_indices": [
    "entity_index.json",
    "cross_reference_index.json"
  ],
  "enhanced_queries": true
}
```

---

## MONITORING & LOGS

### Log Files

Logs are stored in `logs/` directory:

```
logs/
  dedact_20250203.log  # Daily log file
  errors/              # Error-specific logs
  checkpoints/         # Processing checkpoints
```

### Check Processing Status

```bash
# View recent logs
tail -f logs/dedact_*.log

# Check for errors
grep ERROR logs/dedact_*.log

# Processing statistics
dedact status
```

### Checkpoints

Resume interrupted processing:

```bash
# List checkpoints
ls checkpoints/

# Resume from checkpoint
dedact process docs/ --resume checkpoint_id
```

---

## PERFORMANCE OPTIMIZATION

### Memory Optimization
- Use `--parallel` based on available RAM
- 8GB RAM: 2-4 workers
- 16GB RAM: 4-8 workers
- 32GB RAM: 8-16 workers

### Speed Optimization
```bash
# Maximum speed (lower quality)
dedact process docs/ --confidence 0.50 --parallel 16

# Balanced (recommended)
dedact process docs/ --confidence 0.60 --parallel 8

# Maximum quality (slower)
dedact process docs/ --confidence 0.80 --parallel 4
```

### Disk Space
- Estimate: 10-20% of original corpus size for outputs
- OCR images cached: ~50MB per 100 pages
- Database: ~5-10% of corpus size

---

## TROUBLESHOOTING

### Common Issues

**Tesseract not found:**
```bash
# Add to PATH (Windows)
setx PATH "%PATH%;C:\Program Files\Tesseract-OCR"

# Verify
tesseract --version
```

**spaCy model missing:**
```bash
python -m spacy download en_core_web_lg
```

**Memory errors:**
```bash
# Reduce parallel workers
dedact process docs/ --parallel 2

# Process in batches
dedact process docs/batch1/ --output results/batch1/
dedact process docs/batch2/ --output results/batch2/
```

**Import errors:**
```bash
# Reinstall in editable mode
pip install -e .
```

---

## BACKUP & RECOVERY

### Checkpoint System

Automatic checkpoints every 3-5 operations:

```python
from src.utils import CheckpointManager

# Save checkpoint
manager = CheckpointManager()
manager.save_checkpoint('corpus_processing', state)

# Load checkpoint
state = manager.load_checkpoint('corpus_processing')

# Resume processing
# (automatic with --resume flag)
```

### Export Backup

```bash
# Export all results
dedact export output/ --format json
dedact export output/ --format csv

# Backup to external drive
cp -r output/ /backup/dedact_$(date +%Y%m%d)/
```

---

## SECURITY CONSIDERATIONS

### Sensitive Data

**Epstein Corpus:**
- ✅ Victim protection MANDATORY
- ✅ Manual review REQUIRED
- ✅ Pseudonymization before any analysis
- ✅ No external database validation
- ✅ No MCP integration (too sensitive)
- ❌ Never publish victim information

**All Projects:**
- Store outputs on encrypted drives
- Limit access to authorized researchers
- Follow IRB guidelines if applicable
- Legal consultation for sensitive discoveries

### Credentials

Never commit:
- Database passwords
- API keys
- Configuration with sensitive paths

Use environment variables:
```bash
export DEDACT_DB_PASSWORD="your_password"
export DEDACT_NEO4J_PASSWORD="your_password"
```

---

## MAINTENANCE

### Regular Tasks

**Weekly:**
- Review error logs
- Check disk space
- Backup checkpoints

**Monthly:**
- Update dependencies: `pip install -U -r requirements.txt`
- Rebuild spaCy models if updated
- Archive old logs

**Quarterly:**
- Performance review
- Configuration optimization
- Test suite expansion

---

## SUPPORT

### Internal Documentation
- `README.md` - Overview
- `docs/QUICK_START.md` - Basic usage
- `docs/VULNERABILITY_TYPES.md` - Redaction types
- `SESSION_SUMMARY.md` - Development details

### Code Reference
- `SYSTEM_ARCHITECTURE.md` - Technical specs
- `DEDACT_PROTOCOLS.md` - Methodology
- Module docstrings - API documentation

### Research Integration
- Crisis Capitalism protocols v3.0.2
- Research Veritas v1.0
- Fine Print Project standards

---

## VERSION HISTORY

**1.0.0** (2025-02-03)
- Initial production release
- Complete 6-module pipeline
- Crisis Capitalism, Epstein, HIRM configs
- PostgreSQL + Neo4j integration
- MCP server integration
- Comprehensive testing framework

---

**Last Updated:** 2025-02-03  
**Status:** PRODUCTION READY  
**Deployment Tested:** ✅  
**Documentation:** Complete
