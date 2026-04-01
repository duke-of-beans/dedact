# DEDACT Protocols v1.0
## Complete Methodology for Document De-Redaction and Forensic Analysis

**Status:** Foundation Document  
**Version:** 1.0.0  
**Created:** 2025-02-03  
**Compliance:** Research Veritas v1.0, Crisis Capitalism Research Protocols v3.0.2

---

## Executive Summary

DEDACT implements a comprehensive framework for recovering improperly redacted content from document corpuses. Improper redaction occurs when visual overlays (black rectangles, annotations) are applied without permanently removing underlying text, metadata, or image data. This creates exploitable vulnerabilities where original content remains extractable through technical forensic methods.

This protocol defines systematic procedures for detection, extraction, verification, and documentation of recovered content while maintaining research-grade rigor and ethical safeguards.

---

## Core Principles

### 1. **Verification Before Conclusion**
- Every recovered element requires confidence scoring
- Multiple extraction methods cross-validate findings
- False positives documented and filtered
- Chain of custody maintained throughout

### 2. **Ethical Operation**
- Victim protection paramount
- Responsible disclosure framework
- Manual review for sensitive content
- No automated publication of recovered data

### 3. **Research Rigor**
- Reproducible methodology
- Source verification protocols
- Bias mitigation frameworks
- Falsification criteria stated explicitly

### 4. **Technical Excellence**
- Graceful degradation when extraction fails
- Comprehensive error logging
- Performance optimization
- Modular, testable components

---

## Redaction Vulnerability Types

### Type 1: Visual Overlay Redaction
**Mechanism:** Black rectangle drawn over text as annotation layer

**Vulnerability:**
- Original text remains in PDF text stream
- Copy/paste reveals content
- Text search still functional
- Screen readers can access text

**Detection:**
- Compare visual rendering to text layer
- Search for annotation objects in PDF structure
- Test copy/paste functionality
- OCR comparison (visual vs. extractable text)

**Extraction:**
- Direct text stream parsing
- PDF object inspection
- Layer separation and analysis

**Confidence Factors:**
- Text stream matches visual gap location: HIGH
- Annotation object present at position: HIGH
- Font/style consistent with surrounding text: MEDIUM
- Context suggests redacted content type: LOW

### Type 2: Image-Based Redaction Artifacts
**Mechanism:** Document scanned after manual redaction, but compression artifacts reveal edges

**Vulnerability:**
- JPEG compression creates visible text remnants
- Black box edges don't perfectly align with pixels
- Color bleeding reveals character shapes
- OCR can detect partial letterforms

**Detection:**
- Edge detection algorithms on black regions
- Compression artifact analysis
- Contrast enhancement reveals remnants
- OCR with preprocessing

**Extraction:**
- Image enhancement techniques
- OCR with character recognition thresholds lowered
- Machine learning pattern matching
- Contextual reconstruction

**Confidence Factors:**
- Clear letterforms visible after enhancement: MEDIUM
- OCR produces readable text: MEDIUM
- Context suggests specific content: LOW
- Multiple independent OCR engines agree: HIGH

### Type 3: Metadata Leakage
**Mechanism:** Redacted content preserved in document metadata or properties

**Vulnerability:**
- Author/creator fields contain names
- Revision history shows deleted content
- Custom properties store original data
- Comments and annotations not removed

**Detection:**
- Comprehensive metadata extraction (ExifTool)
- PDF internal object inspection
- Revision tracking analysis
- Hidden layer enumeration

**Extraction:**
- Metadata parsing
- Comment extraction
- Revision history reconstruction
- Hidden object recovery

**Confidence Factors:**
- Metadata field explicitly labeled: HIGH
- Content matches document context: MEDIUM
- Timestamp suggests original authorship: LOW
- Multiple metadata fields corroborate: HIGH

### Type 4: Incomplete Selection Redaction
**Mechanism:** Redactor selected text imprecisely, leaving fragments

