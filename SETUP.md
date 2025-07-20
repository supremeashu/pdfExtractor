# Quick Setup Guide

Get the PDF Heading Extractor running in under 5 minutes! 🚀

## 🔧 Prerequisites

- **Python 3.8+** (check with `python --version`)
- **Git** (for cloning the repository)
- **10MB disk space** for dependencies

## ⚡ Quick Install

### Option 1: Automated Setup (Recommended)

```bash
# Clone repository
git clone https://github.com/your-username/headingExtractor.git
cd headingExtractor

# Automatic setup (installs everything)
python setup.py
```

### Option 2: Manual Setup

```bash
# Clone repository
git clone https://github.com/your-username/headingExtractor.git
cd headingExtractor

# Create virtual environment (recommended)
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 🧪 Verify Installation

```bash
# Test basic functionality
python simple_test.py

# Test CLI interface
python main.py --help
```

**Expected output**: ✅ All tests pass, CLI help displays

## 🎯 Quick Test

```bash
# Place your PDF in the project folder, then:
python main.py extract your_document.pdf

# View results:
python main.py view your_document_headings.json
```

## 🚨 Common Issues

**Import Error**: `No module named 'fitz'`

```bash
pip install PyMuPDF
```

**Permission Error**: Close PDF file if open in another application

**Empty Results**: Try lower confidence threshold:

```bash
python main.py extract document.pdf --min-confidence 0.5
```

## 📚 Next Steps

- 📖 Read the full [README.md](README.md) for detailed usage
- 🔍 Check [examples/](examples/) for sample PDFs and outputs
- 🤝 See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup

---

**Need help?** Create an issue with your error message and sample PDF! 🆘
