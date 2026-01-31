# ClinExplain AI

**A Human-Centered Medical Report Interpretation System**

[![Kaggle](https://img.shields.io/badge/Kaggle-MedGemma_Challenge-20BEFF?logo=kaggle)](https://www.kaggle.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Educational-green)](LICENSE)

> ⚠️ **Medical Disclaimer**: This is an educational project. It is NOT a medical device and should NOT be used for clinical decision-making, diagnosis, or treatment.

---

## Overview

ClinExplain AI is a safety-first AI system that helps patients and learners understand complex clinical and radiology reports by:

1. **Extracting key medical findings** from report text
2. **Identifying attention points** that may require follow-up
3. **Simplifying medical terminology** into plain language
4. **Communicating uncertainty** explicitly and transparently

**What this system does NOT do**:
- Diagnose medical conditions
- Recommend treatments
- Replace professional medical interpretation
- Make predictions about patient outcomes

---

## Design Philosophy

This project prioritizes:

- **Safety over capability**: Conservative, transparent outputs
- **Extraction over generation**: Summarizing existing text, not creating new claims
- **Uncertainty over confidence**: Explicit acknowledgment of limitations
- **Human-centered design**: Accessible language, clear disclaimers
- **Ethical restraint**: No diagnostic or treatment recommendations

---

## Project Structure

```
med_project/
│
├── README.md                       # This file
├── ARCHITECTURE.md                 # System design & data flow
├── PROMPTING_STRATEGY.md           # Prompt engineering details
├── LIMITATIONS.md                  # Ethical considerations & constraints
├── requirements.txt                # Python dependencies
├── LICENSE                         # License information
│
├── notebook.ipynb                  # Main Kaggle notebook (to be created)
│
├── src/                            # Core system components
│   ├── __init__.py
│   ├── config.py                   # Configuration & constants
│   ├── validator.py                # Input validation & sanitization
│   ├── prompts.py                  # Prompt templates
│   ├── inference.py                # MedGemma inference wrapper
│   ├── postprocessor.py            # Safety filters & validation
│   ├── formatter.py                # Output formatting & rendering
│   └── utils.py                    # Helper functions
│
├── tests/                          # Test suite
│   ├── __init__.py
│   ├── test_validator.py
│   ├── test_postprocessor.py
│   ├── test_formatter.py
│   └── sample_reports.json         # Test data
│
├── ui/                             # Optional Gradio interface
│   └── app.py
│
└── docs/                           # Additional documentation
    ├── DESIGN_DECISIONS.md         # Rationale for key choices
    └── EVALUATION.md               # Testing & validation approach
```

---

## Key Features

### 1. Structured Information Extraction
- Extracts findings explicitly mentioned in reports
- Requires source quotes for every extraction
- Assigns confidence scores (high/medium/low)
- Preserves ambiguity and uncertainty from original text

### 2. Safety-First Post-Processing
- Filters out diagnostic language ("you have X")
- Removes treatment recommendations
- Validates JSON schema compliance
- Cross-references extractions with source text

### 3. Patient-Friendly Simplification
- Converts medical jargon to plain language
- 6th-8th grade reading level
- Non-alarmist, informative tone
- Encourages professional consultation

### 4. Transparency & Uncertainty
- Displays confidence scores for all extractions
- Flags uncertain or ambiguous information
- Prominent disclaimers on every output
- Acknowledges system limitations

---

## Technical Approach

### Model
- **MedGemma** (inference-only via Kaggle)
- Specialized medical language model
- Used for extraction, not generation

### Inference Strategy
- Low temperature (0.1) for consistency
- Structured JSON outputs to reduce hallucinations
- Source attribution required for all claims
- Conservative defaults when uncertain

### Safety Mechanisms
1. **Input validation**: Length limits, basic sanitization
2. **Prompt constraints**: Explicit "do not diagnose" instructions
3. **Post-processing filters**: Forbidden phrase detection
4. **Output validation**: Schema compliance, source verification
5. **Disclaimer injection**: Automatic safety notices

---

## Installation & Setup

### Prerequisites
- Python 3.10+
- Kaggle account (for MedGemma access)
- Basic understanding of medical terminology (helpful but not required)

### Local Setup

```bash
# Clone or download the project
cd med_project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/

# (Optional) Launch Gradio UI
python ui/app.py
```

### Kaggle Notebook Setup

1. Upload project files to Kaggle
2. Enable MedGemma in notebook settings
3. Run cells sequentially
4. Test with sample reports

---

## Usage Example

```python
from src.inference import ClinExplainPipeline

# Initialize pipeline
pipeline = ClinExplainPipeline()

# Example clinical report
report = """
Chest X-ray demonstrates mild cardiomegaly. 
Lungs are clear bilaterally. No acute infiltrates. 
No pleural effusion or pneumothorax identified.
"""

# Process report
result = pipeline.process(report)

# Output structure
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
      "source_quote": "Lungs are clear bilaterally",
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
  "patient_summary": "The chest X-ray shows that your heart appears slightly larger than typical (cardiomegaly). Your lungs look clear and normal. Your doctor can explain what this finding means for you specifically.",
  "disclaimer": "⚠️ This is an AI-generated summary for informational purposes only..."
}
```

---

## Evaluation Approach

### Correctness Metrics
- **Extraction accuracy**: Do findings match the report?
- **Hallucination rate**: Are there fabricated claims?
- **Completeness**: Are key findings captured?

### Safety Metrics
- **Forbidden phrase detection**: Count of diagnostic/treatment language
- **Uncertainty communication**: Are low-confidence items flagged?
- **Disclaimer presence**: Is every output properly labeled?

### User Experience Metrics
- **Readability**: Flesch-Kincaid grade level
- **Clarity**: User feedback on understandability
- **Usefulness**: Does it help prepare questions for doctors?

See [EVALUATION.md](docs/EVALUATION.md) for detailed testing methodology.

---

## Known Limitations

### Technical
- **Hallucination risk**: LLMs can generate plausible but incorrect information
- **Context limits**: ~5000 character input maximum
- **English-only**: Optimized for English medical reports
- **No image analysis**: Text reports only

### Functional
- **Not a diagnostic tool**: Cannot replace professional interpretation
- **No treatment advice**: Does not recommend medical actions
- **No outcome prediction**: Cannot estimate prognosis
- **No real-time validation**: Outputs are not medically reviewed

### Ethical
- **No liability**: Educational tool only, no medical responsibility
- **User responsibility**: Must consult healthcare providers
- **Privacy**: Users must remove PII before input

See [LIMITATIONS.md](LIMITATIONS.md) for comprehensive discussion.

---

## Design Decisions

### Why Extraction Instead of Generation?
Extracting information from existing text is safer than generating new medical claims. It reduces hallucination risk and keeps outputs grounded in source material.

### Why JSON Schema Outputs?
Structured outputs are easier to validate, filter, and render safely compared to free-form text.

### Why Low Temperature Inference?
Low temperature (0.1) reduces randomness and increases consistency, which is critical for medical applications.

### Why Prominent Disclaimers?
Users must understand this is AI-generated and not medical advice. Transparency is an ethical requirement.

### Why No Treatment Recommendations?
Providing treatment advice without clinical context is dangerous and potentially harmful.

See [DESIGN_DECISIONS.md](docs/DESIGN_DECISIONS.md) for full rationale.

---

## Contributing

This is an educational project for the Kaggle MedGemma Impact Challenge.

If you'd like to suggest improvements:
1. Focus on safety and correctness over features
2. Propose changes that reduce risk of medical misinformation
3. Maintain conservative, transparent design principles
4. Document rationale for all suggestions

---

## Ethical Guidelines

This project adheres to:
- **Non-maleficence**: Do no harm
- **Transparency**: Clear communication of limitations
- **Autonomy**: Users make their own healthcare decisions
- **Justice**: Accessible to diverse populations

All design decisions prioritize patient safety over technical impressiveness.

---

## License

This project is released under an **Educational Use Only** license.

**Permitted**:
- Learning and educational purposes
- Personal informational use
- Academic research and study

**Prohibited**:
- Clinical or medical use
- Commercial deployment
- Integration into healthcare systems
- Use for diagnosis or treatment

See [LICENSE](LICENSE) for full terms.

---

## Acknowledgments

- **Kaggle MedGemma Impact Challenge** for the opportunity
- **Google DeepMind** for MedGemma model
- **Medical AI research community** for safety guidelines
- **Healthcare professionals** who emphasize the importance of responsible AI

---

## Contact & Support

This is a learning project. For questions:
- Review documentation in `docs/`
- Check [LIMITATIONS.md](LIMITATIONS.md) for known issues
- Refer to [ARCHITECTURE.md](ARCHITECTURE.md) for system design

**Remember**: This tool is for educational purposes only. Always consult qualified healthcare providers for medical advice.

---

## Disclaimer

**IMPORTANT MEDICAL DISCLAIMER**

This software is provided for informational and educational purposes only. It is not intended to be a substitute for professional medical advice, diagnosis, or treatment.

Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition. Never disregard professional medical advice or delay in seeking it because of something you have read in this tool's output.

If you think you may have a medical emergency, call your doctor or emergency services immediately.

The creators of this tool make no representations or warranties of any kind, express or implied, about the completeness, accuracy, reliability, suitability or availability of the information provided.

**Use at your own risk.**

---

**Version**: 1.0  
**Last Updated**: 2026-01-28  
**Status**: Development / Educational
