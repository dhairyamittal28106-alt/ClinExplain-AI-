# ClinExplain AI: System Architecture & Design

## 1. System Overview

**Purpose**: Convert complex clinical/radiology reports into structured findings, risk flags, and patient-friendly explanations.

**Critical Constraint**: This is an **informational tool only**. It does NOT diagnose, treat, or provide medical advice.

---

## 2. Architecture Components

### 2.1 Data Flow Pipeline

```
Clinical Report (Input)
    ↓
[1] Input Validation & Sanitization
    ↓
[2] MedGemma Inference (Structured Extraction)
    ↓
[3] Post-Processing & Safety Filters
    ↓
[4] Output Formatting & Uncertainty Quantification
    ↓
Structured Output (JSON) → UI Rendering
```

### 2.2 Component Breakdown

#### **Component 1: Input Validation**
- **Purpose**: Ensure input is safe, reasonable length, and contains medical text
- **Checks**:
  - Length limits (50-5000 characters)
  - Basic sanitization (remove PII patterns if detected)
  - Reject empty or non-medical inputs
- **Rationale**: Prevent garbage-in-garbage-out; reduce hallucination risk

#### **Component 2: MedGemma Inference Engine**
- **Model**: MedGemma (inference-only via Kaggle API or local)
- **Task**: Structured information extraction (NOT generation)
- **Output Format**: JSON with strict schema
- **Rationale**: Structured outputs are easier to validate than free text

#### **Component 3: Post-Processing & Safety Layer**
- **Functions**:
  - Filter out diagnostic language ("you have", "diagnosis is")
  - Flag high-uncertainty extractions
  - Remove treatment recommendations
  - Validate output schema
- **Rationale**: Model outputs cannot be trusted blindly in medical contexts

#### **Component 4: Output Formatter**
- **Generates**:
  1. Key Findings (bullet points)
  2. Attention Flags (color-coded, non-alarmist)
  3. Patient-Friendly Summary (6th-8th grade reading level)
  4. Uncertainty Statement (always displayed)
- **Rationale**: Transparency and accessibility are ethical requirements

---

## 3. Prompting Strategy

### 3.1 Core Principles

1. **Extraction over Generation**: Ask model to extract, not infer
2. **Structured Outputs**: Force JSON schema to reduce hallucinations
3. **Explicit Constraints**: Tell model what NOT to do
4. **Uncertainty Handling**: Request confidence indicators
5. **Grounding**: Anchor responses to input text only

### 3.2 Prompt Template Design

**Prompt Structure**:
```
[SYSTEM CONTEXT]
You are a medical information extraction assistant.
Your role is to extract and summarize information from clinical reports.
You do NOT diagnose, recommend treatments, or provide medical advice.

[TASK DEFINITION]
Extract the following from the report:
1. Key medical findings mentioned in the text
2. Any abnormalities or attention points noted
3. Medical terminology that needs simplification

[CONSTRAINTS]
- Only extract information explicitly stated in the report
- Do not infer diagnoses not mentioned
- Do not recommend treatments
- Mark uncertain extractions clearly
- Use exact quotes when possible

[OUTPUT FORMAT]
Return valid JSON with this schema:
{
  "findings": [{"text": "...", "source_quote": "...", "confidence": "high|medium|low"}],
  "attention_flags": [{"flag": "...", "severity": "info|caution", "context": "..."}],
  "terminology": [{"medical_term": "...", "simple_explanation": "..."}]
}

[INPUT REPORT]
{clinical_report_text}
```

### 3.3 Why This Design?

| Design Choice | Rationale |
|---------------|-----------|
| JSON output | Parseable, validatable, reduces free-form hallucination |
| Confidence scores | Enables filtering low-confidence extractions |
| Source quotes | Allows verification against original text |
| Explicit "do nots" | Reduces risk of overstepping medical boundaries |
| Terminology extraction | Enables controlled simplification (not model-generated explanations) |

---

## 4. Code Structure (Kaggle-Compatible)

```
med_project/
│
├── notebook.ipynb              # Main Kaggle notebook
├── requirements.txt            # Dependencies
├── README.md                   # Project documentation
│
├── src/
│   ├── __init__.py
│   ├── validator.py            # Input validation
│   ├── inference.py            # MedGemma wrapper
│   ├── postprocessor.py        # Safety filters
│   ├── formatter.py            # Output generation
│   └── prompts.py              # Prompt templates
│
├── tests/
│   ├── test_validator.py
│   ├── test_postprocessor.py
│   └── sample_reports.json     # Test cases
│
├── ui/
│   └── app.py                  # Gradio interface (optional)
│
└── docs/
    ├── ARCHITECTURE.md         # This file
    ├── LIMITATIONS.md          # Known limitations
    └── ETHICAL_CONSIDERATIONS.md
```

