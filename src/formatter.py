"""
ClinExplain AI - Output Formatting Module

This module handles formatting of extracted findings into user-friendly
markdown output with readability scoring and disclaimer injection.
"""

import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

try:
    import textstat
    TEXTSTAT_AVAILABLE = True
except ImportError:
    TEXTSTAT_AVAILABLE = False

from .config import (
    get_primary_disclaimer,
    UNCERTAINTY_NOTICE,
    TARGET_READING_LEVEL,
    MAX_READING_LEVEL,
    ConfidenceLevel,
    SeverityLevel,
)


@dataclass
class FormattedOutput:
    """Formatted output with metadata"""
    markdown: str
    readability_score: Optional[float]
    word_count: int
    has_uncertainties: bool


class OutputFormatter:
    """
    Formats structured extraction results into user-friendly markdown.
    
    Features:
    - Markdown formatting with emoji icons
    - Color-coded severity levels
    - Readability scoring
    - Automatic disclaimer injection
    - Confidence indicators
    """
    
    def __init__(self, include_disclaimer: bool = True):
        """
        Initialize formatter.
        
        Args:
            include_disclaimer: Whether to include medical disclaimer
        """
        self.include_disclaimer = include_disclaimer
    
    def format_full_output(
        self,
        extraction: Dict[str, Any],
        summary: Optional[Dict[str, Any]] = None
    ) -> FormattedOutput:
        """
        Format complete output including findings and summary.
        
        Args:
            extraction: Extracted findings (from MedGemma)
            summary: Patient-friendly summary (optional)
            
        Returns:
            FormattedOutput with markdown and metadata
        """
        sections = []
        
        
        if self.include_disclaimer:
            sections.append(self._format_disclaimer())
        
        
        if extraction.get("findings"):
            sections.append(self._format_findings(extraction["findings"]))
        
        
        if extraction.get("attention_flags"):
            sections.append(self._format_attention_flags(extraction["attention_flags"]))
        
        
        if summary:
            sections.append(self._format_patient_summary(summary))
        
        
        if extraction.get("terminology"):
            sections.append(self._format_terminology(extraction["terminology"]))
        
        
        has_uncertainties = bool(extraction.get("uncertainties"))
        if has_uncertainties:
            sections.append(self._format_uncertainties(extraction["uncertainties"]))
        
        
        markdown = "\n\n---\n\n".join(sections)
        
        
        summary_text = summary.get("summary", "") if summary else ""
        readability = self._calculate_readability(summary_text) if summary_text else None
        
        
        word_count = len(markdown.split())
        
        return FormattedOutput(
            markdown=markdown,
            readability_score=readability,
            word_count=word_count,
            has_uncertainties=has_uncertainties
        )
    
    def _format_disclaimer(self) -> str:
        """Format medical disclaimer section"""
        disclaimer = get_primary_disclaimer()
        return f"{disclaimer}"
    
    def _format_findings(self, findings: List[Dict[str, Any]]) -> str:
        """Format key findings section"""
        lines = ["## 📋 Key Findings\n"]
        
        for finding in findings:
            text = finding.get("text", "")
            confidence = finding.get("confidence", "unknown")
            category = finding.get("category", "observation")
            
            
            conf_icon = self._get_confidence_icon(confidence)
            
            
            cat_icon = self._get_category_icon(category)
            
            lines.append(f"• {cat_icon} {text} {conf_icon}")
        
        return "\n".join(lines)
    
    def _format_attention_flags(self, flags: List[Dict[str, Any]]) -> str:
        """Format attention flags section"""
        lines = ["## ⚠️ Attention Flags\n"]
        
        for flag in flags:
            flag_text = flag.get("flag", "")
            severity = flag.get("severity", "info")
            context = flag.get("context", "")
            
            
            severity_icon = self._get_severity_icon(severity)
            
            lines.append(f"**{severity_icon} {flag_text}**")
            if context:
                lines.append(f"  *{context}*\n")
        
        return "\n".join(lines)
    
    def _format_patient_summary(self, summary: Dict[str, Any]) -> str:
        """Format patient-friendly summary section"""
        lines = ["## 💬 Patient-Friendly Summary\n"]
        
        
        summary_text = summary.get("summary", "")
        if summary_text:
            lines.append(summary_text)
            lines.append("")
        
        
        key_points = summary.get("key_points", [])
        if key_points:
            lines.append("**Key Points:**")
            for point in key_points:
                lines.append(f"• {point}")
            lines.append("")
        
        
        next_steps = summary.get("next_steps_note", "")
        if next_steps:
            lines.append(f"**Next Steps:** {next_steps}")
        
        return "\n".join(lines)
    
    def _format_terminology(self, terminology: List[Dict[str, Any]]) -> str:
        """Format medical terminology section"""
        lines = ["## 📖 Medical Terms Explained\n"]
        
        for term in terminology:
            medical_term = term.get("medical_term", "")
            explanation = term.get("simple_explanation", "")
            confidence = term.get("confidence", "unknown")
            
            conf_icon = self._get_confidence_icon(confidence)
            
            lines.append(f"• **{medical_term}**: {explanation} {conf_icon}")
        
        return "\n".join(lines)
    
    def _format_uncertainties(self, uncertainties: List[str]) -> str:
        """Format uncertainties section"""
        lines = [UNCERTAINTY_NOTICE, ""]
        
        for uncertainty in uncertainties:
            lines.append(f"• {uncertainty}")
        
        return "\n".join(lines)
    
    def _get_confidence_icon(self, confidence: str) -> str:
        """Get icon for confidence level"""
        icons = {
            "high": "✓",
            "medium": "~",
            "low": "?",
        }
        return f"*({icons.get(confidence, '?')} {confidence})*"
    
    def _get_category_icon(self, category: str) -> str:
        """Get icon for finding category"""
        icons = {
            "observation": "👁️",
            "measurement": "📏",
            "abnormality": "⚠️",
            "normal": "✓",
        }
        return icons.get(category, "•")
    
    def _get_severity_icon(self, severity: str) -> str:
        """Get icon for severity level"""
        icons = {
            "info": "ℹ️",
            "caution": "⚠️",
        }
        return icons.get(severity, "•")
    
    def _calculate_readability(self, text: str) -> Optional[float]:
        """
        Calculate Flesch-Kincaid grade level.
        
        Args:
            text: Text to analyze
            
        Returns:
            Grade level (float) or None if textstat unavailable
        """
        if not TEXTSTAT_AVAILABLE or not text:
            return None
        
        try:
            grade_level = textstat.flesch_kincaid_grade(text)
            return round(grade_level, 1)
        except Exception:
            return None
    
    def format_readability_report(self, readability_score: Optional[float]) -> str:
        """
        Format readability assessment.
        
        Args:
            readability_score: Flesch-Kincaid grade level
            
        Returns:
            Formatted readability report
        """
        if readability_score is None:
            return "**Readability**: Not calculated"
        
        
        if readability_score <= TARGET_READING_LEVEL:
            status = "✓ Excellent"
            color = "green"
        elif readability_score <= MAX_READING_LEVEL:
            status = "~ Good"
            color = "yellow"
        else:
            status = "⚠️ May be too complex"
            color = "orange"
        
        return f"**Readability**: Grade {readability_score} ({status})"






def format_output(
    extraction: Dict[str, Any],
    summary: Optional[Dict[str, Any]] = None,
    include_disclaimer: bool = True
) -> FormattedOutput:
    """
    Convenience function to format output.
    
    Args:
        extraction: Extracted findings
        summary: Patient summary (optional)
        include_disclaimer: Include medical disclaimer
        
    Returns:
        FormattedOutput
    """
    formatter = OutputFormatter(include_disclaimer=include_disclaimer)
    return formatter.format_full_output(extraction, summary)


def format_to_markdown(
    extraction: Dict[str, Any],
    summary: Optional[Dict[str, Any]] = None
) -> str:
    """
    Quick format to markdown string.
    
    Args:
        extraction: Extracted findings
        summary: Patient summary (optional)
        
    Returns:
        Markdown string
    """
    result = format_output(extraction, summary)
    return result.markdown
