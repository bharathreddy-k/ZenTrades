import os
import json
import re


def extract_account_id(filename):
    return os.path.splitext(filename)[0].lower().replace(" ", "_")


def extract_business_hours(text):
    """Extract business hours from text."""
    text_lower = text.lower()
    
    # Pattern: "Monday through Friday, 8 AM to 5 PM"
    pattern = r"(monday\s+(?:through|to|thru|-)\s+friday)[,\s]+(\d+\s*am)\s+(?:to|-)\s+(\d+\s*pm)"
    match = re.search(pattern, text_lower)
    
    if match:
        days = "Monday-Friday"
        start_time = match.group(2).upper().replace(" ", "")
        end_time = match.group(3).upper().replace(" ", "")
        return f"{days} {start_time} - {end_time}"
    
    return None


def extract_timezone(text):
    """Extract timezone from text."""
    text_lower = text.lower()
    
    timezones = {
        "eastern": "Eastern",
        "est": "Eastern",
        "et": "Eastern",
        "central": "Central",
        "cst": "Central",
        "ct": "Central",
        "mountain": "Mountain",
        "mst": "Mountain",
        "mt": "Mountain",
        "pacific": "Pacific",
        "pst": "Pacific",
        "pt": "Pacific"
    }
    
    for key, value in timezones.items():
        if f" {key} " in f" {text_lower} " or text_lower.endswith(key):
            return value
    
    return None


def extract_address(text):
    """Extract office address from text."""
    # Pattern: number + street + city, state zip
    pattern = r"(\d+\s+[A-Za-z\s]+(?:road|street|avenue|drive|lane|way|boulevard|parkway|rd|st|ave|dr|ln|blvd|pkwy)),?\s+([A-Za-z\s]+),\s+([A-Z]{2})[,\s]+(\d{5})"
    match = re.search(pattern, text, re.IGNORECASE)
    
    if match:
        return f"{match.group(1)}, {match.group(2)}, {match.group(3)} {match.group(4)}"
    
    return None


def extract_phone_numbers(text):
    """Extract phone numbers from text."""
    phones = {}
    
    # Pattern for phone numbers
    phone_pattern = r"(\d{3}[-\s]?\d{3}[-\s]?\d{4})"
    
    # Office/main line
    if "office line" in text.lower() or "main office" in text.lower():
        context = text[max(0, text.lower().find("office")-50):text.lower().find("office")+100]
        match = re.search(phone_pattern, context)
        if match:
            phones["office_number"] = match.group(1).replace("-", "-").replace(" ", "-")
    
    # On-call/emergency number  
    if "personal cell" in text.lower() or "on-call number" in text.lower() or "after hours" in text.lower():
        if "personal cell" in text.lower():
            idx = text.lower().find("personal cell")
        else:
            idx = text.lower().find("on-call")
        context = text[max(0, idx-20):idx+100]
        match = re.search(phone_pattern, context)
        if match:
            phones["on_call_number"] = match.group(1).replace(" ", "-")
    
    return phones


def extract_email(text):
    """Extract email address from text."""
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    match = re.search(pattern, text)
    return match.group(0) if match else None


def extract_emergency_definition(text):
    """Extract detailed emergency definitions."""
    text_lower = text.lower()
    emergency_list = []
    
    # Look for explicit emergency definitions
    if "emergency for us means" in text_lower or "emergency means" in text_lower:
        # Extract the sentence/section
        start_idx = text_lower.find("emergency")
        context = text[start_idx:start_idx+500]
        
        scenarios = [
            "power outage", "exposed wiring", "sparking outlet", "sparking panel",
            "sparking electrical", "burning smell", "electrical fire", "electrical fires"
        ]
        
        for scenario in scenarios:
            if scenario in context.lower():
                emergency_list.append(scenario.title())
    
    return list(set(emergency_list)) if emergency_list else None


def extract_callback_time(text):
    """Extract callback time commitment."""
    text_lower = text.lower()
    
    # Look for callback times in minutes
    patterns = [
        r"(\d+)\s*minutes?",
        r"(\d+)\s*min",
        r"within\s+(\d+)"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text_lower)
        if match and "call back" in text_lower[max(0, match.start()-50):match.end()+50]:
            return int(match.group(1))
    
    return None


def extract_updates(transcript_text):
    """Extract all updates from onboarding transcript."""
    updates = {}
    
    # Business hours
    hours = extract_business_hours(transcript_text)
    if hours:
        updates["business_hours"] = hours
    
    # Timezone
    tz = extract_timezone(transcript_text)
    if tz:
        updates["timezone"] = tz
    
    # Address
    addr = extract_address(transcript_text)
    if addr:
        updates["office_address"] = addr
    
    # Emergency definition
    emerg = extract_emergency_definition(transcript_text)
    if emerg:
        updates["emergency_definition"] = emerg
    
    # Phone numbers
    phones = extract_phone_numbers(transcript_text)
    if phones:
        updates["phone_numbers"] = phones
    
    # Email
    email = extract_email(transcript_text)
    if email:
        updates["emergency_contact_email"] = email
    
    # Callback time
    callback_mins = extract_callback_time(transcript_text)
    if callback_mins:
        updates["callback_time_minutes"] = callback_mins
    
    # Call transfer rules (build from phones)
    if phones:
        updates["call_transfer_rules"] = {
            "business_hours_number": phones.get("office_number"),
            "after_hours_emergency_number": phones.get("on_call_number"),
            "timeout_seconds": 30,
            "retry_policy": "Take message if no answer"
        }
    
    return updates


def save_patch(account_id, patch):
    """Save patch file for account."""
    path = f"../outputs/accounts/{account_id}"
    os.makedirs(path, exist_ok=True)
    
    with open(f"{path}/patch.json", "w") as f:
        json.dump(patch, f, indent=4)


def main():
    dataset_path = "../dataset/onboarding"
    
    if not os.path.exists(dataset_path):
        print(f"❌ ERROR: Dataset path not found: {dataset_path}")
        return
    
    files = os.listdir(dataset_path)
    transcript_files = [f for f in files if f.endswith(".txt")]
    
    if not transcript_files:
        print(f"⚠️  No transcript files (.txt) found in {dataset_path}")
        return
    
    print(f"\n{'='*60}")
    print(f"🟩 Pipeline B: Onboarding Extraction (Updates)")
    print(f"{'='*60}\n")

    for file in transcript_files:
        print(f"📄 Processing: {file}")
        
        with open(os.path.join(dataset_path, file), "r", encoding="utf-8") as f:
            transcript_text = f.read()

        account_id = extract_account_id(file)
        patch = extract_updates(transcript_text)
        save_patch(account_id, patch)
        
        print(f"   ✅ Created patch for: {account_id}")
        print(f"   📝 Extracted {len(patch)} fields")
        print(f"   📁 Saved to: outputs/accounts/{account_id}/patch.json\n")

    print(f"{'='*60}")
    print(f"✅ Onboarding extraction complete. Processed {len(transcript_files)} file(s).")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()