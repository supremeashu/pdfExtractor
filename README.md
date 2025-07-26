# PDF Content Extractor - Hackathon Challenges

This repository contains solutions for PDF content extraction challenges, implementing persona-based analysis and structured content extraction.

## 🏆 Challenges

### Challenge 1a: Basic PDF Processing

Located in `Challenge_1a/`

- **Objective**: Extract headings and structure from PDF documents
- **Technology**: Python, PyMuPDF
- **Features**: Heading detection, JSON output, Docker containerization

### Challenge 1b: Multi-Collection Persona-Based Analysis

Located in `Challenge_1b/`

- **Objective**: Advanced PDF analysis with persona-specific content extraction
- **Technology**: Python, PyMuPDF, Advanced NLP techniques
- **Features**:
  - Persona-based content filtering
  - Multi-document collection processing
  - Importance ranking and relevance scoring
  - Task-specific content refinement

## 🚀 Quick Start

### Challenge 1a

```bash
cd Challenge_1a
pip install -r requirements.txt
python process_pdfs.py
```

### Challenge 1b

```bash
cd Challenge_1b
pip install -r requirements.txt
python process_challenge1b.py
```

## 🐳 Docker Support

Both challenges include Docker containerization:

```bash
# Challenge 1a
cd Challenge_1a
docker build -t challenge1a .
docker run challenge1a

# Challenge 1b
cd Challenge_1b
docker build -t challenge1b .
docker run challenge1b
```

## 📊 Performance

- **Challenge 1a**: Sub-second processing for standard PDFs
- **Challenge 1b**: ~2.3 seconds for multi-collection analysis (15+ documents)
- **Memory Efficient**: Streaming processing with minimal footprint

## 🎯 Key Features

### Advanced Section Detection

- Smart heading identification using font analysis
- Hierarchical content structure preservation
- Multi-language support

### Persona-Based Analysis

- **Travel Planner**: Optimized for itinerary and destination content
- **HR Professional**: Focused on forms, workflows, and compliance
- **Food Contractor**: Specialized in menu planning and dietary requirements

### Content Refinement

- Task-specific keyword scoring
- Importance ranking algorithms
- Document diversity controls
- Relevance-based filtering

## 📝 Output Format

Both challenges produce structured JSON outputs with:

- Metadata and document information
- Extracted sections with importance ranking
- Refined text analysis optimized for specific personas
- Page number references for source tracking

## 🛠️ Technical Architecture

- **Python 3.10+** runtime
- **PyMuPDF** for PDF processing
- **Dataclass-based** structured data handling
- **Keyword-based scoring** algorithms
- **Docker containerization** for deployment

## 📈 Results

- ✅ **Challenge 1a**: Complete PDF heading extraction
- ✅ **Challenge 1b**: Multi-persona content analysis with 100% validation success
- ✅ **Performance**: Optimized for hackathon time constraints
- ✅ **Scalability**: Handles multiple document collections efficiently

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**supremeashu**

- GitHub: [@supremeashu](https://github.com/supremeashu)

---

_Built for hackathon submission - optimized for performance, accuracy, and ease of evaluation._
