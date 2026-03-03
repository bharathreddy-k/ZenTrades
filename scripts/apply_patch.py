import os
import json


def load_v1(account_id):
    path = f"../outputs/accounts/{account_id}/v1/memo.json"
    with open(path, "r") as f:
        return json.load(f)


def load_patch(account_id):
    path = f"../outputs/accounts/{account_id}/patch.json"
    with open(path, "r") as f:
        return json.load(f)


def apply_patch_logic(v1, patch):
    """Apply patch to v1 memo, creating v2 with tracked changes."""
    v2 = v1.copy()
    changes = []

    for key, new_value in patch.items():
        old_value = v1.get(key)

        # Skip if values are identical
        if old_value == new_value:
            continue
        
        # Handle nested updates (like phone_numbers, call_transfer_rules)
        if isinstance(new_value, dict) and isinstance(old_value, dict):
            # Merge dictionaries
            merged = old_value.copy()
            merged.update(new_value)
            v2[key] = merged
            
            changes.append({
                "field": key,
                "old_value": old_value,
                "new_value": merged,
                "reason": "Updated from onboarding call"
            })
        else:
            # Direct replacement
            v2[key] = new_value
            changes.append({
                "field": key,
                "old_value": old_value,
                "new_value": new_value,
                "reason": "Clarified during onboarding"
            })
    
    # Update version and source
    v2["version"] = "v2"
    v2["source"] = "onboarding_transcript"
    v2["notes"] = "Updated with onboarding call details"
    
    # Update questions_or_unknowns - remove resolved items
    if "questions_or_unknowns" in v2 and changes:
        resolved_fields = {change["field"] for change in changes}
        v2["questions_or_unknowns"] = [
            q for q in v2.get("questions_or_unknowns", [])
            if not any(field.lower() in q.lower() for field in resolved_fields)
        ]

    return v2, changes


def save_v2(account_id, v2):
    path = f"../outputs/accounts/{account_id}/v2"
    os.makedirs(path, exist_ok=True)

    with open(f"{path}/memo.json", "w") as f:
        json.dump(v2, f, indent=4)


def save_changelog(account_id, changes):
    """Save detailed changelog for version upgrade."""
    os.makedirs("../changelog", exist_ok=True)
    
    from datetime import datetime
    
    changelog = {
        "account_id": account_id,
        "version_upgrade": "v1 -> v2",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_changes": len(changes),
        "changes": changes,
        "summary": f"Applied {len(changes)} update(s) from onboarding call"
    }
    
    path = f"../changelog/{account_id}_v1_to_v2.json"
    with open(path, "w") as f:
        json.dump(changelog, f, indent=4)


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
    print(f"🔄 Applying Patches: v1 → v2")
    print(f"{'='*60}\n")

    processed = 0
    
    for account_id in accounts:
        if account_id.startswith("."):
            continue

        try:
            # Check if patch exists
            patch_path = f"../outputs/accounts/{account_id}/patch.json"
            if not os.path.exists(patch_path):
                print(f"⏭️  Skipping {account_id}: No patch file found")
                continue
            
            print(f"📄 Processing: {account_id}")
            
            v1 = load_v1(account_id)
            patch = load_patch(account_id)
            v2, changes = apply_patch_logic(v1, patch)
            save_v2(account_id, v2)
            save_changelog(account_id, changes)
            
            print(f"   ✅ Applied {len(changes)} change(s)")
            print(f"   📁 Saved to: outputs/accounts/{account_id}/v2/")
            print(f"   📝 Changelog: changelog/{account_id}_v1_to_v2.json\n")
            
            processed += 1

        except FileNotFoundError as e:
            print(f"   ⚠️  Error: {e}")
            continue

    print(f"{'='*60}")
    print(f"✅ Patch complete. Processed {processed} account(s).")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()