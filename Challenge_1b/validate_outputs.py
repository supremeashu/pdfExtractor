#!/usr/bin/env python3
"""
Validation script for Challenge 1b outputs
"""
import json
from pathlib import Path

def validate_output_structure(output_data: dict, collection_name: str) -> bool:
    """Validate the output JSON structure"""
    print(f"\nValidating {collection_name}:")
    
    # Check required top-level keys
    required_keys = ['metadata', 'extracted_sections', 'subsection_analysis']
    for key in required_keys:
        if key not in output_data:
            print(f"  ❌ Missing required key: {key}")
            return False
        print(f"  ✅ Found key: {key}")
    
    # Check metadata structure
    metadata = output_data['metadata']
    metadata_keys = ['input_documents', 'persona', 'job_to_be_done']
    for key in metadata_keys:
        if key not in metadata:
            print(f"  ❌ Missing metadata key: {key}")
            return False
        print(f"  ✅ Metadata has: {key}")
    
    # Check extracted sections structure
    sections = output_data['extracted_sections']
    if not isinstance(sections, list):
        print("  ❌ extracted_sections should be a list")
        return False
    
    if sections:
        section_keys = ['document', 'section_title', 'importance_rank', 'page_number']
        for key in section_keys:
            if key not in sections[0]:
                print(f"  ❌ Missing section key: {key}")
                return False
        print(f"  ✅ Extracted {len(sections)} sections with correct structure")
    
    # Check subsection analysis structure  
    subsections = output_data['subsection_analysis']
    if not isinstance(subsections, list):
        print("  ❌ subsection_analysis should be a list")
        return False
    
    if subsections:
        subsection_keys = ['document', 'refined_text', 'page_number']
        for key in subsection_keys:
            if key not in subsections[0]:
                print(f"  ❌ Missing subsection key: {key}")
                return False
        print(f"  ✅ Analyzed {len(subsections)} subsections with correct structure")
    
    print(f"  ✅ {collection_name} validation passed!")
    return True

def main():
    """Main validation function"""
    print("=== Challenge 1b Output Validation ===")
    
    base_dir = Path(".")
    collections = ["Collection 1", "Collection 2", "Collection 3"]
    
    all_valid = True
    
    for collection in collections:
        output_file = base_dir / collection / "challenge1b_output.json"
        
        if not output_file.exists():
            print(f"\n❌ Output file not found for {collection}")
            all_valid = False
            continue
        
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                output_data = json.load(f)
            
            if not validate_output_structure(output_data, collection):
                all_valid = False
        
        except Exception as e:
            print(f"\n❌ Error validating {collection}: {e}")
            all_valid = False
    
    if all_valid:
        print("\n🎉 All outputs are valid!")
        print("Challenge 1b implementation is ready for submission!")
    else:
        print("\n❌ Some outputs failed validation")
    
    return all_valid

if __name__ == "__main__":
    main()
