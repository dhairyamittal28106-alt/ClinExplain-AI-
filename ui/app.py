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
            <div style="padding: 20px; background: #fee; border-left: 4px solid #e74c3c; border-radius: 4px;">
                <h3 style="color: #e74c3c; margin-top: 0;">❌ Analysis Could Not Be Completed</h3>
                <p><strong>Reason:</strong> {result.error}</p>
                <p><strong>What to do:</strong></p>
                <ul>
                    <li>Ensure you've pasted the full clinical report</li>
                    <li>Check that the text is readable and contains medical content</li>
                    <li>Verify the report is at least 50 characters long</li>
                </ul>
                <p style="margin-top: 15px; padding: 10px; background: #fff3cd; border-radius: 4px;">
                    ⚠️ <strong>If you need urgent medical help, contact your doctor or emergency services immediately.</strong>
                </p>
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
        <div style="padding: 15px; background: #d4edda; border-left: 4px solid #28a745; border-radius: 4px; margin-bottom: 20px;">
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
        <div style="padding: 20px; background: #fee; border-left: 4px solid #e74c3c; border-radius: 4px;">
            <h3 style="color: #e74c3c; margin-top: 0;">❌ System Error</h3>
            <p><strong>Error:</strong> {str(e)}</p>
            <p>Please try again or contact support if this persists.</p>
        </div>
        """
        return ("", "", "", "", {}, error_html)


def clear_all():
    """Reset all fields to initial state."""
    return ("", None, "", "", "", "", {}, "")


# Custom CSS for medical-grade UI
custom_css = """
/* Medical-grade color palette */
:root {
    --primary-color: #2C3E50;
    --accent-color: #3498DB;
    --warning-color: #F39C12;
    --error-color: #E74C3C;
    --success-color: #27AE60;
    --bg-light: #ECF0F1;
}

