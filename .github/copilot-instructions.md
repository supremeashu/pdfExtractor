<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

## Project: PDF Heading Extractor

This is a Python application for extracting structured headings and titles from PDF documents.

### Key Technologies:

- **PyMuPDF (fitz)**: Primary PDF processing library for text extraction and font analysis
- **PDFplumber**: Secondary PDF library for text extraction and layout analysis
- **pandas**: Data manipulation and analysis
- **scikit-learn**: Machine learning features for heading classification
- **click**: Command-line interface framework
- **rich**: Enhanced console output and formatting

### Code Structure Guidelines:

- Use type hints for all function parameters and return values
- Follow dataclass patterns for structured data representations
- Implement comprehensive error handling for PDF processing edge cases
- Use logging for debugging and monitoring extraction processes
- Create modular, testable functions with single responsibilities

### PDF Processing Considerations:

- Handle both text-based and image-based PDFs gracefully
- Account for various font encoding issues and special characters
- Implement robust page boundary detection and text positioning
- Consider document layout variations (single/multi-column, headers/footers)
- Handle edge cases like rotated text, tables, and embedded images

### Heading Detection Strategy:

- Combine font analysis (size, weight, family) with text patterns
- Use statistical analysis to determine relative heading importance
- Implement whitespace and positioning analysis for structure detection
- Apply machine learning classification as a secondary validation method
- Consider document-specific patterns and formatting conventions
