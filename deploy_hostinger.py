import paramiko, sys, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HOST = '187.124.245.99'
PORT = 65002
USER = 'u284669846'
PASS = '[3pPybi0[3pPybi0'

VPS_HOST = '72.62.93.117'
VPS_PASS = "5KT4'ub5B5oD8V9TB#/u"

LOCAL_THEME = r'd:\project\plantsmag\plantsmag-premium'
LOCAL_BASE  = r'd:\project\plantsmag'

REMOTE_BASE  = '/home/u284669846/htdocs/plantsmag.com'
THEME_REMOTE = f'{REMOTE_BASE}/wp-content/themes/plantsmag-premium'

print("=" * 65)
print("Connecting to Hostinger...")
print("=" * 65)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, port=PORT, username=USER, password=PASS, timeout=20)
print("SSH connected!")

_, out, _ = ssh.exec_command('whoami && pwd && ls /home/u284669846/', timeout=10)
print(out.read().decode('utf-8', errors='replace'))

# Find correct web root
_, out2, _ = ssh.exec_command('find /home/u284669846 -name "wp-config.php" 2>/dev/null | head -3', timeout=15)
wp_config = out2.read().decode().strip()
print(f"\nwp-config.php: {wp_config}")

# Determine actual web root
if wp_config:
    REMOTE_BASE = os.path.dirname(wp_config)
    THEME_REMOTE = f'{REMOTE_BASE}/wp-content/themes/plantsmag-premium'
    print(f"Web root: {REMOTE_BASE}")

sftp = ssh.open_sftp()

FILES = [
    # (local, remote)
    (rf'{LOCAL_THEME}\assets\css\lead-magnet.css',         f'{THEME_REMOTE}/assets/css/lead-magnet.css'),
    (rf'{LOCAL_THEME}\assets\js\disease-finder.js',        f'{THEME_REMOTE}/assets/js/disease-finder.js'),
    (rf'{LOCAL_THEME}\assets\js\watering-calculator.js',   f'{THEME_REMOTE}/assets/js/watering-calculator.js'),
    (rf'{LOCAL_THEME}\inc\class-disease-finder.php',       f'{THEME_REMOTE}/inc/class-disease-finder.php'),
    (rf'{LOCAL_THEME}\inc\class-watering-calculator.php',  f'{THEME_REMOTE}/inc/class-watering-calculator.php'),
    (rf'{LOCAL_THEME}\inc\lead-capture.php',               f'{THEME_REMOTE}/inc/lead-capture.php'),
    (rf'{LOCAL_THEME}\functions.php',                      f'{THEME_REMOTE}/functions.php'),
]

print("\n📦 Uploading Phase 2 files...")
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

# Flush OPcache / clear theme cache
_, out3, _ = ssh.exec_command(f'find /home/u284669846 -name "wp" -type f 2>/dev/null | head -1', timeout=10)
wp_cli = out3.read().decode().strip()
if wp_cli:
    _, out4, _ = ssh.exec_command(f'{wp_cli} cache flush --path={REMOTE_BASE} 2>&1', timeout=15)
    print(f"WP cache flush: {out4.read().decode().strip()[:80]}")

ssh.close()
print("\nDone!")
