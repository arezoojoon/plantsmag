import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('187.124.245.99', port=65002, username='u284669846', password='[3pPybi0[3pPybi0', timeout=20)

def run(cmd):
    _, o, e = ssh.exec_command(cmd)
    return o.read().decode('utf-8').strip(), e.read().decode('utf-8').strip()

wp_dir = '/home/u284669846/domains/plantsmag.com/public_html'

# Delete old app password
print("Deleting old application password...")
out, err = run(f'cd {wp_dir} && wp user application-password delete n8n-bloger 1d780ea5-38bc-4195-a2b4-e726a5c316cb')
print(f"  {out} {err}")

# Create new application password
print("\nCreating new application password...")
out, err = run(f'cd {wp_dir} && wp user application-password create n8n-bloger n8n-publish-2026 --porcelain')
print(f"  New password: {out}")
if err:
    print(f"  Error: {err}")

ssh.close()
