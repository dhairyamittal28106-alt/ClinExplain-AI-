"""
ClinExplain AI - Gradio Frontend Application

A safety-first medical report interpretation interface.
Designed for transparency, clarity, and ethical restraint.
"""

import gradio as gr
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.pipeline import ClinExplainPipeline, PipelineResult
from ui.utils.text_highlighter import highlight_source_quotes
from ui.utils.confidence_formatter import format_confidence_visual, format_findings_html, format_flags_html
from ui.components.safety_banner import DISCLAIMER_HTML, USAGE_GUIDE_HTML
from ui.components.report_viewer import format_original_report
from ui.components.explanation_panel import format_patient_summary
from ui.components.metadata_display import format_metadata_panel

# Initialize pipeline (will use mock mode by default for demo)
# Set use_mock=False when running with actual MedGemma in Kaggle
pipeline = ClinExplainPipeline(use_mock=True, include_disclaimer=True)


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from uploaded PDF file.
    
    Args:
        file_path: Path to uploaded PDF
        
    Returns:
        Extracted text content
    """
    try:
        # TODO: Implement PDF extraction for production
        # For now, return instruction message
        return "PDF upload feature coming soon. Please paste text directly for now."
    except Exception as e:
        return f"Error reading PDF: {str(e)}"


def process_report(text_input: str, file_input) -> tuple:
    """
    Main processing function for clinical reports.
    
    Args:
        text_input: Pasted report text
        file_input: Uploaded PDF file
        
    Returns:
        Tuple of (original_html, findings_html, flags_html, summary_md, metadata_json, error_msg)
    """
    # Handle input source
    if file_input is not None:
        report_text = extract_text_from_pdf(file_input.name)
    elif text_input and text_input.strip():
        report_text = text_input.strip()
    else:
        return (
            "",
            "",
            "",
            "",
            {},
            "⚠️ Please provide a clinical report by pasting text or uploading a PDF."
        )
    
    # Run pipeline
    try:
        result: PipelineResult = pipeline.process(
            report_text,
            include_summary=True,
            filter_low_confidence=False
        )
        
        # Handle failure
        if not result.success:
            error_html = f"""
            <div class="med-banner danger">
                <h3 style="margin-top: 0; display: flex; align-items: center; gap: 0.5rem; color: var(--danger-text) !important;">
                    ❌ Analysis Could Not Be Completed
                </h3>
                <p><strong>Reason:</strong> {result.error}</p>
                <p><strong>What to do:</strong></p>
                <ul>
                    <li>Ensure you've pasted the full clinical report</li>
                    <li>Check that the text is readable and contains medical content</li>
                    <li>Verify the report is at least 50 characters long</li>
                </ul>
                <div class="med-banner warning" style="margin-top: 1rem; margin-bottom: 0;">
                    ⚠️ <strong>If you need urgent medical help, contact your doctor or emergency services immediately.</strong>
                </div>
            </div>
            """
            return ("", "", "", "", {}, error_html)
        
        # Format successful result
        original_html = format_original_report(
            report_text,
            result.extraction
        )
        
        findings_html = format_findings_html(
            result.extraction.get('findings', [])
        )
        
        flags_html = format_flags_html(
            result.extraction.get('attention_flags', [])
        )
        
        summary_md = format_patient_summary(
            result.summary,
            result.extraction.get('terminology', [])
        )
        
        metadata = format_metadata_panel(result)
        
        success_msg = f"""
        <div class="med-banner success">
            <strong>✓ Analysis Complete</strong> - {len(result.extraction.get('findings', []))} findings extracted, 
            {len(result.extraction.get('attention_flags', []))} attention flags identified
        </div>
        """
        
        return (
            original_html,
            findings_html,
            flags_html,
            summary_md,
            metadata,
            success_msg
        )
        
    except Exception as e:
        error_html = f"""
        <div class="med-banner danger">
            <h3 style="color: var(--danger-text) !important; margin-top: 0;">❌ System Error</h3>
            <p><strong>Error:</strong> {str(e)}</p>
            <p>Please try again or contact support if this persists.</p>
        </div>
        """
        return ("", "", "", "", {}, error_html)


def clear_all():
    """Reset all fields to initial state."""
    return ("", None, "", "", "", "", {}, "")


# Custom CSS for Professional Dark Hospital UI (Radiology Style)

custom_css = """
/* ===== FORCE HERO IMAGE SIZE (FINAL OVERRIDE) - KEEPING USER FIX ===== */
.gradio-container .hero-doctor-img {
    width: 380px !important;
    max-width: 380px !important;
    height: auto !important;
    object-fit: cover !important;
    border-radius: 16px !important;
}

