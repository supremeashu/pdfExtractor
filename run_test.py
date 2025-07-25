#!/usr/bin/env python3
"""
Quick test runner for the PDF processing script with custom paths
"""
import os
import sys
from pathlib import Path

# Import the main script components
from process_pdfs import FastPDFHeadingExtractor
import json
import time

def run_with_custom_paths(input_dir, output_dir):
    """Run PDF processing with custom input/output directories"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    print(f"Processing PDFs from: {input_path}")
    print(f"Output directory: {output_path}")
    
    # Ensure output directory exists
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Initialize extractor
    extractor = FastPDFHeadingExtractor()
    
    # Get all PDF files
    pdf_files = list(input_path.glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in input directory")
        return
    
    print(f"Found {len(pdf_files)} PDF files to process")
    
    total_start_time = time.time()
    
    for pdf_file in pdf_files:
        print(f"\nProcessing: {pdf_file.name}")
        start_time = time.time()
        
        # Extract headings
        result = extractor.extract_headings(str(pdf_file))
        
        # Create output filename
        output_file = output_path / f"{pdf_file.stem}.json"
        
        # Save result
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        processing_time = time.time() - start_time
        print(f"  ✓ Completed in {processing_time:.3f}s")
        print(f"  ✓ Title: {result.get('title', 'None')}")
        print(f"  ✓ Found {len(result['outline'])} headings")
        print(f"  ✓ Output: {output_file.name}")
    
    total_time = time.time() - total_start_time
    print(f"\n=== Processing Complete ===")
    print(f"Total time: {total_time:.3f} seconds")
    print(f"Average per file: {total_time/len(pdf_files):.3f} seconds")
    print(f"Processed {len(pdf_files)} files successfully")

if __name__ == "__main__":
    # Use command line arguments or defaults
    input_dir = sys.argv[1] if len(sys.argv) > 1 else "sample_dataset/pdfs"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "sample_dataset/outputs"
    
    run_with_custom_paths(input_dir, output_dir)
