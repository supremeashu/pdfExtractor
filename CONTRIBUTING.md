# Contributing to PDF Heading Extractor

Thank you for your interest in contributing to the PDF Heading Extractor! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

### Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:

```bash
git clone https://github.com/your-username/headingExtractor.git
cd headingExtractor
```

3. **Create a virtual environment**:

```bash
python -m venv dev-env
source dev-env/bin/activate  # Linux/Mac
dev-env\Scripts\activate     # Windows
```

4. **Install dependencies**:

```bash
pip install -r requirements.txt
```

5. **Run tests** to verify setup:

```bash
python simple_test.py
python run_tests.py
```

## 🔧 Development Guidelines

### Code Style

- **Python Style**: Follow PEP 8 guidelines
- **Type Hints**: Use type annotations for all function parameters and return values
- **Docstrings**: Add comprehensive docstrings for all public methods
- **Error Handling**: Implement proper exception handling for PDF processing edge cases

### Code Structure

```python
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class HeadingInfo:
    """Represents extracted heading information."""
    text: str
    level: int
    page: int
    font_size: float
    confidence: float

def extract_headings(pdf_path: str, max_pages: int = 50) -> Dict[str, any]:
    """
    Extract headings from PDF document.

    Args:
        pdf_path: Path to PDF file
        max_pages: Maximum pages to process

    Returns:
        Dictionary containing extracted headings and metadata

    Raises:
        FileNotFoundError: If PDF file doesn't exist
        PDFProcessingError: If PDF cannot be processed
    """
    pass
```

### Testing

- **Add tests** for new features in `test_utils.py`
- **Test edge cases** including corrupted PDFs, empty documents, etc.
- **Verify with real PDFs** from different sources (academic, corporate, etc.)

Example test:

```python
def test_heading_extraction():
    """Test basic heading extraction functionality."""
    extractor = PDFHeadingExtractor()
    result = extractor.extract_headings("test_document.pdf")

    assert "title" in result
    assert "headings" in result
    assert len(result["headings"]) > 0
    assert all("level" in h for h in result["headings"])
```

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment details**:

   - Python version
   - Operating system
   - Package versions (`pip list`)

2. **Sample PDF** (if possible) or description of PDF characteristics
3. **Error message** with full traceback
4. **Expected behavior** vs actual behavior
5. **Steps to reproduce** the issue

## ✨ Feature Requests

For new features, please provide:

1. **Use case description** - Why is this feature needed?
2. **Proposed implementation** - How should it work?
3. **Example usage** - Code examples of how it would be used
4. **Alternatives considered** - Other approaches you've thought about

## 🔀 Pull Requests

### Before Submitting

- [ ] Code follows style guidelines
- [ ] Tests pass (`python run_tests.py`)
- [ ] New features include tests
- [ ] Documentation updated if needed
- [ ] Commit messages are descriptive

### Pull Request Process

1. **Create feature branch**:

```bash
git checkout -b feature/your-feature-name
```

2. **Make changes** following guidelines above

3. **Test thoroughly**:

```bash
python simple_test.py
python run_tests.py
# Test with various PDF types
```

4. **Commit with descriptive messages**:

```bash
git commit -m "Add support for multi-column PDF layouts"
```

5. **Push to your fork**:

```bash
git push origin feature/your-feature-name
```

6. **Create pull request** with:
   - Clear description of changes
   - Reference to related issues
   - Screenshots/examples if applicable

## 📋 Areas for Contribution

### High Priority

- **OCR Integration**: Support for image-based PDFs
- **Layout Analysis**: Better handling of multi-column documents
- **Font Detection**: Improved font family classification
- **Performance**: Optimization for large PDFs (>50 pages)

### Medium Priority

- **Export Formats**: Support for Markdown, HTML output
- **Configuration**: GUI for configuration settings
- **Batch Processing**: Parallel processing for multiple PDFs
- **Machine Learning**: Enhanced ML models for heading classification

### Documentation

- **Tutorial videos**: Step-by-step usage guides
- **API documentation**: Comprehensive function documentation
- **Examples**: More sample PDFs and expected outputs
- **Troubleshooting**: Common issues and solutions

## 🏗️ Architecture Overview

### Core Components

```
pdf_heading_extractor.py    # Main extraction engine
├── FontInfo               # Font analysis data structures
├── TextElement           # Text element representation
├── Heading               # Heading data structure
└── PDFHeadingExtractor   # Main extractor class

main.py                   # CLI interface
├── extract()             # Single PDF extraction
├── batch()              # Batch processing
└── view()               # Result visualization

config.py                # Configuration management
pdf_utils.py             # Advanced PDF utilities
test_utils.py            # Testing framework
```

### Key Algorithms

1. **Font Analysis**: Statistical analysis of font properties
2. **Text Classification**: Rule-based + ML heading detection
3. **Hierarchy Detection**: Level assignment based on font size/weight
4. **Confidence Scoring**: Reliability metrics for each heading

## 🤔 Questions?

- **Check existing issues** for similar questions
- **Review documentation** and troubleshooting section
- **Run with `--verbose`** to see detailed processing
- **Create an issue** with "question" label

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to PDF Heading Extractor! 🎉
