import paramiko
import time

HOST = "72.62.93.117"
PORT = 22
USER = "root"
PASSWORD = "5KT4'ub5B5oD8V9TB#/u"
DOMAIN = "app.72.62.93.117.nip.io"

def run_ssh_command(ssh, cmd):
    print(f"Running: {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    
    while True:
        line = stdout.readline()
        if not line:
            break
        print(line.strip().encode('ascii', 'ignore').decode('ascii'), flush=True)
        
    err = stderr.read().decode('utf-8')
    if err:
        print(f"STDERR: {err}")
    exit_status = stdout.channel.recv_exit_status()
    print(f"Exit status: {exit_status}\n")
    return exit_status

def setup_ssl():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(f"Connecting to {HOST}...")
        ssh.connect(HOST, port=PORT, username=USER, password=PASSWORD, timeout=10)
        print("Connected!")

        nginx_conf = f"""
server {{
    listen 80;
    server_name {DOMAIN};

    location / {{
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \\$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \\$host;
        proxy_cache_bypass \\$http_upgrade;
    }}
}}
"""
        commands = [
            "apt-get update",
            "apt-get install -y nginx certbot python3-certbot-nginx",
            f"echo \"{nginx_conf}\" > /etc/nginx/sites-available/{DOMAIN}",
            f"ln -sf /etc/nginx/sites-available/{DOMAIN} /etc/nginx/sites-enabled/",
            "nginx -t",
            "systemctl reload nginx",
            f"certbot --nginx -d {DOMAIN} --non-interactive --agree-tos -m admin@plantsmag.com --redirect"
        ]

        for cmd in commands:
            run_ssh_command(ssh, cmd)

        ssh.close()
        print("SSL Setup Complete!")

    except Exception as e:
        print(f"Setup failed: {e}")

if __name__ == "__main__":
    setup_ssl()
