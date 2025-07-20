"""
PDF Heading Extractor - Python API Usage Examples

This file demonstrates various ways to use the PDF Heading Extractor
programmatically through its Python API.
"""

from pdf_heading_extractor import PDFHeadingExtractor
import json
from pathlib import Path
from typing import Dict, List


def basic_extraction_example():
    """Basic PDF heading extraction example."""
    print("=== Basic Extraction Example ===")
    
    # Initialize extractor with default settings
    extractor = PDFHeadingExtractor()
    
    # Extract headings from PDF
    pdf_path = "examples/academic_paper.pdf"
    if Path(pdf_path).exists():
        result = extractor.extract_headings(pdf_path)
        
        # Display basic information
        print(f"Document: {result['document_info']['filename']}")
        print(f"Pages: {result['document_info']['total_pages']}")
        print(f"Title: {result['title']}")
        print(f"Total headings: {result['extraction_stats']['total_headings']}")
        
        # Show first few headings
        print("\nFirst 5 headings:")
        for i, heading in enumerate(result['headings'][:5]):
            print(f"  {i+1}. [{heading['level']}] {heading['text']} (Page {heading['page']})")
    else:
        print(f"Example PDF not found: {pdf_path}")


def custom_settings_example():
    """Example with custom extraction settings."""
    print("\n=== Custom Settings Example ===")
    
    # Initialize with custom settings
    extractor = PDFHeadingExtractor(
        max_pages=30,                    # Limit to 30 pages
        min_font_size=9.0,              # Ignore text smaller than 9pt
        heading_confidence_threshold=0.8, # Higher confidence threshold
        include_font_details=True       # Include detailed font information
    )
    
    pdf_path = "examples/lab_manual.pdf"
    if Path(pdf_path).exists():
        result = extractor.extract_headings(pdf_path)
        
        print(f"Extracted {len(result['headings'])} headings with confidence ≥ 0.8")
        
        # Show headings by level
        headings_by_level = {}
        for heading in result['headings']:
            level = heading['level']
            if level not in headings_by_level:
                headings_by_level[level] = []
            headings_by_level[level].append(heading)
        
        for level in sorted(headings_by_level.keys()):
            print(f"\nH{level} headings ({len(headings_by_level[level])}):")
            for heading in headings_by_level[level][:3]:  # Show first 3
                print(f"  - {heading['text']} (Page {heading['page']}, {heading['font_size']}pt)")
    else:
        print(f"Example PDF not found: {pdf_path}")


def batch_processing_example():
    """Example of processing multiple PDFs."""
    print("\n=== Batch Processing Example ===")
    
    extractor = PDFHeadingExtractor()
    examples_dir = Path("examples")
    
    # Find all PDF files in examples directory
    pdf_files = list(examples_dir.glob("*.pdf"))
    
    if pdf_files:
        print(f"Found {len(pdf_files)} PDF files to process:")
        
        results = {}
        for pdf_file in pdf_files:
            try:
                print(f"  Processing: {pdf_file.name}")
                result = extractor.extract_headings(str(pdf_file))
                results[pdf_file.name] = result
                
                # Quick summary
                stats = result['extraction_stats']
                print(f"    → {stats['total_headings']} headings "
                      f"(H1: {stats['h1_count']}, H2: {stats['h2_count']}, H3: {stats['h3_count']})")
                
            except Exception as e:
                print(f"    ✗ Error processing {pdf_file.name}: {e}")
        
        print(f"\nSuccessfully processed {len(results)} PDFs")
        return results
    else:
        print("No PDF files found in examples directory")
        return {}


