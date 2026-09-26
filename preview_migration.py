import paramiko

VPS_HOST = '72.62.93.117'
VPS_PASS = "5KT4'ub5B5oD8V9TB#/u"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(VPS_HOST, port=22, username='root', password=VPS_PASS, timeout=15)

script = """
cd /var/www/plantsmag-apps
echo "Current directory: $(pwd)"
echo "PATH: $PATH"
node -v
npx -v
export DATABASE_URL="postgresql://plantsmag_staging_user:staging_secure_pass_2026@localhost:5432/plantsmag_staging?schema=public"
export DIRECT_URL="postgresql://plantsmag_staging_user:staging_secure_pass_2026@localhost:5432/plantsmag_staging?schema=public"
echo "=== SQL PREVIEW ==="
npx prisma@6 migrate diff --from-empty --to-schema-datamodel prisma/schema.prisma --script
"""

stdin, stdout, stderr = ssh.exec_command(script)
output = stdout.read().decode('utf-8', errors='replace')
error = stderr.read().decode('utf-8', errors='replace')

print("=== SQL PREVIEW ===")
print(output)

if error:
    print("=== ERRORS ===")
    print(error)

ssh.close()
