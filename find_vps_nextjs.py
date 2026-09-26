import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

VPS_HOST = '72.62.93.117'
VPS_PASS = "5KT4'ub5B5oD8V9TB#/u"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(VPS_HOST, port=22, username='root', password=VPS_PASS, timeout=15)
print("VPS connected")

# Short-timeout targeted commands only
cmds = [
    'ls /root/',
    'ls /var/www/',
    'ls /opt/',
    'pm2 list',
    'ls /root/plantsmag-nextjs-apps/ 2>/dev/null || echo not_there',
    'ls /root/plantsmag/ 2>/dev/null || echo not_there',
    'ls /var/www/plantsmag/ 2>/dev/null || echo not_there',
]
for cmd in cmds:
    try:
        _, out, _ = ssh.exec_command(cmd, timeout=8)
        out.channel.settimeout(8)
        r = out.read().decode('utf-8', errors='replace').strip()
        if r and r != 'not_there':
            print(f'\n[{cmd}]\n  {r[:300]}')
    except Exception as e:
        print(f'  TIMEOUT/ERR: {cmd[:40]} — {e}')

ssh.close()
print("\nDone.")
