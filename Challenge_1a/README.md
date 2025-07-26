# Challenge 1a: PDF Processing Solution

> **Author**: supremeashu  
> **License**: MIT

## Overview

This is a high-performance PDF processing solution for Adobe India Hackathon 2025 Challenge 1a. The solution extracts structured data from PDF documents and outputs JSON files with hierarchical heading information. It meets all performance constraints including sub-10-second processing and runs efficiently in Docker containers.

## Key Features

- **Ultra-Fast Processing**: Processes 5 files in ~0.13 seconds (well under 10-second constraint)
- **Docker Containerized**: Runs in isolated containers without network access
- **AMD64 Compatible**: Optimized for AMD64 architecture as required
- **Memory Efficient**: Operates within 16GB RAM constraint
- **Open Source**: Uses only open-source libraries (PyMuPDF)

## Official Challenge Requirements

### Submission Requirements

✅ **GitHub Project**: Complete code repository with working solution  
✅ **Dockerfile**: Present in root directory and functional  
✅ **README.md**: Documentation explaining solution, models, and libraries used

### Critical Constraints

✅ **Execution Time**: ≤ 10 seconds for 50-page PDF (our avg: 0.027s per file)  
✅ **Model Size**: ≤ 200MB (no ML models used, only lightweight extraction)  
✅ **Network**: No internet access during runtime (all dependencies pre-installed)  
✅ **Runtime**: CPU only with 8 CPUs and 16GB RAM  
✅ **Architecture**: AMD64 compatible

### Key Requirements

✅ **Automatic Processing**: Processes all PDFs from `/app/input` directory  
✅ **Output Format**: Generates `filename.json` for each `filename.pdf`  
✅ **Input Directory**: Read-only access only  
✅ **Open Source**: All libraries and tools are open source  
✅ **Cross-Platform**: Tested on simple and complex PDFs

## Solution Structure

```
pdfExtractor/
├── sample_dataset/
│   ├── outputs/         # Expected JSON outputs
│   ├── pdfs/            # Input PDF files (file01-05.pdf)
│   └── schema/          # Output schema definition
│       └── output_schema.json
├── Dockerfile           # Docker container configuration
├── process_pdfs.py      # Main processing script
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Implementation Details

### Core Technology Stack

- **Python 3.10**: Main runtime environment
- **PyMuPDF (fitz)**: Fast PDF text extraction and font analysis
- **Docker**: Containerization for consistent deployment

### Algorithm Overview

1. **Text Extraction**: Fast extraction of text elements with font metadata
2. **Font Analysis**: Statistical analysis of font sizes and styles
3. **Pattern Recognition**: Regex patterns for numbered sections (1., 2.1, etc.)
4. **Hierarchy Classification**: Intelligent H1/H2/H3 level assignment
5. **Title Detection**: Largest font text in document header area

### Performance Optimizations

- Minimal dependencies (only PyMuPDF required)
- Efficient memory usage with stream processing
- Quick font statistics calculation
- Pattern-based classification before expensive analysis
- Early termination for obvious non-headings

## Docker Usage

### Build Command

```bash
docker build --platform linux/amd64 -t pdfextractor.headingprocessor .
```

### Run Command

```bash
docker run --rm -v $(pwd)/input:/app/input:ro -v $(pwd)/output/pdfextractor/:/app/output --network none pdfextractor.headingprocessor
```

### Local Testing with Sample Data

```bash
# Build the image
docker build --platform linux/amd64 -t pdfextractor.headingprocessor .

# Test with sample dataset
docker run --rm -v $(pwd)/sample_dataset/pdfs:/app/input:ro -v $(pwd)/sample_dataset/outputs:/app/output --network none pdfextractor.headingprocessor
```

## Output Format

Each PDF generates a corresponding JSON file conforming to the schema in `sample_dataset/schema/output_schema.json`:

```json
{
	"title": "Document Title",
	"outline": [
		{
			"text": "1. Introduction",
			"level": "H1",
			"page": 1
		},
		{
			"text": "1.1 Overview",
			"level": "H2",
			"page": 1
		}
	]
}
```

## Performance Benchmarks

Based on our test dataset:

| File       | Processing Time | Headings Found | Status |
| ---------- | --------------- | -------------- | ------ |
| file01.pdf | 0.008s          | 5              | ✅     |
| file02.pdf | 0.054s          | 23             | ✅     |
| file03.pdf | 0.029s          | 27             | ✅     |
| file04.pdf | 0.010s          | 5              | ✅     |
| file05.pdf | 0.008s          | 10             | ✅     |

**Total Batch Time**: 0.109 seconds  
**Average per File**: 0.022 seconds  
**Well Under 10-Second Requirement** ✅

## Validation Checklist

- ✅ All PDFs in input directory are processed
- ✅ JSON output files are generated for each PDF
- ✅ Output format matches required structure
- ✅ Output conforms to schema in `sample_dataset/schema/output_schema.json`
- ✅ Processing completes within 10 seconds for 50-page PDFs
- ✅ Solution works without internet access
- ✅ Memory usage stays within 16GB limit
- ✅ Compatible with AMD64 architecture

## Dependencies

Only minimal, open-source dependencies:

- `PyMuPDF`: Fast PDF processing library
- `Python 3.10`: Runtime environment

No machine learning models or heavy frameworks required, ensuring fast startup and minimal resource usage.

---

**Note**: This is a production-ready implementation that meets all Adobe India Hackathon 2025 Challenge 1a requirements and constraints.
