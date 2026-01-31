"""
Confidence Formatter Utility

Visual formatting for confidence levels and findings display.
"""

from typing import List, Dict, Any


def format_confidence_visual(confidence: str) -> str:
    """
    Convert confidence level to visual indicator.
    
    Args:
        confidence: 'high', 'medium', or 'low'
        
    Returns:
        HTML with visual confidence indicator
    """
    confidence_lower = confidence.lower()
    
    if confidence_lower == 'high':
        dots = '●●●'
        color_var = 'var(--success-600)'
        label = 'High'
    elif confidence_lower == 'medium':
        dots = '●●○'
        color_var = 'var(--warning-600)'
        label = 'Medium'
    elif confidence_lower == 'low':
        dots = '●○○'
        color_var = 'var(--danger-600)'
        label = 'Low'
    else:
        dots = '○○○'
        color_var = 'var(--slate-400)'
        label = 'Unknown'
    
    return f'<span style="color: {color_var}; font-weight: 600; font-variant-numeric: tabular-nums;">{dots} {label}</span>'


def format_findings_html(findings: List[Dict[str, Any]]) -> str:
    """
    Format findings list as HTML.
    
    Args:
        findings: List of finding dictionaries
        
    Returns:
        HTML formatted findings
    """
    if not findings:
        return """
        <div class="med-card">
            <h3>🔍 Key Findings</h3>
            <div style="text-align: center; padding: 2rem; color: var(--slate-500);">
                <p>No findings extracted from this report.</p>
            </div>
        </div>
        """
    
    html_parts = ['<div class="med-card"><h3>🔍 Key Findings Extracted</h3>']
    
    for i, finding in enumerate(findings, 1):
        text = finding.get('text', 'No text available')
        source = finding.get('source_quote', 'No source')
        confidence = finding.get('confidence', 'unknown')
        category = finding.get('category', 'general')
        
        confidence_html = format_confidence_visual(confidence)
        
        # Category emoji
        category_emoji = {
            'observation': '👁️',
            'normal': '✓',
            'abnormal': '⚠️',
            'measurement': '📏',
            'general': '•'
        }.get(category.lower(), '•')
        
        finding_html = f"""
        <div class="finding-item">
            <div class="finding-header">
                <span style="font-weight: 600; color: var(--slate-800);">{category_emoji} {text}</span>
                <span style="font-size: 0.9em;">{confidence_html}</span>
            </div>
            <div style="margin-top: 0.5rem; font-size: 0.9em; color: var(--slate-600);">
                <strong>Source:</strong> <code style="background: var(--warning-50); padding: 2px 6px; border-radius: 4px; color: var(--slate-700);">"{source}"</code>
            </div>
        </div>
        """
        html_parts.append(finding_html)
    
    html_parts.append('</div>')
    return ''.join(html_parts)


def format_flags_html(flags: List[Dict[str, Any]]) -> str:
    """
    Format attention flags as HTML.
    
    Args:
        flags: List of attention flag dictionaries
        
    Returns:
        HTML formatted flags
    """
    if not flags:
        return """
        <div class="med-card">
            <h3>⚠️ Attention Flags</h3>
            <div class="med-banner success">
                <strong>✓ No attention flags identified</strong>
                <p style="margin: 0.5rem 0 0 0;">
                    The AI did not identify any findings that require special attention or follow-up.
                    However, always discuss your complete results with your healthcare provider.
                </p>
            </div>
        </div>
        """
    
    html_parts = [
        '<div class="med-card">',
        '<h3>⚠️ Points for Discussion with Your Doctor</h3>',
        '<div class="med-banner warning">',
        '<strong>Important:</strong> These are NOT diagnoses. They are items that may require clinical correlation. ',
        'Your doctor will interpret these in the context of your complete health picture.',
        '</div>'
    ]
    
    for i, flag in enumerate(flags, 1):
        flag_text = flag.get('flag', 'No description')
        severity = flag.get('severity', 'info')
        context = flag.get('context', '')
        source = flag.get('source_quote', '')
        
        # Severity styling
        if severity.lower() == 'warning':
            banner_class = 'warning'
            icon = '⚠️'
        else:  # info
            banner_class = 'info'
            icon = 'ℹ️'
        
        flag_html = f"""
        <div class="med-banner {banner_class}">
            <div style="font-size: 1.05em; font-weight: 600; margin-bottom: 0.5rem;">
                {icon} {flag_text}
            </div>
            {f'<div style="margin: 0.25rem 0;"><strong>Context:</strong> {context}</div>' if context else ''}
            {f'<div style="margin: 0.25rem 0;"><strong>Source:</strong> <code style="background: rgba(255,255,255,0.5); padding: 2px 6px; border-radius: 4px;">"{source}"</code></div>' if source else ''}
        </div>
        """
        html_parts.append(flag_html)
    
    html_parts.append('</div>')
    return ''.join(html_parts)
