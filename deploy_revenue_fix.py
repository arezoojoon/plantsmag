"""
PlantsMag Revenue Fix — Deploy Script
======================================
Deploys:
  1. WordPress theme files (functions.php, footer.php, front-page.php)
  2. Next.js .next/static output (disease-finder + watering-calculator)

Run: python deploy_revenue_fix.py
"""

import paramiko
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HOST = '187.124.245.99'
PORT = 65002
USER = 'u284669846'
PASS = '[3pPybi0[3pPybi0'

LOCAL_THEME     = r'd:\project\plantsmag\plantsmag-premium'
LOCAL_NEXTJS    = r'd:\project\plantsmag\plantsmag-nextjs-apps'
LOCAL_BASE      = r'd:\project\plantsmag'

print("=" * 65)
print("  PlantsMag Revenue Fix — Deploy")
print("=" * 65)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, port=PORT, username=USER, password=PASS, timeout=20)
print("✅ SSH connected")

# Detect web root
_, out, _ = ssh.exec_command('find /home/u284669846 -name "wp-config.php" 2>/dev/null | head -1', timeout=15)
wp_config = out.read().decode().strip()
REMOTE_BASE  = os.path.dirname(wp_config) if wp_config else '/home/u284669846/htdocs/plantsmag.com'
THEME_REMOTE = f'{REMOTE_BASE}/wp-content/themes/plantsmag-premium'

# Detect Next.js app location on server
_, out2, _ = ssh.exec_command('find /home/u284669846 -name "disease-finder" -type d 2>/dev/null | head -3', timeout=15)
nextjs_dirs = out2.read().decode().strip()
print(f"Next.js dirs on server: {nextjs_dirs[:200] if nextjs_dirs else 'not found'}")

# Try to find the Next.js app root
_, out3, _ = ssh.exec_command('find /home/u284669846 -name "package.json" -not -path "*/node_modules/*" 2>/dev/null | head -5', timeout=15)
pkg_dirs = out3.read().decode().strip()
print(f"package.json locations: {pkg_dirs[:200]}")

sftp = ssh.open_sftp()

# ── 1. WordPress Theme Files ──────────────────────────────────
THEME_FILES = [
    (rf'{LOCAL_THEME}\functions.php',   f'{THEME_REMOTE}/functions.php'),
    (rf'{LOCAL_THEME}\footer.php',      f'{THEME_REMOTE}/footer.php'),
    (rf'{LOCAL_THEME}\front-page.php',  f'{THEME_REMOTE}/front-page.php'),
]

print("\n📦 Uploading WordPress theme files...")
ok = 0
for local, remote in THEME_FILES:
    try:
        sftp.put(local, remote)
        size = os.path.getsize(local)
        print(f"  ✅ {os.path.basename(local)} ({size:,} bytes)")
        ok += 1
    except Exception as e:
        print(f"  ❌ {os.path.basename(local)}: {e}")

print(f"  → {ok}/{len(THEME_FILES)} theme files uploaded")

# ── 2. Next.js Static Files ──────────────────────────────────
# The Next.js app's .next/static dir contains the compiled JS/CSS
# We also need to replace the page JS files for disease-finder and watering-calculator
nextjs_static_local = os.path.join(LOCAL_NEXTJS, '.next', 'static')

