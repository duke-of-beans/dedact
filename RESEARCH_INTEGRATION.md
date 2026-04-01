# DEDACT Research Integration Framework
## Global Positioning and Cross-Project Architecture

**Version:** 1.0.0  
**Created:** 2025-02-03  
**Purpose:** Define how DEDACT integrates with existing research infrastructure and projects

---

## Executive Summary

DEDACT is not a standalone tool - it's a universal capability layer that enhances every research project involving document analysis. This framework defines integration patterns, data flows, and architectural decisions for embedding DEDACT across the research ecosystem.

**Core Principle:** Build intelligence, not plumbing. DEDACT should enhance existing workflows without requiring researchers to learn new systems.

---

## Global Research Architecture

### Tier 1: Universal Infrastructure (DEDACT Layer)

```
┌─────────────────────────────────────────────────────────────┐
│                    DEDACT Core Engine                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Ingestion  │  │  Extraction  │  │   Analysis   │      │
│  │   & Quality  │→ │  & Recovery  │→ │  & Network   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                               │
│  Output: JSON, Neo4j, PostgreSQL, CSV, Markdown              │
└─────────────────────────────────────────────────────────────┘
         ↓                    ↓                    ↓
    ┌────────┐          ┌──────────┐         ┌──────────┐
    │ Crisis │          │  Epstein │         │   HIRM   │
    │Capital │          │  Corpus  │         │ Research │
    └────────┘          └──────────┘         └──────────┘
```

### Tier 2: Project-Specific Integration

Each research project accesses DEDACT through:
1. **Configuration Files:** Project-specific YAML defining processing parameters
2. **Data Pipelines:** Automated workflows from raw docs to analysis-ready databases
3. **MCP Integration:** Zero-token corpus access with recovered content included
4. **Unified Databases:** Cross-corpus queries combining multiple projects

---

## Integration Patterns

### Pattern 1: Corpus Enhancement

**Use Case:** Existing document corpus needs redaction recovery

**Implementation:**
```yaml
project: crisis_capitalism
corpus_location: D:\Research\FINE PRINT\crisis capitalism\
enhancement:
  input_formats: [pdf, docx]
  processing:
    - redaction_detection
    - text_extraction
    - entity_recognition
    - network_mapping
  output_location: D:\Research\FINE PRINT\crisis capitalism\recovered\
  integration:
    - merge_with_existing_json
    - update_mcp_indices
    - enhance_network_graphs
```

**Workflow:**
1. DEDACT scans corpus for PDF/DOCX files
2. Processes each document through full pipeline
3. Outputs enhanced JSON with recovered content marked
4. MCP server indices updated to include new data
5. Researchers query normally, get enriched results automatically

**Benefits:**
- Zero workflow disruption
- Transparent enhancement
- Preserved provenance
- Reversible if needed

### Pattern 2: Real-Time Processing

**Use Case:** New documents arrive continuously (FOIA responses, leaks, releases)

**Implementation:**
```yaml
project: crisis_capitalism
watch_directory: D:\Research\FINE PRINT\incoming\
processing:
  trigger: file_system_watcher
  immediate: true
  pipeline:
    - quality_assessment
    - redaction_detection
    - extraction_priority_queue
    - entity_extraction
    - database_insert
  notification: true
```

**Workflow:**
1. New document arrives in watch directory
2. File system watcher triggers DEDACT processing
3. Document processed through full pipeline
4. Results inserted into project database
5. Researcher notified of completion
6. Document moved to processed archive

**Benefits:**
- Immediate availability
- No manual intervention
- Consistent processing
- Audit trail automatic

### Pattern 3: Cross-Corpus Analysis

**Use Case:** Research question spans multiple corpuses (Epstein + Panama Papers + Crisis Capitalism)

**Implementation:**
```yaml
analysis: cross_corpus_network
corpuses:
  - epstein: D:\Research\FINE PRINT\CORPUSES\Epstein\
  - panama_papers: D:\Research\FINE PRINT\CORPUSES\PanamaPapers\
  - crisis_capitalism: D:\Research\FINE PRINT\crisis capitalism\
processing:
  entity_normalization: true
  cross_corpus_matching:
    - fuzzy_name_matching
    - temporal_correlation
    - geographic_overlap
  output:
    - unified_neo4j_graph
    - relationship_matrix
    - temporal_timeline
```

