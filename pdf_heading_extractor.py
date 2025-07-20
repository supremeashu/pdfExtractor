"""
PDF Heading Extractor - Core Module

A robust PDF heading extraction system that combines font analysis, 
text pattern recognition, and machine learning to identify document structure.
"""

import fitz  # PyMuPDF
import pdfplumber
import re
import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import logging
import numpy as np
from collections import Counter, defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class FontInfo:
    """Font information extracted from PDF text"""
    size: float
    name: str
    weight: str  # bold, normal, etc.
    italic: bool
    bbox: Tuple[float, float, float, float]  # x0, y0, x1, y1
    
    @property
    def is_bold(self) -> bool:
        return 'bold' in self.weight.lower() or 'Bold' in self.name
    
    @property
    def is_italic(self) -> bool:
        return self.italic or 'italic' in self.name.lower()


@dataclass
class TextElement:
    """Individual text element with position and formatting"""
    text: str
    font: FontInfo
    page_number: int
    position_y: float  # Normalized Y position (0-1)
    line_length: int
    whitespace_above: float = 0.0
    whitespace_below: float = 0.0
    
    @property
    def is_potential_heading(self) -> bool:
        """Basic heuristics to identify potential headings"""
        return (
            len(self.text.strip()) > 3 and
            len(self.text.strip()) < 200 and
            not self.text.endswith('.') and
            (self.font.is_bold or self.font.size > 12)
        )


@dataclass
class Heading:
    """Extracted heading with metadata"""
    text: str
    level: int  # 1, 2, 3 for H1, H2, H3
    page: int
    font_size: float
    font_weight: str
    confidence: float
    position_y: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'text': self.text.strip(),
            'level': self.level,
            'page': self.page,
            'font_size': round(self.font_size, 1),
            'font_weight': self.font_weight,
            'confidence': round(self.confidence, 2)
        }


@dataclass
class ExtractionResult:
    """Complete extraction result"""
    document_info: Dict[str, Any]
    title: Optional[str]
    headings: List[Heading]
    extraction_stats: Dict[str, int]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'document_info': self.document_info,
            'title': self.title,
            'headings': [h.to_dict() for h in self.headings],
            'extraction_stats': self.extraction_stats
        }


