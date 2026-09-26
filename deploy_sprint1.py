import paramiko, sys, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HOST = '187.124.245.99'
PORT = 65002
USER = 'u284669846'
PASS = '[3pPybi0[3pPybi0'

LOCAL_THEME = r'd:\project\plantsmag\plantsmag-premium'

REMOTE_BASE  = '/home/u284669846/public_html' # default, will verify
THEME_REMOTE = f'{REMOTE_BASE}/wp-content/themes/plantsmag-premium'

print("=" * 65)
print("Connecting to Hostinger for Sprint 1 Deploy...")
print("=" * 65)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, port=PORT, username=USER, password=PASS, timeout=20)
print("SSH connected!")

# Find correct web root
_, out2, _ = ssh.exec_command('find /home/u284669846 -name "wp-config.php" | grep "plantsmag" | head -1', timeout=15)
wp_config = out2.read().decode().strip()

if not wp_config:
    _, out2, _ = ssh.exec_command('find /home/u284669846/public_html -name "wp-config.php" 2>/dev/null | head -1', timeout=15)
    wp_config = out2.read().decode().strip()

if wp_config:
    REMOTE_BASE = os.path.dirname(wp_config)
    THEME_REMOTE = f'{REMOTE_BASE}/wp-content/themes/plantsmag-premium'
    print(f"Web root: {REMOTE_BASE}")
else:
    print("Warning: wp-config.php not found. Assuming /home/u284669846/public_html")

sftp = ssh.open_sftp()

# Ensure assets dir exists remotely
try:
    sftp.stat(f'{THEME_REMOTE}/assets')
except IOError:
    sftp.mkdir(f'{THEME_REMOTE}/assets')

FILES = [
    (rf'{LOCAL_THEME}\front-page.php', f'{THEME_REMOTE}/front-page.php'),
    (rf'{LOCAL_THEME}\functions.php',  f'{THEME_REMOTE}/functions.php'),
    (rf'{LOCAL_THEME}\assets\hero-plant.webp', f'{THEME_REMOTE}/assets/hero-plant.webp'),
]

print("\n📦 Uploading Sprint 1 files...")
ok = 0
for local, remote in FILES:
    try:
        sftp.put(local, remote)
        size = os.path.getsize(local)
        print(f"  ✅ {os.path.basename(local)} ({size:,} bytes)")
        ok += 1
    except Exception as e:
        print(f"  ❌ {os.path.basename(local)}: {e}")

sftp.close()
print(f"\n✅ Uploaded {ok}/{len(FILES)} files")

# Find WP-CLI and flush LiteSpeed cache
_, out3, _ = ssh.exec_command(f'find /home/u284669846 -name "wp" -type f 2>/dev/null | head -1', timeout=10)
wp_cli = out3.read().decode().strip()
if wp_cli:
    print(f"Running WP-CLI ({wp_cli}) cache flush...")
    _, out4, _ = ssh.exec_command(f'{wp_cli} litespeed-purge all --path={REMOTE_BASE} 2>&1', timeout=15)
    print(f"Litespeed Cache Purge: {out4.read().decode().strip()}")
    _, out5, _ = ssh.exec_command(f'{wp_cli} cache flush --path={REMOTE_BASE} 2>&1', timeout=15)
    print(f"Object Cache Flush: {out5.read().decode().strip()}")

ssh.close()
print("\nDone!")
