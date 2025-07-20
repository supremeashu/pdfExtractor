"""
Example usage and demonstration of the PDF Heading Extractor
"""

from pdf_heading_extractor import PDFHeadingExtractor, ExtractionResult
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import json
import os

console = Console()


def demonstrate_api_usage():
    """Demonstrate Python API usage"""
    console.print("[bold blue]PDF Heading Extractor - API Demo[/bold blue]\n")
    
    # Initialize the extractor with custom settings
    extractor = PDFHeadingExtractor(
        max_pages=25,  # Process up to 25 pages
        min_font_size=10.0,  # Minimum font size to consider
        heading_confidence_threshold=0.7  # Higher threshold for better precision
    )
    
    console.print("[cyan]Extractor initialized with custom settings:[/cyan]")
    console.print(f"  • Max pages: {extractor.max_pages}")
    console.print(f"  • Min font size: {extractor.min_font_size}")
    console.print(f"  • Confidence threshold: {extractor.heading_confidence_threshold}")
    
    # Example PDF path (you would replace this with your actual PDF)
    example_pdf = "sample_document.pdf"
    
    if os.path.exists(example_pdf):
        console.print(f"\n[green]Processing PDF:[/green] {example_pdf}")
        
        try:
            # Extract headings
            result = extractor.extract_headings(example_pdf)
            
            # Display results
            display_extraction_result(result)
            
            # Save to JSON
            output_file = "demo_output.json"
            extractor.save_json(result, output_file)
            console.print(f"\n[green]✓ Results saved to:[/green] {output_file}")
            
        except Exception as e:
            console.print(f"[red]Error processing PDF:[/red] {str(e)}")
    else:
        console.print(f"\n[yellow]Example PDF not found:[/yellow] {example_pdf}")
        console.print("[yellow]Please provide a PDF file to test with[/yellow]")
        
        # Show example output format instead
        show_example_output()


def display_extraction_result(result: ExtractionResult):
    """Display extraction results in a formatted way"""
    
    # Document information
    doc_info = result.document_info
    info_panel = Panel(
        f"[bold]Filename:[/bold] {doc_info['filename']}\n"
        f"[bold]Total Pages:[/bold] {doc_info['total_pages']}\n"
        f"[bold]Processed:[/bold] {doc_info.get('total_text_elements', 'N/A')} text elements\n"
        f"[bold]Extracted:[/bold] {doc_info['extraction_timestamp']}",
        title="Document Information",
        border_style="blue"
    )
    console.print(info_panel)
    
    # Document title
    if result.title:
        title_panel = Panel(
            f"[bold white]{result.title}[/bold white]",
            title="Document Title",
            border_style="green"
        )
        console.print(title_panel)
    
    # Headings table
    if result.headings:
        table = Table(title="Extracted Headings", show_header=True, header_style="bold magenta")
        table.add_column("Level", style="cyan", width=8)
        table.add_column("Text", style="white", min_width=40)
        table.add_column("Page", style="blue", width=6)
        table.add_column("Font Size", style="green", width=10)
        table.add_column("Weight", style="yellow", width=8)
        table.add_column("Confidence", style="red", width=10)
        
        for heading in result.headings:
            level_indicator = "H" + str(heading.level)
            text_preview = heading.text[:60] + ("..." if len(heading.text) > 60 else "")
            
            table.add_row(
                level_indicator,
                text_preview,
                str(heading.page),
                f"{heading.font_size:.1f}",
                heading.font_weight,
                f"{heading.confidence:.2f}"
            )
        
        console.print(table)
    
    # Statistics
    stats = result.extraction_stats
    stats_panel = Panel(
        f"[bold]Total Headings:[/bold] {stats['total_headings']}\n"
        f"[bold]H1 (Main headings):[/bold] {stats['h1_count']}\n"
        f"[bold]H2 (Sub-headings):[/bold] {stats['h2_count']}\n"
        f"[bold]H3 (Sub-sub-headings):[/bold] {stats['h3_count']}",
        title="Extraction Statistics",
        border_style="yellow"
    )
    console.print(stats_panel)


def show_example_output():
    """Show example output format"""
    console.print("\n[bold cyan]Example Output Format:[/bold cyan]")
    
    example_json = {
        "document_info": {
            "filename": "research_paper.pdf",
            "total_pages": 12,
            "extraction_timestamp": "2025-01-20T15:30:00Z",
            "total_text_elements": 287
        },
        "title": "Machine Learning Applications in Document Analysis",
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
                "text": "Related Work",
                "level": 2,
                "page": 3,
                "font_size": 14.0,
                "font_weight": "bold",
                "confidence": 0.88
            },
            {
                "text": "Deep Learning Approaches",
                "level": 3,
                "page": 4,
                "font_size": 12.0,
                "font_weight": "bold",
                "confidence": 0.82
            }
        ],
        "extraction_stats": {
            "total_headings": 15,
            "h1_count": 5,
            "h2_count": 7,
            "h3_count": 3
        }
    }
    
    console.print(json.dumps(example_json, indent=2))


def demonstrate_batch_processing():
    """Demonstrate batch processing capabilities"""
    console.print("\n[bold blue]Batch Processing Example[/bold blue]")
    
    # This would be used for processing multiple PDFs
    console.print("[cyan]To process multiple PDFs:[/cyan]")
    console.print("1. Place PDFs in a folder (e.g., 'documents/')")
    console.print("2. Run: python main.py batch documents/ --output-dir results/")
    console.print("3. Find JSON files for each PDF in 'results/' folder")
    
    console.print("\n[yellow]Command line options:[/yellow]")
    console.print("  --max-pages 50          # Limit pages per document")
    console.print("  --confidence-threshold 0.7  # Set confidence level")
    console.print("  --pattern *.pdf         # File pattern to match")


def demonstrate_json_viewing():
    """Demonstrate JSON result viewing"""
    console.print("\n[bold blue]Viewing Results[/bold blue]")
    
    console.print("[cyan]To view extraction results:[/cyan]")
    console.print("python main.py view results/document_headings.json")
    
    console.print("\n[cyan]To validate JSON format:[/cyan]")
    console.print("python test_utils.py")


if __name__ == "__main__":
    # Run the demonstration
    demonstrate_api_usage()
    demonstrate_batch_processing()
    demonstrate_json_viewing()
    
    console.print("\n[bold green]Demo completed![/bold green]")
    console.print("\n[dim]For more information, see README.md or run: python main.py --help[/dim]")
