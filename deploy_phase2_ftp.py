import ftplib, sys, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Hostinger FTP credentials
FTP_HOST = 'plantsmag.com'
FTP_USER = 'u925720261'
FTP_PASS = 'Artinmag@1402'
REMOTE_BASE  = '/public_html'
THEME_REMOTE = '/public_html/wp-content/themes/plantsmag-premium'

LOCAL_BASE  = r'd:\project\plantsmag'
LOCAL_THEME = rf'{LOCAL_BASE}\plantsmag-premium'

def upload_ftp(ftp, local_path, remote_path):
    try:
        with open(local_path, 'rb') as f:
            ftp.storbinary(f'STOR {remote_path}', f)
        size = os.path.getsize(local_path)
        print(f'  ✅ {os.path.basename(local_path)} ({size:,} bytes)')
        return True
    except Exception as e:
        print(f'  ❌ {os.path.basename(local_path)}: {e}')
        return False

print('=' * 55)
print('Deploying Phase 2 via FTP to Hostinger')
print('=' * 55)

ftp = ftplib.FTP(FTP_HOST, timeout=30)
ftp.login(FTP_USER, FTP_PASS)
ftp.set_pasv(True)
print(f'Connected: {ftp.getwelcome()[:50]}')

# 1. CSS
print('\n📦 CSS:')
upload_ftp(ftp, rf'{LOCAL_THEME}\assets\css\lead-magnet.css',
           f'{THEME_REMOTE}/assets/css/lead-magnet.css')

# 2. JavaScript
print('\n📦 JavaScript:')
upload_ftp(ftp, rf'{LOCAL_THEME}\assets\js\disease-finder.js',
           f'{THEME_REMOTE}/assets/js/disease-finder.js')
upload_ftp(ftp, rf'{LOCAL_THEME}\assets\js\watering-calculator.js',
           f'{THEME_REMOTE}/assets/js/watering-calculator.js')

# 3. PHP Templates
print('\n📦 PHP Templates:')
upload_ftp(ftp, rf'{LOCAL_THEME}\inc\class-disease-finder.php',
           f'{THEME_REMOTE}/inc/class-disease-finder.php')
upload_ftp(ftp, rf'{LOCAL_THEME}\inc\class-watering-calculator.php',
           f'{THEME_REMOTE}/inc/class-watering-calculator.php')

# 4. Functions.php
print('\n📦 Theme Functions:')
upload_ftp(ftp, rf'{LOCAL_THEME}\functions.php',
           f'{THEME_REMOTE}/functions.php')

# 5. Lead Capture API
print('\n📦 Lead Capture REST API:')
upload_ftp(ftp, rf'{LOCAL_BASE}\lead-capture.php',
           f'{REMOTE_BASE}/lead-capture.php')

ftp.quit()
print('\n' + '=' * 55)
print('Deployment complete!')
print('=' * 55)
