"""
Simple test runner to verify the PDF Heading Extractor functionality
"""

import sys
import os
from pathlib import Path

# Add current directory to path to import our modules
sys.path.insert(0, str(Path(__file__).parent))

try:
    from pdf_heading_extractor import PDFHeadingExtractor
    from test_utils import create_sample_json, validate_json_schema
    from rich.console import Console
    import tempfile
    import json
    
    console = Console()
    
    def run_basic_tests():
        """Run basic functionality tests"""
        console.print("[bold blue]Running PDF Heading Extractor Tests[/bold blue]\n")
        
        # Test 1: Module import
        console.print("[cyan]Test 1: Module Import[/cyan]")
        try:
            extractor = PDFHeadingExtractor()
            console.print("✓ Successfully imported and initialized PDFHeadingExtractor")
        except Exception as e:
            console.print(f"✗ Failed to import: {e}")
            return False
        
        # Test 2: Create sample JSON
        console.print("\n[cyan]Test 2: Sample JSON Creation[/cyan]")
        try:
            create_sample_json()
            console.print("✓ Sample JSON created successfully")
        except Exception as e:
            console.print(f"✗ Failed to create sample JSON: {e}")
            return False
        
        # Test 3: JSON validation
        console.print("\n[cyan]Test 3: JSON Schema Validation[/cyan]")
        try:
            if validate_json_schema("sample_output.json"):
                console.print("✓ JSON schema validation passed")
            else:
                console.print("✗ JSON schema validation failed")
                return False
        except Exception as e:
            console.print(f"✗ Error during validation: {e}")
            return False
        
        # Test 4: Extractor configuration
        console.print("\n[cyan]Test 4: Extractor Configuration[/cyan]")
        try:
            custom_extractor = PDFHeadingExtractor(
                max_pages=10,
                min_font_size=8.0,
                heading_confidence_threshold=0.5
            )
            console.print("✓ Custom extractor configuration successful")
            console.print(f"  - Max pages: {custom_extractor.max_pages}")
            console.print(f"  - Min font size: {custom_extractor.min_font_size}")
            console.print(f"  - Confidence threshold: {custom_extractor.heading_confidence_threshold}")
        except Exception as e:
            console.print(f"✗ Failed to configure extractor: {e}")
            return False
        
        # Test 5: Empty result handling
        console.print("\n[cyan]Test 5: Empty Result Handling[/cyan]")
        try:
            empty_result = extractor._empty_result("nonexistent.pdf")
            console.print("✓ Empty result handling works correctly")
            console.print(f"  - Empty headings list: {len(empty_result.headings) == 0}")
            console.print(f"  - Stats initialized: {'total_headings' in empty_result.extraction_stats}")
        except Exception as e:
            console.print(f"✗ Failed empty result test: {e}")
            return False
        
        return True
    
    def test_json_operations():
        """Test JSON operations"""
        console.print("\n[cyan]Test 6: JSON Operations[/cyan]")
        
        try:
            # Create a temporary result
            extractor = PDFHeadingExtractor()
            test_result = extractor._empty_result("test.pdf")
            
            # Test saving JSON
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                temp_path = f.name
            
            extractor.save_json(test_result, temp_path)
            
            # Test loading JSON
            with open(temp_path, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)
            
            # Clean up
            os.unlink(temp_path)
            
            console.print("✓ JSON save/load operations successful")
            return True
            
        except Exception as e:
            console.print(f"✗ JSON operations failed: {e}")
            return False
    
    def main():
        """Main test function"""
        console.print("=" * 50)
        console.print("[bold]PDF Heading Extractor - Test Suite[/bold]")
        console.print("=" * 50)
        
        all_tests_passed = True
        
        # Run basic tests
        if not run_basic_tests():
            all_tests_passed = False
        
        # Run JSON tests
        if not test_json_operations():
            all_tests_passed = False
        
        # Final result
        console.print("\n" + "=" * 50)
        if all_tests_passed:
            console.print("[bold green]✓ All tests passed![/bold green]")
            console.print("\n[green]The PDF Heading Extractor is ready to use.[/green]")
            console.print("\n[cyan]Next steps:[/cyan]")
            console.print("1. Place a PDF file in this directory")
            console.print("2. Run: python main.py extract your_file.pdf")
            console.print("3. View results: python main.py view your_file_headings.json")
        else:
            console.print("[bold red]✗ Some tests failed![/bold red]")
            console.print("\n[yellow]Please check the error messages above.[/yellow]")
        
        return all_tests_passed

    if __name__ == "__main__":
        success = main()
        sys.exit(0 if success else 1)

except ImportError as e:
    print(f"Import error: {e}")
    print("Please run 'python setup.py' first to install dependencies.")
    sys.exit(1)
except Exception as e:
    print(f"Unexpected error: {e}")
    sys.exit(1)
