#!/usr/bin/env python3
"""
PDF Processing Script for Adobe Hackathon Challenge 1a
Processes all PDFs from /app/input and outputs JSON to /app/output
"""

import os
import sys
import json
import time
from pathlib import Path

# Import our fast extractor
import fitz  # PyMuPDF
import re
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple
from collections import Counter

@dataclass
class FontInfo:
    size: float
    name: str
    is_bold: bool
    bbox: Tuple[float, float, float, float]

@dataclass
class TextElement:
    text: str
    font: FontInfo
    page_number: int
    position_y: float

@dataclass
class Heading:
    text: str
    level: int
    page: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'text': self.text.strip(),
            'level': f"H{self.level}",
            'page': self.page
        }

class FastPDFHeadingExtractor:
    """Optimized PDF heading extraction for Adobe Hackathon"""
    
    def __init__(self, max_pages: int = 50):
        self.max_pages = max_pages
        
        # Optimized patterns for common document structures
        self.h1_patterns = [
            r'^\d+\.\s+[A-Z]',  # "1. Introduction"
            r'^[A-Z][A-Z\s]{8,}$',  # "INTRODUCTION"
            r'^(Introduction|Conclusion|References|Acknowledgements|Abstract)$'
        ]
        
        self.h2_patterns = [
            r'^\d+\.\d+\s+[A-Z]',  # "2.1 Subsection"
        ]
    
    def extract_headings(self, pdf_path: str) -> Dict[str, Any]:
        """Fast extraction with minimal processing"""
        try:
            # Extract text elements quickly
            text_elements = self._extract_text_fast(pdf_path)
            
            if not text_elements:
                return {"title": None, "outline": []}
            
            # Quick font analysis
            font_sizes = [elem.font.size for elem in text_elements]
            avg_size = sum(font_sizes) / len(font_sizes)
            max_size = max(font_sizes)
            
            # Extract title (largest text on first page)
            title = self._extract_title_fast(text_elements, max_size)
            
            # Find headings using size and pattern heuristics
            headings = self._find_headings_fast(text_elements, avg_size, title)
            
            return {
                "title": title,
                "outline": [h.to_dict() for h in headings]
            }
            
        except Exception as e:
            print(f"Error processing {pdf_path}: {e}")
            return {"title": None, "outline": []}
    
    def _extract_text_fast(self, pdf_path: str) -> List[TextElement]:
        """Fast text extraction with minimal processing"""
        elements = []
        
        doc = fitz.open(pdf_path)
        total_pages = min(len(doc), self.max_pages)
        
        for page_num in range(total_pages):
            page = doc[page_num]
            page_height = page.rect.height
            
            # Get text with font info
            blocks = page.get_text("dict")
            
            for block in blocks.get("blocks", []):
                if "lines" not in block:
                    continue
                    
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if len(text) < 3 or len(text) > 200:
                            continue
                        
                        # Quick font info extraction
                        font_info = FontInfo(
                            size=span["size"],
                            name=span["font"],
                            is_bold="Bold" in span["font"] or span["flags"] & 2**4,
                            bbox=span["bbox"]
                        )
                        
                        # Normalized Y position
                        position_y = span["bbox"][1] / page_height
                        
                        elements.append(TextElement(
                            text=text,
                            font=font_info,
                            page_number=page_num + 1,
                            position_y=position_y
                        ))
        
        doc.close()
        return elements
    
    def _extract_title_fast(self, elements: List[TextElement], max_size: float) -> Optional[str]:
        """Quick title extraction"""
        # Look for largest text on first page
        first_page = [e for e in elements if e.page_number == 1]
        if not first_page:
            return None
        
        # Find elements with largest font in upper part of page
        title_candidates = [
            e for e in first_page 
            if e.font.size >= max_size * 0.85 and 
               e.position_y < 0.5 and
               len(e.text.strip()) > 3 and
               not e.text.strip().isdigit() and
               not e.text.strip() in ['----------------', '____']
        ]
        
        if not title_candidates:
            return None
        
        # Sort by position
        title_candidates.sort(key=lambda x: x.position_y)
        
        # Try to combine title parts that are close together
        combined_parts = []
        last_y = None
        
        for candidate in title_candidates:
            if last_y is not None and abs(candidate.position_y - last_y) < 0.05:
                # Combine with previous part
                if combined_parts:
                    combined_parts[-1] += " " + candidate.text.strip()
            else:
                # Start a new title part
                combined_parts.append(candidate.text.strip())
            last_y = candidate.position_y
        
        # Return the longest combined title part
        if combined_parts:
            longest_title = max(combined_parts, key=len)
            if len(longest_title) > 5:
                return longest_title
        
        return None
    
    def _find_headings_fast(self, elements: List[TextElement], avg_size: float, title: str) -> List[Heading]:
        """Fast heading detection using size and patterns"""
        headings = []
        
        for element in elements:
            # Skip if it's the title
            if title and element.text.strip().lower() == title.strip().lower():
                continue
            
            # Skip obvious non-headings
            text_strip = element.text.strip()
            if (len(text_strip) < 3 or 
                text_strip.endswith('.') or
                text_strip.isdigit() or
                text_strip in ['----------------', '____', '....']):
                continue
            
            # Pattern-based classification first
            level = self._classify_level_fast(element.text, element.font.size, avg_size)
            
            # Size-based filtering for non-pattern matches
            if level == 0:
                if element.font.size > avg_size * 1.3 or element.font.is_bold:
                    # Classify by size
                    size_ratio = element.font.size / avg_size
                    if size_ratio > 1.5:
                        level = 1
                    elif size_ratio > 1.2:
                        level = 2
                    elif element.font.is_bold:
                        level = 3
            
            if level > 0:
                headings.append(Heading(
                    text=element.text,
                    level=level,
                    page=element.page_number
                ))
        
        # Sort by page and remove duplicates
        headings.sort(key=lambda x: (x.page, x.text))
        seen = set()
        unique_headings = []
        for h in headings:
            key = (h.text.lower().strip(), h.page)
            if key not in seen:
                seen.add(key)
                unique_headings.append(h)
        
        return unique_headings
    
    def _classify_level_fast(self, text: str, font_size: float, avg_size: float) -> int:
        """Fast level classification"""
        text_strip = text.strip()
        
        # H1 patterns
        for pattern in self.h1_patterns:
            if re.match(pattern, text_strip):
                return 1
        
        # H2 patterns  
        for pattern in self.h2_patterns:
            if re.match(pattern, text_strip):
                return 2
        
        # Size-based classification
        size_ratio = font_size / avg_size
        if size_ratio > 1.5:
            return 1
        elif size_ratio > 1.2:
            return 2
        elif size_ratio > 1.1:
            return 3
        
        return 0  # Not a heading

