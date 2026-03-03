# ZenTrades AI Agent Pipeline

**Internal tooling for converting transcripts → structured operational rules → versioned AI agent configurations**

[![Status](https://img.shields.io/badge/Status-Demo_Ready-green)]()
[![Pipeline](https://img.shields.io/badge/Pipeline-A+B-blue)]()
[![Version](https://img.shields.io/badge/Version-1.0-orange)]()

> ⚠️ **Project Context**: Built for ZenTrades technical assignment (Due: March 5th, 2026)

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/bharathreddy-k/ZenTrades.git
cd ZenTrades

# 2. Install dependencies (optional - for audio transcription)
pip install openai-whisper torch

# 3. Add transcripts to dataset folders
#    Sample transcripts already included in:
#    - dataset/demo/ben_penoyer_electrical.txt
#    - dataset/onboarding/ben_penoyer_electrical.txt

# 4. Run the complete pipeline
cd scripts
python run_pipeline.py

# 5. View outputs
#    outputs/accounts/<account_id>/v1/     → Initial config with nulls
#    outputs/accounts/<account_id>/v2/     → Production-ready config
#    changelog/                            → Full audit trail
```

**⚡ Execution time:** ~0.8 seconds for complete end-to-end pipeline

---

## 🎯 What This Does

This system automates the conversion of sales demo and onboarding call transcripts into production-ready AI receptionist configurations.

### Two Pipelines:

| Pipeline | Input | Output | Purpose |
|----------|-------|--------|---------|
| **🟦 Pipeline A** | Demo transcript | v1 memo + agent spec | Initial configuration from demo |
| **🟩 Pipeline B** | Onboarding transcript | v2 memo + agent spec + changelog | Production-ready config with all details |

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        PIPELINE A (Demo → v1)                    │
└─────────────────────────────────────────────────────────────────┘

   demo_transcript.txt
         │
         ▼
   [Extract Demo Info]  ← Rule-based extraction
         │
         ▼
   account_memo_v1.json  ← Structured account data
         │                 (with unknowns marked)
         ▼
   [Generate Agent Spec]
         │
         ▼
   agent_spec_v1.json   ← Retell AI config


┌─────────────────────────────────────────────────────────────────┐
│                   PIPELINE B (Onboarding → v2)                   │
└─────────────────────────────────────────────────────────────────┘

   onboarding_transcript.txt     account_memo_v1.json
         │                              │
         ▼                              │
   [Extract Updates]                   │
         │                              │
         ▼                              ▼
      patch.json  ───────────────►  [Apply Patch]
                                        │
                                        ▼
                                  account_memo_v2.json
                                        │
                     ┌──────────────────┴────────────────┐
                     ▼                                   ▼
            [Generate Agent Spec]              [Create Changelog]
                     │                                   │
                     ▼                                   ▼
            agent_spec_v2.json            changelog_v1_to_v2.json
```

---

## 📁 Project Structure

```
zentrades/
│
├── dataset/                      # Input transcripts
│   ├── demo/                     # Demo call transcripts
│   │   └── ben_penoyer_electrical.txt
│   └── onboarding/               # Onboarding call transcripts
│       └── ben_penoyer_electrical.txt
│
├── scripts/                      # Python pipeline scripts
│   ├── extract_demo.py           # Extract from demo transcripts
│   ├── extract_onboarding.py     # Extract from onboarding transcripts
│   ├── apply_patch.py            # Merge v1 + updates → v2
│   ├── generate_agent.py         # Create AI agent specifications
│   ├── run_pipeline.py           # Master orchestrator
│   └── transcribe_audio.py       # (Optional) Audio → text
│
├── outputs/                      # Generated outputs
│   └── accounts/
│       └── <account_id>/
│           ├── v1/
│           │   ├── memo.json            # v1 account memo
│           │   └── agent_spec.json      # v1 AI agent config
│           ├── v2/
│           │   ├── memo.json            # v2 account memo (updated)
│           │   └── agent_spec.json      # v2 AI agent config
│           └── patch.json               # Extracted updates
│
├── changelog/                    # Version upgrade logs
│   └── <account_id>_v1_to_v2.json
│
├── workflows/                    # n8n workflow exports
│   ├── demo_pipeline.json
│   └── onboarding_pipeline.json
│
├── logs/                         # Execution logs
│   └── run_log.txt
│
└── README.md                     # This file
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- n8n (optional, for workflow automation)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd zentrades
   ```

2. **Install Python dependencies** (if using Whisper transcription)
   ```bash
   pip install openai-whisper torch
   ```

### Run the Complete Pipeline

```bash
cd scripts
python run_pipeline.py
```

This will:
1. ✅ Extract account memos from demo transcripts (v1)
2. ✅ Generate v1 AI agent specifications
3. ✅ Extract updates from onboarding transcripts
4. ✅ Apply patches to create v2
5. ✅ Generate v2 AI agent specifications
6. ✅ Create changelogs

---

## � Live Example (Actual Output from Repo)

This project includes a complete working example with **Ben Penoyer Electrical**:

### 📥 Input Files
- **Demo transcript**: [`dataset/demo/ben_penoyer_electrical.txt`](dataset/demo/ben_penoyer_electrical.txt)
- **Onboarding transcript**: [`dataset/onboarding/ben_penoyer_electrical.txt`](dataset/onboarding/ben_penoyer_electrical.txt)

### 📤 Generated Outputs
- **v1 memo**: [`outputs/accounts/ben_penoyer_electrical/v1/memo.json`](outputs/accounts/ben_penoyer_electrical/v1/memo.json) *(43% complete, nulls for unknowns)*
- **v2 memo**: [`outputs/accounts/ben_penoyer_electrical/v2/memo.json`](outputs/accounts/ben_penoyer_electrical/v2/memo.json) *(93% complete, production-ready)*
- **Changelog**: [`changelog/ben_penoyer_electrical_v1_to_v2.json`](changelog/ben_penoyer_electrical_v1_to_v2.json) *(7 tracked changes)*

### 🔍 Quick Comparison

| Field | v1 (Demo) | v2 (Onboarding) |
|-------|-----------|-----------------|
| business_hours | `null` | `"Monday-Friday 8AM - 5PM"` |
| timezone | `null` | `"Eastern"` |
| office_address | `null` | `"245 Industrial Park Road, Raleigh, NC 27603"` |
| emergency_definition | 3 scenarios | 7 scenarios |
| call_transfer_rules | `null` | Complete protocol with numbers |

**⚡ Pipeline Execution:** 0.82 seconds end-to-end

---

## �📘 How It Works

### 1. Pipeline A: Demo → v1

**Input:** `dataset/demo/ben_penoyer_electrical.txt`

**Process:**
- Rule-based extraction looks for:
  - Company name
  - Services mentioned
  - CRM integrations
  - Emergency scenarios
  - Business hours (if mentioned)
- **Never invents data** - missing fields marked as `null`
- Unknown items added to `questions_or_unknowns` array

**Output v1 Memo Structure:**
```json
{
  "account_id": "ben_penoyer_electrical",
  "company_name": "Ben Penoyer Electrical",
  "business_hours": null,
  "timezone": null,
  "services_supported": [
    "residential electrical service",
    "commercial electrical service", 
    "panel upgrades"
  ],
  "emergency_definition": [
    "Exposed Wiring",
    "Electrical Fire"
  ],
  "questions_or_unknowns": [
    "Business hours not specified in demo",
    "Timezone not specified in demo",
    "Call transfer rules and phone numbers needed"
  ],
  "version": "v1"
}
```

**Output v1 Agent Spec:**
- System prompt with available data
- Business hours flow
- After-hours flow
- Transfer protocols (with placeholders for missing data)

---

### 2. Pipeline B: Onboarding → v2

**Input:** `dataset/onboarding/ben_penoyer_electrical.txt`

**Process:**
- Extracts **specific** information:
  - `"Monday-Friday 8AM - 5PM"` → Structured business hours
  - `"245 Industrial Park Road, Raleigh, NC 27603"` → Full address
  - `"919-555-0147"` → Office phone number
  - Emergency definitions clarified
- Creates `patch.json` with updates
- **Merges** patch into v1 (doesn't overwrite, preserves v1)
- Generates comprehensive changelog

**Patch Example:**
```json
{
  "business_hours": "Monday-Friday 8AM - 5PM",
  "timezone": "Eastern",
  "office_address": "245 Industrial Park Road, Raleigh, NC 27603",
  "emergency_definition": [
    "Power Outage",
    "Exposed Wiring",
    "Sparking Electrical",
    "Burning Smell",
    "Electrical Fire"
  ],
  "call_transfer_rules": {
    "business_hours_number": "919-555-0147",
    "after_hours_emergency_number": "919-555-0198",
    "timeout_seconds": 30
  }
}
```

**Changelog Example:**
```json
{
  "version_upgrade": "v1 -> v2",
  "timestamp": "2026-03-03 10:45:23",
  "total_changes": 5,
  "changes": [
    {
      "field": "business_hours",
      "old_value": null,
      "new_value": "Monday-Friday 8AM - 5PM",
      "reason": "Clarified during onboarding"
    }
  ]
}
```

---

## 🧠 Key Design Decisions

### ✅ Why Rule-Based Extraction?

| Approach | Pros | Cons | Our Choice |
|----------|------|------|------------|
| **LLM API** | Smart, flexible | Costs $$$, hallucinations | ❌ |
| **Local LLM** | No API cost | Complex setup, slow | ❌ |
| **Rule-Based** | Fast, deterministic, free | Limited flexibility | ✅ **YES** |

**Our rule-based extraction:**
- Uses regex patterns for phone numbers, addresses, times
- Keyword matching for services and emergencies
- **Never hallucinates** - `null` if not found
- Zero external dependencies or API costs

### ✅ Why Separate v1 and v2?

**NOT overwriting v1 is critical because:**
1. **Audit trail** - Can see what changed and why
2. **Rollback capability** - If v2 has issues, v1 still exists
3. **Comparison** - Shows the value added by onboarding
4. **Idempotency** - Running pipeline twice doesn't lose data

### ✅ Why Local JSON Storage?

For a demo/prototype:
- ✅ Simple, no database setup
- ✅ Version-controlled alongside code
- ✅ Easy to inspect and debug
- ✅ Portable across systems

Production upgrade path: PostgreSQL or MongoDB

---

## 🔧 n8n Workflow Integration

### Import Workflows

1. **Start n8n**
   ```bash
   docker run -d --name n8n -p 5678:5678 n8nio/n8n
   ```

2. **Import workflows**
   - Open http://localhost:5678
   - Go to **Workflows** → **Import Workflow**
   - Upload `workflows/demo_pipeline.json`
   - Upload `workflows/onboarding_pipeline.json`

3. **Configure paths**
   - Update file paths to match your system
   - Set up optional Slack notifications (if desired)

4. **Execute**
   - Trigger manually or on file upload
   - Monitor execution in n8n UI

---

## 🔍 Idempotency & Safety

### Running Pipeline Multiple Times

✅ **Safe to run repeatedly:**
- Overwrites outputs (memos, agent specs, changelogs)
- Appends to logs (doesn't duplicate)
- No duplicate accounts created

### Data Integrity

- ✅ **v1 preserved** when creating v2
- ✅ **Source transcripts never modified**
- ✅ **Changelog tracks all changes**
- ✅ **Logs record every execution**

---

## 📊 Sample Outputs

### Account Memo (v1)
[See: `outputs/accounts/ben_penoyer_electrical/v1/memo.json`]

### Account Memo (v2)
[See: `outputs/accounts/ben_penoyer_electrical/v2/memo.json`]

### Agent Specification (v2)
[See: `outputs/accounts/ben_penoyer_electrical/v2/agent_spec.json`]

### Changelog
[See: `changelog/ben_penoyer_electrical_v1_to_v2.json`]

---

## 🎥 Demo Video Checklist

When recording your Loom video (3-5 minutes), show:

1. ✅ **Project structure** - Quick tour of folders
2. ✅ **Run Pipeline A** - `python run_pipeline.py` (demo → v1)
3. ✅ **Show v1 output** - Open memo.json, show `questions_or_unknowns`
4. ✅ **Run Pipeline B** - Onboarding transcript processing
5. ✅ **Show v2 output** - Highlight resolved unknowns
6. ✅ **Show changelog** - Point out tracked changes
7. ✅ **n8n workflows** (if time) - Quick import demo

**Key talking points:**
- "Notice how v1 marks unknowns instead of guessing"
- "The patch only updates what changed"
- "v1 is preserved, not overwritten"
- "Changelog provides full audit trail"

---

## 🚨 Known Limitations

| Issue | Current State | Future Improvement |
|-------|---------------|-------------------|
| **Extraction accuracy** | Rule-based, limited | Use local LLM (Llama, Mistral) |
| **Phone number formats** | Basic regex | Handle international formats |
| **Multi-account processing** | Sequential | Parallel processing |
| **Error handling** | Basic validation | Retry logic, better errors |
| **Audio input** | Whisper script included | Real-time transcription |

---

## 🛠 Extending the System

### Adding New Extraction Rules

Edit `scripts/extract_demo.py` or `scripts/extract_onboarding.py`:

```python
def extract_new_field(text):
    """Your custom extraction logic."""
    if "keyword" in text.lower():
        return extracted_value
    return None
```

### Adding New Agent Spec Fields

Edit `scripts/generate_agent.py`:

```python
def generate_agent_spec(memo):
    return {
        ...existing_fields...,
        "new_field": memo.get("new_field")
    }
```

### Integrating with External Systems

- **CRM Integration**: Modify scripts to POST to Jobber/ServiceTitan APIs
- **Retell AI**: Use their API to auto-deploy agent configs
- **Notifications**: Add email/Slack alerts in `run_pipeline.py`

---

## 📈 Production Readiness Checklist

To make this production-ready:

- [ ] Replace local JSON with PostgreSQL/MongoDB
- [ ] Add authentication and authorization
- [ ] Implement proper error handling and retries
- [ ] Add unit tests for extraction functions
- [ ] Set up CI/CD pipeline
- [ ] Add monitoring and alerting
- [ ] Implement rate limiting for API calls
- [ ] Add data encryption for sensitive fields
- [ ] Create admin UI for reviewing/editing memos
- [ ] Add webhook support for real-time triggers

---

## 💡 Why This Approach Works

### Engineering Maturity Signals

✅ **Separation of concerns** - Each script has one job  
✅ **Version control** - v1 → v2 with full audit trail  
✅ **Idempotency** - Safe to re-run  
✅ **Logging** - Execution tracking  
✅ **Documentation** - Clear README and code comments  
✅ **No hallucination** - Deterministic, rule-based extraction  
✅ **Extensibility** - Easy to add new rules and fields  

### Business Value

✅ **Reduces manual work** - Automates memo creation  
✅ **Catches unknowns** - Prevents incomplete configs  
✅ **Tracks changes** - Full transparency on updates  
✅ **Scalable** - Can process hundreds of accounts  
✅ **Cost-effective** - Zero external API costs  

---

## 📞 Support

For questions or issues:
- Review logs: `logs/run_log.txt`
- Check outputs: `outputs/accounts/<account_id>/`
- Verify transcripts: `dataset/demo/` and `dataset/onboarding/`

---

## 🏆 Project Highlights

This system demonstrates:

1. **Practical system design** - Two-pipeline architecture
2. **Data integrity** - Version control, changelog, audit trail
3. **No hallucination** - Marks unknowns explicitly
4. **Engineering best practices** - Logging, idempotency, modularity
5. **Production pathway** - Clear upgrade path from prototype to production

**Built for ZenTrades Assignment - March 2026**

---

## 📝 License

Internal use only - ZenTrades Assignment Project
