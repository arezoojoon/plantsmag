import paramiko
import os
import sys

VPS_HOST = '72.62.93.117'
VPS_PASS = "5KT4'ub5B5oD8V9TB#/u"
LOCAL_NEXTJS = r'd:\project\plantsmag\plantsmag-nextjs-apps'
REMOTE_APP = '/var/www/plantsmag-apps'

print("Connecting to VPS...")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(VPS_HOST, port=22, username='root', password=VPS_PASS, timeout=15)
sftp = ssh.open_sftp()

def ensure_remote_dir(path):
    try:
        sftp.stat(path)
    except FileNotFoundError:
        ssh.exec_command(f'mkdir -p "{path}"')

def upload_file(local_path, remote_path):
    try:
        ensure_remote_dir(os.path.dirname(remote_path))
        sftp.put(local_path, remote_path)
        print(f"Uploaded: {remote_path}")
    except Exception as e:
        print(f"Failed to upload {remote_path}: {e}")

print("Uploading Phase 1 files to VPS...")

files_to_upload = [
    ('prisma/schema.prisma', 'prisma/schema.prisma'),
    ('worker.js', 'worker.js'),
    ('.env.local.example', '.env.local.example'),
    ('src/app/api/stripe/checkout/route.ts', 'src/app/api/stripe/checkout/route.ts'),
    ('src/app/api/stripe/webhook/route.ts', 'src/app/api/stripe/webhook/route.ts'),
    ('src/app/rescue-plan/[token]/page.tsx', 'src/app/rescue-plan/[token]/page.tsx'),
    ('package.json', 'package.json')
]

for local_rel, remote_rel in files_to_upload:
    local_path = os.path.join(LOCAL_NEXTJS, local_rel)
    remote_path = f"{REMOTE_APP}/{remote_rel}"
    if os.path.exists(local_path):
        upload_file(local_path, remote_path)
    else:
        print(f"Warning: Local file not found: {local_path}")

print("Running npm install on VPS (this might take a minute)...")
stdin, stdout, stderr = ssh.exec_command(f'cd {REMOTE_APP} && npm install @prisma/client pg-boss stripe --save && npm install prisma --save-dev')
exit_status = stdout.channel.recv_exit_status()
print(stdout.read().decode())
if exit_status == 0:
    print("Packages installed successfully on VPS.")
else:
    print("Error installing packages:")
    print(stderr.read().decode())

print("Generating Prisma client on VPS...")
stdin, stdout, stderr = ssh.exec_command(f'cd {REMOTE_APP} && npx prisma generate')
exit_status = stdout.channel.recv_exit_status()
print(stdout.read().decode())

sftp.close()
ssh.close()
print("Done!")
