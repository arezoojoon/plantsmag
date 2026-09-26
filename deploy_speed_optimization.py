import paramiko, sys, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HOST = '187.124.245.99'
PORT = 65002
USER = 'u284669846'
PASS = '[3pPybi0[3pPybi0'

LOCAL_THEME = r'd:\project\plantsmag\plantsmag-premium'

print("Connecting to Hostinger...")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, port=PORT, username=USER, password=PASS, timeout=20)
print("SSH connected!")

# Fixed web root
REMOTE_BASE = '/home/u284669846/domains/plantsmag.com/public_html'
THEME_REMOTE = f'{REMOTE_BASE}/wp-content/themes/plantsmag-premium'

sftp = ssh.open_sftp()
FILES = [
    (rf'{LOCAL_THEME}\style.css', f'{THEME_REMOTE}/style.css'),
    (rf'{LOCAL_THEME}\header.php', f'{THEME_REMOTE}/header.php')
]
for local, remote in FILES:
    print(f"Uploading {local} to {remote}...")
    sftp.put(local, remote)
sftp.close()

# Use WP-CLI to configure LiteSpeed cache
_, out3, _ = ssh.exec_command(f'find /home/u284669846 -name "wp" -type f 2>/dev/null | head -1', timeout=10)
wp_cli = out3.read().decode().strip()

commands = [
    # Install Litespeed
    f'{wp_cli} plugin install litespeed-cache --activate --path={REMOTE_BASE}',
    
    # Enable cache features
    f'{wp_cli} lscache-admin set_option cache-priv true --path={REMOTE_BASE}',
    f'{wp_cli} lscache-admin set_option cache-rest true --path={REMOTE_BASE}',
    
    # CSS/JS Optimization
    f'{wp_cli} lscache-admin set_option optm-css_min true --path={REMOTE_BASE}',
    f'{wp_cli} lscache-admin set_option optm-css_comb true --path={REMOTE_BASE}',
    f'{wp_cli} lscache-admin set_option optm-js_min true --path={REMOTE_BASE}',
    f'{wp_cli} lscache-admin set_option optm-js_comb true --path={REMOTE_BASE}',
    f'{wp_cli} lscache-admin set_option optm-html_min true --path={REMOTE_BASE}',
    f'{wp_cli} lscache-admin set_option optm-qs_rm true --path={REMOTE_BASE}',
    f'{wp_cli} lscache-admin set_option optm-ggfonts_rm true --path={REMOTE_BASE}',
    f'{wp_cli} lscache-admin set_option optm-js_defer 2 --path={REMOTE_BASE}',
    
    # Media Optimization
    f'{wp_cli} lscache-admin set_option media-lazy true --path={REMOTE_BASE}',
    
    # Purge all
    f'{wp_cli} lscache-admin purge all --path={REMOTE_BASE}'
]

for cmd in commands:
    print(f"Running: {cmd}")
    _, out, err = ssh.exec_command(cmd)
    res = out.read().decode().strip()
    if res:
        print(res)
    error = err.read().decode().strip()
    if error:
        print(f"Error: {error}")

ssh.close()
print("Speed optimization deployed successfully!")