**Workflow:**
1. DEDACT loads all three corpuses into unified graph
2. Entity normalization identifies same people/orgs across corpuses
3. Network analysis finds connections between corpuses
4. Timeline view shows when entities appear in which corpus
5. Researcher can query: "Show me everyone in Epstein corpus who also appears in Crisis Capitalism defense contractor networks"

**Benefits:**
- Discover hidden connections
- Validate findings across datasets
- Build comprehensive pictures
- Generate new research questions

---

## Project-Specific Integration Guides

### Crisis Capitalism Research

**Current State:**
- 130+ parts, 2,300 pages
- Crisis Capitalism Research Protocols v3.0.2
- MCP server integration for zero-token access
- Focus: Systematic extraction mechanisms

**DEDACT Enhancement:**

**Primary Applications:**
1. **Congressional Trading Disclosure Redactions**
   - SEC Edgar filings often have improper redactions
   - Recover executive names, dollar amounts, dates
   - Build trading networks automatically
   - Integrate with existing congressional tracking

2. **Defense Contract FOIA Responses**
   - Government heavily redacts contractor relationships
   - Extract company connections, personnel, dollar flows
   - Validate Big Three ownership patterns
   - Document enforcement collapse evidence

3. **Healthcare Merger FTC Filings**
   - Competitive sensitivity redactions
   - Recover market share data, pricing strategies
   - Build acquisition timelines
   - Connect to insurance extraction mechanisms

**Configuration:**
```yaml
project: crisis_capitalism
protocols: v3.0.2
integration:
  mcp_server: D:\Research\FINE PRINT\crisis capitalism\
  output_format: json_with_investigative_leads
  confidence_threshold: 0.60
  entity_types:
    - PERSON (executives, politicians)
    - ORG (companies, government agencies)
    - MONEY (dollar amounts, valuations)
    - DATE (transaction dates, filing dates)
  network_focus:
    - big_three_connections (Vanguard, BlackRock, State Street)
    - congressional_traders
    - revolving_door_personnel
  quality_standards:
    - t1_t2_source_verification
    - falsification_criteria_required
    - alternative_explanations (minimum 3)
    - bias_checks (all 14 critical)
```

**Output Structure:**
```json
{
  "document_id": "SEC_EDGAR_0001234567_20231215",
  "processing": {
    "dedact_version": "1.0.0",
    "timestamp": "2025-02-03T14:23:15Z",
    "confidence_threshold": 0.60
  },
  "redactions": [
    {
      "location": {"page": 5, "region": [120, 450, 380, 480]},
      "type": "visual_overlay",
      "recovered_content": {
        "text": "Vanguard Group increased position to 8.7% ($127M)",
        "confidence": 0.92,
        "method": "direct_text_extraction"
      },
      "entities": [
        {"type": "ORG", "text": "Vanguard Group", "verified": true},
        {"type": "PERCENT", "text": "8.7%"},
        {"type": "MONEY", "text": "$127M"}
      ],
      "investigative_lead": {
        "status": "HIGH_PRIORITY",
        "pattern": "Big Three ownership increase during congressional trading period",
        "verification_needed": "Cross-ref with congressional trade disclosures same timeframe"
      }
    }
  ]
}
```

### Epstein Corpus Research

**Current State:**
- 51,902 existing files (26.6 GB JSON)
- New DOJ releases: 12 datasets (~205 GB PDFs)
- Focus: Network mapping, timeline reconstruction

**DEDACT Enhancement:**

**Primary Applications:**
1. **Network Reconstruction**
   - Recover names from relationship documents
   - Build comprehensive person-to-person graph
   - Identify hidden connections
   - Temporal ordering of relationships

2. **Timeline Validation**
   - Extract dates from redacted calendars
   - Recover travel logs
   - Build verified chronology
   - Cross-reference with flight logs

3. **Financial Flow Mapping**
   - Recover dollar amounts from financial docs
   - Build transaction networks
   - Identify shell companies
   - Follow money flows

