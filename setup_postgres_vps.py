import paramiko
import time

VPS_HOST = '72.62.93.117'
VPS_PASS = "5KT4'ub5B5oD8V9TB#/u"

print("Connecting to VPS to provision PostgreSQL...")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    ssh.connect(VPS_HOST, port=22, username='root', password=VPS_PASS, timeout=15)
    
    commands = [
        "apt-get update",
        "DEBIAN_FRONTEND=noninteractive apt-get install -y postgresql postgresql-contrib",
        "systemctl enable postgresql",
        "systemctl start postgresql",
        # Create Prod DB and User
        "sudo -u postgres psql -c \"CREATE USER plantsmag_prod_user WITH PASSWORD 'prod_secure_pass_2026';\"",
        "sudo -u postgres psql -c \"CREATE DATABASE plantsmag_prod OWNER plantsmag_prod_user;\"",
        # Create Staging DB and User
        "sudo -u postgres psql -c \"CREATE USER plantsmag_staging_user WITH PASSWORD 'staging_secure_pass_2026';\"",
        "sudo -u postgres psql -c \"CREATE DATABASE plantsmag_staging OWNER plantsmag_staging_user;\"",
        # Grant privileges
        "sudo -u postgres psql -c \"GRANT ALL PRIVILEGES ON DATABASE plantsmag_prod TO plantsmag_prod_user;\"",
        "sudo -u postgres psql -c \"GRANT ALL PRIVILEGES ON DATABASE plantsmag_staging TO plantsmag_staging_user;\"",
        # Check databases
        "sudo -u postgres psql -c \"\\l\""
    ]
    
    for cmd in commands:
        print(f"Executing: {cmd}")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        exit_status = stdout.channel.recv_exit_status()
        print(stdout.read().decode('utf-8', errors='replace'))
        err = stderr.read().decode('utf-8', errors='replace')
        if err:
            print(f"Error/Warning: {err}")
            
    # Set up .env.staging on the VPS
    env_content = """# App
NEXT_PUBLIC_APP_URL=http://72.62.93.117:3001

# PostgreSQL Staging
DATABASE_URL=postgresql://plantsmag_staging_user:staging_secure_pass_2026@localhost:5432/plantsmag_staging?schema=public
DIRECT_URL=postgresql://plantsmag_staging_user:staging_secure_pass_2026@localhost:5432/plantsmag_staging?schema=public
PG_BOSS_DATABASE_URL=postgresql://plantsmag_staging_user:staging_secure_pass_2026@localhost:5432/plantsmag_staging?schema=public

# Stripe (Test)
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_test_...
"""
    print("Writing .env.staging to /var/www/plantsmag-apps/.env.staging ...")
    write_cmd = f"cat << 'EOF' > /var/www/plantsmag-apps/.env.staging\n{env_content}\nEOF"
    ssh.exec_command(write_cmd)
    
finally:
    ssh.close()
    print("Disconnected.")
