"""
Export Generators Module
Generate exports in multiple formats
"""

from pathlib import Path
from typing import Dict, List
import json
import csv


class ExportGenerator:
    """
    Generate exports in multiple formats
    
    Formats: JSON, CSV, HTML, Markdown, Cypher
    """
    
    def __init__(self, output_dir: Path):
        """
        Initialize export generator
        
        Args:
            output_dir: Output directory for exports
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def export_json(self, data: Dict, filename: str) -> Path:
        """Export data as JSON"""
        output_path = self.output_dir / filename
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        return output_path
    
    def export_csv(self, data: List[Dict], filename: str) -> Path:
        """Export data as CSV"""
        output_path = self.output_dir / filename
        
        if not data:
            return output_path
        
        keys = data[0].keys()
        
        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        
        return output_path
    
    def export_markdown(self, sections: Dict[str, str], filename: str) -> Path:
        """Export data as Markdown"""
        output_path = self.output_dir / filename
        
        with open(output_path, 'w') as f:
            for title, content in sections.items():
                f.write(f"# {title}\n\n")
                f.write(f"{content}\n\n")
        
        return output_path
    
    def export_html_report(self, data: Dict, filename: str) -> Path:
        """Generate HTML report"""
        output_path = self.output_dir / filename
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>DEDACT Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #4CAF50; color: white; }}
            </style>
        </head>
        <body>
            <h1>DEDACT Processing Report</h1>
            <p>Generated: {data.get('timestamp', 'Unknown')}</p>
            <h2>Statistics</h2>
            <pre>{json.dumps(data.get('statistics', {}), indent=2)}</pre>
        </body>
        </html>
        """
        
        with open(output_path, 'w') as f:
            f.write(html)
        
        return output_path
