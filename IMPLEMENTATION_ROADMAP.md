# ClinExplain AI: Implementation Roadmap

## Current Status

**Completed Components** ✅:
1. System architecture design
2. Prompting strategy documentation
3. Limitations and ethical considerations documentation
4. Project structure setup
5. Configuration module (`src/config.py`)
6. Input validation module (`src/validator.py`)
7. Prompt templates module (`src/prompts.py`)
8. Post-processing and safety module (`src/postprocessor.py`)
9. Requirements specification

**Remaining Components** 🔨:
1. MedGemma inference wrapper
2. Output formatter
3. Utility functions
4. Test suite
5. Sample data
6. Gradio UI (optional)
7. Kaggle notebook
8. Evaluation framework

---

## Implementation Phases

### Phase 1: Core Inference (Next Steps)

**Goal**: Get basic end-to-end pipeline working

#### 1.1 MedGemma Inference Wrapper (`src/inference.py`)

**Purpose**: Interface with MedGemma model for extraction

**Key Functions**:
```python
class MedGemmaInference:
    def __init__(self, model_name: str, api_key: Optional[str] = None)
    def extract_findings(self, report_text: str) -> Dict[str, Any]
    def simplify_findings(self, structured_findings: Dict) -> Dict[str, Any]
    def _call_model(self, prompt: str) -> str
```

**Implementation Notes**:
- Use Google Generative AI SDK for MedGemma access
- Handle API errors gracefully (timeouts, rate limits)
- Implement retry logic with exponential backoff
- Log all API calls for debugging
- Use low temperature (0.1) for consistency

**Dependencies**:
- `google-generativeai` package
- API key from Kaggle secrets or environment variable

**Testing**:
- Mock API responses for unit tests
- Test with sample reports
- Verify JSON parsing works

---

#### 1.2 Output Formatter (`src/formatter.py`)

**Purpose**: Convert structured extractions into user-friendly output

**Key Functions**:
```python
class OutputFormatter:
    def format_findings(self, extraction: Dict) -> str
    def format_attention_flags(self, flags: List[Dict]) -> str
    def format_patient_summary(self, summary: Dict) -> str
    def format_full_output(self, extraction: Dict, summary: Dict) -> str
    def calculate_readability(self, text: str) -> float
```

**Implementation Notes**:
- Use markdown for formatting (Gradio/Jupyter friendly)
- Add color coding for severity levels
- Include confidence indicators
- Always prepend disclaimer
- Calculate Flesch-Kincaid readability score

**Dependencies**:
- `textstat` for readability scoring
- Markdown formatting utilities

---

#### 1.3 Main Pipeline (`src/pipeline.py`)

**Purpose**: Orchestrate entire workflow

**Key Functions**:
```python
class ClinExplainPipeline:
    def __init__(self, model_name: str, strict_mode: bool = True)
    def process(self, report_text: str) -> Dict[str, Any]
    def _validate_input(self, text: str) -> ValidationResult
    def _extract_findings(self, text: str) -> Dict[str, Any]
    def _post_process(self, raw_output: str, original: str) -> SafetyCheckResult
    def _generate_summary(self, findings: Dict) -> Dict[str, Any]
    def _format_output(self, findings: Dict, summary: Dict) -> str
```

**Workflow**:
1. Validate input → reject if invalid
2. Extract findings with MedGemma → parse JSON
3. Post-process for safety → filter violations
4. Generate patient summary → simplify
5. Format final output → add disclaimers
6. Return structured result

---

### Phase 2: Testing & Validation

#### 2.1 Unit Tests

**Files to Create**:
- `tests/test_validator.py`: Test input validation logic
- `tests/test_postprocessor.py`: Test safety filters
- `tests/test_formatter.py`: Test output formatting
- `tests/test_prompts.py`: Test prompt building

**Coverage Goals**:
- Input validation: edge cases (empty, too long, non-medical)
- Post-processing: forbidden phrases, schema validation
- Formatting: readability, disclaimer inclusion

---

#### 2.2 Integration Tests

**Test End-to-End Pipeline**:
- Normal reports (no abnormalities)
- Abnormal reports (clear findings)
- Ambiguous reports (uncertain language)
- Edge cases (very short, very long)

