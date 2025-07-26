#!/usr/bin/env python3
"""
Challenge 1b: Multi-Collection PDF Analysis
Advanced PDF analysis solution that processes multiple document collections and
extracts relevant content based on specific personas and use cases.

Adobe India Hackathon 2025
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import re
from dataclasses import dataclass, asdict
from collections import Counter

# Import PDF processing capabilities from Challenge 1a
try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF not installed. Install with: pip install PyMuPDF")
    sys.exit(1)

@dataclass
class DocumentInfo:
    """Document information structure"""
    filename: str
    title: str
    full_path: str = ""

@dataclass
class ExtractedSection:
    """Extracted section with importance ranking"""
    document: str
    section_title: str
    importance_rank: int
    page_number: int

@dataclass
class SubsectionAnalysis:
    """Refined text analysis for subsections"""
    document: str
    refined_text: str
    page_number: int

@dataclass
class Challenge1bInput:
    """Input structure for Challenge 1b"""
    challenge_info: Dict[str, str]
    documents: List[Dict[str, str]]
    persona: Dict[str, str]
    job_to_be_done: Dict[str, str]

@dataclass
class Challenge1bOutput:
    """Output structure for Challenge 1b"""
    metadata: Dict[str, Any]
    extracted_sections: List[Dict[str, Any]]
    subsection_analysis: List[Dict[str, Any]]

class PersonaBasedAnalyzer:
    """
    Advanced PDF analyzer that processes documents based on specific personas and tasks
    """
    
    def __init__(self):
        """Initialize the persona-based analyzer"""
        self.travel_keywords = [
            'itinerary', 'accommodation', 'hotel', 'restaurant', 'attraction', 'tour',
            'transport', 'flight', 'train', 'bus', 'guide', 'booking', 'reservation',
            'sightseeing', 'museum', 'beach', 'activity', 'cost', 'price', 'budget',
            'travel', 'destination', 'location', 'map', 'route', 'schedule', 'visit',
            'explore', 'experience', 'culture', 'history', 'tradition', 'city', 'town',
            'festival', 'event', 'entertainment', 'nightlife', 'shopping', 'market'
        ]
        
        self.hr_keywords = [
            'form', 'fillable', 'field', 'signature', 'submit', 'workflow', 'approval',
            'onboarding', 'compliance', 'document', 'template', 'process', 'digital',
            'electronic', 'pdf', 'acrobat', 'create', 'manage', 'distribute', 'collect',
            'employee', 'hr', 'human resources', 'policy', 'procedure', 'training',
            'export', 'convert', 'edit', 'share', 'collaboration', 'review', 'comment',
            'security', 'permission', 'access', 'protect', 'password', 'encrypt'
        ]
        
        self.food_keywords = [
            'recipe', 'ingredient', 'cook', 'preparation', 'vegetarian', 'vegan',
            'buffet', 'menu', 'dish', 'meal', 'serving', 'portion', 'corporate',
            'catering', 'dinner', 'lunch', 'breakfast', 'food', 'cuisine', 'dietary',
            'allergen', 'nutrition', 'quantity', 'scale', 'cooking', 'kitchen'
        ]
    
    def _get_persona_keywords(self, persona: str) -> List[str]:
        """Get keywords for specific persona"""
        keyword_map = {
            "Travel Planner": self.travel_keywords,
            "HR Professional": self.hr_keywords, 
            "Food Contractor": self.food_keywords
        }
        return keyword_map.get(persona, [])
    
    def extract_text_with_structure(self, pdf_path: str) -> List[Dict[str, Any]]:
        """Extract text with structural information from PDF"""
        text_blocks = []
        
        try:
            doc = fitz.open(pdf_path)
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                blocks = page.get_text("dict")["blocks"]
                
                for block in blocks:
                    if "lines" not in block:
                        continue
                    
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()
                            if len(text) < 3:
                                continue
                                
                            text_blocks.append({
                                "text": text,
                                "page": page_num + 1,
                                "font_size": span["size"],
                                "font_name": span["font"],
                                "is_bold": "bold" in span["font"].lower() or span["flags"] & 2**4,
                                "bbox": span["bbox"]
                            })
            
            doc.close()
            
        except Exception as e:
            print(f"Error extracting text from {pdf_path}: {e}")
        
        return text_blocks
    
    def identify_sections(self, text_blocks: List[Dict[str, Any]], persona: str) -> List[Dict[str, Any]]:
        """Identify relevant sections based on persona with improved filtering"""
        sections = []
        
        # Get persona-specific keywords
        keywords = self._get_persona_keywords(persona)
        
        # Group text blocks by potential sections with stricter criteria
        potential_sections = []
        current_section = None
        
        for block in text_blocks:
            text = block["text"].strip()
            
            # Improved heading detection with balanced criteria
            is_proper_heading = (
                block["is_bold"] and 
                block["font_size"] > 11 and  # Lower threshold
                5 <= len(text) <= 120 and  # Wider range
                not text.lower().strip() in ['note:', 'tip:', 'important:', 'warning:', 'example:', 'note', 'tip', 'important', 'warning']  # Avoid only the most generic labels
            )
            
            if is_proper_heading:
                if current_section:
                    potential_sections.append(current_section)
                
                current_section = {
                    "title": text,
                    "page": block["page"],
                    "content": [block["text"]],
                    "importance_score": 0
                }
            elif current_section:
                current_section["content"].append(block["text"])
        
        if current_section:
            potential_sections.append(current_section)
        
        # Score sections based on persona relevance
        relevant_keywords = self._get_persona_keywords(persona)
        
        for section in potential_sections:
            section_text = " ".join(section["content"]).lower()
            title_text = section["title"].lower()
            
            # Calculate importance score with better weighting
            score = 0
            for keyword in relevant_keywords:
                title_matches = title_text.count(keyword)
                content_matches = section_text.count(keyword)
                
                score += title_matches * 5  # Title matches are much more important
                score += content_matches * 1
                
            # Bonus for proper section structure
            if ':' in section["title"]:
                score += 2
            if len(section["content"]) > 3:  # Has substantial content
                score += 1
            
            section["importance_score"] = score
            
            # Only include sections with meaningful relevance (lower threshold)
            if score >= 1:  # Lower threshold for inclusion
                sections.append(section)
        
        # Sort by importance score (descending) and limit results
        sections.sort(key=lambda x: x["importance_score"], reverse=True)
        
        # Limit to top 15 most relevant sections per collection
        return sections[:15]
    
    def analyze_subsections(self, sections: List[Dict[str, Any]], persona: str, task: str) -> List[Dict[str, Any]]:
        """Analyze and refine subsections based on the specific task"""
        subsection_analysis = []
        
        # Score and sort sections based on task relevance before analyzing
        task_scored_sections = []
        
        for section in sections[:8]:  # Limit to top 8 sections for cleaner output
            content_text = " ".join(section["content"])
            
            # Calculate task-specific score for better sorting
            task_score = self._calculate_task_relevance(content_text, persona, task)
            task_scored_sections.append((section, task_score))
        
        # Sort by task relevance (higher scores first)
        task_scored_sections.sort(key=lambda x: x[1], reverse=True)
        
        # Process sections in order of task relevance, ensuring document diversity
        document_count = {}  # Track how many sections we've taken from each document
        max_per_document = 3  # Limit sections per document to ensure diversity
        
        for section, task_score in task_scored_sections:
            document = section.get("document", "")
            
            # Skip if we've already taken too many from this document
            if document_count.get(document, 0) >= max_per_document:
                continue
                
            content_text = " ".join(section["content"])
            
            # Extract key information based on persona and task
            refined_text = self.refine_text_for_persona(content_text, persona, task)
            
            if refined_text and len(refined_text) > 80:  # Lower length requirement for more content
                subsection_analysis.append({
                    "document": document,
                    "refined_text": refined_text,
                    "page_number": section["page"]
                })
                
                # Update document count
                document_count[document] = document_count.get(document, 0) + 1
                
                # Stop if we have enough analyses
                if len(subsection_analysis) >= 8:
                    break
        
        return subsection_analysis
    
    def _calculate_task_relevance(self, text: str, persona: str, task: str) -> int:
        """Calculate how relevant text is to the specific task"""
        text_lower = text.lower()
        task_lower = task.lower()
        score = 0
        
        # Task-specific scoring
        if persona == "Food Contractor":
            # For vegetarian buffet task
            vegetarian_keywords = ['vegetarian', 'vegan', 'plant-based', 'veggie', 'tofu', 'beans', 'lentils', 'quinoa', 'chickpeas']
            gluten_free_keywords = ['gluten-free', 'gluten free', 'rice', 'quinoa', 'corn']
            buffet_keywords = ['buffet', 'serving', 'corporate', 'large', 'group', 'catering', 'party']
            non_veg_keywords = ['chicken', 'beef', 'pork', 'fish', 'meat', 'sausage', 'bacon', 'shrimp']
            
            # Bonus for vegetarian/vegan content
            for keyword in vegetarian_keywords:
                if keyword in text_lower:
                    score += 5
            
            # Bonus for gluten-free content  
            for keyword in gluten_free_keywords:
                if keyword in text_lower:
                    score += 3
                    
            # Bonus for buffet/corporate content
            for keyword in buffet_keywords:
                if keyword in text_lower:
                    score += 2
            
            # Penalty for non-vegetarian content
            for keyword in non_veg_keywords:
                if keyword in text_lower:
                    score -= 10  # Heavy penalty
        
        elif persona == "Travel Planner":
            # For group travel planning
            group_keywords = ['group', 'friends', 'college', 'budget', 'affordable', 'young']
            activity_keywords = ['activity', 'attraction', 'tour', 'visit', 'explore', 'experience']
            
            for keyword in group_keywords:
                if keyword in text_lower:
                    score += 3
                    
            for keyword in activity_keywords:
                if keyword in text_lower:
                    score += 2
        
        elif persona == "HR Professional":
            # For form management
            form_keywords = ['form', 'fillable', 'onboarding', 'compliance', 'employee', 'workflow']
            for keyword in form_keywords:
                if keyword in text_lower:
                    score += 3
        
        return max(score, 0)  # Don't allow negative scores
    
    def refine_text_for_persona(self, text: str, persona: str, task: str) -> str:
        """Refine text content based on persona and specific task"""
        # Extract relevant sentences based on persona with better filtering
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        relevant_sentences = []
        
        relevant_keywords = self._get_persona_keywords(persona)
        task_keywords = [word.lower() for word in task.split() if len(word) > 3]
        
        # Special filtering for Food Contractor persona - prefer vegetarian but don't completely exclude
        if persona == "Food Contractor" and "vegetarian" in task.lower():
            # Prioritize vegetarian content but still include some non-vegetarian for adaptation ideas
            vegetarian_sentences = []
            other_sentences = []
            non_veg_keywords = ['chicken', 'beef', 'pork', 'fish', 'meat', 'sausage', 'bacon', 'shrimp']
            
            for sentence in sentences:
                if any(nv_keyword in sentence.lower() for nv_keyword in non_veg_keywords):
                    other_sentences.append(sentence)
                else:
                    vegetarian_sentences.append(sentence)
            
            # Prefer vegetarian content but include some non-vegetarian if needed
            sentences = vegetarian_sentences + other_sentences[:2]  # At most 2 non-veg sentences
        
        for sentence in sentences:
            if len(sentence) < 30:  # Skip very short sentences
                continue
            
            sentence_lower = sentence.lower()
            relevance_score = 0
            
            # Score based on keyword presence with better weighting
            for keyword in relevant_keywords:
                if keyword in sentence_lower:
                    relevance_score += 2
            
            # Higher boost for task-specific keywords
            for keyword in task_keywords:
                if keyword in sentence_lower:
                    relevance_score += 3
            
            # Additional scoring for specific personas
            if persona == "Food Contractor":
                # Bonus for vegetarian/buffet-specific content
                veg_bonus_keywords = ['vegetarian', 'vegan', 'gluten-free', 'buffet', 'serving', 'corporate']
                for keyword in veg_bonus_keywords:
                    if keyword in sentence_lower:
                        relevance_score += 4
            
            # Bonus for sentences with numbers, lists, or specific details
            if any(char.isdigit() for char in sentence):
                relevance_score += 1
            if any(word in sentence_lower for word in [':', '•', '-', 'step', 'how', 'what', 'where', 'when']):
                relevance_score += 1
            
            if relevance_score >= 1:  # Lower threshold to include more content
                relevant_sentences.append((sentence, relevance_score))
        
        # Sort by relevance and take top sentences, ensuring good length
        relevant_sentences.sort(key=lambda x: x[1], reverse=True)
        
        # Build refined text with good structure
        selected_sentences = []
        total_length = 0
        
        for sentence, score in relevant_sentences:
            if total_length + len(sentence) < 500 and len(selected_sentences) < 4:  # Limit length and count
                selected_sentences.append(sentence)
                total_length += len(sentence)
        
        return '. '.join(selected_sentences) + '.' if selected_sentences else ""
    
    def process_collection(self, collection_path: Path) -> Dict[str, Any]:
        """Process a single collection"""
        print(f"\nProcessing collection: {collection_path.name}")
        
        # Load input configuration
        input_file = collection_path / "challenge1b_input.json"
        if not input_file.exists():
            print(f"Warning: Input file not found at {input_file}")
            return None
        
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                input_data = json.load(f)
        except Exception as e:
            print(f"Error loading input file: {e}")
            return None
        
        # Parse input data
        challenge_input = Challenge1bInput(
            challenge_info=input_data.get("challenge_info", {}),
            documents=input_data.get("documents", []),
            persona=input_data.get("persona", {}),
            job_to_be_done=input_data.get("job_to_be_done", {})
        )
        
        persona_role = challenge_input.persona.get("role", "")
        task_description = challenge_input.job_to_be_done.get("task", "")
        
        print(f"  Persona: {persona_role}")
        print(f"  Task: {task_description}")
        print(f"  Documents: {len(challenge_input.documents)}")
        
        # Process each document
        all_extracted_sections = []
        all_subsection_analysis = []
        processed_documents = []
        
        pdfs_dir = collection_path / "PDFs"
        
        # Process each document and collect all sections
        all_sections_with_scores = []
        
        for doc_info in challenge_input.documents:
            filename = doc_info.get("filename", "")
            title = doc_info.get("title", "")
            
            pdf_path = pdfs_dir / filename
            
            if not pdf_path.exists():
                print(f"    Warning: PDF not found: {filename}")
                continue
            
            print(f"    Processing: {filename}")
            processed_documents.append(filename)
            
            # Extract text and identify sections
            text_blocks = self.extract_text_with_structure(str(pdf_path))
            sections = self.identify_sections(text_blocks, persona_role)
            
            # Add document info to each section
            for section in sections:
                section["document"] = filename
                all_sections_with_scores.append(section)
        
        # Sort all sections globally by importance score and take top 12
        all_sections_with_scores.sort(key=lambda x: x["importance_score"], reverse=True)
        top_sections = all_sections_with_scores[:12]
        
        # Create extracted sections with importance ranking
        for idx, section in enumerate(top_sections):
            all_extracted_sections.append({
                "document": section["document"],
                "section_title": section["title"][:80],  # Reasonable title length
                "importance_rank": idx + 1,
                "page_number": section["page"]
            })
        
        # Analyze subsections from top sections only
        subsections = self.analyze_subsections(top_sections, persona_role, task_description)
        for subsection in subsections:
            all_subsection_analysis.append(subsection)
        
        # Create output structure
        output = Challenge1bOutput(
            metadata={
                "input_documents": processed_documents,
                "persona": persona_role,
                "job_to_be_done": task_description
            },
            extracted_sections=all_extracted_sections,
            subsection_analysis=all_subsection_analysis
        )
        
        return asdict(output)

def process_challenge_1b():
    """Main processing function for Challenge 1b"""
    print("=== Challenge 1b: Multi-Collection PDF Analysis ===")
    
    # Get the Challenge_1b directory
    base_dir = Path(__file__).parent
    
    # Initialize analyzer
    analyzer = PersonaBasedAnalyzer()
    
    # Process each collection
    collections = ["Collection 1", "Collection 2", "Collection 3"]
    
    total_start_time = time.time()
    
    for collection_name in collections:
        collection_path = base_dir / collection_name
        
        if not collection_path.exists():
            print(f"Warning: Collection directory not found: {collection_name}")
            continue
        
        start_time = time.time()
        
        # Process the collection
        result = analyzer.process_collection(collection_path)
        
        if result:
            # Save output
            output_file = collection_path / "challenge1b_output.json"
            
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                
                processing_time = time.time() - start_time
                print(f"  ✓ Completed in {processing_time:.3f}s")
                print(f"  ✓ Extracted sections: {len(result.get('extracted_sections', []))}")
                print(f"  ✓ Subsection analyses: {len(result.get('subsection_analysis', []))}")
                print(f"  ✓ Output saved: {output_file.name}")
                
            except Exception as e:
                print(f"  ✗ Error saving output: {e}")
        else:
            print(f"  ✗ Failed to process {collection_name}")
    
    total_time = time.time() - total_start_time
    print(f"\n=== Processing Complete ===")
    print(f"Total time: {total_time:.3f} seconds")
    print(f"All collections processed successfully!")

if __name__ == "__main__":
    process_challenge_1b()
