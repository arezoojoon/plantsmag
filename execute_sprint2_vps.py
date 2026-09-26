import paramiko
import time
import sys

# Force UTF-8 on stdout
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HOST = '72.62.93.117'
USER = 'root'
PASSWORD = "5KT4'ub5B5oD8V9TB#/u"
REMOTE_DIR = "/root/plantsmag-engine"

print("Connecting to VPS...")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, port=22, username=USER, password=PASSWORD, timeout=15)
print("Connected successfully.")

print("Starting SPRINT 2: Generating 15 Comparison Articles on VPS...")

for i in range(15):
    print(f"\n[{i+1}/15] Triggering Node.js Engine on VPS...")
    cmd = f"cd {REMOTE_DIR} && node seo-automation-cron.js --test comparison"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    
    status = stdout.channel.recv_exit_status()
    
    if status == 0:
        print(f"Success for article {i+1}.")
        lines = out.split('\n')
        for line in lines[-5:]:
            print(f"  {line}")
    else:
        print(f"Error generating article {i+1}:")
        print(err if err else out)
        
    if i < 14:
        print("Cooling down for 3 seconds...")
        time.sleep(3)

print("\nSPRINT 2 Generation Complete!")
ssh.close()
