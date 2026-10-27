"""
ClinExplain AI - Input Validation Module

This module handles validation and sanitization of clinical report inputs
to ensure they are safe, reasonable, and suitable for processing.
"""

import re
from typing import Tuple, Optional, List
from dataclasses import dataclass

from .config import (
    INPUT_MIN_LENGTH,
    INPUT_MAX_LENGTH,
    INPUT_WARNING_LENGTH,
    PII_WARNING
)


@dataclass
class ValidationResult:
    """Result of input validation"""
    is_valid: bool
    sanitized_text: Optional[str]
    warnings: List[str]
    errors: List[str]


class InputValidator:
    """
    Validates and sanitizes clinical report inputs.
    
    Checks:
    - Length constraints
    - Basic PII detection (warns user)
    - Empty or whitespace-only input
    - Non-medical content (basic heuristic)
    """
    
    
    PII_PATTERNS = {
        "mrn": r"\b(MRN|Medical Record Number)[\s:]*\d+",
        "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
        "dob": r"\b(DOB|Date of Birth)[\s:]*\d{1,2}[/-]\d{1,2}[/-]\d{2,4}",
        "phone": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    }
    
    
    MEDICAL_INDICATORS = [
        
        "patient", "diagnosis", "examination", "findings", "impression",
        "history", "clinical", "radiology", "imaging", "scan", "x-ray",
        "ct", "mri", "ultrasound", "report", "study", "chest", "abdomen",
        "pelvis", "brain", "spine", "cardiac", "pulmonary", "hepatic",
        "renal", "normal", "abnormal", "unremarkable", "significant",
        
        
        "heart", "lung", "liver", "kidney", "brain", "bone", "muscle",
        "blood", "tissue", "organ", "artery", "vein", "lymph",
        
        
        "fracture", "lesion", "mass", "nodule", "opacity", "effusion",
        "edema", "inflammation", "infection", "hemorrhage", "ischemia",
    ]
    
    def __init__(self):
        """Initialize the validator"""
        self.pii_regex = {
            name: re.compile(pattern, re.IGNORECASE)
            for name, pattern in self.PII_PATTERNS.items()
        }
    
    def validate(self, text: str) -> ValidationResult:
        """
        Validate and sanitize input text.
        
        Args:
            text: Raw input text from user
            
        Returns:
            ValidationResult with validation status, sanitized text, and messages
        """
        warnings = []
        errors = []
        
        
        if not text or not text.strip():
            return ValidationResult(
                is_valid=False,
                sanitized_text=None,
                warnings=[],
                errors=["Input is empty. Please provide a clinical report."]
            )
        
        
        sanitized = self._sanitize_text(text)
        
        
        length = len(sanitized)
        
        if length < INPUT_MIN_LENGTH:
            errors.append(
                f"Input is too short ({length} characters). "
                f"Minimum length is {INPUT_MIN_LENGTH} characters."
            )
        
        if length > INPUT_MAX_LENGTH:
            errors.append(
                f"Input is too long ({length} characters). "
                f"Maximum length is {INPUT_MAX_LENGTH} characters. "
                f"Please truncate the report or process in sections."
            )
        
        if INPUT_WARNING_LENGTH <= length <= INPUT_MAX_LENGTH:
            warnings.append(
                f"Input is quite long ({length} characters). "
                f"Consider shortening for better results."
            )
        
        
        pii_warnings = self._check_pii(sanitized)
        if pii_warnings:
            warnings.extend(pii_warnings)
            warnings.append(PII_WARNING)
        
        
        if not self._appears_medical(sanitized):
            warnings.append(
                "Input does not appear to contain medical terminology. "
                "This system is designed for clinical reports. "
                "Results may be poor for non-medical text."
            )
        
        
        is_valid = len(errors) == 0
        
        return ValidationResult(
            is_valid=is_valid,
            sanitized_text=sanitized if is_valid else None,
            warnings=warnings,
            errors=errors
        )
    
    def _sanitize_text(self, text: str) -> str:
        """
        Basic text sanitization.
        
        - Strip leading/trailing whitespace
        - Normalize line breaks
        - Remove excessive whitespace
        """
        
        text = text.strip()
        
        
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        
        text = re.sub(r' {3,}', '  ', text)
        
        return text
    
    def _check_pii(self, text: str) -> List[str]:
        """
        Check for potential PII patterns.
        
        Note: This is NOT comprehensive PII detection.
        It's a basic check to warn users.
        """
        warnings = []
        
        for pii_type, pattern in self.pii_regex.items():
            if pattern.search(text):
                warnings.append(
                    f"Potential {pii_type.upper()} detected. "
                    f"Please remove personal identifying information."
                )
        
        return warnings
    
    def _appears_medical(self, text: str) -> bool:
        """
        Basic heuristic to check if text appears to be medical content.
        
        Checks if text contains at least 2 medical indicator terms.
        This is NOT a robust classifier, just a basic sanity check.
        """
        text_lower = text.lower()
        
        
        indicator_count = sum(
            1 for indicator in self.MEDICAL_INDICATORS
            if indicator in text_lower
        )
        
        
        return indicator_count >= 2
    
    def truncate_if_needed(self, text: str) -> Tuple[str, bool]:
        """
        Truncate text if it exceeds maximum length.
        
        Args:
            text: Input text
            
        Returns:
            Tuple of (truncated_text, was_truncated)
        """
        if len(text) <= INPUT_MAX_LENGTH:
            return text, False
        
        
        truncated = text[:INPUT_MAX_LENGTH]
        
        
        last_period = truncated.rfind('.')
        last_newline = truncated.rfind('\n')
        
        boundary = max(last_period, last_newline)
        
        if boundary > INPUT_MAX_LENGTH * 0.8:  
            truncated = truncated[:boundary + 1]
        
        return truncated, True






def validate_input(text: str) -> ValidationResult:
    """
    Convenience function to validate input.
    
    Args:
        text: Input text to validate
        
    Returns:
        ValidationResult
    """
    validator = InputValidator()
    return validator.validate(text)


def quick_validate(text: str) -> bool:
    """
    Quick validation check (returns only boolean).
    
    Args:
        text: Input text to validate
        
    Returns:
        True if valid, False otherwise
    """
    result = validate_input(text)
    return result.is_valid