def process_pdfs():
    """
    Main processing function that processes all PDFs from /app/input
    and outputs JSON files to /app/output
    """
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    
    print(f"Processing PDFs from: {input_dir}")
    print(f"Output directory: {output_dir}")
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize extractor
    extractor = FastPDFHeadingExtractor()
    
    # Get all PDF files
    pdf_files = list(input_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in input directory")
        return
    
    print(f"Found {len(pdf_files)} PDF files to process")
    
    total_start_time = time.time()
    
    for pdf_file in pdf_files:
        print(f"Processing: {pdf_file.name}")
        
        start_time = time.time()
        
        # Extract headings
        result = extractor.extract_headings(str(pdf_file))
        
        # Generate output filename
        output_file = output_dir / f"{pdf_file.stem}.json"
        
        # Save JSON output
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        print(f"  ✓ Completed in {processing_time:.3f}s")
        print(f"  ✓ Found {len(result['outline'])} headings")
        print(f"  ✓ Output: {output_file.name}")
    
    total_time = time.time() - total_start_time
    print(f"\n=== Processing Complete ===")
    print(f"Total time: {total_time:.3f} seconds")
    print(f"Average per file: {total_time/len(pdf_files):.3f} seconds")
    print(f"Processed {len(pdf_files)} files successfully")

if __name__ == "__main__":
    process_pdfs()
