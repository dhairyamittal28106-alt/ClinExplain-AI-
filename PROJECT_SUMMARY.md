# ClinExplain AI: Project Summary

## What Has Been Built

This document provides a high-level overview of the ClinExplain AI project structure and design rationale.

---

## Project Vision

**ClinExplain AI** is a human-centered AI system designed to help patients and learners understand complex clinical and radiology reports. It prioritizes **safety, transparency, and ethical restraint** over technical sophistication.

### Core Principles

1. **Safety First**: Every design decision prioritizes preventing medical misinformation
2. **Extraction Over Generation**: Summarize existing text rather than create new claims
3. **Transparency**: Explicit uncertainty communication and prominent disclaimers
4. **Human-Centered**: Accessible language, clear limitations, encourages professional consultation
5. **Ethical Restraint**: No diagnoses, no treatment recommendations, no predictions

---

## System Architecture

### Data Flow

```
Clinical Report (Text Input)
    ↓
[1] Input Validation
    ├─ Length checks (50-5000 chars)
    ├─ Basic PII detection
    └─ Medical content verification
    ↓
[2] MedGemma Inference
    ├─ Extraction prompt (structured JSON)
    ├─ Low temperature (0.1)
    └─ Source attribution required
    ↓
[3] Post-Processing & Safety
    ├─ JSON schema validation
    ├─ Forbidden phrase detection
    ├─ Source quote verification
    └─ Hallucination filtering
    ↓
[4] Output Formatting
    ├─ Key findings (bullet points)
    ├─ Attention flags (color-coded)
    ├─ Patient summary (6th-8th grade)
    └─ Disclaimer (always displayed)
    ↓
Formatted Output (Markdown)
```

---

## Key Components

### 1. Configuration (`src/config.py`)

**Purpose**: Centralized constants and settings

**Contains**:
- Input validation parameters
- Model inference settings (temperature, max tokens)
- Safety constraints (forbidden phrases)
- JSON schemas for validation
- Disclaimers and notices
- Readability targets

**Why**: Single source of truth for all configurable parameters

---

### 2. Input Validator (`src/validator.py`)

**Purpose**: Ensure inputs are safe and appropriate

**Checks**:
- Length constraints (50-5000 characters)
- Basic PII patterns (warns user)
- Medical content indicators
- Text sanitization (whitespace, line breaks)

**Why**: Garbage-in-garbage-out prevention; reduce hallucination risk

---

### 3. Prompt Templates (`src/prompts.py`)

**Purpose**: Structured prompts for MedGemma

**Templates**:
1. **Extraction Prompt**: Extract findings, flags, terminology
2. **Simplification Prompt**: Generate patient-friendly summary
3. **Validation Prompt**: Safety check AI outputs

**Design**:
- Explicit constraints ("do NOT diagnose")
- JSON schema enforcement
- Source attribution required
- Confidence scoring requested
- Few-shot examples included

**Why**: Structured outputs reduce hallucinations; explicit constraints enforce safety

---

### 4. Post-Processor (`src/postprocessor.py`)

**Purpose**: Validate and sanitize model outputs

**Safety Checks**:
- JSON schema compliance
- Forbidden phrase detection (diagnostic/treatment language)
- Source quote verification (cross-reference with input)
- Hallucination detection (missing sources)
- Confidence filtering

**Why**: Model outputs cannot be trusted blindly in medical contexts

---

### 5. Remaining Components (To Be Implemented)

- **Inference Engine** (`src/inference.py`): MedGemma API wrapper
- **Output Formatter** (`src/formatter.py`): Markdown rendering, readability scoring
- **Main Pipeline** (`src/pipeline.py`): Orchestrate entire workflow
- **Utilities** (`src/utils.py`): Helper functions
- **Tests** (`tests/`): Unit and integration tests
- **UI** (`ui/app.py`): Gradio interface
- **Notebook** (`notebook.ipynb`): Kaggle submission

---

## Safety Mechanisms

### Multi-Layer Defense

1. **Input Layer**: Validate and sanitize user input
2. **Prompt Layer**: Constrain model behavior via instructions
3. **Post-Processing Layer**: Filter unsafe outputs
4. **Output Layer**: Add disclaimers, mark uncertainty

### Forbidden Content

**Diagnostic Language**:
- "You have [condition]"
- "Diagnosis is [condition]"
- "This confirms [diagnosis]"

**Treatment Recommendations**:
- "You should take [medication]"
- "Recommended treatment is [action]"
- "You need surgery"

**Predictive Claims**:
- "Prognosis is [outcome]"
- "You will develop [condition]"
- "Life expectancy is [time]"

### Uncertainty Handling

- All extractions have confidence scores (high/medium/low)
- Ambiguous findings are preserved as ambiguous
- Missing information is explicitly acknowledged
- Low-confidence extractions can be filtered out

---

## Design Rationale

### Why Extraction Instead of Generation?

**Extraction** (summarizing existing text) is safer than **generation** (creating new claims) because:
- Reduces hallucination risk
- Keeps outputs grounded in source material
- Easier to verify correctness
- Less likely to overstep medical boundaries

### Why JSON Schema Outputs?

Structured JSON outputs are:
- Parseable and validatable
- Easier to filter for safety
- More consistent than free-form text
- Reduce model creativity (which can cause hallucinations)

### Why Low Temperature (0.1)?

Low temperature inference:
- Reduces randomness
- Increases consistency
- Decreases hallucination risk
- Critical for medical applications

