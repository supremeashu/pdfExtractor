#!/usr/bin/env python3
"""
Batch process all PDF files for comparison with expected outputs
"""

import time
from fast_extractor import FastPDFHeadingExtractor, save_json

def main():
    pdf_files = ['file01.pdf', 'file02.pdf', 'file03.pdf', 'file04.pdf', 'file05.pdf']
    
    print("=== Fast PDF Heading Extraction - Batch Processing ===")
    
    total_start = time.time()
    extractor = FastPDFHeadingExtractor()
    
    for pdf_file in pdf_files:
        print(f"\nProcessing: {pdf_file}")
        
        start_time = time.time()
        result = extractor.extract_headings(pdf_file)
        end_time = time.time()
        
        output_file = pdf_file.replace('.pdf', '_headings.json')
        save_json(result, output_file)
        
        print(f"  ✓ Saved to: {output_file}")
        print(f"  ✓ Found {len(result['outline'])} headings")
        print(f"  ✓ Time: {end_time - start_time:.3f}s")
    
    total_time = time.time() - total_start
    print(f"\n=== Batch Complete ===")
    print(f"Total processing time: {total_time:.3f} seconds")
    print(f"Average per file: {total_time/len(pdf_files):.3f} seconds")

if __name__ == "__main__":
    main()
