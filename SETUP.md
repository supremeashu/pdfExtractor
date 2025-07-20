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
git clone https://github.com/supremeashu/pdfExtractor.git
cd pdfExtractor

# Create virtual environment (recommended)
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies with proper encoding
pip install --upgrade pip setuptools wheel
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
# Solution 1: Upgrade pip and try again
pip install --upgrade pip setuptools wheel
pip install PyMuPDF

# Solution 2: If on Windows and still failing
pip install --only-binary=all PyMuPDF
```

**Build Error on macOS**: `Microsoft Visual C++ required`
```bash
# Install Xcode command line tools
xcode-select --install
```

**Build Error on Linux**: `gcc not found`
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install build-essential python3-dev

# CentOS/RHEL
sudo yum groupinstall "Development Tools"
sudo yum install python3-devel
```

**Permission Error**: Close PDF file if open in another application

**Empty Results**: Try lower confidence threshold:
```bash
python main.py extract document.pdf --min-confidence 0.5
```

**Virtual Environment Issues**:
```bash
# Windows - ensure proper activation
.venv\Scripts\activate
# Verify Python path
python -c "import sys; print(sys.executable)"

# Should show path inside .venv folder
```

## 📚 Next Steps

- 📖 Read the full [README.md](README.md) for detailed usage
- 🔍 Check [examples/](examples/) for sample PDFs and outputs
- 🤝 See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup

---

**Need help?** Create an issue with your error message and sample PDF! 🆘