### Why Prominent Disclaimers?

Users must understand:
- This is AI-generated (not human-reviewed)
- This is informational only (not medical advice)
- This may contain errors (not guaranteed accurate)
- Professional consultation is required (not a replacement)

**Ethical requirement**: Transparency about limitations

---

## Known Limitations

### Technical
- **Hallucination risk**: LLMs can fabricate plausible but incorrect information
- **Context limits**: Maximum ~5000 character input
- **English-only**: Optimized for English medical reports
- **No image analysis**: Text reports only

### Functional
- **Not diagnostic**: Cannot replace professional interpretation
- **No treatment advice**: Does not recommend medical actions
- **No predictions**: Cannot estimate outcomes or prognosis
- **No validation**: Outputs are not medically reviewed

### Ethical
- **No liability**: Educational tool only
- **User responsibility**: Must consult healthcare providers
- **Privacy**: Users must remove PII before input
- **No emergency use**: Not for urgent medical situations

---

## Evaluation Strategy

### Correctness Metrics
- **Extraction accuracy**: Do findings match the report?
- **Hallucination rate**: Are there fabricated claims?
- **Completeness**: Are key findings captured?

### Safety Metrics
- **Forbidden phrases**: Count of violations
- **Uncertainty communication**: Are low-confidence items flagged?
- **Disclaimer presence**: Is every output properly labeled?

### User Experience Metrics
- **Readability**: Flesch-Kincaid grade level (target: 6th-8th)
- **Clarity**: User feedback on understandability
- **Usefulness**: Does it help prepare questions for doctors?

---

## Project Structure

```
med_project/
├── README.md                    # Project overview
├── ARCHITECTURE.md              # System design
├── PROMPTING_STRATEGY.md        # Prompt engineering details
├── LIMITATIONS.md               # Ethical considerations
├── IMPLEMENTATION_ROADMAP.md    # Development plan
├── requirements.txt             # Dependencies
│
├── src/                         # Core system
│   ├── config.py               ✅ Configuration
│   ├── validator.py            ✅ Input validation
│   ├── prompts.py              ✅ Prompt templates
│   ├── postprocessor.py        ✅ Safety filters
│   ├── inference.py            🔨 MedGemma wrapper
│   ├── formatter.py            🔨 Output formatting
│   ├── pipeline.py             🔨 Main orchestration
│   └── utils.py                🔨 Utilities
│
├── tests/                       # Test suite
│   ├── test_validator.py       🔨 Validation tests
│   ├── test_postprocessor.py   🔨 Safety tests
│   ├── test_formatter.py       🔨 Formatting tests
│   └── sample_reports.json     🔨 Test data
│
├── ui/                          # User interface
│   └── app.py                  🔨 Gradio app
│
├── docs/                        # Additional docs
│   ├── DESIGN_DECISIONS.md     🔨 Rationale
│   └── EVALUATION.md           🔨 Testing approach
│
└── notebook.ipynb              🔨 Kaggle notebook
```

**Legend**: ✅ Complete | 🔨 To be implemented

---

## Next Steps

### Immediate (Phase 1)
1. Implement MedGemma inference wrapper
2. Implement output formatter
3. Implement main pipeline
4. Create sample test reports
5. Test end-to-end workflow

### Short-term (Phase 2-3)
1. Build test suite
2. Create Gradio UI
3. Develop Kaggle notebook
4. Run evaluation on sample reports

### Final (Phase 4-6)
1. Document evaluation results
2. Polish code and documentation
3. Prepare Kaggle submission
4. Final review and testing

---

## Success Criteria

**Minimum Viable Product**:
- ✅ System architecture designed
- ✅ Safety mechanisms defined
- ✅ Core modules implemented (4/8)
- 🔨 End-to-end pipeline functional
- 🔨 Passes safety tests
- 🔨 Kaggle notebook runs

**Stretch Goals**:
- 🔨 Gradio UI deployed
- 🔨 80%+ test coverage
- 🔨 Evaluation on 50+ reports
- 🔨 Zero safety violations
- 🔨 Consistent readability scores

---

## Questions for You

Before proceeding with implementation, please clarify:

1. **MedGemma Access**: How should we access MedGemma in Kaggle?
   - Via Gemini API with API key?
   - Via Kaggle's built-in model access?
   - Local inference (if model weights available)?

2. **Sample Data**: Where should we get clinical reports for testing?
   - Use synthetic examples we create?
   - Find public datasets (MIMIC-III, etc.)?
   - You'll provide examples?

3. **Evaluation**: How rigorous should evaluation be?
   - Manual review of 20-30 reports (quick)?
   - Comprehensive testing with 50+ reports (thorough)?
   - Just demonstrate it works (minimal)?

4. **UI Priority**: How important is the Gradio interface?
   - Essential for submission?
   - Nice-to-have?
   - Skip for now?

5. **Timeline**: What's your target completion date?
   - This week?
   - Next week?
   - Flexible?

---

## Why This Approach?

This project is designed to be:

1. **Resume-Grade**: Demonstrates thoughtful engineering, not just coding
2. **Ethically Sound**: Shows understanding of medical AI responsibilities
3. **Technically Rigorous**: Multi-layer safety, comprehensive testing
4. **Well-Documented**: Clear rationale for every decision
5. **Honest**: Acknowledges limitations rather than overpromising

**This is the kind of project that medical AI researchers would respect.**

---

**Status**: Foundation complete, ready for implementation phase.

**Last Updated**: 2026-01-28
