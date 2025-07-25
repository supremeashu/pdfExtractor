#!/usr/bin/env python3
"""
Fast PDF heading extraction script
Usage: python fast_extract.py <pdf_file>
"""

import sys
import time
from fast_extractor import FastPDFHeadingExtractor, save_json

def main():
    if len(sys.argv) != 2:
        print("Usage: python fast_extract.py <pdf_file>")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    output_file = pdf_file.replace('.pdf', '_headings.json')
    
    print(f"Extracting headings from: {pdf_file}")
    
    # Time the extraction
    start_time = time.time()
    
    extractor = FastPDFHeadingExtractor()
    result = extractor.extract_headings(pdf_file)
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    # Save result
    save_json(result, output_file)
    
    print(f"✓ Complete! Output saved to: {output_file}")
    print(f"  Found {len(result['outline'])} headings")
    print(f"  Execution time: {execution_time:.2f} seconds")

if __name__ == "__main__":
    main()
