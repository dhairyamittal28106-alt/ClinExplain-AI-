# ClinExplain AI: Prompting Strategy

## 1. Prompt Engineering Principles for Medical AI

### 1.1 Core Constraints

Medical AI prompting is fundamentally different from general-purpose LLM use because:

- **Hallucinations are dangerous**: Fabricated medical information can cause harm
- **Uncertainty must be explicit**: Confidence matters more than completeness
- **Extraction > Generation**: Summarizing existing text is safer than creating new claims
- **Grounding is critical**: Every output must be traceable to input text
- **Negative constraints matter**: Telling the model what NOT to do is as important as the task

### 1.2 Prompt Design Philosophy

| Principle | Implementation |
|-----------|----------------|
| **Structured Output** | Force JSON schema to reduce free-form hallucination |
| **Explicit Boundaries** | Define what the model should NOT do |
| **Source Attribution** | Require quotes from original text |
| **Confidence Scoring** | Ask model to self-assess uncertainty |
| **Task Decomposition** | Break complex tasks into atomic extractions |
| **Conservative Defaults** | Prefer "unclear" over guessing |

---

## 2. Prompt Templates

### 2.1 Primary Extraction Prompt

```python
EXTRACTION_PROMPT = """You are a medical information extraction assistant.

**Your Role**:
- Extract and organize information from clinical reports
- Summarize findings clearly and accurately
- Identify medical terminology that needs simplification

**Critical Constraints**:
- Extract ONLY information explicitly stated in the report
- Do NOT infer diagnoses not mentioned
- Do NOT recommend treatments or medical actions
- Do NOT make predictions about patient outcomes
- If information is unclear or missing, mark it as "uncertain"
- Use exact quotes from the report when possible

**Task**:
Analyze the following clinical report and extract:

1. **Key Findings**: Medical observations, measurements, or abnormalities mentioned
2. **Attention Flags**: Items marked as abnormal, requiring follow-up, or noted as significant
3. **Medical Terminology**: Complex terms that would benefit from plain-language explanation

**Output Format**:
Return ONLY valid JSON matching this schema:

{
  "findings": [
    {
      "text": "Brief description of finding",
      "source_quote": "Exact quote from report",
      "confidence": "high|medium|low",
      "category": "observation|measurement|abnormality|normal"
    }
  ],
  "attention_flags": [
    {
      "flag": "What requires attention",
      "severity": "info|caution",
      "context": "Why this is flagged",
      "source_quote": "Exact quote from report"
    }
  ],
  "terminology": [
    {
      "medical_term": "Technical term from report",
      "simple_explanation": "Plain language explanation (one sentence)",
      "confidence": "high|medium|low"
    }
  ],
  "uncertainties": [
    "List any information that was unclear or could not be extracted"
  ]
}

**Clinical Report**:
{report_text}

**Important**: Return ONLY the JSON object. Do not include explanations, preamble, or markdown formatting.
"""
```

### 2.2 Simplification Prompt (Secondary)

```python
SIMPLIFICATION_PROMPT = """You are a medical communication specialist helping patients understand clinical reports.

**Task**: Create a patient-friendly summary of the following medical findings.

**Requirements**:
- Use 6th-8th grade reading level
- Avoid medical jargon (or explain it immediately)
- Be accurate but not alarming
- Do NOT diagnose or recommend treatment
- Acknowledge what is uncertain or requires professional interpretation

**Tone**: Informative, calm, supportive

**Input Findings**:
{structured_findings}

**Output Format**:
Return a JSON object with:
{
  "summary": "2-3 paragraph patient-friendly explanation",
  "key_points": ["Bullet point 1", "Bullet point 2", ...],
  "next_steps_note": "General guidance on consulting healthcare provider"
}

**Critical**: Do not use phrases like:
- "You have [condition]"
- "This means you need [treatment]"
- "You should [action]"

Instead use:
- "The report mentions [finding]"
- "This may indicate [general category]"
- "Your doctor can explain [specific detail]"
"""
```

