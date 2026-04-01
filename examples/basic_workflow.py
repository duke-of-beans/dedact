"""
DEDACT Example Usage Script
Demonstrates basic workflow for document processing
"""

from pathlib import Path
from src.ingestion import FileDiscoverer
from src.detection import VisualLayerAnalyzer, TextLayerAnalyzer, RedactionCorrelator
from src.extraction import DirectTextRecoverer, OCRProcessor
from src.analysis import EntityRecognizer
from src.storage import ExportGenerator
from src.utils import setup_logging

def main():
    """Basic DEDACT workflow example"""
    
    # Setup logging
    logger = setup_logging(log_level='INFO')
    logger.info("DEDACT Example Workflow")
    
    # Configuration
    input_dir = Path('data/sample_pdfs')
    output_dir = Path('output/example')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Step 1: Discover PDFs
    logger.info("Step 1: Discovering PDFs...")
    discoverer = FileDiscoverer()
    files = list(discoverer.discover(input_dir))
    logger.info(f"Found {len(files)} PDF files")
    
    if not files:
        logger.warning("No PDF files found")
        return
    
    # Step 2: Detect redactions
    logger.info("Step 2: Detecting redactions...")
    visual_analyzer = VisualLayerAnalyzer()
    text_analyzer = TextLayerAnalyzer()
    correlator = RedactionCorrelator()
    
    all_redactions = []
    for file in files:
        visual_candidates = visual_analyzer.analyze(file.path)
        text_positions, text_gaps = text_analyzer.analyze(file.path)
        redactions = correlator.correlate(visual_candidates, text_positions, text_gaps)
        all_redactions.extend([(file.path, r) for r in redactions])
    
    # Step 3: Extract content
    logger.info("Step 3: Extracting content...")
    recoverer = DirectTextRecoverer()
    
    recovered = []
    for pdf_path, redaction in all_redactions:
        if redaction.extractable:
            content = recoverer.extract(pdf_path, redaction)
            if content:
                recovered.append(content)
    
    # Step 4: Entity extraction
    logger.info("Step 4: Extracting entities...")
    recognizer = EntityRecognizer()
    
    all_entities = []
    for content in recovered:
        entities = recognizer.extract(content.text)
        all_entities.extend(entities)
    
    # Step 5: Export results
    logger.info("Step 5: Exporting results...")
    exporter = ExportGenerator(output_dir)
    
    exporter.export_json(
        {'recovered_content': [{'text': r.text, 'confidence': r.confidence} for r in recovered]},
        'recovered_content.json'
    )
    
    logger.info(f"Results: {output_dir}")
    print(f"\nProcessed: {len(files)} documents")
    print(f"Recovered: {len(recovered)} items")
    print(f"Entities: {len(all_entities)}")

if __name__ == '__main__':
    main()
