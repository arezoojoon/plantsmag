import paramiko
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.62.93.117', port=22, username='root', password="5KT4'ub5B5oD8V9TB#/u", timeout=15)

def run(cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=20)
    return stdout.read().decode('utf-8', errors='replace').strip()

print(run("pm2 stop n8n"))
print(run("pm2 stop plantsmag-seo"))
print(run("pm2 save"))

ssh.close()
