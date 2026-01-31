"""
Safety Banner Component

Persistent medical disclaimer and usage guidance.
"""


DISCLAIMER_HTML = """
<div class="med-banner warning">
    <h2 style="margin-top: 0; display: flex; align-items: center; gap: 0.5rem; font-size: 1.1rem;">
        ⚠️ IMPORTANT MEDICAL DISCLAIMER
    </h2>
    <p>
        <strong>This tool does NOT provide medical advice, diagnosis, or treatment.</strong>
    </p>
    <p style="margin-top: 0.5rem;">
        This system is for <strong>informational and educational purposes only</strong>.
        It extracts and simplifies information from clinical reports but cannot replace
        professional medical interpretation.
    </p>
    <p style="margin-top: 0.5rem;">
        <strong>Always consult a qualified healthcare provider for medical decisions.</strong>
        If you think you have a medical emergency, call your doctor or emergency services immediately.
    </p>
</div>
"""

USAGE_GUIDE_HTML = """
<div class="med-card">
    <h3 style="display: flex; align-items: center; gap: 0.5rem;">
        ℹ️ How to Use This Tool
    </h3>
    
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-top: 1rem;">
        <div>
            <h4 style="color: var(--success-600); margin-top: 0;">✓ What This Tool Does</h4>
            <ul style="padding-left: 1.25rem; margin-top: 0.5rem;">
                <li>Extracts key findings from your clinical report</li>
                <li>Highlights the exact text the AI analyzed</li>
                <li>Explains medical terms in plain language</li>
                <li>Shows confidence levels for each finding</li>
                <li>Identifies points to discuss with your doctor</li>
            </ul>
        </div>
        
        <div>
            <h4 style="color: var(--danger-600); margin-top: 0;">✗ What This Tool Does NOT Do</h4>
            <ul style="padding-left: 1.25rem; margin-top: 0.5rem;">
                <li>Diagnose medical conditions</li>
                <li>Recommend treatments or medications</li>
                <li>Replace your doctor's interpretation</li>
                <li>Predict medical outcomes</li>
                <li>Provide clinical decision support</li>
            </ul>
        </div>
    </div>
    
    <div class="med-banner info" style="margin-top: 1.5rem; margin-bottom: 0;">
        <strong>Privacy Reminder:</strong> Remove all personal information (name, date of birth, ID numbers) 
        from your report before uploading. This tool does not store your data, but protecting your privacy 
        is your responsibility.
    </div>
</div>
"""