**Configuration:**
```yaml
project: epstein_corpus
source_documents: D:\Research\FINE PRINT\epstein_documents\yung_megafone\
datasets: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
integration:
  existing_json: D:\Research\FINE PRINT\CORPUSES\Epstein\
  output_format: neo4j_graph
  victim_protection: MAXIMUM
  
processing:
  entity_types:
    - PERSON (redact potential victims)
    - ORG (companies, foundations, entities)
    - GPE (locations, travel destinations)
    - DATE (meetings, travel, transactions)
    - MONEY (payments, transfers)
  
  network_analysis:
    - co_occurrence (same document = potential connection)
    - temporal_ordering (chronological relationships)
    - geographic_clustering (travel patterns)
    - financial_flows (transaction networks)
  
  victim_safeguards:
    - auto_flag_age_references (<18 = victim indicator)
    - manual_review_required: ALL person entities
    - pseudonymization: true
    - access_control: researcher_only
```

**Phased Processing:**
```yaml
phase_1:
  datasets: [5, 6, 7]  # Small, complete datasets
  purpose: methodology_validation
  timeline: immediate
  
phase_2:
  datasets: [1, 2, 3, 4]  # Medium datasets on DSL+
  purpose: corpus_expansion
  timeline: next_few_days
  
phase_3:
  datasets: [8, 9, 10, 11, 12]  # Large datasets
  purpose: comprehensive_processing
  timeline: after_1gb_internet_external_hd
  requirements:
    - external_hd_available
    - 1gb_internet_active
    - sustained_processing_capacity
```

### HIRM Research

**Current State:**
- Medical research methodology
- Empirical science focus
- Shares Research Veritas v1.0 principles

**DEDACT Enhancement:**

**Primary Applications:**
1. **Clinical Trial Document Analysis**
   - FDA submission redactions (competitive data)
   - Recover adverse event details
   - Extract trial protocol specifics
   - Build drug company networks

2. **Medical Research Paper Redactions**
   - Funding source concealment
   - Conflict of interest details
   - Methodology specifics
   - Raw data recovery

3. **FDA Approval Documents**
   - Redacted safety data
   - Manufacturer communications
   - Internal review concerns
   - Regulatory decision details

**Configuration:**
```yaml
project: hirm
protocols: research_veritas_v1.0
domain: medical_research
integration:
  corpus_location: D:\Research\HIRM\documents\
  output_format: research_database
  
processing:
  entity_types:
    - PERSON (researchers, executives)
    - ORG (pharmaceutical companies, hospitals, universities)
    - CHEMICAL (drug compounds, formulations)
    - DISEASE (conditions studied)
    - MONEY (funding amounts, payments)
  
  network_analysis:
    - funding_flows (who pays whom)
    - researcher_conflicts (industry ties)
    - institutional_relationships (academic-corporate)
    - regulatory_capture (revolving_door)
  
  quality_standards:
    - peer_review_compatible
    - reproducible_methodology
    - statistical_significance_testing
    - medical_ethics_compliance
```

---

## Unified Database Architecture

### Master Entity Resolution

**Challenge:** Same person/org appears in multiple corpuses with variations

**Solution:** Unified entity resolution layer

```
┌─────────────────────────────────────────────────────────┐
│             Master Entity Resolution Database            │
│                                                           │
│  Entity: "Vanguard Group Inc."                           │
│    Aliases: ["Vanguard", "Vanguard Group", "VGI"]       │
│    Appears in:                                           │
│      - Crisis Capitalism: 61 mechanisms                  │
│      - Epstein Corpus: 0 appearances (Big Three absence)│
│      - Panama Papers: [TBD]                              │
│    Relationships: [BlackRock, State Street, ...]         │
│    Confidence: 0.98                                      │
└─────────────────────────────────────────────────────────┘
```

**Implementation:**
```python
# Entity resolution workflow
def resolve_entity(name, corpus):
    # Check master database
    canonical = master_db.find_canonical(name)
    if canonical:
        return canonical
    
    # Fuzzy match existing entities
    matches = fuzzy_search(name, threshold=0.85)
    if matches:
        # Manual review if multiple high-confidence matches
        return human_disambiguate(name, matches)
    
    # Create new entity
    new_entity = create_entity(name, corpus)
    return new_entity
```

