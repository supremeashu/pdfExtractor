"""
PDF Heading Extractor - Command Line Interface

Provides a user-friendly CLI for extracting headings from PDF documents.
"""

import click
import os
import glob
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from pdf_heading_extractor import PDFHeadingExtractor, ExtractionResult
import json

console = Console()


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """PDF Heading Extractor - Extract structured headings from PDF documents"""
    pass


@cli.command()
@click.argument('pdf_path', type=click.Path(exists=True))
@click.option('--output', '-o', default=None, help='Output JSON file path')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.option('--max-pages', default=50, help='Maximum pages to process')
@click.option('--confidence-threshold', default=0.6, help='Heading confidence threshold (0.0-1.0)')
def extract(pdf_path, output, verbose, max_pages, confidence_threshold):
    """Extract headings from a single PDF file"""
    
    # Validate inputs
    if not pdf_path.lower().endswith('.pdf'):
        console.print("[red]Error: File must be a PDF[/red]")
        return
    
    if confidence_threshold < 0.0 or confidence_threshold > 1.0:
        console.print("[red]Error: Confidence threshold must be between 0.0 and 1.0[/red]")
        return
    
    # Set default output path
    if output is None:
        pdf_name = Path(pdf_path).stem
        output = f"{pdf_name}_headings.json"
    
    console.print(f"[blue]Processing PDF:[/blue] {pdf_path}")
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            task = progress.add_task("Extracting headings...", total=None)
            
            # Initialize extractor
            extractor = PDFHeadingExtractor(
                max_pages=max_pages,
                heading_confidence_threshold=confidence_threshold
            )
            
            # Extract headings
            result = extractor.extract_headings(pdf_path)
            
            progress.update(task, description="Saving results...")
            
            # Save results
            extractor.save_json(result, output)
        
        # Display results
        _display_results(result, verbose)
        
        console.print(f"\n[green]✓ Extraction complete![/green] Results saved to: {output}")
        
    except Exception as e:
        console.print(f"[red]Error processing PDF: {str(e)}[/red]")


@cli.command()
@click.argument('input_dir', type=click.Path(exists=True))
@click.option('--output-dir', '-o', default='results', help='Output directory for JSON files')
@click.option('--pattern', default='*.pdf', help='File pattern to match')
@click.option('--max-pages', default=50, help='Maximum pages to process per PDF')
@click.option('--confidence-threshold', default=0.6, help='Heading confidence threshold')
def batch(input_dir, output_dir, pattern, max_pages, confidence_threshold):
    """Batch process multiple PDF files"""
    
    # Find PDF files
    pdf_files = glob.glob(os.path.join(input_dir, pattern))
    
    if not pdf_files:
        console.print(f"[yellow]No PDF files found in {input_dir} matching pattern {pattern}[/yellow]")
        return
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    console.print(f"[blue]Found {len(pdf_files)} PDF files to process[/blue]")
    console.print(f"[blue]Output directory:[/blue] {output_dir}")
    
    # Initialize extractor
    extractor = PDFHeadingExtractor(
        max_pages=max_pages,
        heading_confidence_threshold=confidence_threshold
    )
    
    success_count = 0
    error_count = 0
    
    with Progress(console=console) as progress:
        task = progress.add_task("Processing PDFs...", total=len(pdf_files))
        
        for pdf_file in pdf_files:
            filename = Path(pdf_file).stem
            output_file = os.path.join(output_dir, f"{filename}_headings.json")
            
            try:
                progress.update(task, description=f"Processing {filename}...")
                
                result = extractor.extract_headings(pdf_file)
                extractor.save_json(result, output_file)
                
                success_count += 1
                
            except Exception as e:
                console.print(f"[red]Error processing {filename}: {str(e)}[/red]")
                error_count += 1
            
            progress.advance(task)
    
    # Summary
    console.print(f"\n[green]✓ Batch processing complete![/green]")
    console.print(f"Successfully processed: {success_count}")
    if error_count > 0:
        console.print(f"[yellow]Errors: {error_count}[/yellow]")


