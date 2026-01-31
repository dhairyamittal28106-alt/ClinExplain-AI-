# ClinExplain AI: System Architecture Overview

## Visual System Design

```
┌─────────────────────────────────────────────────────────────────┐
│                     ClinExplain AI System                       │
│                  Human-Centered Medical AI                      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  INPUT LAYER                                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Clinical Report (Text)                                         │
│  ┌───────────────────────────────────────────────────────┐     │
│  │ "Chest X-ray demonstrates mild cardiomegaly.          │     │
│  │  Lungs are clear bilaterally. No acute findings."     │     │
│  └───────────────────────────────────────────────────────┘     │
│                           ↓                                     │
│  [InputValidator] src/validator.py                             │
│  • Length check (50-5000 chars)                                │
│  • PII detection warning                                       │
│  • Medical content verification                                │
│  • Text sanitization                                           │
│                           ↓                                     │
│  ✅ Valid Input → Continue                                     │
│  ❌ Invalid Input → Reject with error                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  PROMPT LAYER                                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [PromptBuilder] src/prompts.py                                │
│                                                                 │
│  Extraction Prompt Template:                                   │
│  ┌───────────────────────────────────────────────────────┐     │
│  │ System: You are a medical information extractor       │     │
│  │ Constraints: Do NOT diagnose, treat, or predict       │     │
│  │ Task: Extract findings, flags, terminology            │     │
│  │ Format: Return JSON with source quotes                │     │
│  │ Input: {clinical_report}                              │     │
│  └───────────────────────────────────────────────────────┘     │
│                           ↓                                     │
│  Config: temperature=0.1, max_tokens=1500                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  INFERENCE LAYER                                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [MedGemmaInference] src/inference.py (TO BE IMPLEMENTED)      │
│                                                                 │
│  ┌─────────────────────────────────────────────────────┐       │
│  │         MedGemma Model (Google)                     │       │
│  │                                                     │       │
│  │  • Medical domain knowledge                        │       │
│  │  • Structured extraction                           │       │
│  │  • Low temperature (consistent)                    │       │
│  └─────────────────────────────────────────────────────┘       │
│                           ↓                                     │
│  Raw JSON Output:                                              │
│  {                                                             │
│    "findings": [...],                                          │
│    "attention_flags": [...],                                   │
│    "terminology": [...],                                       │
│    "uncertainties": [...]                                      │
│  }                                                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  SAFETY LAYER                                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [PostProcessor] src/postprocessor.py                          │
│                                                                 │
│  Safety Checks:                                                │
│  ┌───────────────────────────────────────────────────────┐     │
│  │ 1. JSON Schema Validation                             │     │
│  │    ✓ Required fields present                          │     │
│  │    ✓ Correct data types                               │     │
│  │                                                        │     │
│  │ 2. Forbidden Phrase Detection                         │     │
│  │    ✗ "You have [condition]"                           │     │
│  │    ✗ "You should take [treatment]"                    │     │
│  │    ✗ "Prognosis is [outcome]"                         │     │
│  │                                                        │     │
│  │ 3. Source Quote Verification                          │     │
│  │    ✓ Quotes exist in original text                    │     │
│  │    ✗ Missing or fabricated quotes                     │     │
│  │                                                        │     │
│  │ 4. Hallucination Detection                            │     │
│  │    ✓ All findings have source attribution             │     │
│  │    ✗ Claims without evidence                          │     │
│  │                                                        │     │
│  │ 5. Confidence Filtering                               │     │
│  │    ✓ High/medium confidence kept                      │     │
│  │    ? Low confidence flagged                           │     │
│  └───────────────────────────────────────────────────────┘     │
│                           ↓                                     │
│  ✅ Safe Output → Continue                                     │
│  ❌ Unsafe Output → Reject or sanitize                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  FORMATTING LAYER                                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [OutputFormatter] src/formatter.py (TO BE IMPLEMENTED)        │
│                                                                 │
│  Generate:                                                     │
│  ┌───────────────────────────────────────────────────────┐     │
│  │ 1. Key Findings (Bullet Points)                       │     │
│  │    • Heart appears mildly enlarged (cardiomegaly)     │     │
│  │    • Lungs appear normal                              │     │
│  │                                                        │     │
│  │ 2. Attention Flags (Color-Coded)                      │     │
│  │    ⚠️ Mild heart enlargement noted (INFO)            │     │
│  │                                                        │     │
│  │ 3. Patient Summary (6th-8th grade)                    │     │
│  │    "The chest X-ray shows that your heart            │     │
│  │     appears slightly larger than typical..."          │     │
│  │                                                        │     │
│  │ 4. Medical Terms Explained                            │     │
│  │    • Cardiomegaly = Heart enlargement                 │     │
│  │                                                        │     │
│  │ 5. Disclaimer (Always Displayed)                      │     │
│  │    ⚠️ This is AI-generated, not medical advice       │     │
│  └───────────────────────────────────────────────────────┘     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  OUTPUT LAYER                                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Final Formatted Output (Markdown)                             │
│  ┌───────────────────────────────────────────────────────┐     │
│  │ ⚠️ IMPORTANT MEDICAL DISCLAIMER                       │     │
│  │ This is AI-generated for informational purposes only. │     │
│  │ NOT medical advice. Consult healthcare provider.      │     │
│  │                                                        │     │
│  │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │     │
│  │                                                        │     │
│  │ 📋 KEY FINDINGS                                       │     │
│  │ • Finding 1 (confidence: high)                        │     │
│  │ • Finding 2 (confidence: high)                        │     │
│  │                                                        │     │
│  │ ⚠️ ATTENTION FLAGS                                    │     │
│  │ • Flag 1 (severity: info)                             │     │
│  │                                                        │     │
│  │ 💬 PATIENT-FRIENDLY SUMMARY                           │     │
│  │ [Plain language explanation...]                       │     │
│  │                                                        │     │
│  │ 📖 MEDICAL TERMS EXPLAINED                            │     │
│  │ • Term 1: Simple explanation                          │     │
│  │                                                        │     │
│  │ ℹ️ UNCERTAINTIES                                      │     │
│  │ • [Any unclear information noted]                     │     │
│  └───────────────────────────────────────────────────────┘     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Status

| Component | File | Status | Purpose |
|-----------|------|--------|---------|
| **Configuration** | `src/config.py` | ✅ Complete | Constants, schemas, disclaimers |
| **Input Validator** | `src/validator.py` | ✅ Complete | Validate and sanitize input |
| **Prompt Templates** | `src/prompts.py` | ✅ Complete | Structured prompts for MedGemma |
| **Post-Processor** | `src/postprocessor.py` | ✅ Complete | Safety checks and filtering |
| **Inference Engine** | `src/inference.py` | 🔨 To Do | MedGemma API wrapper |
| **Output Formatter** | `src/formatter.py` | 🔨 To Do | Format and render output |
| **Main Pipeline** | `src/pipeline.py` | 🔨 To Do | Orchestrate workflow |
| **Utilities** | `src/utils.py` | 🔨 To Do | Helper functions |
| **Tests** | `tests/*.py` | 🔨 To Do | Unit and integration tests |
| **UI** | `ui/app.py` | 🔨 To Do | Gradio interface |
| **Notebook** | `notebook.ipynb` | 🔨 To Do | Kaggle submission |

---

## Safety Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MULTI-LAYER SAFETY                       │
└─────────────────────────────────────────────────────────────┘

Layer 1: INPUT VALIDATION
├─ Length constraints
├─ PII warnings
└─ Medical content check

Layer 2: PROMPT CONSTRAINTS
├─ Explicit "do not" instructions
├─ JSON schema enforcement
└─ Source attribution requirement

Layer 3: POST-PROCESSING FILTERS
├─ Forbidden phrase detection
├─ Schema validation
├─ Source verification
└─ Hallucination detection

Layer 4: OUTPUT FORMATTING
├─ Disclaimer injection
├─ Uncertainty marking
├─ Confidence display
└─ Professional consultation encouragement

Result: Defense-in-depth for medical safety
```

---

## Data Flow Example

**Input**:
```
"Chest X-ray demonstrates mild cardiomegaly. 
 Lungs are clear bilaterally. No acute findings."
```

**After Validation**:
```
✅ Length: 89 chars (valid)
✅ Medical content: detected
✅ PII: none detected
→ Proceed to inference
```

**After Extraction**:
```json
{
  "findings": [
    {
      "text": "Heart appears mildly enlarged",
      "source_quote": "mild cardiomegaly",
      "confidence": "high",
      "category": "observation"
    }
  ],
  "attention_flags": [
    {
      "flag": "Mild heart enlargement noted",
      "severity": "info",
      "context": "May require clinical correlation",
      "source_quote": "mild cardiomegaly"
    }
  ]
}
```

**After Safety Check**:
```
✅ JSON valid
✅ No forbidden phrases
✅ Source quotes verified
✅ No hallucinations
→ Proceed to formatting
```

**Final Output**:
```markdown
⚠️ **IMPORTANT MEDICAL DISCLAIMER**
This is AI-generated for informational purposes only...

## 📋 Key Findings
• Heart appears mildly enlarged (high confidence)
• Lungs appear normal (high confidence)

## ⚠️ Attention Flags
• Mild heart enlargement noted (INFO)
  Context: May require clinical correlation

## 💬 Patient-Friendly Summary
The chest X-ray shows that your heart appears 
slightly larger than typical (cardiomegaly)...

## 📖 Medical Terms
• Cardiomegaly: Enlargement of the heart
```

---

## Design Philosophy Summary

| Principle | Implementation |
|-----------|----------------|
| **Safety First** | Multi-layer validation, forbidden phrases, disclaimers |
| **Extraction > Generation** | Summarize existing text, require source quotes |
| **Structured Outputs** | JSON schema enforcement reduces hallucinations |
| **Low Temperature** | Consistent, conservative inference (0.1) |
| **Transparency** | Confidence scores, uncertainty flags, limitations |
| **Human-Centered** | Plain language, accessible, encourages consultation |
| **Ethical Restraint** | No diagnoses, no treatments, no predictions |

---

## What Makes This Resume-Grade?

1. **Thoughtful Architecture**: Not just "call API and display"
2. **Safety Engineering**: Multi-layer defense against medical misinformation
3. **Ethical Awareness**: Explicit limitations and disclaimers
4. **Code Quality**: Modular, testable, well-documented
5. **Design Rationale**: Every decision is justified
6. **Honest Assessment**: Acknowledges what it cannot do

**This demonstrates engineering maturity and medical AI responsibility.**

---

**Status**: Foundation complete (4/11 components)  
**Next**: Implement inference, formatter, and pipeline  
**Timeline**: ~7-10 days to completion

**Last Updated**: 2026-01-28
