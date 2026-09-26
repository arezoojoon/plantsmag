import paramiko
import sys

host = '72.62.93.117'
user = 'root'
passwd = "5KT4'ub5B5oD8V9TB#/u"

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, port=22, username=user, password=passwd, timeout=15)
print("Connected!")

def run(cmd):
    stdin, stdout, stderr = client.exec_command(cmd)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    sys.stdout.write(out + "\n")
    if err.strip():
        sys.stdout.write("ERR: " + err[:300] + "\n")

run("ls /var/www/")
run("pm2 list --no-color 2>&1 | cat")
run("node --version 2>&1")
run("docker --version 2>&1 || echo 'no docker'")
run("nginx -v 2>&1 || echo 'no nginx'")
run("free -m | cat")
run("df -h | grep -v tmpfs | cat")

client.close()
print("Done.")
