# ClinExplain AI

ClinExplain AI is a safety-focused prototype for turning clinical report text into structured findings and patient-friendly explanations. It validates input, runs an extraction/explanation pipeline, checks output against source text, and presents results through a Gradio interface.

This project is for research and demonstration. It does not diagnose or replace a qualified healthcare professional. Avoid submitting identifiable patient information.

## Setup and run

Use Python 3.10 or newer:

    python -m venv .venv
    # Activate the environment, then:
    pip install -r requirements.txt
    python ui/app.py

Gradio prints the local interface address, typically `http://localhost:7860`. Some inference paths require a model or provider configuration; review `src/config.py` before enabling external inference.

## Demos

    python tests/quick_test.py
    python tests/simple_demo.py
    python tests/demo.py

## Project layout

- `src/`: validation, prompts, inference, orchestration, post-processing, and formatting
- `ui/`: Gradio app and result components
- `tests/`: demo scripts and sample reports
- `SYSTEM_OPERATIONAL.md`: recorded system notes

Output is explanatory text for review, not medical advice.
