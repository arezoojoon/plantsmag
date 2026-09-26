import paramiko, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('187.124.245.99', port=65002, username='u284669846', password='[3pPybi0[3pPybi0', timeout=20)

def run(cmd):
    _, o, _ = ssh.exec_command(cmd)
    return o.read().decode('utf-8', errors='replace')

wp = '/home/u284669846/domains/plantsmag.com/public_html'

# Debug: dump full title of post #1185 from database
php = (
    '<?php\n'
    'require_once("/home/u284669846/domains/plantsmag.com/public_html/wp-load.php");\n'
    'global $wpdb;\n'
    '$title = $wpdb->get_var("SELECT post_title FROM wp_posts WHERE ID = 1185");\n'
    'echo "LENGTH: " . strlen($title) . "\\n";\n'
    'echo "FULL:\\n";\n'
    'echo $title . "\\n";\n'
    'echo "\\nJSON_DECODE_TEST:\\n";\n'
    '$d = json_decode($title, true);\n'
    'echo "Result: " . ($d ? "SUCCESS" : "FAIL") . "\\n";\n'
    'echo "json_last_error: " . json_last_error_msg() . "\\n";\n'
    'echo "\\nHEX of first 50 bytes:\\n";\n'
    'echo bin2hex(substr($title, 0, 50)) . "\\n";\n'
    '?>\n'
)

sftp = ssh.open_sftp()
with sftp.open(wp + '/debug_title.php', 'w') as f:
    f.write(php)
sftp.close()

out = run('cd ' + wp + ' && php debug_title.php 2>&1')
print(out)
run('rm ' + wp + '/debug_title.php')
ssh.close()
