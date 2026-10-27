"""
Simple Demo - Show One Complete Example
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.pipeline import create_pipeline


def main():
    print("=" * 70)
    print("ClinExplain AI - Single Report Demo")
    print("=" * 70)
    print()
    
    
    report = """Chest X-ray demonstrates mild cardiomegaly. Lungs are clear bilaterally. 
No acute infiltrates. No pleural effusion or pneumothorax identified. 
Recommend clinical correlation."""
    
    print("INPUT REPORT:")
    print("-" * 70)
    print(report)
    print("-" * 70)
    print()
    
    
    print("Initializing pipeline...")
    pipeline = create_pipeline(use_mock=True)
    print("✓ Ready\n")
    
    
    print("Processing report...")
    result = pipeline.process(report)
    print()
    
    if result.success:
        print("=" * 70)
        print("OUTPUT:")
        print("=" * 70)
        print()
        print(result.formatted_output)
        print()
        print("=" * 70)
        print("METADATA:")
        print("=" * 70)
        print(f"Findings extracted: {len(result.extraction.get('findings', []))}")
        print(f"Attention flags: {len(result.extraction.get('attention_flags', []))}")
        print(f"Medical terms explained: {len(result.extraction.get('terminology', []))}")
        print(f"Readability score: {result.readability_score}")
        print(f"Warnings: {len(result.warnings)}")
        if result.warnings:
            for w in result.warnings:
                print(f"  - {w}")
        print("=" * 70)
    else:
        print(f"✗ Error: {result.error}")


if __name__ == "__main__":
    main()