### Cross-Corpus Query Interface

**SQL Example:**
```sql
-- Find all entities appearing in both Epstein and Crisis Capitalism corpuses
SELECT 
    e.canonical_name,
    COUNT(DISTINCT cc.document_id) as cc_appearances,
    COUNT(DISTINCT ep.document_id) as ep_appearances,
    ARRAY_AGG(DISTINCT cc.context) as cc_contexts,
    ARRAY_AGG(DISTINCT ep.context) as ep_contexts
FROM entities e
JOIN corpus_appearances cc ON e.entity_id = cc.entity_id AND cc.corpus = 'crisis_capitalism'
JOIN corpus_appearances ep ON e.entity_id = ep.entity_id AND ep.corpus = 'epstein'
GROUP BY e.canonical_name
ORDER BY (cc_appearances + ep_appearances) DESC;
```

**Neo4j Cypher Example:**
```cypher
// Network path between Epstein corpus person and Crisis Capitalism mechanism
MATCH path = shortestPath(
  (epstein_person:Person {corpus: 'epstein'})-[*]-(cc_mechanism:Mechanism {corpus: 'crisis_capitalism'})
)
WHERE epstein_person.name = 'Specific Name'
RETURN path, length(path) as degrees_of_separation
ORDER BY degrees_of_separation
LIMIT 10;
```

---

## MCP Server Integration

### Zero-Token Corpus Access Enhancement

**Current MCP Architecture:**
```
D:\Research\FINE PRINT\crisis capitalism\
  ├── Part_001.md
  ├── Part_002.md
  └── ...
```

**Enhanced with DEDACT:**
```
D:\Research\FINE PRINT\crisis capitalism\
  ├── Part_001.md
  ├── Part_002.md
  ├── ...
  └── recovered\
      ├── SEC_EDGAR_filings\
      │   ├── recovered_content.json
      │   └── entity_networks.json
      ├── FOIA_responses\
      │   ├── recovered_content.json
      │   └── entity_networks.json
      └── indices\
          ├── master_entity_index.json
          ├── cross_reference_index.json
          └── confidence_scores.json
```

**MCP Query Enhancement:**
```python
# Standard MCP query (existing)
result = mcp.search_corpus("Vanguard ownership patterns")

# Enhanced MCP query (with DEDACT)
result = mcp.search_corpus(
    query="Vanguard ownership patterns",
    include_recovered=True,  # Include DEDACT findings
    min_confidence=0.60,     # Filter by confidence
    sources=["original", "recovered"]  # Query both
)

# Result includes:
# - Original corpus findings
# - Recovered content from redacted documents
# - Confidence scores for each finding
# - Provenance (which extraction method)
```

---

## Continuous Integration Workflow

### Automated Processing Pipeline

```yaml
pipeline: dedact_continuous_integration

triggers:
  - new_document_arrival
  - corpus_update
  - scheduled_reprocessing

stages:
  1_ingestion:
    - file_system_watch
    - quality_assessment
    - deduplication
    - priority_assignment
  
  2_processing:
    - redaction_detection
    - content_extraction
    - entity_recognition
    - confidence_scoring
  
  3_integration:
    - entity_resolution
    - database_insertion
    - network_graph_update
    - mcp_index_refresh
  
  4_notification:
    - researcher_alert
    - statistics_update
    - error_reporting
    - quality_metrics

checkpoints:
  - after_each_document
  - after_each_batch
  - daily_summary
  
recovery:
  - automatic_retry (max 3)
  - checkpoint_resume
  - error_isolation
  - manual_intervention_flag
```

---

## Performance and Scalability

### Processing Capacity Planning

**Small Scale (100-1,000 documents):**
- Single machine processing
- Sequential workflow
- Full logging enabled
- Interactive monitoring

**Medium Scale (1,000-100,000 documents):**
- Parallel processing (8-16 workers)
- Batch checkpointing
- Summary logging
- Background monitoring

