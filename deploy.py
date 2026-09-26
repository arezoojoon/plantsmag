import paramiko
import os
import zipfile
import sys
import time

HOSTS = ["72.62.93.117", "72.82.93.117"]
PORT = 22
USER = "root"
PASSWORD = "5KT4'ub5B5oD8V9TB#/u"

def create_zip(src_dir, zip_name):
    print(f"Creating {zip_name} from {src_dir}...")
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(src_dir):
            if 'node_modules' in dirs:
                dirs.remove('node_modules')
            if '.next' in dirs:
                dirs.remove('.next')
            if '.git' in dirs:
                dirs.remove('.git')
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=src_dir)
                zipf.write(file_path, arcname)
    print("Zip created successfully.")

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

def deploy():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        connected = False
        for host in HOSTS:
            print(f"Attempting to connect to {host}...")
            try:
                ssh.connect(host, port=PORT, username=USER, password=PASSWORD, timeout=10)
                connected = True
                print(f"Connected successfully to {host}!")
                break
            except Exception as e:
                print(f"Failed to connect to {host}: {e}")
        
        if not connected:
            print("Could not connect to any of the provided IP addresses.")
            return

        # Upload zip
        sftp = ssh.open_sftp()
        remote_zip = '/root/plantsmag-apps.zip'
        print("Uploading zip file...")
        sftp.put('plantsmag-apps.zip', remote_zip)
        sftp.close()
        print("Upload complete.")
        
        # Setup server
        commands = [
            "cd /var/www/plantsmag-apps && npm run build",
            "npm install -g pm2",
            "pm2 delete plantsmag-apps || true",
            "cd /var/www/plantsmag-apps && pm2 start npm --name 'plantsmag-apps' -- start",
            "pm2 save"
        ]
        
        for cmd in commands:
            run_ssh_command(ssh, cmd)
            
        ssh.close()
        print("Deployment successful!")
        
    except Exception as e:
        print(f"Deployment failed: {e}")

if __name__ == "__main__":
    create_zip(r'd:\project\plantsmag\plantsmag-nextjs-apps', 'plantsmag-apps.zip')
    deploy()
