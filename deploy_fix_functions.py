import paramiko, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('187.124.245.99', port=65002, username='u284669846', password='[3pPybi0[3pPybi0', timeout=20)

def run(cmd):
    _, o, _ = ssh.exec_command(cmd)
    return o.read().decode('utf-8', errors='replace')

wp = '/home/u284669846/domains/plantsmag.com/public_html'
theme = wp + '/wp-content/themes/plantsmag-premium'

# Upload fixed functions.php
print("Uploading fixed remote_functions.php...")
sftp = ssh.open_sftp()

# Read the fixed local file
with open(r'd:\project\plantsmag\remote_functions.php', 'r', encoding='utf-8') as f:
    content = f.read()

# Write to theme directory as functions.php
with sftp.open(theme + '/functions.php', 'w') as f:
    f.write(content)
sftp.close()
print(f"  Uploaded to {theme}/functions.php")

# Verify the fix
print("\nVerifying IndexNow function...")
out = run(f"grep -n 'plantsmag_instant_indexing_on_publish' {theme}/functions.php")
print(f"  {out.strip()}")

# Check for PowerShell artifacts
out = run(f"grep -c 'System.Management.Automation' {theme}/functions.php")
count = out.strip()
print(f"  PowerShell artifacts remaining: {count}")

# Check for backslash-only variables
out = run(f"grep -c '^\\ ' {theme}/functions.php 2>&1 || echo 0")
print(f"  Backslash variables: {out.strip()}")

# Verify PHP syntax
out = run(f"php -l {theme}/functions.php 2>&1")
print(f"  PHP syntax: {out.strip()}")

# Flush caches
out = run(f'cd {wp} && wp cache flush 2>&1')
print(f"\n  WP cache: {out.strip()}")
out = run(f'cd {wp} && wp litespeed-purge all 2>&1')
print(f"  LiteSpeed: {out.strip()}")

# Test IndexNow key endpoint
import urllib.request, ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

print("\nTesting IndexNow key endpoint...")
try:
    req = urllib.request.Request('https://plantsmag.com/plantsmag-indexnow-key-2026.txt',
                                 headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
        body = r.read().decode('utf-8')
        print(f"  Status: {r.status}")
        print(f"  Body: {body.strip()}")
        if body.strip() == 'plantsmag-indexnow-key-2026':
            print("  IndexNow key verification: WORKING!")
        else:
            print("  IndexNow key verification: WRONG CONTENT")
except Exception as e:
    print(f"  IndexNow key test: {e}")

ssh.close()
print("\nDone!")
