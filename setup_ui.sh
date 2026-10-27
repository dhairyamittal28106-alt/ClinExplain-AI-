#!/bin/bash




set -e  

echo "================================================"
echo "ClinExplain AI - Frontend Setup"
echo "================================================"
echo ""


echo "Checking Python version..."
python3 --version


echo ""
echo "Installing dependencies..."
pip3 install --upgrade pip
pip3 install gradio>=4.0.0 jsonschema>=4.17.0 textstat>=0.7.3

echo ""
echo "✓ Dependencies installed successfully"
echo ""


echo "Verifying installation..."
python3 -c "import gradio; print(f'✓ Gradio {gradio.__version__} installed')"
python3 -c "import jsonschema; print('✓ jsonschema installed')"
python3 -c "import textstat; print('✓ textstat installed')"

echo ""
echo "================================================"
echo "Setup Complete!"
echo "================================================"
echo ""
echo "To launch the UI, run:"
echo "  python3 ui/app.py"
echo ""
echo "Then open your browser to:"
echo "  http://localhost:7860"
echo ""
