import paramiko, sys, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HOST = '187.124.245.99'
PORT = 65002
USER = 'u284669846'
PASS = '[3pPybi0[3pPybi0'
REMOTE_BASE = '/home/u284669846/domains/plantsmag.com/public_html'
LOCAL_PURGE = r'd:\project\plantsmag\purge_cache.php'
REMOTE_PURGE = f'{REMOTE_BASE}/purge_cache.php'

print("Uploading purge script...")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, port=PORT, username=USER, password=PASS, timeout=20)
sftp = ssh.open_sftp()
sftp.put(LOCAL_PURGE, REMOTE_PURGE)
sftp.close()

import requests
print("Executing purge via HTTP...")
r = requests.get('https://plantsmag.com/purge_cache.php')
print(r.text)

print("Deleting purge script...")
ssh.exec_command(f'rm {REMOTE_PURGE}')
ssh.close()
print("Done!")
