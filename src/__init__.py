"""
ClinExplain AI - A Human-Centered Medical Report Interpretation System

This package provides tools for safely extracting and simplifying information
from clinical reports using MedGemma.

Main components:
- validator: Input validation and sanitization
- prompts: Prompt templates for MedGemma
- inference: MedGemma inference wrapper
- postprocessor: Safety filters and output validation
- formatter: Output formatting and rendering
- pipeline: Main orchestration
"""

__version__ = "1.0.0"
__author__ = "ClinExplain AI Team"
__license__ = "Educational Use Only"

from .config import (
    VERSION,
    PROMPT_VERSION,
    get_primary_disclaimer,
    get_inference_config,
)

from .validator import (
    InputValidator,
    ValidationResult,
    validate_input,
    quick_validate,
)

from .prompts import (
    build_extraction_prompt,
    build_simplification_prompt,
    build_validation_prompt,
    get_prompt_info,
)

from .postprocessor import (
    PostProcessor,
    SafetyCheckResult,
    validate_output,
    is_output_safe,
)

from .inference import (
    MedGemmaInference,
    InferenceResult,
    create_inference_engine,
)

from .formatter import (
    OutputFormatter,
    FormattedOutput,
    format_output,
    format_to_markdown,
)

from .pipeline import (
    ClinExplainPipeline,
    PipelineResult,
    create_pipeline,
    quick_process,
)

__all__ = [
    
    "VERSION",
    "PROMPT_VERSION",
    
    
    "get_primary_disclaimer",
    "get_inference_config",
    
    
    "InputValidator",
    "ValidationResult",
    "validate_input",
    "quick_validate",
    
    
    "build_extraction_prompt",
    "build_simplification_prompt",
    "build_validation_prompt",
    "get_prompt_info",
    
    
    "PostProcessor",
    "SafetyCheckResult",
    "validate_output",
    "is_output_safe",
    
    
    "MedGemmaInference",
    "InferenceResult",
    "create_inference_engine",
    
    
    "OutputFormatter",
    "FormattedOutput",
    "format_output",
    "format_to_markdown",
    
    
    "ClinExplainPipeline",
    "PipelineResult",
    "create_pipeline",
    "quick_process",
]
