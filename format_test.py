"""
Simple test to verify the new JSON format without complex dependencies
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mock the necessary classes to test the format
from dataclasses import dataclass
from typing import List
import json

@dataclass
class Heading:
    text: str
    level: int
    page: int
    font_name: str = ""
    font_size: float = 12.0
    bbox: tuple = ()
    confidence: float = 0.8
    
    def to_dict(self) -> dict:
        """Return simplified format for user output"""
        level_str = f"H{self.level}"
        return {
            "text": self.text,
            "level": level_str,
            "page": self.page
        }
    
    def to_detailed_dict(self) -> dict:
        """Return detailed format with all metadata"""
        return {
            "text": self.text,
            "level": self.level,
            "page": self.page,
            "font_name": self.font_name,
            "font_size": self.font_size,
            "bbox": list(self.bbox) if self.bbox else [],
            "confidence": self.confidence
        }

@dataclass
class ExtractionResult:
    title: str
    headings: List[Heading]
    metadata: dict
    
    def to_dict(self) -> dict:
        """Return simplified format for user output"""
        return {
            "title": self.title,
            "outline": [heading.to_dict() for heading in self.headings]
        }
    
    def to_detailed_dict(self) -> dict:
        """Return detailed format with all metadata"""
        return {
            "title": self.title,
            "headings": [heading.to_detailed_dict() for heading in self.headings],
            "metadata": self.metadata
        }

# Test the format
def test_format():
    """Test both output formats"""
    
    # Create sample data
    headings = [
        Heading("Introduction", 1, 1, "Arial-Bold", 16.0, (100, 200, 300, 220), 0.95),
        Heading("Background", 2, 2, "Arial", 14.0, (100, 250, 280, 270), 0.90),
        Heading("Methodology", 1, 3, "Arial-Bold", 16.0, (100, 300, 350, 320), 0.93),
        Heading("Data Analysis", 2, 4, "Arial", 14.0, (100, 350, 320, 370), 0.88),
        Heading("Results", 1, 5, "Arial-Bold", 16.0, (100, 400, 250, 420), 0.96)
    ]
    
    metadata = {
        "extraction_date": "2024-01-15T10:30:00",
        "total_pages": 10,
        "processing_time": 2.5,
        "confidence_threshold": 0.8
    }
    
    result = ExtractionResult("Sample Document", headings, metadata)
    
    # Test simplified format
    print("=== SIMPLIFIED FORMAT (User-Requested) ===")
    simple_output = result.to_dict()
    print(json.dumps(simple_output, indent=2))
    
    print("\n=== DETAILED FORMAT (Full Metadata) ===")
    detailed_output = result.to_detailed_dict()
    print(json.dumps(detailed_output, indent=2))
    
    # Save both formats
    with open("test_simple_format.json", "w", encoding='utf-8') as f:
        json.dump(simple_output, f, indent=2, ensure_ascii=False)
    
    with open("test_detailed_format.json", "w", encoding='utf-8') as f:
        json.dump(detailed_output, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Files saved:")
    print(f"  - test_simple_format.json")
    print(f"  - test_detailed_format.json")

if __name__ == "__main__":
    test_format()
