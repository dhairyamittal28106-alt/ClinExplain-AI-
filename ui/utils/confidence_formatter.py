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
        dots = '●●●●●'
        css_class = 'confidence-high'
        label = 'High'
    elif confidence_lower == 'medium':
        dots = '●●●○○'
        css_class = 'confidence-medium'
        label = 'Medium'
    elif confidence_lower == 'low':
        dots = '●○○○○'
        css_class = 'confidence-low'
        label = 'Low'
    else:
        dots = '○○○○○'
        css_class = 'confidence-low'
        label = 'Unknown'
    
    return f'<span class="{css_class}">{dots} {label}</span>'


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
        <div class="report-section">
            <h3>🔍 Key Findings</h3>
            <p style="color: #666; font-style: italic;">No findings were extracted from this report.</p>
            <p>This may happen if:</p>
            <ul>
                <li>The report contains only normal findings</li>
                <li>The text is too short or unclear</li>
                <li>The AI had low confidence in all extractions</li>
            </ul>
        </div>
        """
    
    html_parts = ['<div class="report-section"><h3>🔍 Key Findings Extracted</h3>']
    
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
        <div style="margin: 15px 0; padding: 15px; background: #f9f9f9; border-left: 4px solid #3498DB; border-radius: 4px;">
            <div style="font-size: 1.1em; font-weight: 600; color: #2C3E50; margin-bottom: 8px;">
                {category_emoji} {i}. {text}
            </div>
            <div style="margin: 5px 0; color: #555;">
                <strong>Source:</strong> <code style="background: #FFF9C4; padding: 2px 6px; border-radius: 3px;">"{source}"</code>
            </div>
            <div style="margin: 5px 0;">
                <strong>Confidence:</strong> {confidence_html}
            </div>
            <div style="margin: 5px 0; color: #666;">
                <strong>Category:</strong> {category.capitalize()}
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
        <div class="report-section">
            <h3>⚠️ Attention Flags</h3>
            <div style="padding: 15px; background: #d4edda; border-left: 4px solid #28a745; border-radius: 4px;">
                <strong>✓ No attention flags identified</strong>
                <p style="margin: 10px 0 0 0;">
                    The AI did not identify any findings that require special attention or follow-up.
                    However, always discuss your complete results with your healthcare provider.
                </p>
            </div>
        </div>
        """
    
    html_parts = [
        '<div class="report-section">',
        '<h3>⚠️ Points for Discussion with Your Doctor</h3>',
        '<div style="padding: 12px; background: #FFF3E0; border-left: 4px solid #FF9800; border-radius: 4px; margin-bottom: 15px;">',
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
            bg_color = '#FFF3E0'
            border_color = '#FF9800'
            icon = '⚠️'
        else:  # info
            bg_color = '#E3F2FD'
            border_color = '#2196F3'
            icon = 'ℹ️'
        
        flag_html = f"""
        <div style="margin: 12px 0; padding: 15px; background: {bg_color}; border-left: 4px solid {border_color}; border-radius: 4px;">
            <div style="font-size: 1.05em; font-weight: 600; color: #2C3E50; margin-bottom: 8px;">
                {icon} {flag_text}
            </div>
            {f'<div style="margin: 5px 0; color: #555;"><strong>Context:</strong> {context}</div>' if context else ''}
            {f'<div style="margin: 5px 0; color: #555;"><strong>Source:</strong> <code style="background: white; padding: 2px 6px; border-radius: 3px;">"{source}"</code></div>' if source else ''}
        </div>
        """
        html_parts.append(flag_html)
    
    html_parts.append('</div>')
    return ''.join(html_parts)