/* Prevent any image from exploding layout */
.gradio-container img {
    max-width: 100%;
    height: auto;
}

/* ===== RADIOLOGY DARK THEME SYSTEM (DEFAULT) ===== */
:root {
    --font-primary: 'Inter', system-ui, -apple-system, sans-serif;
    
    /* Dark Mode Palette (Default) - Deep Navy/Charcoal */
    --bg-page: #0f172a;        /* Slate 900 - Deep Navy */
    --bg-card: #1e293b;        /* Slate 800 - Lighter Navy */
    --border-subtle: #334155;  /* Slate 700 */
    
    --text-main: #f8fafc;      /* Slate 50 - Whiteish */
    --text-muted: #94a3b8;     /* Slate 400 - Muted Grey */
    
    --primary-main: #2dd4bf;   /* Teal 400 - Bright Accent */
    --primary-dim: #115e59;    /* Teal 800 */
    --accent-blue: #38bdf8;    /* Sky 400 */
    
    --shadow-soft: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    --shadow-card: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
    
    --radius-card: 16px;
    
    /* Gradio overrides for dark mode consistency */
    --background-fill-primary: var(--bg-page) !important;
    --background-fill-secondary: var(--bg-card) !important;
    --block-background-fill: var(--bg-card) !important;
    --body-text-color: var(--text-main) !important;
}

/* LIGHT MODE OVERRIDES (Toggled via JS class 'light-mode') */
:root.light-mode,
body.light-mode,
.light-mode .gradio-container,
.gradio-container.light-mode {
    --bg-page: #ffffff !important;
    --bg-card: #ffffff !important;
    --border-subtle: #e2e8f0 !important;
    
    --text-main: #1e293b !important;
    --text-muted: #64748b !important;
    
    --primary-main: #0f766e !important;
    --primary-dim: #115e59 !important;
    --accent-blue: #0ea5e9 !important;
    
    --shadow-soft: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
    --shadow-card: 0 10px 15px -3px rgba(0, 0, 0, 0.05) !important;
    
    --background-fill-primary: #ffffff !important;
    --background-fill-secondary: #f8fafc !important;
    --block-background-fill: #ffffff !important;
    --body-text-color: #1e293b !important;
}

/* Force light mode styles on all elements when light-mode is active */
body.light-mode,
body.light-mode .gradio-container,
.gradio-container.light-mode {
    background-color: #ffffff !important;
    color: #1e293b !important;
}

body.light-mode .med-card,
.gradio-container.light-mode .med-card {
    background-color: #ffffff !important;
    border-color: #e2e8f0 !important;
    color: #1e293b !important;
}

/* Standard Body Styles */
body, .gradio-container {
    background-color: var(--bg-page) !important;
    color: var(--text-main) !important;
    font-family: var(--font-primary) !important;
    transition: background-color 0.3s ease, color 0.3s ease;
}

/* Force light mode on all elements when active */
:root.light-mode *,
body.light-mode *,
.gradio-container.light-mode * {
    transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease !important;
}

/* Components */
.med-card {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-card) !important;
    padding: 2rem !important;
    box-shadow: var(--shadow-soft) !important;
    transition: box-shadow 0.2s ease, background-color 0.3s ease, border-color 0.3s ease;
}

.med-card:hover {
    box-shadow: var(--shadow-card) !important;
    border-color: var(--primary-main) !important; /* Subtle highlight on hover */
}

