"""
ClinExplain AI - Prompt Templates Module

This module contains all prompt templates for MedGemma inference.
Prompts are designed to minimize hallucinations and enforce safety constraints.
"""

from typing import Dict, Any
from .config import PROMPT_VERSION






EXTRACTION_PROMPT_TEMPLATE = """You are a medical information extraction assistant.

**Your Role**:
- Extract and organize information from clinical reports
- Summarize findings clearly and accurately
- Identify medical terminology that needs simplification

**Critical Constraints**:
- Extract ONLY information explicitly stated in the report
- Do NOT infer diagnoses not mentioned
- Do NOT recommend treatments or medical actions
- Do NOT make predictions about patient outcomes
- If information is unclear or missing, mark it as "uncertain"
- Use exact quotes from the report when possible

**Task**:
Analyze the following clinical report and extract:

1. **Key Findings**: Medical observations, measurements, or abnormalities mentioned
2. **Attention Flags**: Items marked as abnormal, requiring follow-up, or noted as significant
3. **Medical Terminology**: Complex terms that would benefit from plain-language explanation

**Output Format**:
Return ONLY valid JSON matching this exact schema:

{{
  "findings": [
    {{
      "text": "Brief description of finding",
      "source_quote": "Exact quote from report",
      "confidence": "high|medium|low",
      "category": "observation|measurement|abnormality|normal"
    }}
  ],
  "attention_flags": [
    {{
      "flag": "What requires attention",
      "severity": "info|caution",
      "context": "Why this is flagged",
      "source_quote": "Exact quote from report"
    }}
  ],
  "terminology": [
    {{
      "medical_term": "Technical term from report",
      "simple_explanation": "Plain language explanation (one sentence)",
      "confidence": "high|medium|low"
    }}
  ],
  "uncertainties": [
    "List any information that was unclear or could not be extracted"
  ]
}}

**Clinical Report**:
{report_text}

**Important**: Return ONLY the JSON object. Do not include explanations, preamble, or markdown formatting.
"""






SIMPLIFICATION_PROMPT_TEMPLATE = """You are a medical communication specialist helping patients understand clinical reports.

**Task**: Create a patient-friendly summary of the following medical findings.

**Requirements**:
- Use 6th-8th grade reading level
- Avoid medical jargon (or explain it immediately)
- Be accurate but not alarming
- Do NOT diagnose or recommend treatment
- Acknowledge what is uncertain or requires professional interpretation

**Tone**: Informative, calm, supportive

**Input Findings**:
{structured_findings}

**Output Format**:
Return ONLY valid JSON matching this exact schema:

{{
  "summary": "2-3 paragraph patient-friendly explanation",
  "key_points": ["Bullet point 1", "Bullet point 2", "..."],
  "next_steps_note": "General guidance on consulting healthcare provider"
}}

**Critical**: Do not use phrases like:
- "You have [condition]"
- "This means you need [treatment]"
- "You should [action]"

Instead use:
- "The report mentions [finding]"
- "This may indicate [general category]"
- "Your doctor can explain [specific detail]"

**Important**:
- Return ONLY valid JSON matching the schema.
- If unsure, still generate a best-effort summary.
- NO markdown allowed (e.g. no ```json ... ``` blocks).
- NO commentary or explanations outside the JSON.
"""






VALIDATION_PROMPT_TEMPLATE = """You are a medical AI safety validator.

**Task**: Review the following AI-generated summary for safety and accuracy issues.

**Check for**:
1. Hallucinations (claims not in original report)
2. Diagnostic language (stating diagnoses)
3. Treatment recommendations
4. Overconfident claims about uncertain information
5. Missing uncertainty acknowledgments

**Original Report**:
{original_report}

**AI-Generated Output**:
{ai_output}

**Return**:
{{
  "is_safe": true|false,
  "issues_found": [
    {{
      "type": "hallucination|diagnosis|treatment|overconfidence",
      "description": "What the issue is",
      "severity": "critical|high|medium|low"
    }}
  ],
  "recommendations": ["What should be fixed"]
}}

**Important**: Return ONLY the JSON object.
"""






EXAMPLE_EXTRACTION_1 = {
    "input": """Chest X-ray demonstrates mild cardiomegaly. Lungs are clear bilaterally. 
No acute infiltrates. No pleural effusion or pneumothorax identified.""",
    
    "output": {
        "findings": [
            {
                "text": "Heart appears mildly enlarged",
                "source_quote": "mild cardiomegaly",
                "confidence": "high",
                "category": "observation"
            },
            {
                "text": "Lungs appear normal with no signs of infection or fluid",
                "source_quote": "Lungs are clear bilaterally. No acute infiltrates",
                "confidence": "high",
                "category": "normal"
            },
            {
                "text": "No fluid around lungs or collapsed lung",
                "source_quote": "No pleural effusion or pneumothorax",
                "confidence": "high",
                "category": "normal"
            }
        ],
        "attention_flags": [
            {
                "flag": "Mild heart enlargement noted",
                "severity": "info",
                "context": "May require clinical correlation with symptoms and history",
                "source_quote": "mild cardiomegaly"
            }
        ],
        "terminology": [
            {
                "medical_term": "cardiomegaly",
                "simple_explanation": "Enlargement of the heart",
                "confidence": "high"
            },
            {
                "medical_term": "pleural effusion",
                "simple_explanation": "Fluid buildup around the lungs",
                "confidence": "high"
            },
            {
                "medical_term": "pneumothorax",
                "simple_explanation": "Collapsed lung due to air in chest cavity",
                "confidence": "high"
            }
        ],
        "uncertainties": []
    }
}


