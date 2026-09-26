import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
HOST='187.124.245.99'; PORT=65002; USER='u284669846'; PASS='[3pPybi0[3pPybi0'
ssh=paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST,port=PORT,username=USER,password=PASS,timeout=20)

cmds=[
    'find /home/u284669846 -name "next.config.ts" -not -path "*/node_modules/*" 2>/dev/null | head -5',
    'ls /home/u284669846/domains/plantsmag.com/',
    'ls /home/u284669846/domains/plantsmag.com/public_html/',
    'find /home/u284669846/domains/plantsmag.com -name ".next" -type d 2>/dev/null | head -5',
]
for cmd in cmds:
    _, out, _ = ssh.exec_command(cmd, timeout=15)
    r = out.read().decode().strip()
    print(f'\n[CMD] {cmd[:70]}')
    print(f'  {r[:300] if r else "(empty)"}')

ssh.close()