**Sample Reports** (`tests/sample_reports.json`):
```json
[
  {
    "id": "normal_chest_xray",
    "text": "Chest X-ray: Heart size normal. Lungs clear. No acute findings.",
    "expected_findings_count": 2,
    "expected_flags_count": 0
  },
  {
    "id": "abnormal_ct",
    "text": "CT abdomen: 3.2 cm mass in right kidney. Requires further evaluation.",
    "expected_findings_count": 1,
    "expected_flags_count": 1
  }
]
```

---

#### 2.3 Safety Tests

**Adversarial Testing**:
- Try to elicit diagnoses
- Try to get treatment recommendations
- Test with non-medical text
- Test with PII-containing text

**Expected Behavior**:
- All forbidden phrases should be caught
- Diagnostic language should be filtered
- Low-confidence extractions should be flagged

---

### Phase 3: User Interface

#### 3.1 Gradio Interface (`ui/app.py`)

**Features**:
- Text area for report input
- Submit button
- Output display with formatted results
- Disclaimer prominently displayed
- Example reports dropdown
- Clear/reset button

**Layout**:
```
┌─────────────────────────────────────┐
│  ClinExplain AI                     │
│  ⚠️ Educational Tool - Not Medical  │
│     Advice                          │
├─────────────────────────────────────┤
│  Input Report:                      │
│  ┌─────────────────────────────┐   │
│  │ [Text area]                 │   │
│  │                             │   │
│  └─────────────────────────────┘   │
│  [Example Reports ▼] [Submit]      │
├─────────────────────────────────────┤
│  Results:                           │
│  ┌─────────────────────────────┐   │
│  │ Key Findings:               │   │
│  │ • Finding 1                 │   │
│  │ • Finding 2                 │   │
│  │                             │   │
│  │ Attention Flags:            │   │
│  │ ⚠️ Flag 1                   │   │
│  │                             │   │
│  │ Patient Summary:            │   │
│  │ [Plain language summary]    │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

**Implementation**:
```python
import gradio as gr
from src.pipeline import ClinExplainPipeline

pipeline = ClinExplainPipeline()

def process_report(report_text):
    result = pipeline.process(report_text)
    return result['formatted_output']

interface = gr.Interface(
    fn=process_report,
    inputs=gr.Textbox(lines=10, label="Clinical Report"),
    outputs=gr.Markdown(label="Analysis Results"),
    title="ClinExplain AI",
    description="⚠️ Educational tool only. Not medical advice.",
    examples=[...],
)

interface.launch()
```

---

### Phase 4: Kaggle Notebook

#### 4.1 Notebook Structure

**Sections**:
1. **Introduction**: Project overview, disclaimers
2. **Setup**: Install dependencies, import modules
3. **Configuration**: Set API keys, model parameters
4. **Data Loading**: Load sample reports (if any)
5. **Pipeline Demo**: Run examples through system
6. **Evaluation**: Test on sample reports, show metrics
7. **Interactive Demo**: Gradio interface
8. **Limitations**: Discuss known issues
9. **Conclusion**: Summary, future work

**Code Cells**:
```python
# Cell 1: Setup
!pip install -q google-generativeai gradio textstat jsonschema

# Cell 2: Imports
from src.pipeline import ClinExplainPipeline
from src.validator import validate_input
from src.config import get_primary_disclaimer

# Cell 3: Initialize
pipeline = ClinExplainPipeline(
    model_name="google/medgemma-2b",
    strict_mode=True
)

# Cell 4: Example
sample_report = """
Chest X-ray demonstrates mild cardiomegaly...
"""
result = pipeline.process(sample_report)
print(result['formatted_output'])