EXAMPLE_EXTRACTION_2 = {
    "input": """CT abdomen/pelvis: Liver shows no focal lesions. Gallbladder, pancreas, 
spleen unremarkable. Kidneys show bilateral simple cysts, largest 2.3 cm on right. 
No hydronephrosis. Bowel gas pattern normal.""",
    
    "output": {
        "findings": [
            {
                "text": "Liver appears normal with no masses",
                "source_quote": "Liver shows no focal lesions",
                "confidence": "high",
                "category": "normal"
            },
            {
                "text": "Gallbladder, pancreas, and spleen appear normal",
                "source_quote": "Gallbladder, pancreas, spleen unremarkable",
                "confidence": "high",
                "category": "normal"
            },
            {
                "text": "Simple fluid-filled cysts in both kidneys",
                "source_quote": "bilateral simple cysts, largest 2.3 cm on right",
                "confidence": "high",
                "category": "observation"
            },
            {
                "text": "No kidney swelling or blockage",
                "source_quote": "No hydronephrosis",
                "confidence": "high",
                "category": "normal"
            }
        ],
        "attention_flags": [
            {
                "flag": "Kidney cysts present (common, usually benign)",
                "severity": "info",
                "context": "Simple cysts are common and typically not concerning, but your doctor can assess",
                "source_quote": "bilateral simple cysts"
            }
        ],
        "terminology": [
            {
                "medical_term": "focal lesions",
                "simple_explanation": "Specific abnormal areas or masses",
                "confidence": "high"
            },
            {
                "medical_term": "unremarkable",
                "simple_explanation": "Normal, nothing unusual noted",
                "confidence": "high"
            },
            {
                "medical_term": "simple cysts",
                "simple_explanation": "Fluid-filled sacs (usually harmless)",
                "confidence": "high"
            },
            {
                "medical_term": "hydronephrosis",
                "simple_explanation": "Swelling of kidney due to urine backup",
                "confidence": "high"
            }
        ],
        "uncertainties": []
    }
}






def build_extraction_prompt(report_text: str, include_examples: bool = False) -> str:
    """
    Build the extraction prompt for MedGemma.
    
    Args:
        report_text: The clinical report to analyze
        include_examples: Whether to include few-shot examples
        
    Returns:
        Formatted prompt string
    """
    prompt = EXTRACTION_PROMPT_TEMPLATE.format(report_text=report_text)
    
    
    if include_examples:
        examples_text = "\n\n**Examples for Reference**:\n\n"
        examples_text += f"Example 1 Input:\n{EXAMPLE_EXTRACTION_1['input']}\n\n"
        examples_text += f"Example 1 Output:\n{EXAMPLE_EXTRACTION_1['output']}\n\n"
        
        
        prompt = prompt.replace(
            "**Clinical Report**:",
            examples_text + "**Clinical Report**:"
        )
    
    return prompt


def build_simplification_prompt(structured_findings: Dict[str, Any]) -> str:
    """
    Build the simplification prompt for patient-friendly summary.
    
    Args:
        structured_findings: The extracted findings (JSON)
        
    Returns:
        Formatted prompt string
    """
    import json
    findings_json = json.dumps(structured_findings, indent=2)
    return SIMPLIFICATION_PROMPT_TEMPLATE.format(structured_findings=findings_json)


def build_validation_prompt(original_report: str, ai_output: str) -> str:
    """
    Build the validation prompt for safety checking.
    
    Args:
        original_report: Original clinical report
        ai_output: AI-generated output to validate
        
    Returns:
        Formatted prompt string
    """
    return VALIDATION_PROMPT_TEMPLATE.format(
        original_report=original_report,
        ai_output=ai_output
    )






PROMPT_METADATA = {
    "version": PROMPT_VERSION,
    "last_updated": "2026-01-28",
    "extraction_prompt_tokens": len(EXTRACTION_PROMPT_TEMPLATE.split()),
    "simplification_prompt_tokens": len(SIMPLIFICATION_PROMPT_TEMPLATE.split()),
    "validation_prompt_tokens": len(VALIDATION_PROMPT_TEMPLATE.split()),
}


def get_prompt_info() -> Dict[str, Any]:
    """Returns metadata about current prompts"""
    return PROMPT_METADATA.copy()
