import paramiko, sys, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Hostinger SFTP credentials
HOSTINGER_HOST = 'srv1156.hstgr.io'
HOSTINGER_USER = 'u925720261'
HOSTINGER_PASS = 'Artinmag@1402'
REMOTE_BASE    = '/home/u925720261/domains/plantsmag.com/public_html'
THEME_REMOTE   = f'{REMOTE_BASE}/wp-content/themes/plantsmag-premium'

LOCAL_BASE = r'd:\project\plantsmag'
LOCAL_THEME = rf'{LOCAL_BASE}\plantsmag-premium'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOSTINGER_HOST, port=65002, username=HOSTINGER_USER, password=HOSTINGER_PASS, timeout=30)
sftp = ssh.open_sftp()

def upload(local_path, remote_path):
    try:
        sftp.put(local_path, remote_path)
        print(f'  ✅ {os.path.basename(local_path)}')
        return True
    except Exception as e:
        print(f'  ❌ {os.path.basename(local_path)}: {e}')
        return False

print('=' * 55)
print('Deploying Phase 2 — Lead Magnet to Hostinger')
print('=' * 55)

# 1. CSS
print('\n📦 CSS:')
upload(rf'{LOCAL_THEME}\assets\css\lead-magnet.css',
       f'{THEME_REMOTE}/assets/css/lead-magnet.css')

# 2. JS
print('\n📦 JavaScript:')
upload(rf'{LOCAL_THEME}\assets\js\disease-finder.js',
       f'{THEME_REMOTE}/assets/js/disease-finder.js')
upload(rf'{LOCAL_THEME}\assets\js\watering-calculator.js',
       f'{THEME_REMOTE}/assets/js/watering-calculator.js')

# 3. PHP classes
print('\n📦 PHP Templates:')
upload(rf'{LOCAL_THEME}\inc\class-disease-finder.php',
       f'{THEME_REMOTE}/inc/class-disease-finder.php')
upload(rf'{LOCAL_THEME}\inc\class-watering-calculator.php',
       f'{THEME_REMOTE}/inc/class-watering-calculator.php')

# 4. Functions.php
print('\n📦 Functions:')
upload(rf'{LOCAL_THEME}\functions.php',
       f'{THEME_REMOTE}/functions.php')

# 5. Lead capture endpoint (in public_html root AND theme/inc)
print('\n📦 Lead Capture API:')
upload(rf'{LOCAL_BASE}\lead-capture.php',
       f'{REMOTE_BASE}/lead-capture.php')
upload(rf'{LOCAL_THEME}\inc\lead-capture.php',
       f'{THEME_REMOTE}/inc/lead-capture.php')

# 6. Verify remote files exist
print('\n🔍 Verifying remote files...')
files_to_check = [
    f'{THEME_REMOTE}/assets/css/lead-magnet.css',
    f'{THEME_REMOTE}/assets/js/disease-finder.js',
    f'{THEME_REMOTE}/assets/js/watering-calculator.js',
    f'{THEME_REMOTE}/inc/class-disease-finder.php',
    f'{THEME_REMOTE}/inc/class-watering-calculator.php',
    f'{REMOTE_BASE}/lead-capture.php',
]
for f in files_to_check:
    try:
        stat = sftp.stat(f)
        size = stat.st_size
        print(f'  ✅ {f.split("/")[-1]} ({size:,} bytes)')
    except:
        print(f'  ❌ MISSING: {f}')

sftp.close()
ssh.close()
print('\n' + '=' * 55)
print('Deployment complete!')
print('=' * 55)