### 2.3 Validation Prompt (Quality Check)

```python
VALIDATION_PROMPT = """You are a medical AI safety validator.

**Task**: Review the following AI-generated summary for safety and accuracy issues.

**Check for**:
1. Hallucinations (claims not in original report)
2. Diagnostic language (stating diagnoses)
3. Treatment recommendations
4. Overconfident claims about uncertain information
5. Missing uncertainty acknowledgments

**Original Report**:
{original_report}

**AI-Generated Output**:
{ai_output}

**Return**:
{
  "is_safe": true|false,
  "issues_found": [
    {
      "type": "hallucination|diagnosis|treatment|overconfidence",
      "description": "What the issue is",
      "severity": "critical|high|medium|low"
    }
  ],
  "recommendations": ["What should be fixed"]
}
"""
```

---

## 3. Prompt Testing Strategy

### 3.1 Test Cases

Create a test suite with:

1. **Normal Reports**: Routine findings, no abnormalities
2. **Abnormal Reports**: Clear abnormalities mentioned
3. **Ambiguous Reports**: Uncertain or incomplete information
4. **Complex Reports**: Multiple findings, technical terminology
5. **Edge Cases**: Very short, very long, non-medical text

### 3.2 Evaluation Criteria

For each test case, check:

- [ ] All findings are grounded in source text
- [ ] No hallucinated information
- [ ] No diagnostic language
- [ ] No treatment recommendations
- [ ] Uncertainties are acknowledged
- [ ] Confidence scores are reasonable
- [ ] JSON schema is valid

### 3.3 Failure Case Handling

| Failure Type | Detection | Response |
|--------------|-----------|----------|
| Invalid JSON | Schema validation | Return error, ask model to retry |
| Missing source quotes | Post-processing check | Flag as low confidence |
| Diagnostic language | Keyword filter | Remove or rephrase |
| Hallucination | Cross-reference with input | Remove finding |
| Empty output | Length check | Return "Unable to extract information" |

---

## 4. Prompt Optimization Techniques

### 4.1 Few-Shot Examples (If Needed)

If zero-shot performance is poor, add 1-2 examples:

```python
EXAMPLE_1 = """
**Example Input**:
"Chest X-ray shows mild cardiomegaly. Lungs are clear. No acute findings."

**Example Output**:
{
  "findings": [
    {
      "text": "Heart appears mildly enlarged",
      "source_quote": "mild cardiomegaly",
      "confidence": "high",
      "category": "observation"
    },
    {
      "text": "Lungs appear normal",
      "source_quote": "Lungs are clear",
      "confidence": "high",
      "category": "normal"
    }
  ],
  "attention_flags": [
    {
      "flag": "Mild heart enlargement noted",
      "severity": "info",
      "context": "May require clinical correlation",
      "source_quote": "mild cardiomegaly"
    }
  ],
  "terminology": [
    {
      "medical_term": "cardiomegaly",
      "simple_explanation": "Enlargement of the heart",
      "confidence": "high"
    }
  ],
  "uncertainties": []
}
"""
```

### 4.2 Chain-of-Thought (If Needed)

For complex reports, add reasoning step:

```python
CHAIN_OF_THOUGHT_PROMPT = """
Before generating the JSON output, first:

1. List all medical findings mentioned in the report
2. Identify which findings are marked as abnormal or significant
3. Note any uncertainties or qualifiers (e.g., "possible", "likely", "cannot rule out")
4. Extract technical terms that need explanation

Then generate the structured JSON output.
"""
```

### 4.3 Temperature & Sampling Settings

Recommended settings for MedGemma:

```python
INFERENCE_CONFIG = {
    "temperature": 0.1,  # Low temperature for consistency
    "top_p": 0.9,        # Nucleus sampling
    "max_tokens": 1500,  # Enough for structured output
    "stop_sequences": ["}"],  # Stop after JSON closes (if supported)
}
```

