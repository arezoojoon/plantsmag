"""
Deploy Next.js build to VPS /var/www/plantsmag-apps
"""
import paramiko, os, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

VPS_HOST = '72.62.93.117'
VPS_PASS = "5KT4'ub5B5oD8V9TB#/u"
LOCAL_NEXTJS = r'd:\project\plantsmag\plantsmag-nextjs-apps'
REMOTE_APP   = '/var/www/plantsmag-apps'

print("Connecting to VPS...")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(VPS_HOST, port=22, username='root', password=VPS_PASS, timeout=15)
print("Connected.")

# Check what's in the app dir
_, out, _ = ssh.exec_command(f'ls {REMOTE_APP}/', timeout=8)
out.channel.settimeout(8)
print(f"Remote app dir contents:\n  {out.read().decode().strip()}")

# Check if .next exists there
_, out2, _ = ssh.exec_command(f'ls {REMOTE_APP}/.next/ 2>/dev/null | head -10 || echo NO_NEXT_DIR', timeout=8)
out2.channel.settimeout(8)
print(f"\n.next dir:\n  {out2.read().decode().strip()}")

# Get pm2 app name
_, out3, _ = ssh.exec_command('pm2 jlist 2>/dev/null | python3 -c "import sys,json; apps=json.load(sys.stdin); [print(a[\'name\'],a[\'pm2_env\'][\'pm_cwd\']) for a in apps]" 2>/dev/null || pm2 list', timeout=10)
out3.channel.settimeout(10)
print(f"\nPM2 apps:\n  {out3.read().decode().strip()[:400]}")

sftp = ssh.open_sftp()

def ensure_remote_dir(sftp, ssh, path):
    """Create remote directory if it doesn't exist."""
    try:
        sftp.stat(path)
    except FileNotFoundError:
        _, _, _ = ssh.exec_command(f'mkdir -p "{path}"', timeout=5)
        import time; time.sleep(0.2)

def upload_dir(local_dir, remote_dir, skip_dirs=None):
    """Recursively upload a local directory to remote."""
    if skip_dirs is None:
        skip_dirs = {'node_modules', 'cache', 'trace', '__pycache__'}
    uploaded = 0
    errors = 0
    for root, dirs, files in os.walk(local_dir):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        rel = os.path.relpath(root, local_dir).replace('\\', '/')
        if rel == '.':
            remote_root = remote_dir
        else:
            remote_root = f"{remote_dir}/{rel}"
        ensure_remote_dir(sftp, ssh, remote_root)
        for fname in files:
            local_file = os.path.join(root, fname)
            remote_file = f"{remote_root}/{fname}"
            try:
                sftp.put(local_file, remote_file)
                uploaded += 1
                if uploaded % 50 == 0:
                    print(f"  ... {uploaded} files uploaded")
            except Exception as e:
                errors += 1
                if errors <= 5:
                    print(f"  ERR: {fname}: {e}")
    return uploaded, errors

# Upload key Next.js directories
print("\n📦 Uploading Next.js source files and public assets...")

local_src = os.path.join(LOCAL_NEXTJS, 'src')
remote_src = f'{REMOTE_APP}/src'
if os.path.isdir(local_src):
    n, e = upload_dir(local_src, remote_src)
    print(f"  ✅ src: {n} files uploaded, {e} errors")

local_public = os.path.join(LOCAL_NEXTJS, 'public')
remote_public = f'{REMOTE_APP}/public'
if os.path.isdir(local_public):
    n, e = upload_dir(local_public, remote_public)
    print(f"  ✅ public: {n} files uploaded, {e} errors")

# Upload config files
config_files = [
    (rf'{LOCAL_NEXTJS}\next.config.ts', f'{REMOTE_APP}/next.config.ts'),
    (rf'{LOCAL_NEXTJS}\package.json', f'{REMOTE_APP}/package.json'),
    (rf'{LOCAL_NEXTJS}\postcss.config.mjs', f'{REMOTE_APP}/postcss.config.mjs'),
    (rf'{LOCAL_NEXTJS}\eslint.config.mjs', f'{REMOTE_APP}/eslint.config.mjs'),
]
for local, remote in config_files:
    if os.path.isfile(local):
        try:
            sftp.put(local, remote)
            print(f"  ✅ {os.path.basename(local)}")
        except Exception as e:
            print(f"  ❌ {os.path.basename(local)}: {e}")

print("\n📦 Uploading compiled .next build output...")
local_next = os.path.join(LOCAL_NEXTJS, '.next')
remote_next = f'{REMOTE_APP}/.next'

if os.path.isdir(local_next):
    n, e = upload_dir(local_next, remote_next)
    print(f"  ✅ .next: {n} files uploaded, {e} errors")
else:
    print("  ⚠️ .next not found locally")

sftp.close()

# Restart the PM2 process
print("\n🔄 Restarting PM2 app...")
_, out4, _ = ssh.exec_command('pm2 restart all 2>&1 || pm2 list', timeout=15)
out4.channel.settimeout(15)
print(f"  {out4.read().decode().strip()[:300]}")

ssh.close()
print("\n✅ VPS deploy complete!")
