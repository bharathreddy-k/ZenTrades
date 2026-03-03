import os
import json


def load_memo(account_id):
    path = f"../outputs/accounts/{account_id}/v1/memo.json"
    with open(path, "r") as f:
        return json.load(f)


def generate_agent_spec(memo):
    """Generate Retell AI agent specification from memo."""
    version = memo.get("version", "v1")
    
    # Build system prompt based on available data
    services_text = "\n- ".join(memo.get("services_supported", ["General services"]))
    
    emergency_text = "Not yet defined."
    if memo.get("emergency_definition"):
        emergency_text = "\n- ".join(memo.get("emergency_definition", []))
    
    hours_text = memo.get("business_hours", "Not specified")
    tz_text = memo.get("timezone", "Not specified")
    
    return {
        "agent_name": f"{memo['account_id']} - {version}",
        "voice_style": "Professional, calm, efficient",
        "voice_speed": "medium",
        "version": version,
        "key_variables": {
            "company_name": memo.get("company_name"),
            "business_hours": memo.get("business_hours"),
            "timezone": memo.get("timezone"),
            "office_address": memo.get("office_address"),
            "services_supported": memo.get("services_supported"),
            "emergency_definition": memo.get("emergency_definition"),
            "integration_constraints": memo.get("integration_constraints")
        },
        "system_prompt": f"""You are a professional AI receptionist for {memo.get('company_name', 'the company')}.

BUSINESS INFORMATION:
Business Hours: {hours_text} ({tz_text})
Office Address: {memo.get('office_address', 'Not provided')}

SERVICES OFFERED:
- {services_text}

EMERGENCY DEFINITION:
- {emergency_text}

RULES:
1. Do NOT invent information that is not provided above.
2. If business hours are unknown, ask caller when they would like to be contacted.
3. Collect only necessary routing details: name, phone number, and issue description.
4. For emergencies, also collect address immediately.
5. Do NOT mention internal tools (Jobber, CRM, etc.) to callers.
6. Be concise, professional, and helpful.
7. If transfer fails, apologize and assure prompt follow-up.
        """,
        "business_hours_flow": [
            "Greet caller professionally.",
            "Ask purpose of call.",
            "Collect caller name and phone number.",
            "Ask qualifying questions based on service type.",
            "Attempt transfer to office line.",
            "If transfer fails, take message and confirm callback within specified time.",
            "Ask if anything else is needed.",
            "Close call politely."
        ],
        "after_hours_flow": [
            "Greet caller professionally.",
            "Inform caller it is after business hours.",
            "Ask purpose of call.",
            "Determine if emergency.",
            "IF EMERGENCY:",
            "  - Collect name, phone number, address, and issue description immediately.",
            "  - Attempt transfer to on-call number.",
            "  - If transfer fails, apologize and assure urgent follow-up.",
            "IF NOT EMERGENCY:",
            "  - Collect name, phone number, and brief description.",
            "  - Confirm someone will call back during next business hours.",
            "Ask if anything else is needed.",
            "Close call politely."
        ],
        "call_transfer_protocol": memo.get("call_transfer_rules", {
            "timeout_seconds": 30,
            "retry_policy": "Take message if no answer",
            "on_fail_message": "We are unable to connect you right now. We will follow up shortly."
        }),
        "integration_notes": memo.get("integration_constraints", []),
        "questions_or_unknowns": memo.get("questions_or_unknowns", [])
    }


def save_agent_spec(account_id, agent_spec):
    path = f"../outputs/accounts/{account_id}/v1/agent_spec.json"
    with open(path, "w") as f:
        json.dump(agent_spec, f, indent=4)


def main():
    accounts_path = "../outputs/accounts"
    
    if not os.path.exists(accounts_path):
        print(f"❌ ERROR: Accounts path not found: {accounts_path}")
        return
    
    accounts = [d for d in os.listdir(accounts_path) if os.path.isdir(os.path.join(accounts_path, d))]
    
    if not accounts:
        print(f"⚠️  No accounts found in {accounts_path}")
        return
    
    print(f"\n{'='*60}")
    print(f"🤖 Generating AI Agent Specifications")
    print(f"{'='*60}\n")

    generated = 0

    for account_id in accounts:
        if account_id.startswith("."):
            continue

        for version in ["v1", "v2"]:
            memo_path = f"../outputs/accounts/{account_id}/{version}/memo.json"

            if os.path.exists(memo_path):
                with open(memo_path, "r") as f:
                    memo = json.load(f)

                agent_spec = generate_agent_spec(memo)
                agent_spec["version"] = version

                save_path = f"../outputs/accounts/{account_id}/{version}/agent_spec.json"
                with open(save_path, "w") as f:
                    json.dump(agent_spec, f, indent=4)
                
                print(f"✅ Generated {version} agent spec for: {account_id}")
                generated += 1

    print(f"\n{'='*60}")
    print(f"✅ Agent spec generation complete. Created {generated} spec(s).")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()