# ClinExplain AI

Safety-focused prototype that structures clinical report text into findings and patient-friendly explanations with source text and confidence metadata. Includes a Gradio interface. For research only; not a diagnosis or substitute for a clinician. Do not submit identifiable patient data.

    python -m venv .venv
    pip install -r requirements.txt
    python ui/app.py

Gradio typically prints a local URL at port 7860. Demos are in tests/; pipeline is in src/. Some inference paths need provider/model setup; review src/config.py.