**Rationale**:
- **Modular**: Each component is testable independently
- **Kaggle-friendly**: Can be collapsed into notebook cells or imported
- **Transparent**: Separate files for prompts, safety logic, and formatting

---

## 5. Safety & Limitations

### 5.1 Built-in Safety Mechanisms

1. **Disclaimer on Every Output**:
   ```
   ⚠️ This is an informational summary only. It is NOT medical advice.
   Always consult a qualified healthcare provider for interpretation.
   ```

2. **Forbidden Phrases Filter**:
   - "You have [condition]"
   - "You should [treatment]"
   - "This means you need [action]"
   - "Diagnosis: [condition]"

3. **Uncertainty Quantification**:
   - Display confidence scores
   - Flag when model is uncertain
   - Show when information is missing

4. **No Predictive Claims**:
   - Do not predict outcomes
   - Do not estimate prognosis
   - Do not compare to population statistics

### 5.2 Known Limitations (Must Disclose)

- **Not a diagnostic tool**: Cannot replace radiologist/clinician review
- **Hallucination risk**: LLMs can generate plausible but incorrect information
- **Context limitations**: May miss nuances requiring clinical expertise
- **No real-time validation**: Outputs are not verified by medical professionals
- **Language barriers**: Optimized for English medical reports
- **No liability**: Tool is for educational/informational purposes only

---

## 6. Evaluation Strategy

### 6.1 Correctness Metrics

- **Extraction Accuracy**: Do findings match report? (manual review)
- **Hallucination Rate**: Are there claims not in the input?
- **Simplification Quality**: Is patient summary accurate and clear?

### 6.2 Safety Metrics

- **Forbidden Phrase Detection**: Count violations
- **Overconfidence Detection**: Are uncertain claims marked?
- **Diagnostic Language**: Flag any diagnostic statements

### 6.3 User Experience Metrics

- **Readability**: Flesch-Kincaid grade level for summaries
- **Completeness**: Are key findings captured?
- **Clarity**: User feedback on understandability

**Rationale**: Medical AI must be evaluated on safety and correctness, not just performance.

---

## 7. Failure Modes & Mitigation

| Failure Mode | Risk | Mitigation |
|--------------|------|------------|
| Model hallucinates findings | High | Post-processing filter, source quote requirement |
| Model gives diagnosis | Critical | Forbidden phrase filter, prompt constraints |
| Model misses critical finding | Medium | Acknowledge limitation, encourage professional review |
| User treats output as medical advice | Critical | Prominent disclaimers, no actionable recommendations |
| Input contains PII | Medium | Basic PII detection, user warning |

---

## 8. Next Steps (Implementation Order)

1. **Set up project structure** (folders, requirements.txt)
2. **Implement input validator** (test with edge cases)
3. **Design and test prompts** (with sample reports)
4. **Build MedGemma inference wrapper** (handle errors gracefully)
5. **Implement post-processing safety layer** (test forbidden phrases)
6. **Create output formatter** (validate JSON schema)
7. **Build minimal UI** (Gradio with clear disclaimers)
8. **Test end-to-end** (with diverse sample reports)
9. **Document limitations** (LIMITATIONS.md)
10. **Prepare Kaggle notebook** (clean, commented, reproducible)

---

## 9. Design Decisions Summary

| Decision | Why |
|----------|-----|
| Extraction-focused prompts | Reduces hallucination vs. generative tasks |
| JSON schema enforcement | Enables validation, reduces free-form errors |
| Multi-layer safety filters | Defense in depth for medical context |
| Explicit uncertainty display | Ethical requirement for AI in healthcare |
| No treatment recommendations | Prevents overstepping medical boundaries |
| Modular code structure | Testability, maintainability, transparency |
| Gradio UI (optional) | Lightweight, Kaggle-compatible, user-friendly |

---

## 10. Open Questions (To Be Resolved)

1. **MedGemma Access**: Kaggle API or local inference? (affects latency)
2. **Sample Data**: Where to source realistic clinical reports? (privacy concerns)
3. **Evaluation Dataset**: How to create ground truth for validation?
4. **Readability Target**: 6th grade? 8th grade? (affects simplification)
5. **UI Deployment**: Kaggle notebook only, or external Gradio link?

**Next Action**: Clarify these questions before implementation begins.
