# ClinExplain AI - Frontend Documentation

## Overview

The ClinExplain AI frontend is a **Gradio-based web interface** designed with safety-first principles for medical AI applications. It provides transparent visualization of the AI pipeline without medical overreach.

---

## Architecture

### Component Structure

```
ui/
├── app.py                          # Main Gradio application
├── components/
│   ├── safety_banner.py            # Persistent disclaimer
│   ├── report_viewer.py            # Original report with highlights
│   ├── explanation_panel.py        # Patient-friendly summaries
│   └── metadata_display.py         # Analysis metrics
└── utils/
    ├── text_highlighter.py         # Source quote highlighting
    └── confidence_formatter.py     # Visual confidence indicators
```

### Design Principles

1. **Safety First**: Persistent disclaimers, no diagnostic language
2. **Transparency**: Show exactly what the AI analyzed
3. **Traceability**: Every finding links to source text
4. **Uncertainty Communication**: Visual confidence indicators
5. **Progressive Disclosure**: Tabbed interface for clarity

---

## Running the UI

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Gradio app
python ui/app.py

# Access at http://localhost:7860
```

### Kaggle Notebook

```python
# In a Kaggle notebook cell
!pip install gradio

# Run the app
from ui.app import app
app.launch(share=True)  # Creates public URL
```

---

## User Flow

### 1. Landing Page

**User sees:**
- Persistent medical disclaimer (cannot be dismissed)
- Usage guide (what tool does/doesn't do)
- Input section (paste text or upload PDF)

**Safety features:**
- Disclaimer is FIRST element
- Clear expectations set before interaction
- Privacy reminder about removing PII

### 2. Input Submission

**User can:**
- Paste clinical report text directly
- Upload PDF file (future enhancement)
- Click "Analyze Report" button

**Validation:**
- Button disabled until input provided
- Client-side length check
- Clear error messages if validation fails

### 3. Processing State

**User sees:**
- Step-by-step progress indicators
- Transparent pipeline stages
- Real-time status updates

**Stages shown:**
1. ✓ Validating input
2. ⏳ Extracting findings with MedGemma
3. ⏸️ Running safety checks
4. ⏸️ Generating explanation

### 4. Results Display

**Tabbed interface with 5 sections:**

#### Tab 1: Original Report
- Read-only display of original text
- Yellow highlights on source quotes
- Legend explaining highlights
- **Purpose**: Verify AI didn't hallucinate

#### Tab 2: Key Findings
- Structured list of extracted findings
- Each finding shows:
  - Extracted text
  - Source quote (verbatim)
  - Confidence level (visual dots)
  - Category (observation/normal/abnormal)
- **Purpose**: Show what AI extracted

#### Tab 3: Attention Flags
- Points for discussion with doctor
- NOT framed as diagnoses
- Context and source for each flag
- Severity indicators (info/warning)
- **Purpose**: Highlight items needing follow-up

#### Tab 4: Plain Language Summary
- Patient-friendly explanation
- 6th-8th grade reading level
- Medical terms explained
- Next steps guidance
- **Purpose**: Help understanding, not diagnosis

#### Tab 5: Analysis Details
- Technical metadata (collapsible)
- Safety check results
- Processing metrics
- Model information
- **Purpose**: Transparency about system

---

## Safety UX Patterns

### Disclaimer Banner

**Position**: Top of page, always visible

**Content**:
```
⚠️ IMPORTANT MEDICAL DISCLAIMER

This tool does NOT provide medical advice, diagnosis, or treatment.
It is for informational and educational purposes only.

Always consult a qualified healthcare provider for medical decisions.
```

**Design**:
- Orange/yellow background (caution color)
- Bold text, large font
- Cannot be dismissed or hidden

### Confidence Visualization

**High Confidence**: ●●●●● (5 filled dots, green)
**Medium Confidence**: ●●●○○ (3 filled dots, orange)
**Low Confidence**: ●○○○○ (1 filled dot, red)

**When confidence is low:**
- Explicit warning shown
- Defers to human expertise
- Suggests consulting doctor

### Error Handling

**Validation Errors**:
```
❌ Analysis Could Not Be Completed

