"""
Setup and installation script for PDF Heading Extractor
"""

import subprocess
import sys
import os
from pathlib import Path


def install_requirements():
    """Install required Python packages"""
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if requirements_file.exists():
        print("Installing Python dependencies...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
            ])
            print("✓ Dependencies installed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Error installing dependencies: {e}")
            return False
    else:
        print("✗ requirements.txt not found")
        return False


def setup_directories():
    """Create necessary directories"""
    directories = ["examples", "output", "temp"]
    
    for directory in directories:
        dir_path = Path(__file__).parent / directory
        dir_path.mkdir(exist_ok=True)
        print(f"✓ Created directory: {directory}")


def download_nltk_data():
    """Download required NLTK data"""
    try:
        import nltk
        print("Downloading NLTK data...")
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        print("✓ NLTK data downloaded")
        return True
    except ImportError:
        print("⚠ NLTK not available - some features may be limited")
        return False
    except Exception as e:
        print(f"⚠ Error downloading NLTK data: {e}")
        return False


def verify_installation():
    """Verify that the installation works"""
    try:
        from pdf_heading_extractor import PDFHeadingExtractor
        print("✓ PDF Heading Extractor module imported successfully")
        
        # Test basic functionality
        extractor = PDFHeadingExtractor()
        print("✓ Extractor initialized successfully")
        
        return True
    except Exception as e:
        print(f"✗ Installation verification failed: {e}")
        return False


def main():
    """Main setup function"""
    print("PDF Heading Extractor - Setup Script")
    print("=" * 40)
    
    # Install requirements
    if not install_requirements():
        print("Setup failed at dependency installation")
        return False
    
    # Setup directories
    setup_directories()
    
    # Download NLTK data
    download_nltk_data()
    
    # Verify installation
    if verify_installation():
        print("\n" + "=" * 40)
        print("✓ Setup completed successfully!")
        print("\nNext steps:")
        print("1. Place your PDF files in the current directory")
        print("2. Run: python main.py extract your_document.pdf")
        print("3. Check the generated JSON output file")
        print("\nFor help: python main.py --help")
        return True
    else:
        print("\n✗ Setup completed with errors")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