class PDFHeadingExtractor:
    """Main PDF heading extraction class"""
    
    def __init__(self, 
                 max_pages: int = 50,
                 min_font_size: float = 10.0,
                 heading_confidence_threshold: float = 0.6):
        self.max_pages = max_pages
        self.min_font_size = min_font_size
        self.heading_confidence_threshold = heading_confidence_threshold
        
        # Common heading patterns
        self.heading_patterns = [
            r'^\d+\.?\s+[A-Z]',  # "1. Introduction" or "1 Introduction"
            r'^[A-Z][A-Z\s]{2,}$',  # "INTRODUCTION", "CHAPTER ONE"
            r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*$',  # "Introduction", "Literature Review"
            r'^Chapter\s+\d+',  # "Chapter 1"
            r'^Section\s+\d+',  # "Section 1"
            r'^Abstract$|^Introduction$|^Conclusion$|^References$',  # Common academic sections
        ]
        
    def extract_headings(self, pdf_path: str) -> ExtractionResult:
        """Main extraction method"""
        logger.info(f"Extracting headings from: {pdf_path}")
        
        try:
            # Extract text elements with font information
            text_elements = self._extract_text_elements(pdf_path)
            
            if not text_elements:
                logger.warning("No text elements extracted from PDF")
                return self._empty_result(pdf_path)
            
            # Analyze font statistics for the document
            font_stats = self._analyze_font_statistics(text_elements)
            
            # Identify potential headings
            potential_headings = self._identify_potential_headings(text_elements, font_stats)
            
            # Classify heading levels
            classified_headings = self._classify_heading_levels(potential_headings, font_stats)
            
            # Extract document title
            title = self._extract_title(text_elements, font_stats)
            
            # Create result
            result = ExtractionResult(
                document_info=self._get_document_info(pdf_path, len(text_elements)),
                title=title,
                headings=classified_headings,
                extraction_stats=self._calculate_stats(classified_headings)
            )
            
            logger.info(f"Extracted {len(classified_headings)} headings")
            return result
            
        except Exception as e:
            logger.error(f"Error extracting headings: {str(e)}")
            return self._empty_result(pdf_path)
    
    def _extract_text_elements(self, pdf_path: str) -> List[TextElement]:
        """Extract text elements with font and position information"""
        text_elements = []
        
        try:
            doc = fitz.open(pdf_path)
            total_pages = min(len(doc), self.max_pages)
            
            for page_num in range(total_pages):
                page = doc[page_num]
                blocks = page.get_text("dict")["blocks"]
                
                page_elements = []
                for block in blocks:
                    if "lines" not in block:
                        continue
                        
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()
                            if len(text) < 3:  # Skip very short text
                                continue
                                
                            font_info = FontInfo(
                                size=span["size"],
                                name=span["font"],
                                weight="bold" if "bold" in span["font"].lower() else "normal",
                                italic="italic" in span["font"].lower(),
                                bbox=span["bbox"]
                            )
                            
                            element = TextElement(
                                text=text,
                                font=font_info,
                                page_number=page_num + 1,
                                position_y=span["bbox"][1] / page.rect.height,
                                line_length=len(text)
                            )
                            
                            page_elements.append(element)
                
                # Calculate whitespace for page elements
                page_elements.sort(key=lambda x: x.font.bbox[1])  # Sort by Y position
                for i, element in enumerate(page_elements):
                    if i > 0:
                        element.whitespace_above = element.font.bbox[1] - page_elements[i-1].font.bbox[3]
                    if i < len(page_elements) - 1:
                        element.whitespace_below = page_elements[i+1].font.bbox[1] - element.font.bbox[3]
                
                text_elements.extend(page_elements)
            
            doc.close()
            
        except Exception as e:
            logger.error(f"Error extracting text elements: {str(e)}")
            # Fallback to pdfplumber
            text_elements.extend(self._extract_with_pdfplumber(pdf_path))
        
        return text_elements
    
    def _extract_with_pdfplumber(self, pdf_path: str) -> List[TextElement]:
        """Fallback extraction using pdfplumber"""
        text_elements = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages[:self.max_pages]):
                    if page.chars:
                        # Group characters into text elements
                        text_elements.extend(self._group_chars_to_elements(page.chars, page_num + 1))
        except Exception as e:
            logger.error(f"Pdfplumber extraction failed: {str(e)}")
        
        return text_elements
    
    def _group_chars_to_elements(self, chars: List[Dict], page_number: int) -> List[TextElement]:
        """Group character data into text elements"""
        elements = []
        
        # Group characters by similar Y position and font
        lines = defaultdict(list)
        for char in chars:
            if char.get('text', '').strip():
                line_key = (round(char['top'], 1), char.get('fontname', ''), char.get('size', 12))
                lines[line_key].append(char)
        
        for (y_pos, font_name, font_size), line_chars in lines.items():
            if len(line_chars) < 3:  # Skip very short lines
                continue
                
            # Combine characters into text
            text = ''.join(char['text'] for char in line_chars)
            
            font_info = FontInfo(
                size=font_size,
                name=font_name,
                weight="bold" if "bold" in font_name.lower() else "normal",
                italic="italic" in font_name.lower(),
                bbox=(
                    min(char['x0'] for char in line_chars),
                    y_pos,
                    max(char['x1'] for char in line_chars),
                    y_pos + font_size
                )
            )
            
            element = TextElement(
                text=text.strip(),
                font=font_info,
                page_number=page_number,
                position_y=y_pos / 800,  # Approximate normalization
                line_length=len(text.strip())
            )
            
            elements.append(element)
        
        return elements
    
    def _analyze_font_statistics(self, text_elements: List[TextElement]) -> Dict[str, Any]:
        """Analyze font usage statistics in the document"""
        font_sizes = [elem.font.size for elem in text_elements]
        font_names = [elem.font.name for elem in text_elements]
        
        stats = {
            'font_sizes': font_sizes,
            'most_common_size': Counter(font_sizes).most_common(1)[0][0] if font_sizes else 12,
            'largest_size': max(font_sizes) if font_sizes else 12,
            'size_percentiles': {
                '75th': np.percentile(font_sizes, 75) if font_sizes else 12,
                '90th': np.percentile(font_sizes, 90) if font_sizes else 12,
                '95th': np.percentile(font_sizes, 95) if font_sizes else 12
            },
            'common_fonts': Counter(font_names).most_common(5),
            'total_elements': len(text_elements)
        }
        
        return stats
    
    def _identify_potential_headings(self, text_elements: List[TextElement], 
                                   font_stats: Dict[str, Any]) -> List[TextElement]:
        """Identify text elements that could be headings"""
        potential_headings = []
        body_text_size = font_stats['most_common_size']
        
        for element in text_elements:
            if not element.is_potential_heading:
                continue
            
            # Font size criteria
            size_score = element.font.size / body_text_size if body_text_size > 0 else 1
            
            # Pattern matching
            pattern_score = self._calculate_pattern_score(element.text)
            
            # Position and formatting criteria
            format_score = self._calculate_format_score(element)
            
            # Combined confidence score
            confidence = (size_score * 0.4 + pattern_score * 0.4 + format_score * 0.2)
            
            if confidence >= self.heading_confidence_threshold:
                potential_headings.append(element)
        
        return potential_headings
    
    def _calculate_pattern_score(self, text: str) -> float:
        """Calculate score based on heading text patterns"""
        score = 0.0
        
        for pattern in self.heading_patterns:
            if re.match(pattern, text.strip(), re.IGNORECASE):
                score = max(score, 0.9)
        
        # Additional scoring criteria
        if text.isupper() and len(text.split()) <= 5:
            score = max(score, 0.7)
        
        if re.match(r'^[A-Z][a-z]', text) and not text.endswith('.'):
            score = max(score, 0.5)
        
        return min(score, 1.0)
    
    def _calculate_format_score(self, element: TextElement) -> float:
        """Calculate score based on formatting characteristics"""
        score = 0.0
        
        # Bold text
        if element.font.is_bold:
            score += 0.4
        
        # Reasonable length for headings
        if 5 <= element.line_length <= 100:
            score += 0.3
        
        # Whitespace above/below
        if element.whitespace_above > 10:
            score += 0.2
        if element.whitespace_below > 5:
            score += 0.1
        
        return min(score, 1.0)
    
    def _classify_heading_levels(self, potential_headings: List[TextElement], 
                                font_stats: Dict[str, Any]) -> List[Heading]:
        """Classify headings into H1, H2, H3 levels"""
        if not potential_headings:
            return []
        
        # Sort by font size (descending) to determine hierarchy
        sorted_headings = sorted(potential_headings, 
                               key=lambda x: x.font.size, reverse=True)
        
        # Determine size thresholds for levels
        sizes = [h.font.size for h in sorted_headings]
        unique_sizes = sorted(set(sizes), reverse=True)
        
        level_thresholds = {}
        if len(unique_sizes) >= 3:
            level_thresholds[1] = unique_sizes[0]  # Largest for H1
            level_thresholds[2] = unique_sizes[1]  # Second largest for H2
            level_thresholds[3] = unique_sizes[2]  # Third largest for H3
        elif len(unique_sizes) == 2:
            level_thresholds[1] = unique_sizes[0]
            level_thresholds[2] = unique_sizes[1]
            level_thresholds[3] = unique_sizes[1]
        else:
            level_thresholds[1] = unique_sizes[0] if unique_sizes else 12
            level_thresholds[2] = unique_sizes[0] if unique_sizes else 12
            level_thresholds[3] = unique_sizes[0] if unique_sizes else 12
        
        classified_headings = []
        
        for element in potential_headings:
            # Determine level based on font size
            level = 3  # Default to H3
            if element.font.size >= level_thresholds[1]:
                level = 1
            elif element.font.size >= level_thresholds[2]:
                level = 2
            
            # Adjust level based on patterns
            if re.match(r'^(Abstract|Introduction|Conclusion|References)$', 
                       element.text.strip(), re.IGNORECASE):
                level = 1
            elif re.match(r'^\d+\.?\s+', element.text.strip()):
                level = min(level, 2)
            
            # Calculate final confidence
            base_confidence = self.heading_confidence_threshold
            pattern_boost = self._calculate_pattern_score(element.text) * 0.3
            format_boost = self._calculate_format_score(element) * 0.2
            
            confidence = min(base_confidence + pattern_boost + format_boost, 1.0)
            
            heading = Heading(
                text=element.text,
                level=level,
                page=element.page_number,
                font_size=element.font.size,
                font_weight="bold" if element.font.is_bold else "normal",
                confidence=confidence,
                position_y=element.position_y
            )
            
            classified_headings.append(heading)
        
        # Sort by page and position
        classified_headings.sort(key=lambda x: (x.page, x.position_y))
        
        return classified_headings
    
    def _extract_title(self, text_elements: List[TextElement], 
                      font_stats: Dict[str, Any]) -> Optional[str]:
        """Extract document title (usually the largest text on first page)"""
        if not text_elements:
            return None
        
        # Look for title on first page
        first_page_elements = [elem for elem in text_elements if elem.page_number == 1]
        
        if not first_page_elements:
            return None
        
        # Find the largest font size on first page
        largest_size = max(elem.font.size for elem in first_page_elements)
        
        # Find elements with largest font size in upper portion of first page
        title_candidates = [
            elem for elem in first_page_elements
            if elem.font.size == largest_size and 
               elem.position_y < 0.3 and  # Upper 30% of page
               len(elem.text.strip()) > 5 and
               len(elem.text.strip()) < 200
        ]
        
        if title_candidates:
            # Sort by position and take the first one
            title_candidates.sort(key=lambda x: x.position_y)
            return title_candidates[0].text.strip()
        
        return None
    
    def _get_document_info(self, pdf_path: str, total_elements: int) -> Dict[str, Any]:
        """Get document metadata"""
        return {
            'filename': pdf_path.split('/')[-1].split('\\')[-1],
            'total_pages': min(self._get_page_count(pdf_path), self.max_pages),
            'extraction_timestamp': datetime.now().isoformat(),
            'total_text_elements': total_elements
        }
    
    def _get_page_count(self, pdf_path: str) -> int:
        """Get total page count of PDF"""
        try:
            doc = fitz.open(pdf_path)
            count = len(doc)
            doc.close()
            return count
        except:
            return 0
    
    def _calculate_stats(self, headings: List[Heading]) -> Dict[str, int]:
        """Calculate extraction statistics"""
        level_counts = Counter(h.level for h in headings)
        return {
            'total_headings': len(headings),
            'h1_count': level_counts.get(1, 0),
            'h2_count': level_counts.get(2, 0),
            'h3_count': level_counts.get(3, 0)
        }
    
    def _empty_result(self, pdf_path: str) -> ExtractionResult:
        """Return empty result for failed extractions"""
        return ExtractionResult(
            document_info=self._get_document_info(pdf_path, 0),
            title=None,
            headings=[],
            extraction_stats={'total_headings': 0, 'h1_count': 0, 'h2_count': 0, 'h3_count': 0}
        )
    
    def save_json(self, result: ExtractionResult, output_path: str) -> None:
        """Save extraction result to JSON file"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)
            logger.info(f"Results saved to: {output_path}")
        except Exception as e:
            logger.error(f"Error saving JSON: {str(e)}")


if __name__ == "__main__":
    # Example usage
    extractor = PDFHeadingExtractor()
    result = extractor.extract_headings("example.pdf")
    extractor.save_json(result, "headings.json")
