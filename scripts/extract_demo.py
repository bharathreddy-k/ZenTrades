import os
import json
import re
from datetime import datetime


def extract_account_id(filename):
    return os.path.splitext(filename)[0].lower().replace(" ", "_")


def extract_company_name(filename, text):
    """Extract company name from filename (best effort)."""
    # Remove file extension and convert to title case
    name = os.path.splitext(filename)[0].replace("_", " ").title()
    return name if name else None


def extract_services(text):
    """Extract mentioned services from transcript."""
    text_lower = text.lower()
    services = []
    
    service_keywords = {
        "residential electrical service": ["residential service", "residential electrical", "residential calls"],
        "commercial electrical service": ["commercial service", "commercial electrical", "commercial projects"],
        "panel upgrades": ["panel upgrade", "panel upgrades", "electrical panel"],
        "rewiring": ["rewiring", "rewire"],
        "repairs": ["repair", "repairs", "troubleshooting"],
        "installations": ["installation", "installations", "install"],
        "EV charger installation": ["ev charger", "electric vehicle charger"]
    }
    
    for service, keywords in service_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            services.append(service)
    
    return services if services else ["Services mentioned generically"]


def extract_emergency_mentions(text):
    """Extract emergency-related information."""
    text_lower = text.lower()
    emergency_triggers = []
    
    # Check for specific emergency scenarios
    emergency_scenarios = [
        "exposed wiring", "electrical fire", "power outage", 
        "sparking outlet", "sparking panel", "burning smell"
    ]
    
    for scenario in emergency_scenarios:
        if scenario in text_lower:
            emergency_triggers.append(scenario.title())
    
    # If emergency is mentioned but not defined
    if "emergency" in text_lower and not emergency_triggers:
        emergency_triggers.append("Emergency mentioned but not clearly defined")
    
    return emergency_triggers if emergency_triggers else None


def extract_integrations(text):
    """Check for CRM or integration mentions."""
    text_lower = text.lower()
    integrations = []
    
    crm_tools = ["jobber", "servicetitan", "housecall pro", "fieldpulse"]
    
    for tool in crm_tools:
        if tool in text_lower:
            integrations.append(f"Uses {tool.title()} CRM (integration pending)")
    
    return integrations


def generate_memo(account_id, filename, transcript_text):
    """Generate account memo from demo transcript."""
    memo = {
        "account_id": account_id,
        "company_name": extract_company_name(filename, transcript_text),
        "business_hours": None,
        "office_address": None,
        "timezone": None,
        "services_supported": extract_services(transcript_text),
        "emergency_definition": extract_emergency_mentions(transcript_text),
        "emergency_routing_rules": None,
        "non_emergency_routing_rules": None,
        "call_transfer_rules": None,
        "integration_constraints": extract_integrations(transcript_text),
        "after_hours_flow_summary": None,
        "office_hours_flow_summary": None,
        "questions_or_unknowns": [],
        "notes": "Generated from demo call transcript",
        "source": "demo_transcript",
        "version": "v1"
    }

    # Detect what's missing and add to unknowns
    if memo["business_hours"] is None:
        memo["questions_or_unknowns"].append("Business hours not specified in demo")
    
    if memo["timezone"] is None:
        memo["questions_or_unknowns"].append("Timezone not specified in demo")
    
    if memo["office_address"] is None:
        memo["questions_or_unknowns"].append("Office address not provided in demo")
    
    if memo["emergency_definition"] is None or "not clearly defined" in str(memo["emergency_definition"]):
        memo["questions_or_unknowns"].append("Emergency definition needs clarification")
    
    if memo["call_transfer_rules"] is None:
        memo["questions_or_unknowns"].append("Call transfer rules and phone numbers needed")

    return memo


def save_memo(account_id, memo):
    base_path = f"../outputs/accounts/{account_id}/v1"
    os.makedirs(base_path, exist_ok=True)

    with open(f"{base_path}/memo.json", "w") as f:
        json.dump(memo, f, indent=4)


def log_run(account_id, pipeline, status):
    """Log pipeline execution with timestamp."""
    os.makedirs("../logs", exist_ok=True)
    log_entry = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {pipeline.upper()} - {account_id} - {status}\n"
    
    with open("../logs/run_log.txt", "a") as log:
        log.write(log_entry)


def main():
    dataset_path = "../dataset/demo"
    
    # Check if dataset folder exists
    if not os.path.exists(dataset_path):
        print(f"❌ ERROR: Dataset path not found: {dataset_path}")
        return
    
    files = os.listdir(dataset_path)
    transcript_files = [f for f in files if f.endswith(".txt")]
    
    if not transcript_files:
        print(f"⚠️  No transcript files (.txt) found in {dataset_path}")
        return
    
    print(f"\n{'='*60}")
    print(f"🟦 Pipeline A: Demo Extraction (v1)")
    print(f"{'='*60}\n")

    for file in transcript_files:
        print(f"📄 Processing: {file}")
        
        with open(os.path.join(dataset_path, file), "r", encoding="utf-8") as f:
            transcript_text = f.read()

        account_id = extract_account_id(file)
        memo = generate_memo(account_id, file, transcript_text)
        save_memo(account_id, memo)
        log_run(account_id, "demo_extraction", "SUCCESS")
        
        print(f"   ✅ Created v1 memo for: {account_id}")
        print(f"   📁 Saved to: outputs/accounts/{account_id}/v1/memo.json\n")

    print(f"{'='*60}")
    print(f"✅ Demo extraction complete. Processed {len(transcript_files)} file(s).")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()