**Rationale**: Low temperature reduces randomness and hallucination risk.

---

## 5. Prompt Iteration Process

### 5.1 Baseline Evaluation

1. Run prompts on 20-30 diverse sample reports
2. Manually review outputs for:
   - Accuracy (findings match report)
   - Safety (no diagnoses/treatments)
   - Completeness (key findings captured)
   - Hallucinations (fabricated information)

3. Calculate metrics:
   - Extraction accuracy: % of findings correctly extracted
   - Hallucination rate: % of outputs with fabricated info
   - Safety violations: Count of forbidden phrases

### 5.2 Iterative Refinement

| Issue Observed | Prompt Adjustment |
|----------------|-------------------|
| Model adds diagnoses | Strengthen "do not diagnose" constraint |
| Missing findings | Add "be thorough" instruction |
| Hallucinations | Add "only extract explicitly stated" emphasis |
| Poor simplifications | Provide reading level target, tone examples |
| Invalid JSON | Add schema example, emphasize format |

### 5.3 Version Control

Track prompt versions:

```python
PROMPT_VERSION = "v1.2"
PROMPT_CHANGELOG = """
v1.0: Initial extraction prompt
v1.1: Added source_quote requirement to reduce hallucinations
v1.2: Strengthened constraints against diagnostic language
"""
```

---

## 6. Handling MedGemma-Specific Considerations

### 6.1 Model Capabilities

MedGemma is trained on medical literature, so it:
- Understands medical terminology well
- May be prone to clinical reasoning (which we want to limit)
- Should perform well on extraction tasks
- May need explicit constraints to avoid diagnostic behavior

### 6.2 Prompt Adaptations

- **Leverage medical knowledge**: Use precise medical terms in prompts
- **Constrain clinical reasoning**: Explicitly disable inference/diagnosis
- **Use structured outputs**: MedGemma should handle JSON well
- **Test thoroughly**: Medical models may behave differently than general LLMs

---

## 7. Ethical Prompt Design

### 7.1 Transparency Requirements

Every output must include:

```python
DISCLAIMER = """
⚠️ **Important Notice**:
This summary is generated by an AI system and is for informational purposes only.
It is NOT a medical diagnosis, treatment recommendation, or substitute for professional medical advice.
Always consult with a qualified healthcare provider for interpretation of medical reports.
This system may make errors or miss important information.
"""
```

### 7.2 Uncertainty Communication

Prompt must ensure:
- Low-confidence extractions are marked
- Missing information is acknowledged
- Ambiguous findings are flagged as such
- No false certainty is conveyed

### 7.3 Bias Mitigation

- Avoid demographic assumptions
- Do not infer patient characteristics not in report
- Use neutral language
- Flag when information is insufficient for extraction

---

## 8. Prompt Maintenance

### 8.1 Monitoring

Track over time:
- User-reported errors
- Hallucination incidents
- Safety violations
- Model behavior changes (if MedGemma updates)

### 8.2 Update Triggers

Update prompts when:
- New failure modes are discovered
- Model behavior changes
- User feedback indicates issues
- Safety requirements evolve

---

## 9. Summary: Prompt Design Checklist

Before deploying any prompt, verify:

- [ ] Task is clearly defined
- [ ] Constraints are explicit (especially "do nots")
- [ ] Output format is specified (JSON schema)
- [ ] Source attribution is required
- [ ] Confidence scoring is requested
- [ ] Uncertainty handling is addressed
- [ ] Safety boundaries are clear
- [ ] Examples are provided (if needed)
- [ ] Prompt has been tested on diverse inputs
- [ ] Failure modes have been considered

---

## 10. Next Steps

1. Implement prompts in `src/prompts.py`
2. Create test suite with sample reports
3. Run baseline evaluation
4. Iterate based on results
5. Document final prompt versions
6. Monitor performance in production

**Remember**: In medical AI, conservative and transparent is better than impressive and opaque.