@cli.command()
@click.argument('json_path', type=click.Path(exists=True))
def view(json_path):
    """View extraction results from a JSON file"""
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Display document info
        doc_info = data.get('document_info', {})
        console.print(Panel(
            f"[bold]Document:[/bold] {doc_info.get('filename', 'Unknown')}\n"
            f"[bold]Pages:[/bold] {doc_info.get('total_pages', 'Unknown')}\n"
            f"[bold]Extracted:[/bold] {doc_info.get('extraction_timestamp', 'Unknown')}",
            title="Document Information"
        ))
        
        # Display title
        title = data.get('title')
        if title:
            console.print(f"\n[bold blue]Title:[/bold blue] {title}")
        
        # Display headings in table
        headings = data.get('headings', [])
        if headings:
            table = Table(title="Extracted Headings")
            table.add_column("Level", style="cyan", width=8)
            table.add_column("Text", style="white")
            table.add_column("Page", style="magenta", width=6)
            table.add_column("Font Size", style="green", width=10)
            table.add_column("Confidence", style="yellow", width=10)
            
            for heading in headings:
                level_str = f"H{heading['level']}"
                table.add_row(
                    level_str,
                    heading['text'][:80] + ("..." if len(heading['text']) > 80 else ""),
                    str(heading['page']),
                    str(heading['font_size']),
                    f"{heading['confidence']:.2f}"
                )
            
            console.print(f"\n{table}")
        
        # Display statistics
        stats = data.get('extraction_stats', {})
        console.print(Panel(
            f"[bold]Total Headings:[/bold] {stats.get('total_headings', 0)}\n"
            f"[bold]H1 Count:[/bold] {stats.get('h1_count', 0)}\n"
            f"[bold]H2 Count:[/bold] {stats.get('h2_count', 0)}\n"
            f"[bold]H3 Count:[/bold] {stats.get('h3_count', 0)}",
            title="Statistics"
        ))
        
    except Exception as e:
        console.print(f"[red]Error reading JSON file: {str(e)}[/red]")


def _display_results(result: ExtractionResult, verbose: bool = False):
    """Display extraction results in a formatted way"""
    
    # Document info
    doc_info = result.document_info
    console.print(Panel(
        f"[bold]Document:[/bold] {doc_info['filename']}\n"
        f"[bold]Pages:[/bold] {doc_info['total_pages']}\n"
        f"[bold]Text Elements:[/bold] {doc_info.get('total_text_elements', 'Unknown')}",
        title="Document Information"
    ))
    
    # Title
    if result.title:
        console.print(f"\n[bold blue]Title:[/bold blue] {result.title}")
    
    # Headings summary
    if result.headings:
        if verbose:
            # Detailed table
            table = Table(title="Extracted Headings")
            table.add_column("Level", style="cyan", width=8)
            table.add_column("Text", style="white")
            table.add_column("Page", style="magenta", width=6)
            table.add_column("Font Size", style="green", width=10)
            table.add_column("Weight", style="blue", width=8)
            table.add_column("Confidence", style="yellow", width=10)
            
            for heading in result.headings:
                level_str = f"H{heading.level}"
                table.add_row(
                    level_str,
                    heading.text[:60] + ("..." if len(heading.text) > 60 else ""),
                    str(heading.page),
                    str(heading.font_size),
                    heading.font_weight,
                    f"{heading.confidence:.2f}"
                )
            
            console.print(f"\n{table}")
        else:
            # Simple list
            console.print("\n[bold]Headings Found:[/bold]")
            for heading in result.headings[:10]:  # Show first 10
                level_indent = "  " * (heading.level - 1)
                console.print(f"{level_indent}[cyan]H{heading.level}[/cyan] {heading.text} [dim](page {heading.page})[/dim]")
            
            if len(result.headings) > 10:
                console.print(f"[dim]... and {len(result.headings) - 10} more headings[/dim]")
    
    # Statistics
    stats = result.extraction_stats
    console.print(Panel(
        f"[bold]Total Headings:[/bold] {stats['total_headings']}\n"
        f"[bold]H1 Count:[/bold] {stats['h1_count']}\n"
        f"[bold]H2 Count:[/bold] {stats['h2_count']}\n"
        f"[bold]H3 Count:[/bold] {stats['h3_count']}",
        title="Statistics"
    ))


if __name__ == '__main__':
    cli()
