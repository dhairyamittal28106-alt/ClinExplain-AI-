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
        <div class="med-card">
            <h3>ℹ️ Summary Not Available</h3>
            <p>The system could not generate a patient-friendly summary for this report.</p>
            <div class="med-banner info" style="margin-top: 1rem;">
                <strong>Reason:</strong> This often happens if the report is very technical, ambiguous, or if the AI had low confidence.
            </div>
            <p style="margin-top: 1rem;"><strong>What to do:</strong> Discuss the original report directly with your healthcare provider.</p>
        </div>
        """
    
    output = ['<div class="med-card">']
    
    
    if 'summary' in summary and summary['summary']:
        output.append("<h3>💬 Plain Language Summary</h3>")
        output.append(f"<p style='font-size: 1.1em; line-height: 1.6; margin-bottom: 1.5rem;'>{summary['summary']}</p>")
    
    
    if 'key_points' in summary and summary['key_points']:
        output.append("<h4 style='color: var(--primary-700); margin-bottom: 0.5rem;'>📌 Key Points</h4>")
        output.append("<ul style='padding-left: 1.25rem; margin-bottom: 1.5rem;'>")
        for point in summary['key_points']:
            output.append(f"<li style='margin-bottom: 0.25rem;'>{point}</li>")
        output.append("</ul>")
    
    
    if terminology:
        output.append("<h4 style='color: var(--primary-700); margin-bottom: 0.5rem;'>📖 Medical Terms Explained</h4>")
        output.append("<div style='display: grid; gap: 0.75rem; margin-bottom: 1.5rem;'>")
        for term in terminology:
            medical_term = term.get('medical_term', 'Unknown')
            explanation = term.get('simple_explanation', 'No explanation available')
            confidence = term.get('confidence', 'unknown')
            
            output.append(f"""
            <div style="background: var(--slate-50); padding: 1rem; border-radius: var(--radius-md); border: 1px solid var(--slate-200);">
                <div style="font-weight: 600; color: var(--slate-800); margin-bottom: 0.25rem;">{medical_term}</div>
                <div style="font-size: 0.95em; color: var(--slate-600);">{explanation}</div>
            </div>
            """)
        output.append("</div>")
    
    
    if 'next_steps_note' in summary and summary['next_steps_note']:
        output.append("""
        <div class="med-banner info">
            <strong>📋 Next Steps:</strong><br/>
            {}
        </div>
        """.format(summary['next_steps_note']))
    
    
    output.append("""
    <div style="border-top: 1px solid var(--slate-200); margin-top: 1.5rem; padding-top: 1rem; font-size: 0.9em; color: var(--slate-500);">
        <strong>⚠️ Important Reminder:</strong> This summary is AI-generated and for informational purposes only.
        Your healthcare provider will interpret your results in the context of your complete medical history.
    </div>
    """)
    
    output.append("</div>")
    return "\n".join(output)
