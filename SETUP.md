# 🚀 Quick Setup Guide

## ⚡ 5-Minute Setup

### Step 1: Verify Python

```bash
python --version
```

**Need:** Python 3.8 or higher

If not installed: [Download Python](https://www.python.org/downloads/)

---

### Step 2: Clone & Navigate

```bash
git clone <your-repo-url>
cd zentrades
```

---

### Step 3: (Optional) Whisper for Audio Transcription

**Only if you need to transcribe audio files:**

```bash
pip install openai-whisper torch
```

**Note:** For the demo, this is **not needed** - sample text transcripts are already provided.

---

### Step 4: Run the Pipeline

```bash
cd scripts
python run_pipeline.py
```

**Expected output:**
```
======================================================================
  🚀 ZENTRADES AI AGENT PIPELINE
======================================================================

Started at: 2026-03-03 18:50:05

...

✅ PIPELINE EXECUTION COMPLETE
```

---

### Step 5: Check Outputs

```bash
# View v1 memo
cat ../outputs/accounts/ben_penoyer_electrical/v1/memo.json

# View v2 memo
cat ../outputs/accounts/ben_penoyer_electrical/v2/memo.json

# View changelog
cat ../changelog/ben_penoyer_electrical_v1_to_v2.json
```

---

## 🔧 Running Individual Scripts

### Extract Demo Transcripts Only

```bash
python extract_demo.py
```

### Extract Onboarding Transcripts Only

```bash
python extract_onboarding.py
```

### Generate Agent Specs

```bash
python generate_agent.py
```

### Apply Patches

```bash
python apply_patch.py
```

---

## 📂 Adding Your Own Transcripts

### For Demo Calls:

1. Save transcript as `.txt` file
2. Place in `dataset/demo/`
3. Filename becomes account ID (e.g., `john_smith_plumbing.txt` → `john_smith_plumbing`)

### For Onboarding Calls:

1. Save transcript as `.txt` file with **same name** as demo
2. Place in `dataset/onboarding/`
3. Must match existing account ID from demo

Example:
```
dataset/
  ├── demo/
  │   └── acme_electric.txt       ← Create v1
  └── onboarding/
      └── acme_electric.txt       ← Update to v2
```

---

## 🐳 (Optional) Running n8n with Docker

### Install Docker

**Windows:** [Docker Desktop](https://www.docker.com/products/docker-desktop)

### Start n8n

```bash
docker run -d --name n8n -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

### Access n8n

Open browser: `http://localhost:5678`

### Import Workflows

1. Click **Workflows** → **Import**
2. Upload `workflows/demo_pipeline.json`
3. Upload `workflows/onboarding_pipeline.json`
4. Update file paths in nodes
5. Click **Execute Workflow**

---

## 🔍 Troubleshooting

### "No module named 'whisper'"

**Solution:** You don't need Whisper for the demo. Skip that installation.

If you want audio transcription:
```bash
pip install openai-whisper torch
```

### "No such file or directory: '../dataset/demo'"

**Solution:** Make sure you're in the `scripts/` folder:
```bash
cd scripts
python run_pipeline.py
```

### "No transcript files found"

**Solution:** Check that `.txt` files exist:
```bash
ls ../dataset/demo/
ls ../dataset/onboarding/
```

Should show `ben_penoyer_electrical.txt` in both.

---

## ✅ Verification Checklist

After running pipeline, verify these files exist:

```
outputs/
  └── accounts/
      └── ben_penoyer_electrical/
          ├── patch.json                           ✅
          ├── v1/
          │   ├── memo.json                        ✅
          │   └── agent_spec.json                  ✅
          └── v2/
              ├── memo.json                        ✅
              └── agent_spec.json                  ✅

changelog/
  └── ben_penoyer_electrical_v1_to_v2.json         ✅

logs/
  └── run_log.txt                                  ✅
```

---

## 🎓 Next Steps

1. ✅ Read `README.md` for full documentation
2. ✅ Read `LOOM_VIDEO_GUIDE.md` for recording tips
3. ✅ Customize extraction rules in `extract_*.py`
4. ✅ Add more sample transcripts
5. ✅ Test with your own data

---

## 📞 Quick Test

**Want to test immediately?**

```bash
# One command to run everything
cd scripts && python run_pipeline.py
```

**Check it worked:**

```bash
# Should show "v1" and "questions_or_unknowns" with nulls
cat ../outputs/accounts/ben_penoyer_electrical/v1/memo.json | grep "business_hours"

# Should show actual value like "Monday-Friday 8AM - 5PM"
cat ../outputs/accounts/ben_penoyer_electrical/v2/memo.json | grep "business_hours"
```

**If both work:** ✅ You're ready!

---

**Need help?** Check `README.md` for detailed documentation.

**Ready to record?** See `LOOM_VIDEO_GUIDE.md` for script.

🚀 **Happy pipeline building!**
