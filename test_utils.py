"""
Test utilities and example usage for PDF Heading Extractor
"""

from pdf_heading_extractor import PDFHeadingExtractor
import json
from rich.console import Console
import os

console = Console()


def test_extractor():
    """Test the extractor with sample data"""
    console.print("[blue]Testing PDF Heading Extractor...[/blue]")
    
    # Initialize extractor
    extractor = PDFHeadingExtractor(
        max_pages=10,  # Limit for testing
        heading_confidence_threshold=0.5
    )
    
    # Test with a sample PDF (if available)
    test_pdf_path = "sample.pdf"
    
    if os.path.exists(test_pdf_path):
        console.print(f"[green]Testing with: {test_pdf_path}[/green]")
        
        try:
            result = extractor.extract_headings(test_pdf_path)
            
            # Display results
            console.print(f"[cyan]Extracted {len(result.headings)} headings[/cyan]")
            
            if result.title:
                console.print(f"[yellow]Title: {result.title}[/yellow]")
            
            for heading in result.headings[:5]:  # Show first 5
                console.print(f"  H{heading.level}: {heading.text} (page {heading.page})")
            
            # Save results
            extractor.save_json(result, "test_results.json")
            console.print("[green]✓ Test completed successfully![/green]")
            
        except Exception as e:
            console.print(f"[red]Test failed: {str(e)}[/red]")
    else:
        console.print(f"[yellow]No test PDF found at {test_pdf_path}[/yellow]")
        console.print("[yellow]Please provide a sample PDF file for testing[/yellow]")


def create_sample_json():
    """Create a sample JSON output for demonstration"""
    sample_data = {
        "document_info": {
            "filename": "sample_document.pdf",
            "total_pages": 15,
            "extraction_timestamp": "2025-01-20T10:30:00Z",
            "total_text_elements": 342
        },
        "title": "Advanced Machine Learning Techniques in Natural Language Processing",
        "headings": [
            {
                "text": "Abstract",
                "level": 1,
                "page": 1,
                "font_size": 16.0,
                "font_weight": "bold",
                "confidence": 0.95
            },
            {
                "text": "Introduction",
                "level": 1,
                "page": 2,
                "font_size": 16.0,
                "font_weight": "bold",
                "confidence": 0.93
            },
            {
                "text": "Background and Related Work",
                "level": 2,
                "page": 3,
                "font_size": 14.0,
                "font_weight": "bold",
                "confidence": 0.88
            },
            {
                "text": "Previous Approaches",
                "level": 3,
                "page": 3,
                "font_size": 12.0,
                "font_weight": "bold",
                "confidence": 0.82
            },
            {
                "text": "Limitations of Current Methods",
                "level": 3,
                "page": 4,
                "font_size": 12.0,
                "font_weight": "bold",
                "confidence": 0.85
            },
            {
                "text": "Methodology",
                "level": 1,
                "page": 5,
                "font_size": 16.0,
                "font_weight": "bold",
                "confidence": 0.94
            },
            {
                "text": "Data Collection and Preprocessing",
                "level": 2,
                "page": 5,
                "font_size": 14.0,
                "font_weight": "bold",
                "confidence": 0.87
            },
            {
                "text": "Model Architecture",
                "level": 2,
                "page": 7,
                "font_size": 14.0,
                "font_weight": "bold",
                "confidence": 0.89
            },
            {
                "text": "Training and Evaluation",
                "level": 2,
                "page": 9,
                "font_size": 14.0,
                "font_weight": "bold",
                "confidence": 0.86
            },
            {
                "text": "Results",
                "level": 1,
                "page": 11,
                "font_size": 16.0,
                "font_weight": "bold",
                "confidence": 0.92
            },
            {
                "text": "Quantitative Analysis",
                "level": 2,
                "page": 11,
                "font_size": 14.0,
                "font_weight": "bold",
                "confidence": 0.84
            },
            {
                "text": "Qualitative Assessment",
                "level": 2,
                "page": 13,
                "font_size": 14.0,
                "font_weight": "bold",
                "confidence": 0.83
            },
            {
                "text": "Discussion",
                "level": 1,
                "page": 14,
                "font_size": 16.0,
                "font_weight": "bold",
                "confidence": 0.91
            },
            {
                "text": "Conclusion",
                "level": 1,
                "page": 15,
                "font_size": 16.0,
                "font_weight": "bold",
                "confidence": 0.94
            },
            {
                "text": "References",
                "level": 1,
                "page": 15,
                "font_size": 16.0,
                "font_weight": "bold",
                "confidence": 0.96
            }
        ],
        "extraction_stats": {
            "total_headings": 15,
            "h1_count": 6,
            "h2_count": 7,
            "h3_count": 2
        }
    }
    
    with open("sample_output.json", "w", encoding="utf-8") as f:
        json.dump(sample_data, f, indent=2, ensure_ascii=False)
    
    console.print("[green]✓ Sample JSON created: sample_output.json[/green]")


def validate_json_schema(json_path: str):
    """Validate JSON output format"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check required fields
        required_fields = ['document_info', 'headings', 'extraction_stats']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            console.print(f"[red]Missing required fields: {missing_fields}[/red]")
            return False
        
        # Check document_info structure
        doc_info = data['document_info']
        doc_required = ['filename', 'total_pages', 'extraction_timestamp']
        doc_missing = [field for field in doc_required if field not in doc_info]
        
        if doc_missing:
            console.print(f"[red]Missing document_info fields: {doc_missing}[/red]")
            return False
        
        # Check headings structure
        headings = data['headings']
        if headings:
            heading_required = ['text', 'level', 'page', 'font_size', 'confidence']
            for i, heading in enumerate(headings[:3]):  # Check first 3
                heading_missing = [field for field in heading_required if field not in heading]
                if heading_missing:
                    console.print(f"[red]Missing heading[{i}] fields: {heading_missing}[/red]")
                    return False
        
        # Check stats structure
        stats = data['extraction_stats']
        stats_required = ['total_headings', 'h1_count', 'h2_count', 'h3_count']
        stats_missing = [field for field in stats_required if field not in stats]
        
        if stats_missing:
            console.print(f"[red]Missing extraction_stats fields: {stats_missing}[/red]")
            return False
        
        console.print("[green]✓ JSON schema validation passed[/green]")
        return True
        
    except json.JSONDecodeError as e:
        console.print(f"[red]Invalid JSON format: {str(e)}[/red]")
        return False
    except Exception as e:
        console.print(f"[red]Error validating JSON: {str(e)}[/red]")
        return False


if __name__ == "__main__":
    console.print("[bold blue]PDF Heading Extractor - Test Suite[/bold blue]\n")
    
    # Create sample output
    create_sample_json()
    
    # Validate sample output
    validate_json_schema("sample_output.json")
    
    # Run extractor test
    test_extractor()