Reason: Input validation failed
Details: Report text is too short (minimum 50 chars)

What to do:
• Ensure you've pasted the full report
• Check that the text is readable
• Contact support if this persists

⚠️ If you need urgent medical help, contact your doctor immediately.
```

**System Errors**:
- Clear error messages
- Actionable guidance
- Safety reminder even in failure
- No technical jargon

---

## Visual Design

### Color Palette

```css
Primary: #2C3E50 (Dark blue-gray) - Professional
Accent: #3498DB (Soft blue) - Trust
Warning: #F39C12 (Orange) - Caution
Error: #E74C3C (Red) - Alert
Success: #27AE60 (Green) - Confirmation
Background: #ECF0F1 (Light gray) - Neutral
```

**Rationale**: Medical UIs avoid bright colors that suggest urgency.

### Typography

- **Headings**: Inter (sans-serif, clean)
- **Body**: Georgia (serif, readable for long text)
- **Code/Data**: Fira Mono (monospace)

### Layout Principles

- **Single column**: No distracting sidebars
- **Generous whitespace**: Reduces cognitive load
- **Progressive disclosure**: Tabs for organization
- **Fixed disclaimer**: Always visible at top

---

## Edge Cases Handled

### 1. Poor Input

**Scenario**: User uploads non-medical text

**UI Response**:
```
❌ This doesn't appear to be a clinical report.
   The system detected no medical terminology.
   
   Please upload a radiology or clinical report.
```

### 2. Ambiguous Reports

**Scenario**: Contradictory statements in report

**UI Response**:
```
⚠️ Conflicting Information Detected

Finding 1: "No abnormalities"
Finding 2: "Mild opacity noted"
Confidence: ●○○○○ Very Low

The AI cannot reconcile these statements.
Your doctor will clarify the actual findings.
```

### 3. No Findings Extracted

**Scenario**: AI extracts nothing

**UI Response**:
```
No findings were extracted from this report.

This may happen if:
• The report contains only normal findings
• The text is too short or unclear
• The AI had low confidence in all extractions

Discuss the original report with your healthcare provider.
```

### 4. Model Uncertainty

**Scenario**: All extractions have low confidence

**UI Response**:
```
⚠️ Limited Confidence in Analysis

The AI could only extract 1 finding with high confidence.
This report may require specialized interpretation.

Recommendation: Discuss directly with your healthcare provider.
```

---

## Customization

### Changing Mock Mode

In `ui/app.py`, line 18:

```python
# For demo/testing (no MedGemma required)
pipeline = ClinExplainPipeline(use_mock=True)

