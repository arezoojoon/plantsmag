import subprocess
import time
import sys

print("Starting SPRINT 2: Generating 15 Comparison Articles")
for i in range(15):
    print(f"[{i+1}/15] Triggering Node.js Engine for Comparison Article...")
    result = subprocess.run(
        ["node", "seo-automation-cron.js", "--test", "comparison"], 
        cwd=r"d:\project\plantsmag\engine",
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(f"Success for article {i+1}.")
        lines = result.stdout.strip().split('\n')
        for line in lines[-5:]:
            print(f"  {line}")
    else:
        print(f"Error generating article {i+1}:")
        print(result.stderr)
    
    if i < 14:
        print("Cooling down for 3 seconds...")
        time.sleep(3)

print("\nSPRINT 2 Generation Complete!")
