"""
Simple PDF Heading Extractor
Usage: python extract.py input.pdf
Output: input_headings.json
"""

import sys
import os
import json
from pdf_heading_extractor import PDFHeadingExtractor

def main():
    # Check command line arguments
    if len(sys.argv) != 2:
        print("Usage: python extract.py input.pdf")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    
    # Check if PDF file exists
    if not os.path.exists(pdf_file):
        print(f"Error: File '{pdf_file}' not found")
        sys.exit(1)
    
    if not pdf_file.lower().endswith('.pdf'):
        print("Error: File must be a PDF")
        sys.exit(1)
    
    # Generate output filename
    base_name = os.path.splitext(pdf_file)[0]
    output_file = f"{base_name}_headings.json"
    
    try:
        print(f"Processing: {pdf_file}")
        
        # Extract headings
        extractor = PDFHeadingExtractor()
        result = extractor.extract_headings(pdf_file)
        
        # Save to JSON (simplified format)
        output_data = result.to_dict()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Complete! Output saved to: {output_file}")
        print(f"  Found {len(result.headings)} headings")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
