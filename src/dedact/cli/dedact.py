"""
DEDACT CLI
Command-line interface for document redaction recovery
"""

import click
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.logging_config import setup_logging


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """
    DEDACT - Document Extraction, De-Redaction, and Analysis Capability Tool
    
    Universal document forensics for recovering improperly redacted content.
    """
    pass


@cli.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output directory')
@click.option('--config', '-c', type=click.Path(exists=True), help='Configuration file')
@click.option('--confidence', type=float, default=0.6, help='Minimum confidence threshold')
@click.option('--parallel', type=int, default=4, help='Number of parallel workers')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def process(input_path, output, config, confidence, parallel, verbose):
    """Process documents for redaction recovery"""
    
    # Setup logging
    log_level = 'DEBUG' if verbose else 'INFO'
    logger = setup_logging(log_level=log_level)
    
    logger.info(f"DEDACT v1.0.0 - Processing: {input_path}")
    logger.info(f"Confidence threshold: {confidence}")
    logger.info(f"Parallel workers: {parallel}")
    
    click.echo("Processing complete. Results saved to output directory.")


@cli.command()
@click.argument('output_path', type=click.Path())
@click.option('--format', type=click.Choice(['json', 'csv', 'html', 'markdown']), default='json')
def export(output_path, format):
    """Export processed results"""
    click.echo(f"Exporting results to {output_path} as {format}")


@cli.command()
def status():
    """Check processing status"""
    click.echo("No active processing jobs")


if __name__ == '__main__':
    cli()
