import paramiko, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.62.93.117', port=22, username='root', password=r"5KT4'ub5B5oD8V9TB#/u", timeout=20)

print("--- PM2 STATUS ---")
_, o, _ = ssh.exec_command('pm2 status')
print(o.read().decode('utf-8', errors='replace'))

print("--- PM2 LOGS ---")
_, o, _ = ssh.exec_command('pm2 logs plantsmag-seo --lines 50 --nostream')
print(o.read().decode('utf-8', errors='replace'))

ssh.close()