# Cell 5: Gradio UI
import gradio as gr
# ... (UI code)
```

---

### Phase 5: Evaluation & Documentation

#### 5.1 Evaluation Framework (`docs/EVALUATION.md`)

**Metrics to Track**:
1. **Extraction Accuracy**: Manual review of 20-30 reports
2. **Hallucination Rate**: % of outputs with fabricated info
3. **Safety Violations**: Count of forbidden phrases
4. **Readability**: Flesch-Kincaid scores
5. **Completeness**: % of key findings captured

**Evaluation Process**:
1. Collect diverse sample reports
2. Run through pipeline
3. Manually review outputs
4. Calculate metrics
5. Document findings

---

#### 5.2 Design Decisions (`docs/DESIGN_DECISIONS.md`)

**Document Why**:
- Extraction vs. generation approach
- JSON schema enforcement
- Low temperature inference
- Forbidden phrase filtering
- Prominent disclaimers
- Conservative uncertainty handling

---

### Phase 6: Polish & Submission

#### 6.1 Code Quality

**Tasks**:
- [ ] Run `black` for formatting
- [ ] Run `flake8` for linting
- [ ] Run `mypy` for type checking
- [ ] Ensure all tests pass
- [ ] Add docstrings to all functions
- [ ] Update README with final instructions

---

#### 6.2 Documentation Review

**Checklist**:
- [ ] README is clear and complete
- [ ] ARCHITECTURE.md is accurate
- [ ] LIMITATIONS.md covers all known issues
- [ ] PROMPTING_STRATEGY.md reflects actual prompts
- [ ] All disclaimers are prominent
- [ ] License is appropriate

---

#### 6.3 Kaggle Submission

**Preparation**:
1. Test notebook in Kaggle environment
2. Ensure all dependencies are available
3. Verify MedGemma access works
4. Add clear markdown explanations
5. Include example outputs
6. Highlight safety features
7. Acknowledge limitations

**Submission Checklist**:
- [ ] Notebook runs end-to-end without errors
- [ ] All outputs are visible
- [ ] Disclaimers are prominent
- [ ] Code is well-commented
- [ ] Evaluation results are included
- [ ] Limitations are clearly stated

---

## Risk Mitigation

### Technical Risks

| Risk | Mitigation |
|------|------------|
| MedGemma API unavailable | Implement fallback, clear error messages |
| Model produces invalid JSON | Robust parsing, retry logic |
| Rate limiting | Implement backoff, queue requests |
| Hallucinations | Multi-layer safety checks, source verification |

### Ethical Risks

| Risk | Mitigation |
|------|------------|
| Users treat as medical advice | Prominent disclaimers, no actionable recommendations |
| Diagnostic language slips through | Comprehensive forbidden phrase list, post-processing |
| Missing critical findings | Acknowledge incompleteness in every output |
| PII exposure | User warnings, no data storage |

---

## Success Criteria

**Minimum Viable Product**:
- [ ] End-to-end pipeline works
- [ ] Extracts findings from sample reports
- [ ] Generates patient-friendly summaries
- [ ] Passes all safety checks
- [ ] Kaggle notebook runs successfully

**Stretch Goals**:
- [ ] Gradio UI deployed
- [ ] Comprehensive test suite (80%+ coverage)
- [ ] Evaluation on 50+ sample reports
- [ ] Readability scores consistently 6th-8th grade
- [ ] Zero safety violations in testing

---

## Timeline Estimate

**Assuming focused work**:

- **Phase 1 (Core Inference)**: 2-3 days
- **Phase 2 (Testing)**: 1-2 days
- **Phase 3 (UI)**: 1 day
- **Phase 4 (Notebook)**: 1 day
- **Phase 5 (Evaluation)**: 1-2 days
- **Phase 6 (Polish)**: 1 day

**Total**: ~7-10 days of focused development

---

## Next Immediate Steps

1. **Implement `src/inference.py`**: MedGemma wrapper
2. **Implement `src/formatter.py`**: Output formatting
3. **Implement `src/pipeline.py`**: Main orchestration
4. **Create sample reports**: Test data in `tests/sample_reports.json`
5. **Test end-to-end**: Run pipeline on samples
6. **Iterate on prompts**: Refine based on results

---

## Questions to Resolve

Before proceeding with implementation:

1. **MedGemma Access**: How will we access MedGemma in Kaggle?
   - Via Gemini API?
   - Via Kaggle Models?
   - Local inference?

2. **Sample Data**: Where to get realistic clinical reports?
   - Public datasets (MIMIC-III, etc.)?
   - Synthetic examples?
   - User-provided?

3. **Evaluation Ground Truth**: How to validate correctness?
   - Manual review only?
   - Expert annotation?
   - Automated metrics?

4. **Deployment Target**: Final delivery format?
   - Kaggle notebook only?
   - Gradio app link?
   - GitHub repo?

---

**Status**: Ready to proceed with Phase 1 implementation.

**Last Updated**: 2026-01-28