/* New Split Hero Section - GRID LAYOUT */
.hero-wrapper {
    background-color: var(--bg-page) !important; /* Matches background for seamless look */
    border-bottom: 1px solid var(--border-subtle);
    padding: 3rem 1rem;
    margin-bottom: 2rem;
    width: 100%;
    transition: background-color 0.3s ease;
}

.hero-content {
    max-width: 1200px;
    margin: 0 auto;
    display: grid !important;
    grid-template-columns: 1fr 380px !important;
    gap: 3rem !important;
    align-items: center !important;
}

.hero-text {
    /* Grid handles sizing */
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 800;
    color: var(--text-main) !important;
    line-height: 1.1;
    margin-bottom: 1.5rem;
    letter-spacing: -0.03em;
}

.hero-subtitle {
    font-size: 1.25rem;
    color: var(--text-muted) !important;
    line-height: 1.6;
    margin-bottom: 0;
    max-width: 90%;
}

.hero-image-container {
    display: flex;
    justify-content: flex-end;
    width: 380px !important;
}

.hero-doctor-img {
    width: 380px !important;      /* FORCE FIXED WIDTH */
    max-width: 380px !important;  
    height: auto !important;
    border-radius: 16px !important;
    object-fit: cover;
    box-shadow: var(--shadow-card) !important;
    display: block;
}

/* Mobile Responsive */
@media (max-width: 900px) {
    .hero-content { 
        grid-template-columns: 1fr !important;
        text-align: center; 
        gap: 2rem !important;
    }
    
    .hero-text { width: 100%; }
    .hero-subtitle { margin: 0 auto; }
    
    .hero-image-container { 
        width: 100% !important;
        justify-content: center;
    }
    
    .hero-doctor-img { 
        width: 100% !important;
        max-width: 380px !important;
    }
    
    .hero-title { font-size: 2.5rem; }
}

/* Trust Banner with Avatars */
.trust-banner-container {
    display: flex;
    align-items: center;
    gap: 1rem;
    background: var(--bg-card); /* Adapted for Dark Mode */
    border: 1px solid var(--primary-main);
    border-radius: 9999px;
    padding: 0.5rem 1.5rem 0.5rem 0.5rem;
    width: fit-content;
    margin-top: 1.5rem;
}

.trust-avatars {
    display: flex;
    height: 40px;
}

.trust-avatars img {
    height: 40px;
    width: auto;
    border-radius: 9999px; /* Fallback if not circular in image */
}

.trust-text {
    font-weight: 600;
    color: var(--primary-main);
    font-size: 0.9rem;
}

/* Form Elements */
textarea, .gr-input {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 12px !important;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.02) !important;
    padding: 1rem !important;
    color: var(--text-main) !important;
}

button.primary {
    background: linear-gradient(135deg, var(--primary-main), var(--accent-blue)) !important;
    color: white !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    padding: 1rem 2.5rem !important;
    font-size: 1.1rem !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3) !important;
}

/* Tabs */
.tab-nav { border-bottom: none !important; margin-bottom: 1rem !important; }
.tab-nav button { border: none !important; background: transparent !important; font-weight: 500 !important; color: var(--text-muted) !important; }
.tab-nav button.selected { color: var(--primary-main) !important; font-weight: 700 !important; border-bottom: 2px solid var(--primary-main) !important; }