if os.path.isdir(nextjs_static_local):
    print("\n📦 Uploading Next.js static assets...")
    
    # Find the server-side Next.js directory
    # First try the common Hostinger path pattern
    possible_paths = [
        '/home/u284669846/htdocs/plantsmag.com/tools',
        '/home/u284669846/htdocs/plantsmag.com/nextjs',
        '/home/u284669846/nextjs-app',
        '/home/u284669846/plantsmag-tools',
    ]
    
    # Ask server where the Next.js app is running
    _, out4, _ = ssh.exec_command('pm2 list 2>/dev/null || echo "pm2 not found"', timeout=10)
    pm2_list = out4.read().decode().strip()
    print(f"  PM2 processes: {pm2_list[:300]}")
    
    _, out5, _ = ssh.exec_command('cat /home/u284669846/.pm2/logs/plantsmag-tools-out.log 2>/dev/null | tail -5 || echo "no pm2 log"', timeout=10)
    pm2_log = out5.read().decode().strip()
    
    # Find actual app directory via pm2 or process list
    _, out6, _ = ssh.exec_command('cat /etc/nginx/conf.d/*.conf 2>/dev/null | grep -E "proxy_pass|root" | grep -v "#" | head -20 || echo "no nginx conf found"', timeout=10)
    nginx_conf = out6.read().decode().strip()
    print(f"  Nginx config excerpt: {nginx_conf[:400]}")
    
    # Upload .next/static (CSS + JS chunks) to all likely locations
    def upload_dir(local_dir, remote_dir, label=""):
        uploaded = 0
        errors = 0
        for root, dirs, files in os.walk(local_dir):
            # Skip node_modules and cache
            dirs[:] = [d for d in dirs if d not in ('node_modules', 'cache', 'trace')]
            rel = os.path.relpath(root, local_dir)
            remote_root = f"{remote_dir}/{rel}".replace('\\', '/').replace('/.', '')
            
            # Ensure remote dir exists
            try:
                sftp.stat(remote_root)
            except FileNotFoundError:
                try:
                    # Create directory recursively via SSH
                    ssh.exec_command(f'mkdir -p "{remote_root}"')
                except Exception:
                    pass
            
            for fname in files:
                local_file = os.path.join(root, fname)
                remote_file = f"{remote_root}/{fname}"
                try:
                    sftp.put(local_file, remote_file)
                    uploaded += 1
                except Exception as e:
                    errors += 1
        print(f"  {label}: {uploaded} files uploaded, {errors} errors")
        return uploaded
    
    # Try uploading to found Next.js locations
    _, out7, _ = ssh.exec_command(
        'find /home/u284669846 -name ".next" -type d 2>/dev/null | head -3',
        timeout=15
    )
    nextjs_remote_dirs = [d.strip() for d in out7.read().decode().strip().split('\n') if d.strip()]
    
    if nextjs_remote_dirs:
        for nextjs_remote in nextjs_remote_dirs:
            print(f"  Found .next at: {nextjs_remote}")
            upload_dir(
                os.path.join(LOCAL_NEXTJS, '.next'),
                nextjs_remote,
                label=f"→ {nextjs_remote}"
            )
    else:
        print("  ⚠️  Could not find .next directory on server — Next.js app may need manual restart")
        print("  Local .next is ready at: d:\\project\\plantsmag\\plantsmag-nextjs-apps\\.next")
else:
    print("  ⚠️  .next directory not found locally — build may not have completed")

# ── 3. Flush WordPress cache ──────────────────────────────────
print("\n🔄 Flushing WordPress cache...")
_, out8, _ = ssh.exec_command(
    f'find /home/u284669846 -name "wp" -executable -type f 2>/dev/null | head -1',
    timeout=10
)
wp_cli = out8.read().decode().strip()

if wp_cli:
    _, out9, _ = ssh.exec_command(
        f'{wp_cli} cache flush --path="{REMOTE_BASE}" 2>&1 && '
        f'{wp_cli} transient delete --all --path="{REMOTE_BASE}" 2>&1',
        timeout=20
    )
    print(f"  {out9.read().decode().strip()[:120]}")
else:
    # Try opcache reset via curl
    _, out10, _ = ssh.exec_command(
        f'curl -s https://plantsmag.com/flush_opcache.php 2>/dev/null | head -1 || echo "no flush script"',
        timeout=15
    )
    print(f"  Opcache flush: {out10.read().decode().strip()}")

sftp.close()
ssh.close()
print("\n✅ Deploy complete!")
print("\n⚠️  MANUAL STEP REQUIRED:")
print("   Go to: https://plantsmag.com/wp-admin/options-general.php")
print("   Change 'Site Title' to: PlantsMag")
print("   Change 'Tagline' to: Expert Plant Care, AI Disease Diagnosis & Watering Tools")
