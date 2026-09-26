import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('187.124.245.99', port=65002, username='u284669846', password='[3pPybi0[3pPybi0', timeout=20)

sftp = ssh.open_sftp()
sftp.put(r'd:\project\plantsmag\plantsmag-premium\functions.php', '/home/u284669846/domains/plantsmag.com/public_html/wp-content/themes/plantsmag-premium/functions.php')
sftp.close()

_, stdout, _ = ssh.exec_command('php -r "opcache_reset();"')
print("OPcache cleared:", stdout.read().decode())

ssh.close()
