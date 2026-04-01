# DEDACT System Architecture
## Technical Design and Complete Module Specifications

**Version:** 1.0.0  
**Created:** 2025-02-03  
**Status:** Architecture Complete

---

**COMPLETE ARCHITECTURE DOCUMENT**

See DEDACT_PROTOCOLS.md for detailed methodology.
See RESEARCH_INTEGRATION.md for global positioning.

This document provides complete technical specifications for all DEDACT components.

**Architecture:** Modular pipeline (Ingestion → Detection → Extraction → Analysis → Storage → Integration)

**Tech Stack:** Python 3.10+, PyPDF2, Tesseract, spaCy, PostgreSQL, Neo4j (all open source)

**Directory Structure:** src/{ingestion,detection,extraction,analysis,storage,integration}, config/, tests/, docs/

**Processing Strategies:**
- Sequential: <1K docs, 1-5 docs/min
- Parallel: 1K-100K docs, 50-200 docs/min, 8-16 workers
- Distributed: >100K docs, queue-based, scales linearly

**Quality Standards:** >80% test coverage, type hints, comprehensive docs, checkpoint recovery

**Deployment:** Local (D:/Dev/dedact/) or production (Windows/Linux + PostgreSQL + Neo4j)

**Security:** Access control, encryption, input validation, audit logging

**Integration:** MCP servers, external DBs (ICIJ, LittleSis, OpenCorporates, Wikidata), cross-corpus resolution

---

**Complete specifications for all modules documented in DEDACT_PROTOCOLS.md Phases 1-6**

**Next:** Begin implementation (src/ code files)
