import paramiko, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('187.124.245.99', port=65002, username='u284669846', password='[3pPybi0[3pPybi0', timeout=20)

def run(cmd):
    _, o, e = ssh.exec_command(cmd)
    return o.read().decode('utf-8', errors='replace'), e.read().decode('utf-8', errors='replace')

wp = '/home/u284669846/domains/plantsmag.com/public_html'

# 1. Check header.php for hardcoded canonical
print("=== 1. Checking header.php for hardcoded canonical ===")
out, _ = run(f'grep -n "canonical" {wp}/wp-content/themes/plantsmag-premium/header.php')
if out.strip():
    print(f"  FOUND canonical in header.php:\n{out}")
else:
    print("  No hardcoded canonical in header.php")

# 2. All canonical references in theme files
print("\n=== 2. All canonical references in theme ===")
out, _ = run(f'grep -rn "canonical" {wp}/wp-content/themes/plantsmag-premium/ --include="*.php"')
print(out[:2000])

# 3. Check active plugins for canonical conflicts
print("\n=== 3. Active plugins ===")
out, _ = run(f'cd {wp} && wp plugin list --status=active --format=table')
print(out[:1000])

# 4. Total published posts
print("\n=== 4. Post count ===")
out, _ = run(f'cd {wp} && wp post list --post_type=post --post_status=publish --format=count')
print(f"Published posts: {out.strip()}")

# 5. Sample post titles (first 20)
print("\n=== 5. Sample post titles (first 20) ===")
out, _ = run(f'cd {wp} && wp post list --post_type=post --post_status=publish --fields=ID,post_title --format=csv 2>&1 | head -21')
print(out)

# 6. Check live canonical on an actual published post
print("\n=== 6. Live canonical tag test ===")
out, _ = run(f'cd {wp} && wp post list --post_type=post --post_status=publish --field=url 2>&1 | head -2')
urls = [u.strip() for u in out.strip().split('\n') if u.strip().startswith('http')]
if urls:
    test_url = urls[0]
    out2, _ = run(f'curl -s "{test_url}" | grep -i canonical')
    print(f"  URL tested: {test_url}")
    print(f"  Canonical tag(s) found:")
    for line in out2.strip().split('\n'):
        print(f"    {line.strip()}")
    # Count canonical tags
    count = out2.lower().count('canonical')
    if count > 1:
        print(f"  WARNING: {count} canonical tags found! This is a conflict!")
    elif count == 1:
        if test_url in out2 or 'plantsmag.com' in out2:
            # Check if it points to homepage instead of the post
            if 'href="https://plantsmag.com/"' in out2 or "href='https://plantsmag.com/'" in out2:
                print("  CRITICAL: Canonical points to HOMEPAGE instead of this post!")
            else:
                print("  OK: Canonical appears correct")

# 7. Check wp_head for double canonical
print("\n=== 7. Checking for wp_head canonical output ===")
out, _ = run(f'grep -rn "rel.*canonical" {wp}/wp-content/themes/plantsmag-premium/ --include="*.php"')
print(out[:1500])

ssh.close()
print("\nDiagnostic complete!")
