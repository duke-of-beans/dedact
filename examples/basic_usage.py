"""
DEDACT Basic Usage Example
Process a single PDF and extract redacted content
"""

from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from dedact.ingestion import FileDiscoverer, FileValidator
from dedact.detection import (
    VisualLayerAnalyzer,
    TextLayerAnalyzer,
    RedactionCorrelator,
    ConfidenceScorer
)
from dedact.extraction import (
    DirectTextRecoverer,
    OCRProcessor,
    MetadataExtractor
)
from dedact.analysis import EntityRecognizer, PatternMatcher
from dedact.utils import setup_logging


def main():
    """Process a single PDF and extract redacted content"""
    
    # Setup logging
    logger = setup_logging(log_level='INFO')
    logger.info("DEDACT Example - Single PDF Processing")
    
    # Configuration
    pdf_path = Path('sample.pdf')  # Change to your PDF
    
    if not pdf_path.exists():
        logger.error(f"PDF not found: {pdf_path}")
        logger.info("Please place a PDF named 'sample.pdf' in the examples directory")
        return
    
    # Step 1: Validate file
    logger.info(f"Step 1: Validating {pdf_path.name}")
    validator = FileValidator()
    if not validator.validate(pdf_path):
        logger.error("File validation failed")
        return
    
    # Step 2: Detect redactions
    logger.info("Step 2: Detecting redactions")
    visual_analyzer = VisualLayerAnalyzer()
    text_analyzer = TextLayerAnalyzer()
    correlator = RedactionCorrelator()
    scorer = ConfidenceScorer()
    
    # Analyze first page
    visual_candidates = visual_analyzer.analyze(pdf_path, page=0)
    text_positions, text_gaps = text_analyzer.analyze(pdf_path, page=0)
    redactions = correlator.correlate(visual_candidates, text_positions, text_gaps)
    
    logger.info(f"Found {len(redactions)} potential redactions")
    
    # Step 3: Extract content
    logger.info("Step 3: Extracting content")
    recoverer = DirectTextRecoverer()
    ocr_processor = OCRProcessor()
    metadata_extractor = MetadataExtractor()
    
    recovered_contents = []
    
    for i, redaction in enumerate(redactions, 1):
        logger.info(f"Processing redaction {i}/{len(redactions)}")
        logger.info(f"  Type: {redaction.vulnerability_type.name}")
        logger.info(f"  Confidence: {redaction.confidence:.2f}")
        
        if redaction.extractable:
            # Try direct text recovery first (Type 1)
            try:
                content = recoverer.extract(pdf_path, redaction)
                recovered_contents.append(content)
                logger.info(f"  ✅ Recovered: {content.text[:100]}...")
            except Exception as e:
                logger.info(f"  Direct recovery failed: {e}")
                
                # Fallback to OCR (Type 2)
                try:
                    ocr_result = ocr_processor.process_region(
                        pdf_path,
                        page=redaction.page,
                        bbox=redaction.bbox
                    )
                    if ocr_result and ocr_result.confidence > 0.6:
                        logger.info(f"  ✅ OCR recovered: {ocr_result.text[:100]}...")
                except Exception as e:
                    logger.info(f"  OCR failed: {e}")
    
    # Step 4: Extract metadata (Type 3)
    logger.info("Step 4: Extracting metadata")
    metadata = metadata_extractor.extract(pdf_path, depth='comprehensive')
    if metadata.relevance_scores:
        logger.info(f"Found {len(metadata.relevance_scores)} relevant metadata items")
    
    # Step 5: Analyze recovered content
    logger.info("Step 5: Analyzing entities")
    recognizer = EntityRecognizer()
    matcher = PatternMatcher()
    
    all_entities = []
    all_patterns = []
    
    for content in recovered_contents:
        entities = recognizer.extract(content.text)
        patterns = matcher.match(content.text)
        all_entities.extend(entities)
        all_patterns.extend(patterns)
    
    logger.info(f"Found {len(all_entities)} entities")
    logger.info(f"Found {len(all_patterns)} structured patterns")
    
    # Step 6: Summary
    logger.info("\n" + "="*60)
    logger.info("PROCESSING SUMMARY")
    logger.info("="*60)
    logger.info(f"File: {pdf_path.name}")
    logger.info(f"Redactions found: {len(redactions)}")
    logger.info(f"Content recovered: {len(recovered_contents)}")
    logger.info(f"Entities extracted: {len(all_entities)}")
    logger.info(f"Patterns matched: {len(all_patterns)}")
    
    # Show sample entities
    if all_entities:
        logger.info("\nSample Entities:")
        for entity in all_entities[:5]:
            logger.info(f"  {entity.type}: {entity.text}")
    
    # Show sample patterns
    if all_patterns:
        logger.info("\nSample Patterns:")
        for pattern in all_patterns[:5]:
            logger.info(f"  {pattern.pattern_type}: {pattern.matched_text}")
    
    logger.info("\n" + "="*60)
    logger.info("Processing complete!")


if __name__ == '__main__':
    main()
