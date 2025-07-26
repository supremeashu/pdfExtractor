# Challenge 1b: Multi-Collection PDF Analysis

> **Author**: supremeashu  
> **License**: MIT

## Overview

Advanced PDF analysis solution that processes multiple document collections and extracts relevant content based on specific personas and use cases.

This solution implements persona-based content analysis across three distinct collections, each tailored to different user roles and tasks. The system intelligently ranks extracted sections by importance and provides refined analysis based on the specific job to be done.

## Project Structure

```
Challenge_1b/
├── Collection 1/                    # Travel Planning
│   ├── PDFs/                       # South of France guides
│   ├── challenge1b_input.json      # Input configuration
│   └── challenge1b_output.json     # Analysis results
├── Collection 2/                    # Adobe Acrobat Learning
│   ├── PDFs/                       # Acrobat tutorials
│   ├── challenge1b_input.json      # Input configuration
│   └── challenge1b_output.json     # Analysis results
├── Collection 3/                    # Recipe Collection
│   ├── PDFs/                       # Cooking guides
│   ├── challenge1b_input.json      # Input configuration
│   └── challenge1b_output.json     # Analysis results
├── process_challenge1b.py          # Main processing script
├── requirements.txt                # Dependencies
└── README.md                       # This file
```

## Collections

### Collection 1: Travel Planning

- **Challenge ID**: round_1b_002
- **Persona**: Travel Planner
- **Task**: Plan a 4-day trip for 10 college friends to South of France
- **Documents**: 5 travel guides (sample)

### Collection 2: Adobe Acrobat Learning

- **Challenge ID**: round_1b_003
- **Persona**: HR Professional
- **Task**: Create and manage fillable forms for onboarding and compliance
- **Documents**: 5 Acrobat guides (sample)

### Collection 3: Recipe Collection

- **Challenge ID**: round_1b_001
- **Persona**: Food Contractor
- **Task**: Prepare vegetarian buffet-style dinner menu for corporate gathering
- **Documents**: 5 cooking guides (sample)

## Input/Output Format

### Input JSON Structure

```json
{
	"challenge_info": {
		"challenge_id": "round_1b_XXX",
		"test_case_name": "specific_test_case"
	},
	"documents": [{ "filename": "doc.pdf", "title": "Title" }],
	"persona": { "role": "User Persona" },
	"job_to_be_done": { "task": "Use case description" }
}
```

### Output JSON Structure

```json
{
	"metadata": {
		"input_documents": ["list"],
		"persona": "User Persona",
		"job_to_be_done": "Task description"
	},
	"extracted_sections": [
		{
			"document": "source.pdf",
			"section_title": "Title",
			"importance_rank": 1,
			"page_number": 1
		}
	],
	"subsection_analysis": [
		{
			"document": "source.pdf",
			"refined_text": "Content",
			"page_number": 1
		}
	]
}
```

## Key Features

- **Persona-based Content Analysis**: Tailors extraction based on user role
- **Importance Ranking**: Sections ranked by relevance to the persona's task
- **Multi-collection Processing**: Handles different document types and use cases
- **Structured JSON Output**: Consistent output format with metadata
- **Task-focused Refinement**: Text analysis refined for specific job requirements

## Implementation Details

### Persona Analysis Engine

The system uses keyword-based scoring to identify relevant content:

- **Travel Planner**: Keywords like 'itinerary', 'accommodation', 'attraction', 'budget'
- **HR Professional**: Keywords like 'form', 'fillable', 'onboarding', 'compliance'
- **Food Contractor**: Keywords like 'recipe', 'vegetarian', 'buffet', 'catering'

### Section Extraction

1. **Text Structure Analysis**: Identifies headings and sections based on font properties
2. **Relevance Scoring**: Scores sections based on persona-specific keywords
3. **Importance Ranking**: Ranks sections by relevance to the specific task
4. **Content Refinement**: Extracts and refines key information for each persona

### Performance Optimization

- **Efficient PDF Processing**: Uses PyMuPDF for fast text extraction
- **Smart Content Filtering**: Processes only relevant sections
- **Memory Management**: Handles large document collections efficiently

## Usage

### Running the Processor

```bash
cd Challenge_1b
python process_challenge1b.py
```

### Installing Dependencies

```bash
pip install -r requirements.txt
```

## Time Constraints Compliance

The solution is designed to meet hackathon time constraints:

- **Fast Processing**: Optimized for quick analysis across multiple collections
- **Scalable Architecture**: Can handle additional collections without major changes
- **Efficient Algorithms**: Smart keyword-based filtering reduces processing time
- **Minimal Dependencies**: Uses only essential libraries (PyMuPDF)

## Sample Output

Each collection generates a JSON output with:

- **Metadata**: Collection information and persona details
- **Extracted Sections**: Top-ranked sections relevant to the persona
- **Subsection Analysis**: Refined content specific to the task

The system automatically processes all three collections and generates comprehensive analysis results for each persona and use case.

---

**Adobe India Hackathon 2025 - Challenge 1b Implementation**