**Large Scale (100,000+ documents):**
- Distributed processing
- Queue-based architecture
- Database sharding
- Automated scaling

### Resource Allocation

**Per Project:**
```yaml
crisis_capitalism:
  expected_volume: 10000_documents
  processing_strategy: parallel
  workers: 8
  checkpoint_interval: 100
  
epstein_corpus:
  expected_volume: 205GB_pdfs
  processing_strategy: distributed
  workers: 16
  checkpoint_interval: 500
  
hirm:
  expected_volume: 5000_documents
  processing_strategy: parallel
  workers: 4
  checkpoint_interval: 50
```

---

## Quality Assurance Across Projects

### Unified Quality Metrics

**Tracked Globally:**
- Processing success rate
- Confidence distribution
- Entity extraction accuracy
- Network graph completeness
- Cross-corpus match rate

**Per-Project Dashboard:**
```
Crisis Capitalism:
  Documents Processed: 8,547 / 10,000
  High Confidence: 6,234 (73%)
  Medium Confidence: 1,890 (22%)
  Low Confidence: 423 (5%)
  Entities Extracted: 47,821
  Network Edges: 123,456
  
Epstein Corpus:
  Documents Processed: 1,247 / 205,000 (Dataset 5 complete)
  High Confidence: 892 (71%)
  Medium Confidence: 287 (23%)
  Low Confidence: 68 (6%)
  Entities Extracted: 12,334
  Network Edges: 34,567
```

---

## Future Integration Opportunities

### Planned Expansions

**Panama Papers Integration:**
- Volume: 2.6 TB
- Focus: Offshore networks, shell companies
- DEDACT Value: Recover beneficial owner redactions

**Pandora Papers Integration:**
- Volume: 2.94 TB
- Focus: Tax haven structures
- DEDACT Value: Extract hidden ownership chains

**FinCEN Files Integration:**
- Volume: Leaked financial crime reports
- Focus: Suspicious activity reports
- DEDACT Value: Recover bank/client identities

### Cross-Domain Research

**Academic Publication Strategy:**
1. Methodology paper (DEDACT technical approach)
2. Application paper (Epstein corpus findings)
3. Comparative analysis (Cross-corpus discoveries)
4. Ethics framework (Responsible redaction recovery)

**Consulting Applications:**
1. Legal discovery support
2. Investigative journalism training
3. Corporate due diligence
4. Regulatory compliance auditing

---

## Governance and Access Control

### Research Tier Access

**Tier 1 (Unrestricted):**
- Public domain documents
- High confidence findings only
- Aggregate statistics
- Published research results

**Tier 2 (Researcher Access):**
- All processed documents
- Medium+ confidence findings
- Individual entity details
- Network graphs

**Tier 3 (Restricted):**
- Low confidence findings
- Victim-identifying information
- Unverified connections
- Raw extraction data

**Access Control:**
```yaml
researcher: david_kirsch
permissions:
  tier_1: true
  tier_2: true
  tier_3: true  # Full access for primary researcher
  
external_collaborator:
  tier_1: true
  tier_2: true  # Requires approval
  tier_3: false # Restricted
```

---

## Documentation Standards

### Project Integration Checklist

**Before Integrating DEDACT:**
- [ ] Define project-specific entity types
- [ ] Establish confidence thresholds
- [ ] Configure victim protection (if applicable)
- [ ] Set up MCP integration points
- [ ] Design database schema
- [ ] Create processing configuration
- [ ] Define quality metrics
- [ ] Establish checkpoint strategy

**During Integration:**
- [ ] Process sample documents
- [ ] Validate confidence scoring
- [ ] Test entity resolution
- [ ] Verify database integration
- [ ] Check MCP query enhancement
- [ ] Review manual review workflow
- [ ] Audit trail verification

**After Integration:**
- [ ] Document integration decisions
- [ ] Update project DNA/protocols
- [ ] Train additional researchers
- [ ] Establish monitoring dashboards
- [ ] Schedule periodic reprocessing
- [ ] Plan corpus expansion

---

**Status:** Research Integration Framework Complete  
**Next Action:** Build SYSTEM_ARCHITECTURE.md (technical specifications)
