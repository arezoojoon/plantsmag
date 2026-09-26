import paramiko, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('187.124.245.99', port=65002, username='u284669846', password='[3pPybi0[3pPybi0', timeout=20)

def run(cmd):
    _, o, _ = ssh.exec_command(cmd)
    return o.read().decode('utf-8', errors='replace')

wp = '/home/u284669846/domains/plantsmag.com/public_html'

# The title is TRUNCATED JSON like: { "title": "Neem Oil for Houseplants: The Ultimate Safe Usag
# We need to extract everything after "title": " and before the end
# Since it's truncated, there's no closing quote

broken_ids = [1185, 1183, 1171, 1165, 1162, 1161, 1160, 1157, 1142, 1135]
ids_str = ",".join(str(x) for x in broken_ids)

php = (
    '<?php\n'
    'require_once("/home/u284669846/domains/plantsmag.com/public_html/wp-load.php");\n'
    'global $wpdb;\n'
    '$ids = array(' + ids_str + ');\n'
    'foreach ($ids as $id) {\n'
    '    $title = $wpdb->get_var("SELECT post_title FROM wp_posts WHERE ID = $id");\n'
    '    $real = "";\n'
    '    // Extract text after "title": " — handle truncated JSON\n'
    '    if (preg_match(\'/"title"\\s*:\\s*"(.+)/\', $title, $m)) {\n'
    '        $real = $m[1];\n'
    '        // Remove trailing quote/brace if present\n'
    '        $real = rtrim($real, \'"\\ },\');\n'
    '        // Trim whitespace\n'
    '        $real = trim($real);\n'
    '    }\n'
    '    if (strlen($real) > 10) {\n'
    '        $slug = sanitize_title($real);\n'
    '        $wpdb->update("wp_posts", array("post_title" => $real, "post_name" => $slug), array("ID" => $id));\n'
    '        echo "FIXED #$id: $real\\n";\n'
    '    } else {\n'
    '        echo "FAIL #$id (len=" . strlen($real) . "): $title\\n";\n'
    '    }\n'
    '}\n'
    'wp_cache_flush();\n'
    'echo "\\nCache flushed.\\n";\n'
    '?>\n'
)

sftp = ssh.open_sftp()
with sftp.open(wp + '/fix_trunc.php', 'w') as f:
    f.write(php)
sftp.close()

out = run('cd ' + wp + ' && php fix_trunc.php 2>&1')
print(out)
run('rm ' + wp + '/fix_trunc.php')

# Verify
print("VERIFICATION:")
for pid in broken_ids:
    t = run(f'cd {wp} && wp post get {pid} --field=post_title 2>&1').strip()
    ok = not t.startswith('{')
    print(f"  [{'OK' if ok else 'BROKEN'}] #{pid}: {t[:70]}")

ssh.close()
