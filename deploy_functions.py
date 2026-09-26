import paramiko
import sys
import os

HOST = '187.124.245.99'
PORT = 65002
USER = 'u284669846'
PASS = '[3pPybi0[3pPybi0'

LOCAL_FILE = r'd:\project\plantsmag\plantsmag-premium\functions.php'
REMOTE_FILE = '/home/u284669846/domains/plantsmag.com/public_html/wp-content/themes/plantsmag-premium/functions.php'

print("Connecting to Hostinger...")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, port=PORT, username=USER, password=PASS, timeout=20)
print("SSH connected!")

sftp = ssh.open_sftp()
sftp.put(LOCAL_FILE, REMOTE_FILE)
sftp.close()
print("functions.php uploaded.")
ssh.close()
