#!/bin/bash

# ClinExplain AI - Complete System Test
# Tests both backend and frontend integration

set -e

echo "================================================"
echo "ClinExplain AI - System Integration Test"
echo "================================================"
echo ""

# Test 1: Backend Components
echo "Test 1: Backend Components"
echo "----------------------------"
python3 tests/quick_test.py
echo "✓ Backend components verified"
echo ""

# Test 2: Frontend Imports
echo "Test 2: Frontend Imports"
echo "------------------------"
python3 -c "
import sys
sys.path.insert(0, '.')
from ui.app import app
from ui.components.safety_banner import DISCLAIMER_HTML
from ui.components.report_viewer import format_original_report
from ui.utils.confidence_formatter import format_confidence_visual
print('✓ All UI components imported successfully')
"
echo ""

# Test 3: Pipeline Integration
echo "Test 3: Pipeline Integration"
echo "----------------------------"
python3 -c "
from src.pipeline import ClinExplainPipeline

pipeline = ClinExplainPipeline(use_mock=True)
result = pipeline.process('Chest X-ray demonstrates mild cardiomegaly. Lungs are clear bilaterally.')

if result.success:
    print(f'✓ Pipeline processed successfully')
    print(f'  - Findings: {len(result.extraction.get(\"findings\", []))}')
    print(f'  - Flags: {len(result.extraction.get(\"attention_flags\", []))}')
    print(f'  - Safety violations: {len(result.safety_result.violations) if result.safety_result else 0}')
else:
    print(f'✗ Pipeline failed: {result.error}')
    exit(1)
"
echo ""

echo "================================================"
echo "All Tests Passed! ✅"
echo "================================================"
echo ""
echo "System is ready to launch:"
echo "  python3 ui/app.py"
echo ""
