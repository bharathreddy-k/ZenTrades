import os
import sys
from datetime import datetime

def print_header(text):
    """Print formatted header."""
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")

def run_command(script_name, description):
    """Run a Python script and handle errors."""
    print(f"▶️  {description}...")
    result = os.system(f"python {script_name}")
    
    if result != 0:
        print(f"❌ ERROR: {script_name} failed with exit code {result}")
        return False
    return True

def main():
    """Execute complete pipeline: Demo → v1 → Onboarding → v2 → Changelog."""
    
    start_time = datetime.now()
    
    print_header("🚀 ZENTRADES AI AGENT PIPELINE")
    print(f"Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Change to scripts directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Pipeline A: Demo → v1
    print_header("PIPELINE A: Demo Transcripts → v1 Agent Specs")
    
    if not run_command("extract_demo.py", "Step 1: Extracting account memos from demo transcripts"):
        sys.exit(1)
    
    if not run_command("generate_agent.py", "Step 2: Generating v1 AI agent specifications"):
        sys.exit(1)
    
    # Pipeline B: Onboarding → v2
    print_header("PIPELINE B: Onboarding Transcripts → v2 Agent Specs")
    
    if not run_command("extract_onboarding.py", "Step 3: Extracting updates from onboarding transcripts"):
        sys.exit(1)
    
    if not run_command("apply_patch.py", "Step 4: Applying patches and creating v2"):
        sys.exit(1)
    
    if not run_command("generate_agent.py", "Step 5: Regenerating agent specifications (v1 + v2)"):
        sys.exit(1)
    
    # Summary
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print_header("✅ PIPELINE EXECUTION COMPLETE")
    print(f"Duration: {duration:.2f} seconds")
    print(f"Completed at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    print("📁 Outputs saved to: outputs/accounts/")
    print("📝 Changelogs saved to: changelog/")
    print("📋 Logs saved to: logs/run_log.txt\n")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()