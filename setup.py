"""
DEDACT Setup Configuration
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_path = Path(__file__).parent / 'README.md'
long_description = readme_path.read_text(encoding='utf-8') if readme_path.exists() else ''

setup(
    name='dedact',
    version='1.0.0',
    description='Document Extraction, De-Redaction, and Analysis Capability Tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='David Kirsch',
    author_email='david@fineprintpress.com',
    url='https://github.com/yourusername/dedact',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    python_requires='>=3.10',
    install_requires=[
        'PyPDF2>=3.0.0',
        'pdf2image>=1.16.3',
        'pdfminer.six>=20221105',
        'pytesseract>=0.3.10',
        'Pillow>=10.0.0',
        'opencv-python>=4.8.0',
        'spacy>=3.7.0',
        'psycopg2-binary>=2.9.9',
        'neo4j>=5.14.0',
        'PyYAML>=6.0',
        'click>=8.1.7',
        'requests>=2.31.0',
        'tqdm>=4.66.0',
        'python-dateutil>=2.8.2',
        'fuzzywuzzy>=0.18.0',
        'python-Levenshtein>=0.21.1',
        'numpy>=1.24.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.4.0',
            'pytest-cov>=4.1.0',
            'pytest-mock>=3.11.1',
            'black>=23.7.0',
            'flake8>=6.1.0',
            'mypy>=1.5.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'dedact=dedact.cli.dedact:cli',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Researchers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    keywords='pdf redaction forensics document-analysis',
)
