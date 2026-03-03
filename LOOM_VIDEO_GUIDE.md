# 🎥 Loom Video Script (3-5 minutes)

## 📋 Before Recording Checklist

- [ ] Open VS Code with project folder
- [ ] Have terminal ready in `scripts/` directory
- [ ] Have a browser tab ready with GitHub
- [ ] Test your audio and screen recording
- [ ] Close unnecessary applications

---

## 🎬 Recording Script

### Scene 1: Introduction (30 seconds)

**[Show Project Folder in VS Code]**

> "Hi! I'm going to show you the ZenTrades AI Agent Pipeline I built. This system converts demo and onboarding call transcripts into production-ready AI agent configurations with full version control and change tracking."

**[Quick folder tree overview]**

> "The structure is clean: we have input transcripts in `dataset/`, Python scripts in `scripts/`, and outputs get organized by account with v1 and v2 folders."

---

### Scene 2: Show Input Transcripts (45 seconds)

**[Open demo transcript]**

> "This is a demo call transcript for Ben Penoyer Electrical. Notice it's a natural conversation where some details are mentioned - like services and emergency scenarios - but critical information like business hours, timezone, and phone numbers are NOT provided yet."

**[Open onboarding transcript]**

> "This is the onboarding call for the same account. Here we get specific details: 'Monday through Friday, 8 AM to 5 PM Eastern', the full address, phone numbers, detailed emergency definitions. This is what fills in all the gaps."

---

### Scene 3: Run Pipeline A (45 seconds)

**[Open terminal, run pipeline]**

```bash
cd scripts
python run_pipeline.py
```

**While it runs:**

> "Pipeline A processes the demo transcript first. Watch the output - it extracts account info, creates v1 memo, generates the AI agent spec."

**[Open v1 memo.json]**

> "Here's the v1 memo. See how `business_hours` is **null**? `timezone` is **null**? The system **never invents data**. Instead, it adds these to the `questions_or_unknowns` array at the bottom. This prevents AI hallucination."

---

### Scene 4: Show v1 Agent Spec (30 seconds)

**[Open v1 agent_spec.json]**

> "The v1 agent spec uses whatever data we have. The system prompt says 'Business hours: Not specified' - it's honest about what's missing. The call flows are generic because we don't have specific rules yet."

---

### Scene 5: Pipeline B Magic (45 seconds)

**[Go back to terminal output, scroll to Pipeline B section]**

> "Pipeline B processes the onboarding transcript. It extracts 7 specific fields - look at that. Then it applies a patch to create v2 **without overwriting v1**."

**[Open v2 memo.json]**

> "Here's v2. Now we have: business hours filled in, timezone is Eastern, full office address, detailed emergency definitions, and phone numbers. And look - the `questions_or_unknowns` list is now almost empty because we resolved those items."

---

### Scene 6: The Changelog (45 seconds)

**[Open changelog JSON]**

**THIS IS THE KEY DIFFERENTIATOR - spend time here!**

> "This is what makes this system production-grade. The changelog shows exactly what changed from v1 to v2. Business hours went from null to 'Monday-Friday 8AM - 5PM'. Emergency definition was expanded. Every change is tracked with old value, new value, and reason."

**[Scroll through changelog]**

> "This gives you a full audit trail. You can see what was added during onboarding, and if something breaks in v2, you can always roll back to v1."

---

### Scene 7: Key Features (30 seconds)

**[Show folder structure again]**

> "Key features of this system:
> 1. **No hallucination** - Unknown fields marked as null
> 2. **Version control** - v1 preserved, not overwritten
> 3. **Full audit trail** - Changelog tracks every change
> 4. **Idempotent** - Safe to run multiple times
> 5. **Zero cost** - Uses rule-based extraction, no LLM APIs"

---

### Scene 8: Integration & Extensibility (20 seconds)

**[Show n8n workflow files]**

> "I've also created n8n workflow JSON files that can be imported for visual automation. The workflows trigger on file upload, run the Python scripts, and can send notifications."

**[Show a quick peek at README]**

> "Everything is documented in the README with architecture diagrams, API specs, and production readiness checklist."

---

### Scene 9: Wrap Up (20 seconds)

> "This system demonstrates practical system design: separation of concerns, data integrity, change tracking, and clear upgrade path from prototype to production. Thanks for watching!"

---

## 🎯 Key Points to Emphasize

1. ⭐ **No hallucination** - Say "null" not "invented data"
2. ⭐ **v1 is preserved** - Not overwritten
3. ⭐ **Changelog is the star** - Full audit trail
4. ⭐ **Rule-based extraction** - Zero API costs
5. ⭐ **Production thinking** - Idempotency, logging, versioning

---

## 📊 Demo Flow Summary

```
Show Structure (30s)
   │
   ▼
Show Transcripts (45s)
   │
   ▼
Run Pipeline (45s)
   │
   ▼
Show v1 Output (30s)
   │
   ▼
Show v2 Output (45s)
   │
   ▼
★ Show Changelog ★ (45s) ← SPEND TIME HERE
   │
   ▼
Key Features (30s)
   │
   ▼
Wrap Up (20s)
```

**Total: ~4 minutes 30 seconds**

---

## 🚫 What NOT to Do

- ❌ Don't apologize or say "I should have..."
- ❌ Don't talk too fast
- ❌ Don't skip the changelog (it's your differentiator!)
- ❌ Don't go into code details (show results, not code)
- ❌ Don't go over 5 minutes

---

## 💡 Pro Tips

✅ Pause briefly between sections  
✅ Use "Notice..." and "See how..." to guide viewer's eyes  
✅ Sound confident - this is a solid system  
✅ Smile when you say "no hallucination" 😊  

---

## 🎯 What Makes This Stand Out

When reviewers watch this, they should think:

1. **"This person understands production systems"** - Version control, audit trails
2. **"They avoid common mistakes"** - No data hallucination
3. **"This is actually usable"** - Clean structure, documented, tested
4. **"They think like an engineer"** - Idempotency, logging, extensibility

---

## 📝 After Recording

- [ ] Watch it once - does it flow well?
- [ ] Check audio quality
- [ ] Verify screen is readable
- [ ] Under 5 minutes? ✅
- [ ] Changelog section clear? ✅

**Good luck! You've got this! 🚀**