**Vulnerability:**
- Partial words/sentences remain
- Line breaks create gaps in selection
- Multi-column layouts cause skipped regions
- Whitespace handling errors

**Detection:**
- Fragment pattern analysis
- Linguistic reconstruction
- Context-based completion
- Statistical language models

**Extraction:**
- Fragment collection and ordering
- NLP-based reconstruction
- Multiple completion candidates
- Probability scoring

**Confidence Factors:**
- Complete words found: HIGH
- Fragments form coherent sentence: MEDIUM
- Language model confidence >80%: MEDIUM
- Multiple valid reconstructions: LOW (report all)

### Type 5: Software Tool Failures
**Mechanism:** Redaction tool has bugs or is misused, leaving content

**Vulnerability:**
- Tool only removes visible layer, not text
- Multi-page documents partially processed
- Batch operations skip files
- Version incompatibilities

**Detection:**
- Software signature analysis
- Consistency checks across documents
- Pattern matching for tool-specific errors
- Cross-document comparison

**Extraction:**
- Standard text extraction
- Error pattern exploitation
- Consistency analysis

**Confidence Factors:**
- Same tool error across multiple docs: HIGH
- Software version known to have bug: HIGH
- Pattern consistent with documented failure: MEDIUM

---

## Processing Workflow

### Phase 1: Ingestion and Assessment

**Step 1.1: File Discovery**
```
Input: Directory path or file list
Process:
  - Recursive directory traversal
  - Format identification (PDF, DOCX, images)
  - Deduplication (SHA256 hashing)
  - Size and accessibility checks
Output: Validated file inventory with metadata
```

**Step 1.2: Quality Assessment**
```
For each file:
  - Check if encrypted/password-protected
  - Verify not corrupted
  - Assess OCR-ability (if image-based)
  - Check for text layer presence
  - Estimate processing time
Output: Quality score, processing strategy recommendation
```

**Step 1.3: Categorization**
```
Classify into:
  - Text-layer PDFs (direct extraction)
  - Image-only PDFs (OCR required)
  - Mixed PDFs (hybrid approach)
  - DOCX files (XML parsing)
  - Scanned images (full OCR pipeline)
Output: Processing queue with strategy assignments
```

### Phase 2: Redaction Detection

**Step 2.1: Visual Layer Analysis**
```
Process:
  - Render each page to image
  - Detect black/white rectangles
  - Measure dimensions and positions
  - Classify as potential redactions vs. design elements
Output: Redaction candidate locations per page
```

**Step 2.2: Text Layer Analysis**
```
Process:
  - Extract complete text stream
  - Map text positions to visual coordinates
  - Identify gaps in text flow
  - Compare text density to visual rendering
Output: Text gap locations and content
```

**Step 2.3: Comparison and Correlation**
```
Process:
  - Overlay text map onto visual redaction map
  - Identify mismatches (text present, visual blocked)
  - Score confidence based on alignment
  - Flag anomalies for manual review
Output: Confirmed redaction vulnerabilities with confidence scores
```

### Phase 3: Content Extraction

**Step 3.1: Direct Text Recovery**
```
For Type 1 vulnerabilities:
  - Extract text from regions matching visual redactions
  - Preserve formatting and positioning
  - Validate against surrounding context
  - Score confidence
Output: Recovered text with position and confidence
```

**Step 3.2: OCR Processing**
```
For Type 2 vulnerabilities:
  - Apply image enhancement (contrast, edge detection)
  - Run Tesseract OCR with optimized settings
  - If confidence low, try alternative preprocessing
  - Cross-validate with multiple OCR engines if available
Output: OCR results with character-level confidence
```

**Step 3.3: Metadata Extraction**
```
For Type 3 vulnerabilities:
  - Run ExifTool comprehensive extraction
  - Parse PDF internal objects
  - Extract comments, annotations, revisions
  - Correlate with document content
Output: Metadata inventory with relevance scoring
```

