import paramiko, sys, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HOST = '187.124.245.99'
PORT = 65002
USER = 'u284669846'
PASS = '[3pPybi0[3pPybi0'

print("Connecting to Hostinger...")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, port=PORT, username=USER, password=PASS, timeout=20)
print("SSH connected!")

REMOTE_BASE = '/home/u284669846/domains/plantsmag.com/public_html'
wp = "wp"

commands = [
    # Install Litespeed
    f'{wp} plugin install litespeed-cache --activate --path={REMOTE_BASE}',
    
    # Enable cache features
    f'{wp} litespeed-option set cache-priv true --path={REMOTE_BASE}',
    f'{wp} litespeed-option set cache-rest true --path={REMOTE_BASE}',
    
    # CSS/JS Optimization
    f'{wp} litespeed-option set optm-css_min true --path={REMOTE_BASE}',
    f'{wp} litespeed-option set optm-css_comb true --path={REMOTE_BASE}',
    f'{wp} litespeed-option set optm-js_min true --path={REMOTE_BASE}',
    f'{wp} litespeed-option set optm-js_comb true --path={REMOTE_BASE}',
    f'{wp} litespeed-option set optm-html_min true --path={REMOTE_BASE}',
    f'{wp} litespeed-option set optm-qs_rm true --path={REMOTE_BASE}',
    f'{wp} litespeed-option set optm-ggfonts_rm true --path={REMOTE_BASE}',
    f'{wp} litespeed-option set optm-js_defer 2 --path={REMOTE_BASE}',
    
    # Media Optimization
    f'{wp} litespeed-option set media-lazy true --path={REMOTE_BASE}',
    
    # Purge all
    f'{wp} litespeed-purge all --path={REMOTE_BASE}'
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
