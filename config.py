# Configuration file for PDF Heading Extractor

# Default extraction settings
DEFAULT_MAX_PAGES = 50
DEFAULT_MIN_FONT_SIZE = 10.0
DEFAULT_CONFIDENCE_THRESHOLD = 0.6

# Font analysis settings
FONT_SIZE_ANALYSIS = {
    'body_text_percentile': 50,  # Most common font size
    'heading_size_multiplier': 1.2,  # Minimum size multiplier for headings
    'title_size_percentile': 95  # Percentile for title font size
}

# Heading detection patterns
HEADING_PATTERNS = [
    r'^\d+\.?\s+[A-Z]',  # "1. Introduction" or "1 Introduction"
    r'^[A-Z][A-Z\s]{2,}$',  # "INTRODUCTION", "CHAPTER ONE"
    r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*$',  # "Introduction", "Literature Review"
    r'^Chapter\s+\d+',  # "Chapter 1"
    r'^Section\s+\d+',  # "Section 1"
    r'^Abstract$|^Introduction$|^Conclusion$|^References$',  # Common academic sections
    r'^Appendix\s+[A-Z]',  # "Appendix A"
    r'^Figure\s+\d+',  # "Figure 1" (might be caption, handle carefully)
    r'^Table\s+\d+',  # "Table 1" (might be caption, handle carefully)
]

# Academic section patterns (high confidence)
ACADEMIC_SECTIONS = [
    'abstract', 'introduction', 'background', 'literature review',
    'methodology', 'methods', 'approach', 'results', 'findings',
    'discussion', 'conclusion', 'references', 'bibliography',
    'acknowledgments', 'appendix'
]

# Formatting criteria weights
SCORING_WEIGHTS = {
    'font_size': 0.4,
    'pattern_match': 0.3,
    'formatting': 0.2,
    'position': 0.1
}

# Text preprocessing settings
TEXT_PROCESSING = {
    'min_heading_length': 3,
    'max_heading_length': 200,
    'min_line_spacing': 5,  # Minimum spacing above heading
    'ignore_patterns': [
        r'^\d+$',  # Just numbers
        r'^[^\w\s]+$',  # Just punctuation
        r'^page\s+\d+$',  # Page numbers
        r'^\w{1,2}$'  # Single/double letters
    ]
}

# Output formatting
OUTPUT_FORMAT = {
    'indent_spaces': 2,
    'ensure_ascii': False,
    'include_confidence': True,
    'include_font_details': True,
    'max_text_preview': 80  # Maximum characters to show in previews
}