**Step 3.4: Fragment Reconstruction**
```
For Type 4 vulnerabilities:
  - Collect partial words/sentences
  - Apply linguistic models for completion
  - Generate multiple candidates
  - Score by probability and context fit
Output: Reconstruction candidates ranked by confidence
```

### Phase 4: Entity Extraction and Analysis

**Step 4.1: Named Entity Recognition**
```
Process recovered text through spaCy:
  - Extract persons (PERSON)
  - Extract organizations (ORG)
  - Extract locations (GPE, LOC)
  - Extract dates (DATE)
  - Extract monetary values (MONEY)
Output: Entity inventory with types and positions
```

**Step 4.2: Pattern Matching**
```
Apply regex for structured data:
  - Phone numbers
  - Email addresses
  - Social Security Numbers
  - Addresses
  - URLs
  - Account numbers
Output: Structured data extractions with validation
```

**Step 4.3: Relationship Mapping**
```
Process:
  - Co-occurrence analysis (entities in same document/section)
  - Temporal relationships (dates with entities)
  - Hierarchical relationships (org charts, ownership)
  - Geographic clustering
Output: Relationship triples (Entity1, Relation, Entity2)
```

### Phase 5: Network Graph Construction

**Step 5.1: Node Creation**
```
For each unique entity:
  - Create node with properties (type, name, aliases)
  - Aggregate mentions across documents
  - Calculate centrality (mention frequency)
  - Assign confidence score
Output: Node database
```

**Step 5.2: Edge Creation**
```
For each relationship:
  - Create edge with properties (type, strength, documents)
  - Weight by co-occurrence frequency
  - Temporal ordering if dates available
  - Source attribution (which documents)
Output: Edge database
```

**Step 5.3: Graph Storage**
```
Load into Neo4j:
  - Nodes with labels and properties
  - Relationships with types and weights
  - Document links for provenance
  - Confidence scores throughout
Output: Queryable graph database
```

### Phase 6: Database Integration and Export

**Step 6.1: Cross-Corpus Verification**
```
Query existing databases:
  - ICIJ Offshore Leaks (entity matches)
  - LittleSis (corporate connections)
  - OpenCorporates (company verification)
  - Wikidata (entity disambiguation)
Process: Match, verify, enrich
Output: Verified and enriched entities
```

**Step 6.2: PostgreSQL Loading**
```
Structure:
  - documents table (metadata, paths, hashes)
  - redactions table (locations, types, confidence)
  - recovered_content table (text, entities, confidence)
  - entities table (normalized, deduplicated)
  - relationships table (connections, weights)
Output: Fully indexed relational database
```

**Step 6.3: Export Generation**
```
Formats:
  - JSON (complete data, programmatic access)
  - CSV (spreadsheet compatible, entity lists)
  - HTML (human-readable reports with highlights)
  - Markdown (documentation and summaries)
  - Neo4j Cypher (graph queries)
Output: Multi-format deliverables
```

---

## Confidence Scoring Framework

### Overall Confidence Calculation

```
Final_Confidence = (Method_Confidence × Source_Quality × Context_Validation)^(1/3)

Where:
  Method_Confidence = Extraction technique reliability (0.0-1.0)
  Source_Quality = Document quality and clarity (0.0-1.0)
  Context_Validation = Surrounding content supports finding (0.0-1.0)
```

### Confidence Levels

**HIGH (0.80-1.00):**
- Direct text extraction with perfect alignment
- Multiple extraction methods agree
- Context strongly supports content
- No alternative explanations
- **Action:** Include in primary analysis

**MEDIUM (0.50-0.79):**
- Single reliable extraction method
- Context somewhat supports content
- Minor inconsistencies present
- Plausible alternative exists
- **Action:** Include with caveats, manual review recommended

**LOW (0.25-0.49):**
- Speculative reconstruction
- Weak context support
- Multiple alternatives equally likely
- Significant uncertainty
- **Action:** Flag as "possible," exclude from statistical analysis

**VERY LOW (<0.25):**
- Highly uncertain
- Reconstruction based on fragments
- No context validation
- More likely false positive
- **Action:** Document but exclude from analysis