/* Disclaimer banner styling */
.disclaimer-banner {
    background: linear-gradient(135deg, #F39C12 0%, #E67E22 100%);
    color: white;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;
    border-left: 6px solid #D35400;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.disclaimer-banner h2 {
    margin-top: 0;
    font-size: 1.3em;
    font-weight: 700;
}

/* Usage guide styling */
.usage-guide {
    background: #E8F4F8;
    padding: 20px;
    border-radius: 8px;
    border-left: 4px solid #3498DB;
    margin-bottom: 20px;
}

.usage-guide h3 {
    color: #2C3E50;
    margin-top: 0;
}

.usage-guide ul {
    margin: 10px 0;
    padding-left: 20px;
}

/* Report sections */
.report-section {
    background: white;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 15px;
    border: 1px solid #ddd;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.report-section h3 {
    color: var(--primary-color);
    margin-top: 0;
    border-bottom: 2px solid var(--accent-color);
    padding-bottom: 10px;
}

/* Confidence indicators */
.confidence-high { color: #27AE60; font-weight: 600; }
.confidence-medium { color: #F39C12; font-weight: 600; }
.confidence-low { color: #E74C3C; font-weight: 600; }

/* Source highlighting */
.source-highlight {
    background: #FFF9C4;
    padding: 2px 4px;
    border-radius: 3px;
    font-weight: 500;
    border-bottom: 2px solid #FBC02D;
}

/* Attention flags */
.flag-info {
    background: #E3F2FD;
    border-left: 4px solid #2196F3;
    padding: 12px;
    margin: 10px 0;
    border-radius: 4px;
}

.flag-warning {
    background: #FFF3E0;
    border-left: 4px solid #FF9800;
    padding: 12px;
    margin: 10px 0;
    border-radius: 4px;
}

/* Buttons */
.primary-button {
    background: var(--accent-color) !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 12px 24px !important;
    border-radius: 6px !important;
}

/* Responsive typography */
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    line-height: 1.6;
}

.summary-text {
    font-family: Georgia, serif;
    font-size: 1.05em;
    line-height: 1.8;
    color: #2C3E50;
}
"""


# Build Gradio Interface
with gr.Blocks(
    theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="gray",
        neutral_hue="slate"
    ),
    css=custom_css,
    title="ClinExplain AI - Medical Report Interpreter"
) as app:
    
    # Header
    gr.Markdown("""
    # 🏥 ClinExplain AI
    ### Human-Centered Medical Report Interpretation System
    """)
    
    # Persistent Disclaimer Banner
    gr.HTML(DISCLAIMER_HTML)
    
    # Usage Guide
    gr.HTML(USAGE_GUIDE_HTML)
    
    # Input Section
    gr.Markdown("## 📄 Upload or Paste Clinical Report")
    
    with gr.Row():
        with gr.Column(scale=2):
            text_input = gr.Textbox(
                label="Paste Report Text",
                placeholder="Paste your clinical or radiology report here...\n\nExample:\nChest X-ray demonstrates mild cardiomegaly. Lungs are clear bilaterally. No acute infiltrates. No pleural effusion or pneumothorax identified.",
                lines=12,
                max_lines=20
            )
        
        with gr.Column(scale=1):
            file_input = gr.File(
                label="Or Upload PDF",
                file_types=[".pdf"],
                type="filepath"
            )
            
            gr.Markdown("""
            **Supported formats:**
            - Plain text (paste directly)
            - PDF files (upload)
            
            **Privacy Note:**
            Remove personal information (name, DOB, ID numbers) before uploading.
            """)
    
    # Action Buttons
    with gr.Row():
        analyze_btn = gr.Button(
            "🔍 Analyze Report",
            variant="primary",
            size="lg"
        )
        clear_btn = gr.Button(
            "🔄 Clear All",
            variant="secondary"
        )
    
    # Status Message
    status_msg = gr.HTML(label="Status")
    
    # Results Section (initially hidden via empty state)
    gr.Markdown("---")
    gr.Markdown("## 📊 Analysis Results")
    
    with gr.Tabs() as results_tabs:
        
        # Tab 1: Original Report with Highlights
        with gr.Tab("📋 Original Report"):
            gr.Markdown("""
            **Your original report with source highlighting**
            
            Yellow highlights show text that was used by the AI to extract findings.
            This helps you verify that the AI didn't hallucinate or misinterpret.
            """)
            original_report_display = gr.HTML(label="Report with Source Highlights")
        
        # Tab 2: Extracted Findings
        with gr.Tab("🔍 Key Findings"):
            gr.Markdown("""
            **Structured findings extracted from your report**
            
            Each finding includes:
            - The extracted information
            - Source quote from your report
            - Confidence level
            - Category
            """)
            findings_display = gr.HTML(label="Extracted Findings")
        
        # Tab 3: Attention Flags
        with gr.Tab("⚠️ Attention Flags"):
            gr.Markdown("""
            **Points to discuss with your doctor**
            
            These are NOT diagnoses. They are items that may require clinical correlation.
            Your doctor will interpret these in the context of your complete health picture.
            """)
            flags_display = gr.HTML(label="Attention Flags")
        
        # Tab 4: Patient-Friendly Summary
        with gr.Tab("💬 Plain Language Summary"):
            gr.Markdown("""
            **Medical terms explained in everyday language**
            
            This summary is written at a 6th-8th grade reading level to help you
            understand the medical terminology in your report.
            """)
            summary_display = gr.Markdown(label="Patient Summary")
        
        # Tab 5: Analysis Metadata
        with gr.Tab("⚙️ Analysis Details"):
            gr.Markdown("""
            **Technical details about the analysis**
            
            This shows what the system did behind the scenes, including:
            - Number of findings extracted
            - Safety check results
            - Confidence metrics
            - Processing information
            """)
            metadata_display = gr.JSON(label="Metadata")
    
    # Event Handlers
    analyze_btn.click(
        fn=process_report,
        inputs=[text_input, file_input],
        outputs=[
            original_report_display,
            findings_display,
            flags_display,
            summary_display,
            metadata_display,
            status_msg
        ]
    )
    
    clear_btn.click(
        fn=clear_all,
        inputs=[],
        outputs=[
            text_input,
            file_input,
            original_report_display,
            findings_display,
            flags_display,
            summary_display,
            metadata_display,
            status_msg
        ]
    )
    
    # Footer
    gr.Markdown("---")
    gr.Markdown("""
    ### 📚 About This Tool
    
    **ClinExplain AI** is an educational system designed to help patients and learners understand clinical reports.
    It uses MedGemma (inference only) to extract and explain medical findings.
    
    **What this tool does:**
    - Extracts key findings from clinical reports
    - Explains medical terminology in plain language
    - Shows exactly what text the AI analyzed
    
    **What this tool does NOT do:**
    - Diagnose medical conditions
    - Recommend treatments
    - Replace your doctor's interpretation
    - Predict medical outcomes
    
    **Version:** 1.0 | **Status:** Educational Demo | **Model:** MedGemma (Mock Mode)
    
    ---
    
    **⚠️ Remember:** Always consult qualified healthcare providers for medical advice.
    This tool is for informational purposes only.
    """)


# Launch configuration
if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,  # Set to True for public sharing
        show_error=True,
        quiet=False
    )
