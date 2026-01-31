"""
ClinExplain AI - Demo Script

This script demonstrates the complete pipeline with sample reports.
Run this to verify the system works end-to-end.
"""

import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.pipeline import create_pipeline


def main():
    """Run demo with sample reports"""
    
    print("=" * 70)
    print("ClinExplain AI - System Demo")
    print("=" * 70)
    print()
    
    # Load sample reports
    sample_file = Path(__file__).parent / "sample_reports.json"
    with open(sample_file) as f:
        samples = json.load(f)
    
    # Create pipeline (using mock inference for demo)
    print("Initializing pipeline (mock mode)...")
    pipeline = create_pipeline(use_mock=True)
    print("✓ Pipeline ready\n")
    
    # Process first 3 samples
    print(f"Processing {min(3, len(samples))} sample reports...\n")
    
    for i, sample in enumerate(samples[:3], 1):
        print("=" * 70)
        print(f"Sample {i}: {sample['id']}")
        print(f"Modality: {sample['modality']}")
        print("=" * 70)
        print()
        
        # Process
        result = pipeline.process(sample['text'])
        
        if result.success:
            print("✓ Processing successful\n")
            print(result.formatted_output)
            print()
            
            # Show metadata
            print("-" * 70)
            print("Metadata:")
            print(f"  Findings extracted: {len(result.extraction.get('findings', []))}")
            print(f"  Attention flags: {len(result.extraction.get('attention_flags', []))}")
            print(f"  Readability score: {result.readability_score}")
            print(f"  Warnings: {len(result.warnings)}")
            if result.warnings:
                for warning in result.warnings:
                    print(f"    - {warning}")
            print("-" * 70)
        else:
            print(f"✗ Processing failed: {result.error}\n")
        
        print()
    
    # Batch processing demo
    print("=" * 70)
    print("Batch Processing Demo")
    print("=" * 70)
    print()
    
    all_reports = [s['text'] for s in samples]
    results = pipeline.process_batch(all_reports, include_summary=True)
    
    # Calculate metrics
    metrics = pipeline.get_metrics(results)
    
    print("\nBatch Processing Metrics:")
    print(f"  Total reports: {metrics['total_reports']}")
    print(f"  Successful: {metrics['successful']}")
    print(f"  Failed: {metrics['failed']}")
    print(f"  Success rate: {metrics['success_rate']:.1%}")
    print(f"  Safety violations: {metrics['safety_violations']}")
    print(f"  Total warnings: {metrics['total_warnings']}")
    print(f"  Avg readability: {metrics['avg_readability']}")
    
    print()
    print("=" * 70)
    print("Demo complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
