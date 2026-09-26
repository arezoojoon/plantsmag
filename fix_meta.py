import paramiko
import sys
import os

HOST = '187.124.245.99'
PORT = 65002
USER = 'u284669846'
PASS = '[3pPybi0[3pPybi0'

php_script = """<?php
require_once('/home/u284669846/domains/plantsmag.com/public_html/wp-load.php');

$posts = [
    'best-plant-apps-2026-planta-greg-vera-comparison' => [
        'title' => 'vera plant care app',
        'excerpt' => 'Trying to find the best vera plant care app? We compare Planta, Greg, and Vera so you can decide which one is right for your indoor jungle.'
    ],
    'keiki-paste-magic-forcing-growth-on-stubborn-monstera-nodes' => [
        'title' => 'does keiki paste work on monstera',
        'excerpt' => 'Wondering does keiki paste work on monstera? We tested the magic paste on stubborn monstera nodes to force new growth. See the results.'
    ],
    'the-monstera-deliciosa-support-guide-moss-pole-vs-coir-pole-vs-trellis' => [
        'title' => 'moss pole vs coco coir pole',
        'excerpt' => 'Moss pole vs coco coir pole: Which support is best for your Monstera Deliciosa? We break down the pros, cons, and which one promotes bigger leaves.'
    ]
];

foreach ($posts as $slug => $data) {
    $post = get_page_by_path($slug, OBJECT, 'post');
    if ($post) {
        $post->post_title = $data['title'];
        $post->post_excerpt = $data['excerpt'];
        wp_update_post($post);
        echo "Updated post: " . $slug . "\\n";
    } else {
        echo "Post not found: " . $slug . "\\n";
    }
}
?>"""

local_script = 'fix_meta_script.php'
with open(local_script, 'w') as f:
    f.write(php_script)

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(HOST, port=PORT, username=USER, password=PASS, timeout=20)
sftp = ssh.open_sftp()
sftp.put(local_script, '/home/u284669846/domains/plantsmag.com/public_html/fix_meta_script.php')
sftp.close()

stdin, stdout, stderr = ssh.exec_command('php /home/u284669846/domains/plantsmag.com/public_html/fix_meta_script.php')
print(stdout.read().decode())
print(stderr.read().decode())

ssh.exec_command('rm /home/u284669846/domains/plantsmag.com/public_html/fix_meta_script.php')
ssh.close()
os.remove(local_script)