### Reporting Standards

**All Recovered Content Must Include:**
1. Source document identification (path, hash, page)
2. Extraction method used
3. Confidence score with breakdown
4. Context (surrounding unredacted text)
5. Alternative interpretations if any
6. Manual review status

**Statistical Analysis:**
- Only HIGH confidence content in quantitative analysis
- MEDIUM confidence reported separately with qualifications
- LOW and VERY LOW excluded from conclusions
- Total counts include all confidence levels with breakdown

---

## Quality Control

### Automated Validation

**Step 1: Internal Consistency**
```
Checks:
  - Extracted text uses same font as document
  - Character spacing matches surrounding text
  - Language model assigns reasonable probability
  - No impossible character combinations
```

**Step 2: Cross-Document Validation**
```
Checks:
  - Same entity mentioned consistently across documents
  - Relationships align with other mentions
  - Temporal ordering makes sense
  - Geographic consistency
```

**Step 3: External Verification**
```
Checks:
  - Entity exists in external databases
  - Relationships confirmed elsewhere
  - Dates align with known events
  - Details match public records
```

### Manual Review Requirements

**Trigger Manual Review When:**
- Confidence score < 0.60
- Content involves potential victim identification
- Contradicts previously verified information
- Appears deliberately misleading
- Has significant legal implications

**Review Process:**
1. Present extracted content with full context
2. Show all extraction methods and results
3. Display confidence score breakdown
4. Provide alternative interpretations
5. Require reviewer decision: Accept / Reject / Modify
6. Document review decision and reasoning

---

## Ethical Safeguards

### Victim Protection Protocol

**Before Processing:**
- Identify document types likely to contain victim information
- Configure filters for PII (Social Security, addresses, etc.)
- Establish manual review workflow for sensitive content

**During Processing:**
- Flag potential victim names (cross-reference with case materials)
- Redact victim information in outputs (create new redactions)
- Watermark all extracted content with "Contains Sensitive Material"

**After Processing:**
- Human review of all victim-related content
- Removal or pseudonymization decisions
- Secure storage with access controls

### Responsible Disclosure

**Non-Public Processing:**
- All recovered content treated as confidential
- No automated publication or distribution
- Access limited to authorized researchers

**Publication Decisions:**
- Legal review required before any public disclosure
- Victim consultation if identifiable
- Public interest vs. privacy harm assessment
- Phased disclosure with warnings

**Coordination:**
- Law enforcement notification if crimes discovered
- Media coordination for responsible reporting
- Academic peer review before publication

---

## Integration with Research Protocols

### Research Veritas v1.0 Compliance

**Investigative Courage:**
- Map all suspicious patterns in recovered content
- Document connections worth investigating
- Mark as "Investigative Leads" when unverified

**Academic Verification:**
- Require T1/T2 sources for conclusions
- State falsification criteria
- Consider alternative explanations
- Report confidence intervals

**Bias Mitigation:**
- Check all 14 critical biases before finalizing
- Seek disconfirming evidence actively
- Document when patterns don't appear
- Test multiple hypotheses

### Crisis Capitalism Research Protocols v3.0.2 Compliance

**Research Phase Standards:**
- "Worth investigating" threshold for pattern mapping
- Preserve all findings as Investigative Leads
- Priority classification (High/Medium/Low/Structural)

**Reporting Phase Standards:**
- Academic verification before claiming extraction
- T1/T2 sources required (original documents)
- Statistical significance testing where applicable
- Integration to existing mechanisms (2-3 minimum)

**Investigative Leads Documentation:**
```yaml
lead_id: "LEAD-DEDACT-001"
status: "HIGH_PRIORITY"
pattern: "Description of recovered content pattern"
evidence:
  - document: "path/to/file.pdf"
    page: 5
    confidence: 0.85
    method: "direct_text_extraction"
temporal_precision: "Exact dates if available"
alternatives:
  - "Could be misalignment of text layer"
  - "Possible OCR error"
verification_pathways:
  - "Cross-reference with Dataset 6 same EFTA range"
  - "Check metadata for original author"
```

