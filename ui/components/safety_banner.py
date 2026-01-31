"""
Safety Banner Component

Persistent medical disclaimer and usage guidance.
"""

DISCLAIMER_HTML = """
<div class="disclaimer-banner">
    <h2>⚠️ IMPORTANT MEDICAL DISCLAIMER</h2>
    <p style="font-size: 1.1em; margin: 10px 0;">
        <strong>This tool does NOT provide medical advice, diagnosis, or treatment.</strong>
    </p>
    <p style="margin: 10px 0;">
        This system is for <strong>informational and educational purposes only</strong>.
        It extracts and simplifies information from clinical reports but cannot replace
        professional medical interpretation.
    </p>
    <p style="margin: 10px 0; font-size: 1.05em;">
        <strong>Always consult a qualified healthcare provider for medical decisions.</strong>
        If you think you have a medical emergency, call your doctor or emergency services immediately.
    </p>
</div>
"""

USAGE_GUIDE_HTML = """
<div class="usage-guide">
    <h3>ℹ️ How to Use This Tool</h3>
    
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 15px;">
        <div>
            <h4 style="color: #27AE60; margin-top: 0;">✓ What This Tool Does</h4>
            <ul style="margin: 5px 0; padding-left: 20px;">
                <li>Extracts key findings from your clinical report</li>
                <li>Highlights the exact text the AI analyzed</li>
                <li>Explains medical terms in plain language</li>
                <li>Shows confidence levels for each finding</li>
                <li>Identifies points to discuss with your doctor</li>
            </ul>
        </div>
        
        <div>
            <h4 style="color: #E74C3C; margin-top: 0;">✗ What This Tool Does NOT Do</h4>
            <ul style="margin: 5px 0; padding-left: 20px;">
                <li>Diagnose medical conditions</li>
                <li>Recommend treatments or medications</li>
                <li>Replace your doctor's interpretation</li>
                <li>Predict medical outcomes</li>
                <li>Provide clinical decision support</li>
            </ul>
        </div>
    </div>
    
    <div style="margin-top: 15px; padding: 12px; background: white; border-radius: 4px; border-left: 4px solid #3498DB;">
        <strong>Privacy Reminder:</strong> Remove all personal information (name, date of birth, ID numbers) 
        from your report before uploading. This tool does not store your data, but protecting your privacy 
        is your responsibility.
    </div>
</div>
"""
