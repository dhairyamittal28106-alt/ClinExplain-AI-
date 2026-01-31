# ClinExplain AI - Quick Start Guide

## Running the Frontend

### Step 1: Install Dependencies

```bash
cd /Users/shivanshpathak/Downloads/med_project
pip install gradio jsonschema textstat
```

### Step 2: Launch the UI

```bash
python ui/app.py
```

### Step 3: Open in Browser

Navigate to: **http://localhost:7860**

---

## Testing with Sample Report

1. Copy this sample report:

```
Chest X-ray demonstrates mild cardiomegaly. Lungs are clear bilaterally. 
No acute infiltrates. No pleural effusion or pneumothorax identified.
```

2. Paste into the text input field
3. Click "🔍 Analyze Report"
4. Explore the 5 result tabs:
   - 📋 Original Report (with highlights)
   - 🔍 Key Findings
   - ⚠️ Attention Flags
   - 💬 Plain Language Summary
   - ⚙️ Analysis Details

---

## What You'll See

### ✅ Expected Output

- **2 findings extracted** (heart enlargement, clear lungs)
- **1 attention flag** (mild cardiomegaly)
- **1 medical term explained** (cardiomegaly)
- **0 safety violations**
- **Patient-friendly summary** in plain language

### 🎨 Visual Features

- Yellow highlights on source quotes in original report
- Confidence dots (●●●●● for high confidence)
- Color-coded attention flags
- Persistent disclaimer banner
- Clean, medical-grade UI

---

## Switching to Production Mode

When ready to use real MedGemma in Kaggle:

1. Open `ui/app.py`
2. Find line 18:
   ```python
   pipeline = ClinExplainPipeline(use_mock=True)
   ```
3. Change to:
   ```python
   pipeline = ClinExplainPipeline(use_mock=False, model_path="/kaggle/input/medgemma")
   ```
4. Run in Kaggle notebook with MedGemma enabled

---

## Troubleshooting

**Port already in use?**
```python
# In ui/app.py, change port:
app.launch(server_port=7861)
```

**Import errors?**
```bash
# Ensure you're in project root
cd /Users/shivanshpathak/Downloads/med_project
python ui/app.py
```

**Slow loading?**
- Mock mode should be instant
- If slow, check your Python environment

---

## Next Steps

1. ✅ Test with sample reports from `tests/sample_reports.json`
2. ✅ Verify all safety features work
3. ✅ Review UI documentation in `ui/README.md`
4. ✅ Prepare for Kaggle deployment

---

**Status**: ✅ Ready to Run  
**Mode**: Mock (Demo)  
**Time to Launch**: <30 seconds
