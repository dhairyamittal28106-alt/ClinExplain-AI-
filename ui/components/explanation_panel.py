"""
Explanation Panel Component

Formats patient-friendly summaries and medical term explanations.
"""

from typing import Dict, Any, List, Optional


def format_patient_summary(
    summary: Optional[Dict[str, Any]],
    terminology: List[Dict[str, Any]]
) -> str:
    """
    Format patient-friendly summary in markdown.
    
    Args:
        summary: Patient summary from pipeline
        terminology: Medical terms with explanations
        
    Returns:
        Markdown formatted summary
    """
    if not summary:
        return """
### ℹ️ Summary Not Available

The system could not generate a patient-friendly summary for this report.
This may happen if:
- The report is very technical or specialized
- The findings are ambiguous
- The AI had low confidence in its interpretation

**What to do:** Discuss the original report directly with your healthcare provider.
"""
    
    output = []
    
    # Main summary text
    if 'summary' in summary and summary['summary']:
        output.append("### 💬 Plain Language Summary\n")
        output.append(summary['summary'])
        output.append("\n")
    
    # Key points
    if 'key_points' in summary and summary['key_points']:
        output.append("### 📌 Key Points\n")
        for point in summary['key_points']:
            output.append(f"- {point}")
        output.append("\n")
    
    # Medical terms explained
    if terminology:
        output.append("### 📖 Medical Terms Explained\n")
        for term in terminology:
            medical_term = term.get('medical_term', 'Unknown')
            explanation = term.get('simple_explanation', 'No explanation available')
            confidence = term.get('confidence', 'unknown')
            
            confidence_emoji = {
                'high': '✓',
                'medium': '~',
                'low': '?'
            }.get(confidence, '?')
            
            output.append(f"**{medical_term}** ({confidence_emoji} {confidence} confidence)")
            output.append(f": {explanation}\n")
    
    # Next steps note
    if 'next_steps_note' in summary and summary['next_steps_note']:
        output.append("### 📋 Next Steps\n")
        output.append(f"> {summary['next_steps_note']}\n")
    
    # Safety reminder
    output.append("\n---\n")
    output.append("**⚠️ Important Reminder**\n\n")
    output.append("This summary is AI-generated and for informational purposes only. ")
    output.append("Your healthcare provider will interpret your results in the context of ")
    output.append("your complete medical history, symptoms, and other test results.\n")
    
    return "\n".join(output)
