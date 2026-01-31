"""
Metadata Display Component

Shows technical analysis details and system metrics.
"""

from typing import Dict, Any


def format_metadata_panel(result) -> Dict[str, Any]:
    """
    Format pipeline result metadata for JSON display.
    
    Args:
        result: PipelineResult object
        
    Returns:
        Dictionary of metadata
    """
    metadata = {
        "analysis_summary": {
            "success": result.success,
            "findings_extracted": len(result.extraction.get('findings', [])) if result.extraction else 0,
            "attention_flags": len(result.extraction.get('attention_flags', [])) if result.extraction else 0,
            "medical_terms_explained": len(result.extraction.get('terminology', [])) if result.extraction else 0,
        },
        "safety_checks": {
            "safety_violations": len(result.safety_result.violations) if result.safety_result else 0,
            "warnings": len(result.warnings),
            "is_safe": result.safety_result.is_safe if result.safety_result else False,
        },
        "quality_metrics": {
            "readability_grade": round(result.readability_score, 1) if result.readability_score else "N/A",
            "validation_passed": result.validation_result.is_valid if result.validation_result else False,
        },
        "processing_info": {
            "input_length_chars": len(result.validation_result.sanitized_text) if result.validation_result else 0,
            "model_mode": "Mock (Demo)" if hasattr(result, 'use_mock') else "Production",
        }
    }
    
    # Add warnings if present
    if result.warnings:
        metadata["warnings_detail"] = result.warnings
    
    # Add safety violations if present
    if result.safety_result and result.safety_result.violations:
        metadata["safety_violations_detail"] = [
            {
                "type": v.get('type'),
                "description": v.get('description'),
                "severity": v.get('severity', 'unknown')
            }
            for v in result.safety_result.violations
        ]
    
    return metadata
