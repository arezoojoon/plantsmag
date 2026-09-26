import paramiko, sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("=" * 60)
print("DEPLOY: Security Patches")
print("=" * 60)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.62.93.117', port=22, username='root', password=r"5KT4'ub5B5oD8V9TB#/u", timeout=20)

sftp = ssh.open_sftp()
files_to_upload = [
    ('d:\\project\\plantsmag\\lead-capture.php', '/root/plantsmag-premium/inc/lead-capture.php'), # Note: I'm putting the main lead-capture into the inc folder just in case
    ('d:\\project\\plantsmag\\fast_index.php', '/root/fast_index.php')
]

for local_path, remote_path in files_to_upload:
    try:
        with open(local_path, 'r', encoding='utf-8') as fh:
            content = fh.read()
        with sftp.open(remote_path, 'w') as fh:
            fh.write(content)
        print(f"  VPS: Uploaded {remote_path}")
    except Exception as e:
         print(f"  VPS: Failed to upload {remote_path}: {e}")

sftp.close()
ssh.close()
print("\nDone!")
