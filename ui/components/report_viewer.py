"""
Report Viewer Component

Displays original report with source quote highlighting.
"""

from typing import Dict, Any, List


def format_original_report(report_text: str, extraction: Dict[str, Any]) -> str:
    """
    Format original report with highlighted source quotes.
    
    Args:
        report_text: Original clinical report text
        extraction: Extraction result with findings and source quotes
        
    Returns:
        HTML formatted report with highlights
    """
    if not extraction:
        return f"""
        <div class="report-section">
            <h3>📋 Original Report</h3>
            <pre style="white-space: pre-wrap; font-family: Georgia, serif; line-height: 1.6;">{report_text}</pre>
        </div>
        """
    
    # Collect all source quotes
    source_quotes = set()
    
    for finding in extraction.get('findings', []):
        if 'source_quote' in finding and finding['source_quote']:
            source_quotes.add(finding['source_quote'])
    
    for flag in extraction.get('attention_flags', []):
        if 'source_quote' in flag and flag['source_quote']:
            source_quotes.add(flag['source_quote'])
    
    # Highlight source quotes in report
    highlighted_text = report_text
    for quote in sorted(source_quotes, key=len, reverse=True):  # Longest first to avoid partial matches
        if quote in highlighted_text:
            highlighted_text = highlighted_text.replace(
                quote,
                f'<span class="source-highlight">{quote}</span>'
            )
    
    legend_html = """
    <div class="med-banner warning" style="margin-bottom: 1rem;">
        <strong>Legend:</strong> <span class="source-highlight">Yellow highlights</span> show text that was used by the AI to extract findings.
        This helps you verify the AI didn't hallucinate or misinterpret.
    </div>
    """
    
    return f"""
    <div class="med-card">
        <h3>📋 Your Original Report</h3>
        {legend_html}
        <div style="background: var(--slate-50); padding: 1.5rem; border-radius: var(--radius-md); border: 1px solid var(--slate-200);">
            <pre style="white-space: pre-wrap; font-family: Georgia, serif; line-height: 1.8; margin: 0; color: var(--slate-800);">{highlighted_text}</pre>
        </div>
    </div>
    """