/* Status Banners */
.med-banner { padding: 1rem; border-radius: 12px; margin-bottom: 1rem; display: flex; align-items: flex-start; gap: 0.75rem; }
.med-banner.warning { background: #451a03; border: 1px solid #d97706; color: #fbbf24; }
.med-banner.success { background: #064e3b; border: 1px solid #10b981; color: #10b981; }
.med-banner.info { background: #1e3a8a; border: 1px solid #3b82f6; color: #60a5fa; }
.med-banner.danger { background: #450a0a; border: 1px solid #ef4444; color: #f87171; }

footer { display: none !important; }
"""

# HTML for Hero Section
HERO_HTML = """
<div class="hero-wrapper">
    <div class="hero-content">
        <div class="hero-text">
            <h1 class="hero-title">Medical Insights,<br>Simplified.</h1>
            <p class="hero-subtitle">ClinExplain AI translates complex clinical reports into clear, plain language you can trust.</p>
            
            <div class="trust-banner-container">
                <div class="trust-avatars">
                    <!-- Serving from /images route mounted via FastAPI -->
                    <img src="/images/team1.jpg" alt="Doctor 1">
                    <img src="/images/team2.jpg" alt="Doctor 2">
                </div>
                <div class="trust-text">
                    Trusted by Medical Professionals
                </div>
            </div>
        </div>
        <div class="hero-image-container">
            <img src="/images/doctor.png" class="hero-doctor-img" alt="Friendly Doctor">
        </div>
    </div>
</div>
"""

# HTML for Team Section
TEAM_HTML = """
<div style="margin-top: 3rem; margin-bottom: 2rem;">
    <h3 style="text-align: center; margin-bottom: 2rem; color: var(--text-main);">Meet Our Medical Advisory Team</h3>
    <div style="display: flex; justify-content: center; gap: 3rem; flex-wrap: wrap;">
        <div style="display: flex; flex-direction: column; align-items: center; text-align: center;">
            <img src="/images/team1.jpg" style="width: 120px; height: 120px; border-radius: 50%; object-fit: cover; box-shadow: var(--shadow-soft); border: 3px solid white;">
            <div style="margin-top: 1rem; font-weight: 600; color: var(--text-main);"></div>
            <div style="font-size: 0.9rem; color: var(--text-muted);">Chief Radiologist</div>
        </div>
        <div style="display: flex; flex-direction: column; align-items: center; text-align: center;">
            <img src="/images/team2.jpg" style="width: 120px; height: 120px; border-radius: 50%; object-fit: cover; box-shadow: var(--shadow-soft); border: 3px solid white;">
            <div style="margin-top: 1rem; font-weight: 600; color: var(--text-main);"></div>
            <div style="font-size: 0.9rem; color: var(--text-muted);">Clinical Director</div>
        </div>
    </div>
</div>
"""

# Build Gradio Interface
with gr.Blocks(
    theme=gr.themes.Soft(
        primary_hue="teal",
        secondary_hue="slate",
        font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"],
        spacing_size="lg",
        radius_size="lg",
        text_size="lg",
    ).set(
        body_background_fill="var(--bg-page)",
        block_background_fill="var(--bg-card)",
        block_border_color="var(--border-subtle)",
        body_text_color="var(--text-main)",
        block_label_text_color="var(--text-muted)",
        input_background_fill="var(--bg-card)",
        button_primary_background_fill="linear-gradient(135deg, var(--primary-main), var(--accent-blue))",
        button_primary_text_color="white",
    ),
    css=custom_css,
    title="ClinExplain AI",
    analytics_enabled=False
) as demo:

    # Hero (Full Width visually handled by CSS targeting)
    gr.HTML(HERO_HTML)
    
    # Main Layout Container
    with gr.Row():
        # Input Section
        with gr.Column(scale=5):
            gr.Markdown("### 📄 Input Report", elem_classes=["med-card-title"])
            
            with gr.Group():
                text_input = gr.Textbox(
                    placeholder="Paste your clinical report here...",
                    lines=12,
                    max_lines=20,
                    show_label=False,
                    elem_id="report-input",
                    container=False
                )
                
                with gr.Row():
                    file_input = gr.File(
                        label="Upload PDF",
                        file_types=[".pdf"],
                        scale=3,
                        type="filepath",
                        min_width=100,
                        container=False
                    )
                    analyze_btn = gr.Button(
                        "Analyze Report",
                        variant="primary",
                        scale=2,
                        size="lg"
                    )
            
            # Guidelines / Disclaimer
            gr.HTML("""
            <div style="margin-top: 2rem; padding-top: 1rem; border-top: 1px solid var(--border-subtle);">
                <p style="font-size: 0.85rem; color: var(--text-muted); line-height: 1.5;">
                    <strong>Privacy Note:</strong> All processing happens locally. 
                    Please remove personal identifiers (Name, MRN, DOB) before uploading.
                    <br><br>
                    <strong>Disclaimer:</strong> This tool is for educational purposes only and does not constitute medical advice.
                </p>
            </div>
            """)
            
        # Results Section
        with gr.Column(scale=7):
            status_msg = gr.HTML(label="Status", visible=True)
            
            # EMPTY STATE PLACEHOLDER
            with gr.Group(visible=True) as placeholder_card:
                gr.HTML("""
                <div class="med-card" style="text-align: center; padding: 4rem 2rem !important; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 400px;">
                    <div style="font-size: 3.5rem; margin-bottom: 1.5rem; opacity: 0.8;">📋</div>
                    <h3 style="color: var(--text-main); margin-bottom: 0.75rem; font-size: 1.5rem;">Ready to Analyze</h3>
                    <p style="color: var(--text-muted); font-size: 1.1rem; max-width: 350px; margin: 0 auto; line-height: 1.6;">
                        Upload a report to see plain-language explanations and key medical findings.
                    </p>
                </div>
                """)

            # RESULTS CONTAINER
            with gr.Group(visible=False) as results_container:
                with gr.Tabs(elem_id="results-tabs"):
                    with gr.Tab("Summary"):
                        summary_display = gr.HTML()
                    
                    with gr.Tab("Findings"):
                        findings_display = gr.HTML()
                    
                    with gr.Tab("Flags"):
                        flags_display = gr.HTML()
                    
                    with gr.Tab("Original"):
                        original_report_display = gr.HTML()
                    
                    with gr.Tab("Info"):
                        metadata_display = gr.JSON()
                
                clear_btn = gr.Button(
                    "Start New Analysis",
                    variant="secondary",
                    size="sm"
                )

    # Team Section
    gr.HTML(TEAM_HTML)

    # Footer
    gr.HTML("""
    <div style="text-align: center; margin-top: 4rem; padding-bottom: 2rem; color: var(--text-muted);">
        <p style="font-size: 0.9rem;">
            Privacy First • Educational Use Only • Not a Medical Device
        </p>
    </div>
    """)

    # Event Handlers
    def analyze_with_visibility(text, file):
        results = process_report(text, file)
        return results + (gr.update(visible=False), gr.update(visible=True))

    def clear_all_wrapped():
        results = clear_all()
        return results + (gr.update(visible=True), gr.update(visible=False))

    analyze_btn.click(
        fn=analyze_with_visibility,
        inputs=[text_input, file_input],
        outputs=[
            original_report_display,
            findings_display,
            flags_display,
            summary_display,
            metadata_display,
            status_msg,
            placeholder_card,
            results_container
        ]
    )
    
    clear_btn.click(
        fn=clear_all_wrapped,
        inputs=[],
        outputs=[
            text_input,
            file_input,
            original_report_display,
            findings_display,
            flags_display,
            summary_display,
            metadata_display,
            status_msg,
            placeholder_card,
            results_container
        ]
    )


# FastAPI Integration for Static Asset Serving
if __name__ == "__main__":
    try:
        from fastapi import FastAPI
        from fastapi.staticfiles import StaticFiles
        import uvicorn
        
        # Create Main App
        app = FastAPI()
        
        # Mount the "public/images" directory to "/images" path
        # This allows accessing http://localhost:7864/images/doctor.png
        app.mount("/images", StaticFiles(directory="public/images"), name="images")
        
        # Mount Gradio App
        # We allow allowed_paths still just in case, but the primary serving is via FastAPI
        app = gr.mount_gradio_app(
    app,
    demo,
    path="/",
    allowed_paths=["public/images"],
    css=custom_css
)

        
        print("Starting FastAPI server on port 7864...")
        uvicorn.run(app, host="0.0.0.0", port=7870)
        
    except ImportError as e:
        print(f"Could not import FastAPI/Uvicorn: {e}")
        print("Falling back to standard Gradio launch (images might not load with /images/ path)")
        demo.launch(
            server_name="0.0.0.0",
            server_port=7864,
            share=False,
            allowed_paths=["public"]
        )
