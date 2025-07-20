"""
Enhanced PDF utilities for the heading extractor
"""

import fitz
import pdfplumber
import re
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)


@dataclass
class PageLayout:
    """Information about page layout and structure"""
    page_number: int
    width: float
    height: float
    margins: Dict[str, float]  # top, bottom, left, right
    columns: int
    text_regions: List[Tuple[float, float, float, float]]  # bbox regions


class PDFAnalyzer:
    """Advanced PDF analysis utilities"""
    
    def __init__(self):
        self.common_headers = ['header', 'page', 'chapter', 'section']
        self.common_footers = ['footer', 'page', 'copyright', '©']
    
    def analyze_document_structure(self, pdf_path: str, max_pages: int = 10) -> Dict[str, Any]:
        """Analyze overall document structure and layout"""
        try:
            doc = fitz.open(pdf_path)
            total_pages = min(len(doc), max_pages)
            
            analysis = {
                'total_pages': len(doc),
                'analyzed_pages': total_pages,
                'page_layouts': [],
                'font_analysis': {},
                'text_statistics': {},
                'document_type': 'unknown'
            }
            
            all_fonts = []
            all_font_sizes = []
            
            for page_num in range(total_pages):
                page = doc[page_num]
                
                # Analyze page layout
                layout = self._analyze_page_layout(page, page_num + 1)
                analysis['page_layouts'].append(layout)
                
                # Collect font information
                blocks = page.get_text("dict")["blocks"]
                for block in blocks:
                    if "lines" not in block:
                        continue
                    for line in block["lines"]:
                        for span in line["spans"]:
                            all_fonts.append(span["font"])
                            all_font_sizes.append(span["size"])
            
            # Font analysis
            analysis['font_analysis'] = self._analyze_fonts(all_fonts, all_font_sizes)
            
            # Document type detection
            analysis['document_type'] = self._detect_document_type(analysis)
            
            doc.close()
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing document structure: {str(e)}")
            return {}
    
    def _analyze_page_layout(self, page, page_number: int) -> PageLayout:
        """Analyze the layout of a single page"""
        rect = page.rect
        
        # Basic layout detection
        text_blocks = page.get_text("dict")["blocks"]
        text_regions = []
        
        for block in text_blocks:
            if "lines" in block:
                bbox = block["bbox"]
                text_regions.append(bbox)
        
        # Estimate margins (simplified)
        margins = {
            'top': 50,  # Default estimates
            'bottom': 50,
            'left': 50,
            'right': 50
        }
        
        # Estimate column count (simplified)
        columns = 1
        if text_regions:
            # Group text by X position to detect columns
            x_positions = [region[0] for region in text_regions]
            unique_x = sorted(set(x_positions))
            if len(unique_x) > 1:
                # Simple heuristic: if there are distinct X positions, might be multi-column
                min_gap = min(unique_x[i+1] - unique_x[i] for i in range(len(unique_x)-1))
                if min_gap > 100:  # Significant gap suggests columns
                    columns = 2
        
        return PageLayout(
            page_number=page_number,
            width=rect.width,
            height=rect.height,
            margins=margins,
            columns=columns,
            text_regions=text_regions
        )
    
    def _analyze_fonts(self, fonts: List[str], sizes: List[float]) -> Dict[str, Any]:
        """Analyze font usage patterns"""
        from collections import Counter
        import numpy as np
        
        font_counts = Counter(fonts)
        size_counts = Counter(sizes)
        
        analysis = {
            'unique_fonts': len(set(fonts)),
            'most_common_font': font_counts.most_common(1)[0] if fonts else None,
            'font_distribution': dict(font_counts.most_common(10)),
            'size_statistics': {
                'min': min(sizes) if sizes else 0,
                'max': max(sizes) if sizes else 0,
                'mean': np.mean(sizes) if sizes else 0,
                'median': np.median(sizes) if sizes else 0,
                'std': np.std(sizes) if sizes else 0
            },
            'size_distribution': dict(size_counts.most_common(10))
        }
        
        return analysis
    
    def _detect_document_type(self, analysis: Dict[str, Any]) -> str:
        """Detect the type of document based on structure analysis"""
        # This is a simplified heuristic - could be expanded with ML
        
        total_pages = analysis.get('total_pages', 0)
        font_analysis = analysis.get('font_analysis', {})
        
        # Academic paper indicators
        if 1 <= total_pages <= 20:
            if font_analysis.get('unique_fonts', 0) <= 3:
                return 'academic_paper'
        
        # Book/report indicators
        elif total_pages > 50:
            return 'book_or_report'
        
        # Article indicators
        elif 5 <= total_pages <= 30:
            return 'article'
        
        return 'document'
    
    def extract_text_with_coordinates(self, pdf_path: str, page_num: int) -> List[Dict[str, Any]]:
        """Extract text with precise coordinate information"""
        text_elements = []
        
        try:
            doc = fitz.open(pdf_path)
            if page_num <= len(doc):
                page = doc[page_num - 1]
                blocks = page.get_text("dict")["blocks"]
                
                for block_idx, block in enumerate(blocks):
                    if "lines" not in block:
                        continue
                    
                    for line_idx, line in enumerate(block["lines"]):
                        for span_idx, span in enumerate(line["spans"]):
                            text_elements.append({
                                'text': span["text"],
                                'bbox': span["bbox"],
                                'font': span["font"],
                                'size': span["size"],
                                'flags': span["flags"],
                                'block_idx': block_idx,
                                'line_idx': line_idx,
                                'span_idx': span_idx,
                                'page': page_num
                            })
            
            doc.close()
            
        except Exception as e:
            logger.error(f"Error extracting text with coordinates: {str(e)}")
        
        return text_elements
    
    def detect_reading_order(self, text_elements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect the reading order of text elements"""
        if not text_elements:
            return []
        
        # Group elements by approximate Y position (lines)
        lines = defaultdict(list)
        for element in text_elements:
            y_pos = round(element['bbox'][1], -1)  # Round to nearest 10
            lines[y_pos].append(element)
        
        # Sort lines by Y position (top to bottom)
        sorted_lines = []
        for y_pos in sorted(lines.keys()):
            # Sort elements in each line by X position (left to right)
            line_elements = sorted(lines[y_pos], key=lambda x: x['bbox'][0])
            sorted_lines.extend(line_elements)
        
        return sorted_lines
    
    def identify_headers_footers(self, pdf_path: str, sample_pages: int = 5) -> Dict[str, Any]:
        """Identify consistent headers and footers across pages"""
        headers = defaultdict(int)
        footers = defaultdict(int)
        
        try:
            doc = fitz.open(pdf_path)
            total_pages = min(len(doc), sample_pages)
            
            for page_num in range(total_pages):
                page = doc[page_num]
                rect = page.rect
                
                # Define header and footer regions (top/bottom 10% of page)
                header_region = (0, 0, rect.width, rect.height * 0.1)
                footer_region = (0, rect.height * 0.9, rect.width, rect.height)
                
                blocks = page.get_text("dict")["blocks"]
                
                for block in blocks:
                    if "lines" not in block:
                        continue
                    
                    bbox = block["bbox"]
                    
                    # Check if block is in header region
                    if (bbox[1] <= header_region[3] and bbox[3] >= header_region[1]):
                        text = " ".join(
                            span["text"] for line in block["lines"] 
                            for span in line["spans"]
                        ).strip()
                        if text and len(text) > 3:
                            headers[text] += 1
                    
                    # Check if block is in footer region
                    elif (bbox[1] <= footer_region[3] and bbox[3] >= footer_region[1]):
                        text = " ".join(
                            span["text"] for line in block["lines"] 
                            for span in line["spans"]
                        ).strip()
                        if text and len(text) > 3:
                            footers[text] += 1
            
            doc.close()
            
            # Find most common headers/footers
            common_headers = [text for text, count in headers.items() 
                           if count >= total_pages * 0.5]
            common_footers = [text for text, count in footers.items() 
                           if count >= total_pages * 0.5]
            
            return {
                'headers': common_headers,
                'footers': common_footers,
                'header_frequency': dict(headers),
                'footer_frequency': dict(footers)
            }
            
        except Exception as e:
            logger.error(f"Error identifying headers/footers: {str(e)}")
            return {'headers': [], 'footers': []}


def clean_text(text: str) -> str:
    """Clean and normalize extracted text"""
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove control characters
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    
    # Normalize quotes
    text = re.sub(r'["""]', '"', text)
    text = re.sub(r"[''']", "'", text)
    
    # Remove soft hyphens
    text = text.replace('\u00ad', '')
    
    return text.strip()


def is_likely_header_footer(text: str, common_headers: List[str], common_footers: List[str]) -> bool:
    """Check if text is likely a header or footer"""
    text_lower = text.lower()
    
    # Check against common patterns
    header_patterns = ['header', 'page', 'chapter']
    footer_patterns = ['footer', 'page', 'copyright', '©']
    
    for pattern in header_patterns + footer_patterns:
        if pattern in text_lower:
            return True
    
    # Check against document-specific headers/footers
    for header in common_headers:
        if text.strip() == header.strip():
            return True
    
    for footer in common_footers:
        if text.strip() == footer.strip():
            return True
    
    return False


if __name__ == "__main__":
    # Example usage
    analyzer = PDFAnalyzer()
    
    # Analyze a sample PDF
    analysis = analyzer.analyze_document_structure("sample.pdf")
    print(f"Document analysis: {analysis}")
