import paramiko, sys, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HOST = '187.124.245.99'
PORT = 65002
USER = 'u284669846'
PASS = '[3pPybi0[3pPybi0'

LOCAL_THEME = r'd:\project\plantsmag\plantsmag-premium'
LOCAL_BASE  = r'd:\project\plantsmag'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, port=PORT, username=USER, password=PASS, timeout=20)

def run(cmd, timeout=15):
    _, o, _ = ssh.exec_command(cmd, timeout=timeout)
    return o.read().decode('utf-8', errors='replace').strip()

print("=" * 65)
print("FINDING plantsmag.com on this server")
print("=" * 65)

# List all domains
print("\nAll domains:")
print(run('ls /home/u284669846/domains/'))
print(run('ls /home/u284669846/public_html/ 2>/dev/null || echo "no public_html"'))

# Search for plantsmag
print("\nSearching for plantsmag...")
print(run('find /home/u284669846 -maxdepth 4 -name "*.com" -type d 2>/dev/null'))
print(run('find /home/u284669846 -maxdepth 5 -name "plantsmag*" -type d 2>/dev/null'))
print(run('find /home/u284669846 -maxdepth 5 -name "wp-config.php" 2>/dev/null'))

# Check public_html
print("\nPublic HTML structure:")
print(run('ls -la /home/u284669846/public_html/ 2>/dev/null || ls -la /home/u284669846/htdocs/ 2>/dev/null || echo NOT_FOUND'))

# Check if plantsmag is in domains/
print("\nDomain folders:")
print(run('ls /home/u284669846/domains/ 2>/dev/null'))

ssh.close()
