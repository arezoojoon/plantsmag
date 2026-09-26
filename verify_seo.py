import paramiko, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('187.124.245.99', port=65002, username='u284669846', password='[3pPybi0[3pPybi0', timeout=20)

def run(cmd):
    _, o, _ = ssh.exec_command(cmd)
    return o.read().decode('utf-8', errors='replace')

wp = '/home/u284669846/domains/plantsmag.com/public_html'

print("=== FINAL VERIFICATION ===\n")

# 1. Canonical tag count on a regular post
print("1. Canonical tag test on a post:")
url = run(f'cd {wp} && wp post list --post_type=post --post_status=publish --field=url 2>&1 | grep http | tail -1').strip()
canonical_lines = run(f'curl -s "{url}" | grep -i canonical')
count = canonical_lines.lower().count('canonical')
print(f"   URL: {url}")
print(f"   Canonical count: {count}")
for line in canonical_lines.strip().split('\n'):
    if line.strip():
        print(f"   {line.strip()}")
if count == 1:
    print("   PASS: Only 1 canonical tag (RankMath)")
else:
    print(f"   FAIL: Expected 1, found {count}")

# 2. Homepage canonical
print("\n2. Homepage canonical test:")
home_canonical = run('curl -s "https://plantsmag.com/" | grep -i canonical')
home_count = home_canonical.lower().count('canonical')
print(f"   Canonical count: {home_count}")
for line in home_canonical.strip().split('\n'):
    if line.strip():
        print(f"   {line.strip()}")

# 3. Sample of updated titles
print("\n3. Sample updated titles (last 10):")
titles = run(f'cd {wp} && wp post list --post_type=post --post_status=publish --fields=ID,post_title --format=csv 2>&1 | tail -10')
print(titles)

# 4. Check modified dates
print("\n4. Modified date check (should all be today):")
dates = run(f'cd {wp} && wp post list --post_type=post --post_status=publish --fields=ID,post_modified --format=csv 2>&1 | head -6')
print(dates)

ssh.close()
print("\n=== VERIFICATION COMPLETE ===")