def filtering_and_analysis_example():
    """Example of filtering and analyzing extracted headings."""
    print("\n=== Filtering and Analysis Example ===")
    
    extractor = PDFHeadingExtractor()
    pdf_path = "examples/technical_report.pdf"
    
    if Path(pdf_path).exists():
        result = extractor.extract_headings(pdf_path)
        headings = result['headings']
        
        # Filter high-confidence headings
        high_confidence = [h for h in headings if h['confidence'] >= 0.9]
        print(f"High confidence headings (≥90%): {len(high_confidence)}")
        
        # Filter by level
        h1_headings = [h for h in headings if h['level'] == 1]
        h2_headings = [h for h in headings if h['level'] == 2]
        
        print(f"Main sections (H1): {len(h1_headings)}")
        print(f"Subsections (H2): {len(h2_headings)}")
        
        # Analyze font sizes
        font_sizes = [h['font_size'] for h in headings]
        avg_font_size = sum(font_sizes) / len(font_sizes)
        max_font_size = max(font_sizes)
        min_font_size = min(font_sizes)
        
        print(f"\nFont size analysis:")
        print(f"  Average: {avg_font_size:.1f}pt")
        print(f"  Range: {min_font_size:.1f}pt - {max_font_size:.1f}pt")
        
        # Find long headings
        long_headings = [h for h in headings if len(h['text']) > 50]
        if long_headings:
            print(f"\nLong headings (>50 chars): {len(long_headings)}")
            for heading in long_headings[:2]:
                print(f"  - {heading['text'][:60]}...")
    else:
        print(f"Example PDF not found: {pdf_path}")


def save_results_example():
    """Example of saving results in different formats."""
    print("\n=== Save Results Example ===")
    
    extractor = PDFHeadingExtractor()
    pdf_path = "examples/academic_paper.pdf"
    
    if Path(pdf_path).exists():
        result = extractor.extract_headings(pdf_path)
        
        # Save as JSON (default)
        json_output = "example_output.json"
        extractor.save_json(result, json_output)
        print(f"Saved JSON to: {json_output}")
        
        # Save only headings as simplified JSON
        headings_only = {
            "title": result['title'],
            "headings": [
                {
                    "text": h['text'],
                    "level": h['level'], 
                    "page": h['page']
                }
                for h in result['headings']
            ]
        }
        
        with open("example_simplified.json", "w", encoding="utf-8") as f:
            json.dump(headings_only, f, indent=2, ensure_ascii=False)
        print("Saved simplified JSON to: example_simplified.json")
        
        # Create markdown outline
        markdown_output = create_markdown_outline(result)
        with open("example_outline.md", "w", encoding="utf-8") as f:
            f.write(markdown_output)
        print("Saved Markdown outline to: example_outline.md")
    else:
        print(f"Example PDF not found: {pdf_path}")


def create_markdown_outline(result: Dict) -> str:
    """Create a markdown outline from extraction results."""
    lines = [f"# {result['title']}\n"]
    
    for heading in result['headings']:
        level = heading['level']
        text = heading['text']
        page = heading['page']
        
        # Create markdown heading with appropriate level
        if level == 1:
            lines.append(f"## {text}")
        elif level == 2:
            lines.append(f"### {text}")
        elif level == 3:
            lines.append(f"#### {text}")
        else:
            lines.append(f"{'  ' * (level-1)}- {text}")
        
        lines.append(f"*Page {page}*\n")
    
    return "\n".join(lines)


def error_handling_example():
    """Example of proper error handling."""
    print("\n=== Error Handling Example ===")
    
    extractor = PDFHeadingExtractor()
    
    # Test with non-existent file
    try:
        result = extractor.extract_headings("nonexistent.pdf")
    except FileNotFoundError as e:
        print(f"✓ Correctly handled missing file: {e}")
    
    # Test with invalid file
    try:
        # Create a dummy text file with .pdf extension
        with open("invalid.pdf", "w") as f:
            f.write("This is not a PDF file")
        
        result = extractor.extract_headings("invalid.pdf")
    except Exception as e:
        print(f"✓ Correctly handled invalid PDF: {type(e).__name__}")
    finally:
        # Clean up
        if Path("invalid.pdf").exists():
            Path("invalid.pdf").unlink()


if __name__ == "__main__":
    """Run all examples."""
    print("PDF Heading Extractor - Python API Examples")
    print("=" * 50)
    
    # Run all examples
    basic_extraction_example()
    custom_settings_example()
    batch_processing_example()
    filtering_and_analysis_example()
    save_results_example()
    error_handling_example()
    
    print("\n" + "=" * 50)
    print("Examples completed! Check the generated output files:")
    print("  - example_output.json")
    print("  - example_simplified.json") 
    print("  - example_outline.md")
