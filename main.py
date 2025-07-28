#!/usr/bin/env python3
"""
Round 1B - Persona-Driven Document Intelligence
Main entry point for analyzing document collections using persona and job context.
"""

import sys
import json
import os
from pathlib import Path
from typing import Dict, Any, List

from src.persona_intelligence import PersonaIntelligenceEngine


def load_specification(spec_path: str) -> Dict[str, Any]:
    """
    Load and parse the input specification JSON file.

    Args:
        spec_path (str): Path to the input JSON specification.

    Returns:
        Dict[str, Any]: Parsed specification data.
    """
    try:
        with open(spec_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading specification file: {e}")
        return {}


def validate_pdfs(pdf_paths: List[str]) -> List[str]:
    """
    Filter and return valid, existing PDF file paths.

    Args:
        pdf_paths (List[str]): List of PDF paths to validate.

    Returns:
        List[str]: List of existing PDF file paths.
    """
    valid_files = []
    for path in pdf_paths:
        if os.path.exists(path):
            valid_files.append(path)
        else:
            print(f"Warning: PDF not found - {path}")
    return valid_files


def main() -> None:
    """
    Main execution logic for persona-driven document analysis.
    Usage: python main_1b.py <input_spec.json> <output_dir>
    """
    if len(sys.argv) != 3:
        print("Usage: python main_1b.py <input_spec.json> <output_dir>")
        sys.exit(1)

    spec_file = sys.argv[1]
    output_dir = Path(sys.argv[2])

    # Load input specification
    spec = load_specification(spec_file)
    if not spec:
        sys.exit(1)

    # Extract required fields
    documents = spec.get("documents", [])
    persona = spec.get("persona")
    job_to_be_done = spec.get("job_to_be_done")

    if not documents or not persona or not job_to_be_done:
        print("Invalid specification: missing 'documents', 'persona', or 'job_to_be_done'.")
        sys.exit(1)

    # Validate documents
    valid_documents = validate_pdfs(documents)
    if not valid_documents:
        print("No valid PDF documents were found. Exiting.")
        sys.exit(1)

    print("Starting document analysis (Round 1B)...")
    print(f"Documents: {len(valid_documents)}")
    print(f"Persona: {persona}")
    print(f"Job to be done: {job_to_be_done}")

    # Initialize processing engine
    engine = PersonaIntelligenceEngine()

    try:
        # Analyze documents
        result = engine.analyze_document_collection(valid_documents, persona, job_to_be_done)

        # Ensure output directory exists
        output_dir.mkdir(parents=True, exist_ok=True)

        # Write result to output
        output_file = output_dir / "challenge1b_output.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print("Analysis complete.")
        print(f"Output saved to: {output_file}")
        print(f"Sections extracted: {len(result.get('extracted_sections', []))}")
        print(f"Subsections analyzed: {len(result.get('subsection_analysis', []))}")

    except Exception as e:
        print(f"Analysis failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