---

## Error Handling and Logging

### Error Classification

**Critical Errors (Stop Processing):**
- File corruption beyond recovery
- Encryption without available password
- System resource exhaustion
- Database connection failures

**Major Errors (Skip Item, Continue):**
- Individual file processing failure
- OCR complete failure
- Extraction method exception
- Invalid output format

**Minor Errors (Log and Continue):**
- Low confidence extractions
- Partial entity recognition
- Network graph ambiguities
- Export format warnings

### Logging Framework

**Log Levels:**
```
DEBUG: Method entry/exit, detailed state
INFO: Processing milestones, statistics
WARNING: Recoverable issues, low confidence
ERROR: Processing failures, data loss
CRITICAL: System failures, data corruption
```

**Log Content:**
```
[Timestamp] [Level] [Module] [Document] [Message]

2025-02-03 14:23:15 INFO RedactionDetector EFTA00008409.pdf Page 5: Found 3 redaction candidates
2025-02-03 14:23:16 WARNING TextExtractor EFTA00008409.pdf Page 5: Low confidence (0.42) on extraction
2025-02-03 14:23:18 ERROR OCRProcessor EFTA00008410.pdf: Tesseract failed, trying fallback
```

**Audit Trail:**
- Every extraction logged with parameters
- Confidence score calculations recorded
- Manual review decisions documented
- Database modifications tracked

---

## Performance Optimization

### Processing Strategies

**Sequential (Default):**
- One document at a time
- Full logging and validation
- Checkpoint after each document
- Suitable for <1000 documents

**Parallel (Scale):**
- Multiple documents simultaneously
- Worker pool configuration
- Checkpoint batches
- Suitable for >1000 documents

**Distributed (Large Corpuses):**
- Multiple machines
- Queue-based work distribution
- Centralized database
- Suitable for >100K documents

### Resource Management

**Memory:**
- Stream large files, don't load entirely
- Clear caches periodically
- Monitor memory usage
- Abort if threshold exceeded

**CPU:**
- Configurable worker threads
- Priority queuing
- Adaptive batch sizing
- Thermal throttling awareness

**Disk:**
- Temporary file cleanup
- Incremental output writing
- Space checks before processing
- Compression for intermediate results

---

## Version Control and Reproducibility

### Processing Versioning

**Every Processing Run Logged:**
```yaml
run_id: "RUN-20250203-142315"
dedact_version: "1.0.0"
configuration:
  confidence_threshold: 0.50
  ocr_enabled: true
  entity_extraction: true
corpus:
  source: "Epstein Dataset 5"
  file_count: 120
  total_size: "61.6 MB"
timestamp:
  started: "2025-02-03T14:23:15Z"
  completed: "2025-02-03T15:47:22Z"
  duration: "1h 24m 7s"
results:
  documents_processed: 120
  redactions_detected: 347
  high_confidence: 231
  medium_confidence: 89
  low_confidence: 27
  entities_extracted: 1547
```

### Reproducibility Requirements

**For Every Result:**
- Exact DEDACT version used
- Configuration file preserved
- Source file hashes recorded
- Processing timestamp
- Random seeds (if any)
- External dependencies versions

**Replication Process:**
```
1. Obtain identical source files (hash verification)
2. Install exact DEDACT version
3. Apply identical configuration
4. Run with same parameters
5. Compare results (should match exactly)
```

---

## Next Protocol Documents

1. **SYSTEM_ARCHITECTURE.md** - Technical design and module specifications
2. **API_REFERENCE.md** - Programmatic interface documentation
3. **USER_GUIDE.md** - End-to-end usage examples
4. **SECURITY_CONSIDERATIONS.md** - Threat model and mitigations
5. **TROUBLESHOOTING.md** - Common issues and solutions

---

**Status:** Foundation Complete  
**Next Action:** Build SYSTEM_ARCHITECTURE.md
