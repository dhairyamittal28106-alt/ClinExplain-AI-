"""
ClinExplain AI - Main Pipeline

This module orchestrates the complete workflow from input validation
through extraction, safety checking, and output formatting.
"""

import json
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict

from .validator import InputValidator, ValidationResult
from .inference import MedGemmaInference
from .postprocessor import PostProcessor, SafetyCheckResult
from .formatter import OutputFormatter, FormattedOutput

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class PipelineResult:
    """Complete pipeline result"""
    success: bool
    formatted_output: Optional[str]
    extraction: Optional[Dict[str, Any]]
    summary: Optional[Dict[str, Any]]
    validation_result: ValidationResult
    safety_result: Optional[SafetyCheckResult]
    readability_score: Optional[float]
    error: Optional[str]
    warnings: list


class ClinExplainPipeline:
    """
    Main pipeline orchestrating the complete ClinExplain AI workflow.
    
    Workflow:
    1. Validate input
    2. Extract findings with MedGemma
    3. Post-process for safety
    4. Generate patient summary
    5. Format output
    """
    
    def __init__(
        self,
        model_path: Optional[str] = None,
        strict_mode: bool = True,
        use_mock: bool = False,
        include_disclaimer: bool = True
    ):
        """
        Initialize pipeline.
        
        Args:
            model_path: Path to MedGemma model weights
            strict_mode: If True, reject outputs with any safety violations
            use_mock: Use mock inference for testing
            include_disclaimer: Include medical disclaimer in output
        """
        logger.info("Initializing ClinExplain AI Pipeline")
        
        self.strict_mode = strict_mode
        self.use_mock = use_mock
        
        # Initialize components
        self.validator = InputValidator()
        self.inference = MedGemmaInference(
            model_path=model_path,
            use_mock=use_mock
        )
        self.postprocessor = PostProcessor(strict_mode=strict_mode)
        self.formatter = OutputFormatter(include_disclaimer=include_disclaimer)
        
        logger.info("Pipeline initialized successfully")
    
    def process(
        self,
        report_text: str,
        include_summary: bool = True,
        filter_low_confidence: bool = False
    ) -> PipelineResult:
        """
        Process a clinical report end-to-end.
        
        Args:
            report_text: Clinical report text
            include_summary: Whether to generate patient-friendly summary
            filter_low_confidence: Whether to filter low-confidence extractions
            
        Returns:
            PipelineResult with formatted output and metadata
        """
        logger.info("=" * 60)
        logger.info("Starting pipeline processing")
        logger.info("=" * 60)
        
        warnings = []
        
        # Step 1: Validate input
        logger.info("Step 1: Validating input")
        validation_result = self.validator.validate(report_text)
        
        if not validation_result.is_valid:
            logger.error("Input validation failed")
            return PipelineResult(
                success=False,
                formatted_output=None,
                extraction=None,
                summary=None,
                validation_result=validation_result,
                safety_result=None,
                readability_score=None,
                error="; ".join(validation_result.errors),
                warnings=validation_result.warnings
            )
        
        warnings.extend(validation_result.warnings)
        sanitized_text = validation_result.sanitized_text
        logger.info(f"✓ Input validated ({len(sanitized_text)} characters)")
        
        # Step 2: Extract findings
        logger.info("Step 2: Extracting findings with MedGemma")
        extraction_result = self.inference.extract_findings(sanitized_text)
        
        if not extraction_result.success:
            logger.error("Extraction failed")
            return PipelineResult(
                success=False,
                formatted_output=None,
                extraction=None,
                summary=None,
                validation_result=validation_result,
                safety_result=None,
                readability_score=None,
                error=f"Extraction failed: {extraction_result.error}",
                warnings=warnings
            )
        
        logger.info("✓ Findings extracted")
        
        # Step 3: Post-process for safety
        logger.info("Step 3: Running safety checks")
        safety_result = self.postprocessor.process(
            extraction_result.output,
            sanitized_text
        )
        
        if not safety_result.is_safe:
            logger.error("Safety check failed")
            violation_summary = "; ".join([
                f"{v['type']}: {v['description']}"
                for v in safety_result.violations
            ])
            return PipelineResult(
                success=False,
                formatted_output=None,
                extraction=None,
                summary=None,
                validation_result=validation_result,
                safety_result=safety_result,
                readability_score=None,
                error=f"Safety violations: {violation_summary}",
                warnings=warnings + safety_result.warnings
            )
        
        warnings.extend(safety_result.warnings)
        extraction = safety_result.sanitized_output
        logger.info(f"✓ Safety checks passed ({len(extraction.get('findings', []))} findings)")
        
        # Optional: Filter low confidence
        if filter_low_confidence:
            logger.info("Filtering low-confidence extractions")
            extraction = self.postprocessor.filter_low_confidence(extraction)
        
        # Step 4: Generate patient summary (optional)
        summary = None
        if include_summary:
            logger.info("Step 4: Generating patient-friendly summary")
            summary_result = self.inference.simplify_findings(extraction)
            
            if summary_result.success:
                try:
                    summary = json.loads(summary_result.output)
                    logger.info("✓ Summary generated")
                except json.JSONDecodeError as e:
                    logger.warning(f"Summary JSON parsing failed: {e}")
                    warnings.append("Patient summary could not be generated")
            else:
                logger.warning("Summary generation failed")
                warnings.append("Patient summary could not be generated")
        
        # Step 5: Format output
        logger.info("Step 5: Formatting output")
        formatted = self.formatter.format_full_output(extraction, summary)
        logger.info(f"✓ Output formatted ({formatted.word_count} words)")
        
        # Log readability
        if formatted.readability_score:
            logger.info(f"Readability: Grade {formatted.readability_score}")
        
        logger.info("=" * 60)
        logger.info("Pipeline processing complete")
        logger.info("=" * 60)
        
        return PipelineResult(
            success=True,
            formatted_output=formatted.markdown,
            extraction=extraction,
            summary=summary,
            validation_result=validation_result,
            safety_result=safety_result,
            readability_score=formatted.readability_score,
            error=None,
            warnings=warnings
        )
    
    def process_batch(
        self,
        reports: list[str],
        include_summary: bool = True
    ) -> list[PipelineResult]:
        """
        Process multiple reports.
        
        Args:
            reports: List of clinical report texts
            include_summary: Whether to generate summaries
            
        Returns:
            List of PipelineResults
        """
        logger.info(f"Processing batch of {len(reports)} reports")
        
        results = []
        for i, report in enumerate(reports, 1):
            logger.info(f"\nProcessing report {i}/{len(reports)}")
            result = self.process(report, include_summary=include_summary)
            results.append(result)
        
        logger.info(f"\nBatch processing complete: {sum(r.success for r in results)}/{len(reports)} successful")
        
        return results
    
    def get_metrics(self, results: list[PipelineResult]) -> Dict[str, Any]:
        """
        Calculate metrics from batch results.
        
        Args:
            results: List of pipeline results
            
        Returns:
            Dictionary of metrics
        """
        total = len(results)
        successful = sum(1 for r in results if r.success)
        
        # Safety metrics
        safety_violations = sum(
            len(r.safety_result.violations)
            for r in results
            if r.safety_result
        )
        
        # Readability metrics
        readability_scores = [
            r.readability_score
            for r in results
            if r.readability_score is not None
        ]
        avg_readability = (
            sum(readability_scores) / len(readability_scores)
            if readability_scores else None
        )
        
        # Warning metrics
        total_warnings = sum(len(r.warnings) for r in results)
        
        return {
            "total_reports": total,
            "successful": successful,
            "failed": total - successful,
            "success_rate": successful / total if total > 0 else 0,
            "safety_violations": safety_violations,
            "total_warnings": total_warnings,
            "avg_readability": round(avg_readability, 1) if avg_readability else None,
        }


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def create_pipeline(
    model_path: Optional[str] = None,
    use_mock: bool = False
) -> ClinExplainPipeline:
    """
    Create and initialize pipeline.
    
    Args:
        model_path: Path to MedGemma model
        use_mock: Use mock inference
        
    Returns:
        Initialized pipeline
    """
    return ClinExplainPipeline(model_path=model_path, use_mock=use_mock)


def quick_process(report_text: str, use_mock: bool = True) -> str:
    """
    Quick processing for testing.
    
    Args:
        report_text: Clinical report
        use_mock: Use mock inference
        
    Returns:
        Formatted markdown output
    """
    pipeline = create_pipeline(use_mock=use_mock)
    result = pipeline.process(report_text)
    
    if result.success:
        return result.formatted_output
    else:
        return f"Error: {result.error}"
