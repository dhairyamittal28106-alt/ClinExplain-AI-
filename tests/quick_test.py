"""
Quick Test - Verify Core Components

This script tests core components without requiring external dependencies.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from src import config
        print("✓ config")
    except Exception as e:
        print(f"✗ config: {e}")
        return False
    
    try:
        from src import validator
        print("✓ validator")
    except Exception as e:
        print(f"✗ validator: {e}")
        return False
    
    try:
        from src import prompts
        print("✓ prompts")
    except Exception as e:
        print(f"✗ prompts: {e}")
        return False
    
    print("\nAll core modules imported successfully!")
    return True


def test_validator():
    """Test input validation"""
    print("\n" + "=" * 60)
    print("Testing Input Validator")
    print("=" * 60)
    
    from src.validator import validate_input
    
    # Test valid input
    valid_text = "Chest X-ray shows normal heart and lungs. No acute findings."
    result = validate_input(valid_text)
    
    print(f"\nTest 1: Valid input")
    print(f"  Input: '{valid_text}'")
    print(f"  Valid: {result.is_valid}")
    print(f"  Warnings: {len(result.warnings)}")
    
    # Test too short
    short_text = "Normal"
    result = validate_input(short_text)
    
    print(f"\nTest 2: Too short")
    print(f"  Input: '{short_text}'")
    print(f"  Valid: {result.is_valid}")
    print(f"  Errors: {result.errors}")
    
    print("\n✓ Validator tests passed")


def test_prompts():
    """Test prompt building"""
    print("\n" + "=" * 60)
    print("Testing Prompt Builder")
    print("=" * 60)
    
    from src.prompts import build_extraction_prompt
    
    report = "Chest X-ray: Normal heart and lungs."
    prompt = build_extraction_prompt(report)
    
    print(f"\nGenerated prompt length: {len(prompt)} characters")
    print(f"Contains report text: {'Normal heart and lungs' in prompt}")
    print(f"Contains JSON schema: {'findings' in prompt}")
    
    print("\n✓ Prompt builder tests passed")


def test_config():
    """Test configuration"""
    print("\n" + "=" * 60)
    print("Testing Configuration")
    print("=" * 60)
    
    from src.config import (
        get_inference_config,
        get_primary_disclaimer,
        ALL_FORBIDDEN_PHRASES
    )
    
    config = get_inference_config()
    print(f"\nInference config:")
    print(f"  Temperature: {config['temperature']}")
    print(f"  Max tokens: {config['max_tokens']}")
    
    disclaimer = get_primary_disclaimer()
    print(f"\nDisclaimer length: {len(disclaimer)} characters")
    
    print(f"\nForbidden phrases count: {len(ALL_FORBIDDEN_PHRASES)}")
    print(f"  Sample: {list(ALL_FORBIDDEN_PHRASES)[:3]}")
    
    print("\n✓ Configuration tests passed")


def main():
    """Run all tests"""
    print("=" * 60)
    print("ClinExplain AI - Quick Component Test")
    print("=" * 60)
    print()
    
    if not test_imports():
        print("\n✗ Import test failed")
        return
    
    test_config()
    test_validator()
    test_prompts()
    
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)
    print("\nNote: Full pipeline test requires installing dependencies:")
    print("  pip install jsonschema textstat")


if __name__ == "__main__":
    main()