# For production (requires MedGemma in Kaggle)
pipeline = ClinExplainPipeline(use_mock=False, model_path="/path/to/medgemma")
```

### Enabling PDF Upload

1. Uncomment PDF extraction code in `app.py`
2. Install PyPDF2: `pip install PyPDF2`
3. Implement `extract_text_from_pdf()` function

### Custom Styling

Edit `custom_css` variable in `ui/app.py`:

```python
custom_css = """
/* Your custom CSS here */
.disclaimer-banner {
    background: your-color;
}
"""
```

---

## Deployment Options

### Option 1: Local Demo

```bash
python ui/app.py
# Access at http://localhost:7860
```

### Option 2: Kaggle Notebook

```python
from ui.app import app
app.launch(share=True)  # Creates public shareable link
```

### Option 3: Hugging Face Spaces

1. Create new Space on Hugging Face
2. Upload project files
3. Set `app_file` to `ui/app.py`
4. Deploy

### Option 4: Gradio Cloud

```bash
gradio deploy ui/app.py
```

---

## Testing the UI

### Manual Testing Checklist

- [ ] Disclaimer visible on load
- [ ] Input validation works (too short, empty)
- [ ] Text input processes correctly
- [ ] Source quotes highlighted in original report
- [ ] Findings display with confidence levels
- [ ] Attention flags show when present
- [ ] Summary renders in markdown
- [ ] Metadata displays correctly
- [ ] Error states show helpful messages
- [ ] Clear button resets all fields

### Sample Test Reports

Use reports from `tests/sample_reports.json`:

```python
# In Python console
from tests.sample_reports import SAMPLE_REPORTS
report = SAMPLE_REPORTS[0]['text']
# Paste into UI
```

---

## Performance Considerations

### Loading Time

- **Mock mode**: Instant (no model loading)
- **Production mode**: 30-60s (MedGemma loading)

### Processing Time

- **Mock mode**: <1s per report
- **Production mode**: 2-5s per report (depending on length)

### Optimization Tips

1. **Lazy load model**: Only load when first report submitted
2. **Cache results**: Store recent analyses
3. **Batch processing**: Process multiple reports together
4. **GPU acceleration**: Use CUDA if available in Kaggle

---

## Accessibility

### Features Implemented

- **Semantic HTML**: Proper heading hierarchy
- **Color contrast**: WCAG AA compliant
- **Keyboard navigation**: All controls accessible via keyboard
- **Screen reader friendly**: Descriptive labels and ARIA attributes

### Future Enhancements

- [ ] High contrast mode toggle
- [ ] Font size adjustment
- [ ] Text-to-speech for summaries
- [ ] Multi-language support

---

## Security & Privacy

### Data Handling

- **No server-side storage**: Reports not saved
- **Client-side processing**: Data stays in browser session
- **No analytics**: No tracking or telemetry
- **PII warning**: Users reminded to remove personal info

### Recommendations

1. **Remove PII**: Name, DOB, ID numbers before upload
2. **Use HTTPS**: Deploy with SSL certificate
3. **Session isolation**: Each user gets isolated session
4. **No logging**: Don't log report content

---

## Troubleshooting

### Common Issues

**Issue**: Gradio not found
```bash
pip install gradio>=4.0.0
```

**Issue**: Import errors
```bash
# Ensure you're in project root
cd /path/to/med_project
python ui/app.py
```

**Issue**: Port already in use
```python
# Change port in app.py
app.launch(server_port=7861)
```

**Issue**: Slow processing
```python
# Enable mock mode for testing
pipeline = ClinExplainPipeline(use_mock=True)
```

---

## Future Enhancements

### Planned Features

1. **PDF Upload**: Full PDF text extraction
2. **Batch Processing**: Upload multiple reports
3. **Export Results**: Download as PDF/JSON
4. **Comparison View**: Compare multiple reports
5. **History**: View past analyses (session-only)

### Not Planned (Safety Reasons)

- ❌ Diagnostic suggestions
- ❌ Treatment recommendations
- ❌ Outcome predictions
- ❌ Medical advice chatbot
- ❌ Social sharing of results

---

## Contributing

### Code Style

- Follow PEP 8 for Python
- Use type hints
- Document all functions
- Write safety-first code

### Pull Request Guidelines

1. **Safety first**: No features that risk medical misinformation
2. **Test thoroughly**: Include manual testing checklist
3. **Document changes**: Update this file
4. **Maintain design**: Follow existing UX patterns

---

## License

Educational use only. See main LICENSE file.

---

## Contact

For questions about the UI:
- Review this documentation
- Check `ui/app.py` comments
- Refer to Gradio docs: https://gradio.app/docs

**Remember**: This is an educational tool. Always consult healthcare providers for medical advice.

---

**Version**: 1.0  
**Last Updated**: 2026-01-31  
**Status**: Production-Ready (Mock Mode) / Kaggle-Ready (Production Mode)
