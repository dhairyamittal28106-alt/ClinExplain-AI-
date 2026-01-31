"""
ClinExplain AI - Post-Processing and Safety Module

This module implements safety filters and validation for model outputs.
It ensures outputs do not contain diagnostic language, treatment recommendations,
or other unsafe content.
"""

import json
import re
from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass

try:
    import jsonschema
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False

from .config import (
    ALL_FORBIDDEN_PHRASES,
    FORBIDDEN_DIAGNOSTIC_PHRASES,
    FORBIDDEN_TREATMENT_PHRASES,
    FORBIDDEN_PREDICTIVE_PHRASES,
    EXTRACTION_SCHEMA,
)


@dataclass
class SafetyCheckResult:
    """Result of safety validation"""
    is_safe: bool
    violations: List[Dict[str, str]]
    warnings: List[str]
    sanitized_output: Optional[Dict[str, Any]]


class PostProcessor:
    """
    Post-processes and validates model outputs for safety and correctness.
    
    Functions:
    - Validate JSON schema compliance
    - Check for forbidden phrases (diagnostic/treatment language)
    - Verify source attribution
    - Filter low-confidence extractions
    - Cross-reference with original text
    """
    
    def __init__(self, strict_mode: bool = True):
        """
        Initialize post-processor.
        
        Args:
            strict_mode: If True, reject outputs with any safety violations
        """
        self.strict_mode = strict_mode
        self.forbidden_phrases = ALL_FORBIDDEN_PHRASES
    
    def process(
        self, 
        raw_output: str, 
        original_text: str
    ) -> SafetyCheckResult:
        """
        Process and validate model output.
        
        Args:
            raw_output: Raw text output from model
            original_text: Original clinical report (for cross-reference)
            
        Returns:
            SafetyCheckResult with validation status and sanitized output
        """
        violations = []
        warnings = []
        
        # Step 1: Parse JSON
        try:
            parsed_output = self._parse_json(raw_output)
        except json.JSONDecodeError as e:
            return SafetyCheckResult(
                is_safe=False,
                violations=[{
                    "type": "invalid_json",
                    "description": f"Output is not valid JSON: {str(e)}",
                    "severity": "critical"
                }],
                warnings=[],
                sanitized_output=None
            )
        
        # Step 2: Validate schema
        schema_valid, schema_errors = self._validate_schema(parsed_output)
        if not schema_valid:
            violations.extend([{
                "type": "schema_violation",
                "description": error,
                "severity": "high"
            } for error in schema_errors])
        
        # Step 3: Check for forbidden phrases
        forbidden_found = self._check_forbidden_phrases(parsed_output)
        if forbidden_found:
            violations.extend(forbidden_found)
        
        # Step 4: Verify source quotes exist in original text
        missing_quotes = self._verify_source_quotes(parsed_output, original_text)
        if missing_quotes:
            warnings.extend([
                f"Source quote not found in original: '{quote}'"
                for quote in missing_quotes
            ])
        
        # Step 5: Check for hallucinations (findings not in source)
        hallucinations = self._detect_hallucinations(parsed_output, original_text)
        if hallucinations:
            violations.extend(hallucinations)
        
        # Step 6: Sanitize output (remove violations if possible)
        sanitized = self._sanitize_output(parsed_output, violations)
        
        # Determine if safe
        critical_violations = [v for v in violations if v.get("severity") == "critical"]
        is_safe = len(critical_violations) == 0 if self.strict_mode else len(violations) == 0
        
        return SafetyCheckResult(
            is_safe=is_safe,
            violations=violations,
            warnings=warnings,
            sanitized_output=sanitized if is_safe else None
        )
    
    def _parse_json(self, raw_output: str) -> Dict[str, Any]:
        """
        Parse JSON from raw output.
        Handles common formatting issues.
        """
        # Remove markdown code blocks if present
        raw_output = re.sub(r'```json\s*', '', raw_output)
        raw_output = re.sub(r'```\s*$', '', raw_output)
        
        # Strip whitespace
        raw_output = raw_output.strip()
        
        # Parse JSON
        return json.loads(raw_output)
    
    def _validate_schema(self, output: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate output against expected JSON schema.
        
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        if not JSONSCHEMA_AVAILABLE:
            # Basic validation without jsonschema
            required_keys = ["findings", "attention_flags", "terminology", "uncertainties"]
            missing = [k for k in required_keys if k not in output]
            if missing:
                return False, [f"Missing required keys: {missing}"]
            return True, []
        
        try:
            jsonschema.validate(instance=output, schema=EXTRACTION_SCHEMA)
            return True, []
        except jsonschema.ValidationError as e:
            return False, [str(e)]
        except jsonschema.SchemaError as e:
            return False, [f"Schema error: {str(e)}"]
    
    def _check_forbidden_phrases(self, output: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Check for forbidden diagnostic/treatment phrases.
        
        Returns:
            List of violations found
        """
        violations = []
        
        # Convert entire output to lowercase string for checking
        output_text = json.dumps(output).lower()
        
        for phrase in self.forbidden_phrases:
            if phrase.lower() in output_text:
                # Determine category
                if phrase in FORBIDDEN_DIAGNOSTIC_PHRASES:
                    category = "diagnostic_language"
                elif phrase in FORBIDDEN_TREATMENT_PHRASES:
                    category = "treatment_recommendation"
                elif phrase in FORBIDDEN_PREDICTIVE_PHRASES:
                    category = "predictive_claim"
                else:
                    category = "forbidden_phrase"
                
                violations.append({
                    "type": category,
                    "description": f"Forbidden phrase detected: '{phrase}'",
                    "severity": "critical",
                    "phrase": phrase
                })
        
        return violations
    
    def _verify_source_quotes(
        self, 
        output: Dict[str, Any], 
        original_text: str
    ) -> List[str]:
        """
        Verify that source quotes actually exist in original text.
        
        Returns:
            List of quotes that were not found
        """
        missing_quotes = []
        original_lower = original_text.lower()
        
        # Check findings
        for finding in output.get("findings", []):
            quote = finding.get("source_quote", "")
            if quote and quote.lower() not in original_lower:
                missing_quotes.append(quote)
        
        # Check attention flags
        for flag in output.get("attention_flags", []):
            quote = flag.get("source_quote", "")
            if quote and quote.lower() not in original_lower:
                missing_quotes.append(quote)
        
        return missing_quotes
    
    def _detect_hallucinations(
        self, 
        output: Dict[str, Any], 
        original_text: str
    ) -> List[Dict[str, str]]:
        """
        Detect potential hallucinations (claims not supported by source).
        
        This is a basic check - not comprehensive.
        """
        violations = []
        
        # For now, rely on source quote verification
        # More sophisticated hallucination detection would require
        # semantic similarity or entailment checking
        
        # Check if findings have source quotes
        for i, finding in enumerate(output.get("findings", [])):
            if not finding.get("source_quote"):
                violations.append({
                    "type": "missing_source",
                    "description": f"Finding #{i+1} lacks source quote: '{finding.get('text', '')}'",
                    "severity": "high"
                })
        
        return violations
    
    def _sanitize_output(
        self, 
        output: Dict[str, Any], 
        violations: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Attempt to sanitize output by removing problematic content.
        
        Args:
            output: Original output
            violations: List of violations found
            
        Returns:
            Sanitized output (or original if no sanitization possible)
        """
        sanitized = output.copy()
        
        # If there are critical violations, we can't safely sanitize
        critical = [v for v in violations if v.get("severity") == "critical"]
        if critical:
            return sanitized
        
        # Remove findings without source quotes
        if "findings" in sanitized:
            sanitized["findings"] = [
                f for f in sanitized["findings"]
                if f.get("source_quote")
            ]
        
        # Remove attention flags without source quotes
        if "attention_flags" in sanitized:
            sanitized["attention_flags"] = [
                f for f in sanitized["attention_flags"]
                if f.get("source_quote")
            ]
        
        return sanitized
    
    def filter_low_confidence(
        self, 
        output: Dict[str, Any], 
        min_confidence: str = "medium"
    ) -> Dict[str, Any]:
        """
        Filter out low-confidence extractions.
        
        Args:
            output: Extraction output
            min_confidence: Minimum confidence level to keep ("high" or "medium")
            
        Returns:
            Filtered output
        """
        confidence_order = {"low": 0, "medium": 1, "high": 2}
        min_level = confidence_order.get(min_confidence, 1)
        
        filtered = output.copy()
        
        # Filter findings
        if "findings" in filtered:
            filtered["findings"] = [
                f for f in filtered["findings"]
                if confidence_order.get(f.get("confidence", "low"), 0) >= min_level
            ]
        
        # Filter terminology
        if "terminology" in filtered:
            filtered["terminology"] = [
                t for t in filtered["terminology"]
                if confidence_order.get(t.get("confidence", "low"), 0) >= min_level
            ]
        
        return filtered


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def validate_output(
    raw_output: str, 
    original_text: str, 
    strict: bool = True
) -> SafetyCheckResult:
    """
    Convenience function to validate model output.
    
    Args:
        raw_output: Raw model output
        original_text: Original clinical report
        strict: Whether to use strict mode
        
    Returns:
        SafetyCheckResult
    """
    processor = PostProcessor(strict_mode=strict)
    return processor.process(raw_output, original_text)


def is_output_safe(raw_output: str, original_text: str) -> bool:
    """
    Quick safety check (returns only boolean).
    
    Args:
        raw_output: Raw model output
        original_text: Original clinical report
        
    Returns:
        True if safe, False otherwise
    """
    result = validate_output(raw_output, original_text)
    return result.is_safe
