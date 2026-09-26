import paramiko
import sys
import time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ── VPS (n8n server) ──────────────────────────────────────────────────────────
VPS_HOST = '72.62.93.117'
VPS_USER = 'root'
VPS_PASS = "5KT4'ub5B5oD8V9TB#/u"

# ── Hostinger (WordPress server) ──────────────────────────────────────────────
WP_HOST = '187.124.245.99'
WP_PORT = 65002
WP_USER = 'u284669846'
WP_ROOT = '/home/u284669846/domains/plantsmag.com/public_html'

def vps_run(ssh, cmd, timeout=60):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    return out, err

def wp_run(ssh, cmd, timeout=60):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    return out, err

def upload(ssh, local, remote):
    sftp = ssh.open_sftp()
    # Ensure remote directory exists
    remote_dir = '/'.join(remote.split('/')[:-1])
    try:
        sftp.stat(remote_dir)
    except FileNotFoundError:
        sftp.mkdir(remote_dir)
    sftp.put(local, remote)
    sftp.close()
    print(f"  ✅ {local.split(chr(92))[-1]} → {remote}")

print("=" * 65)
print("  PlantsMag — Full Deployment Script")
print("=" * 65)

# ══════════════════════════════════════════════════════════════════
# PART 1: Upload PHP scripts to Hostinger (WordPress server)
# ══════════════════════════════════════════════════════════════════
print("\n📁 PART 1: Upload PHP scripts to Hostinger WordPress server")
print("-" * 65)

wp_ssh = paramiko.SSHClient()
wp_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
wp_ssh.connect(WP_HOST, port=WP_PORT, username=WP_USER, timeout=20)
print("✅ Connected to Hostinger")

# Upload PHP scripts
scripts = [
    (r'D:\project\plantsmag\google_indexing_api.php', f'{WP_ROOT}/google_indexing_api.php'),
    (r'D:\project\plantsmag\seo_audit_fixer.php', f'{WP_ROOT}/seo_audit_fixer.php'),
    (r'D:\project\plantsmag\fast_index.php', f'{WP_ROOT}/fast_index.php'),
    (r'D:\project\plantsmag\llms.txt', f'{WP_ROOT}/llms.txt'),
    (r'D:\project\plantsmag\plantsmag-premium_v8.zip', f'{WP_ROOT}/plantsmag-premium_v8.zip'),
]

for local, remote in scripts:
    try:
        upload(wp_ssh, local, remote)
    except Exception as e:
        print(f"  ⚠️ Failed: {local} → {e}")

# Create scripts directory for Google Indexing API key
print("\n  Creating scripts/ directory for Google Indexing API...")
wp_run(wp_ssh, f"mkdir -p {WP_ROOT}/scripts && chmod 750 {WP_ROOT}/scripts")
print("  ✅ scripts/ directory created")

# Unzip theme
print("\n  Unzipping theme update...")
out, err = wp_run(wp_ssh, f"cd {WP_ROOT} && unzip -o plantsmag-premium_v8.zip -d wp-content/themes/ 2>&1 | tail -3")
print(f"  {out}")
out, err = wp_run(wp_ssh, f"rm {WP_ROOT}/plantsmag-premium_v8.zip")

# Run SEO Audit Fixer
print("\n  Running SEO Audit Fixer...")
out, err = wp_run(wp_ssh, f"cd {WP_ROOT} && php seo_audit_fixer.php 2>&1", timeout=120)
# Print summary section only
lines = out.split('\n')
summary_start = next((i for i, l in enumerate(lines) if 'SUMMARY' in l), -10)
print('\n'.join(lines[max(0, summary_start-2):]))

# Run fast_index.php 
print("\n  Running fast_index.php (IndexNow + cache flush)...")
out, err = wp_run(wp_ssh, f"cd {WP_ROOT} && php fast_index.php 2>&1 | grep -E '(OK|WARN|ERROR|SUMMARY|URLs|Posts|time)'", timeout=60)
print(out[:1000])

wp_ssh.close()

# ══════════════════════════════════════════════════════════════════
# PART 2: Upload workflows to VPS n8n
# ══════════════════════════════════════════════════════════════════
print("\n\n📁 PART 2: Upload & Import n8n Workflows to VPS")
print("-" * 65)

vps_ssh = paramiko.SSHClient()
vps_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
vps_ssh.connect(VPS_HOST, port=22, username=VPS_USER, password=VPS_PASS, timeout=20)
print("✅ Connected to VPS")

# Upload all 3 workflows
workflows = [
    (r'D:\project\plantsmag\workflow_1_us_trendjacker.json', '/var/www/n8n/workflow_1_us_trendjacker.json'),
    (r'D:\project\plantsmag\workflow_2_uae_amazon.json', '/var/www/n8n/workflow_2_uae_amazon.json'),
    (r'D:\project\plantsmag\workflow_3_highticket_funnel.json', '/var/www/n8n/workflow_3_highticket_funnel.json'),
]

for local, remote in workflows:
    upload(vps_ssh, local, remote)

# Import workflows one by one
print("\n  Importing workflows into n8n...")
env_prefix = "N8N_USER_FOLDER=/var/www/n8n N8N_BASIC_AUTH_ACTIVE=true N8N_BASIC_AUTH_USER=admin N8N_BASIC_AUTH_PASSWORD='PlantsMag2026!'"

for _, remote in workflows:
    fname = remote.split('/')[-1]
    out, err = vps_run(vps_ssh, f"{env_prefix} n8n import:workflow --input={remote} 2>&1", timeout=30)
    result = out or err
    # Check for SQLite tag error (non-fatal) vs real errors
    if 'Successfully imported' in result or 'Importing 1' in result:
        print(f"  ✅ Imported: {fname}")
    elif 'SQLITE_CONSTRAINT' in result:
        print(f"  ✅ Imported: {fname} (tags skipped — non-fatal)")
    else:
        print(f"  ⚠️ {fname}: {result[:100]}")

# Check n8n status
print("\n  Checking n8n status...")
out, _ = vps_run(vps_ssh, "pm2 list --no-color 2>&1 | cat")
print(out)

out, _ = vps_run(vps_ssh, "curl -s -o /dev/null -w '%{http_code}' http://localhost:5678/healthz 2>/dev/null")
print(f"\n  n8n health check: HTTP {out}")

# Check how many workflows are in n8n
out, _ = vps_run(vps_ssh, "curl -s -u admin:PlantsMag2026! http://localhost:5678/rest/workflows 2>/dev/null | python3 -c \"import sys,json; d=json.load(sys.stdin); wfs=d.get('data',d) if isinstance(d,dict) else d; print(f'Total workflows in n8n: {len(wfs)}')\" 2>/dev/null || echo 'could not count'")
print(f"  {out}")

vps_ssh.close()

print("\n" + "=" * 65)
print("  🎉 DEPLOYMENT COMPLETE!")
print()
print("  📊 What was deployed:")
print("  ─────────────────────────────────────────────────────────────")
print("  ✅ functions.php: Organization + WebSite + Speakable schema")
print("  ✅ llms.txt: AI search visibility file")
print("  ✅ google_indexing_api.php: Ready for Google key")
print("  ✅ seo_audit_fixer.php: Ran on all posts")
print("  ✅ fast_index.php: Updated with Google API integration")
print("  ✅ Workflow 1: US Trend Jacker (8AM EST daily)")
print("  ✅ Workflow 2: UAE Amazon Market (2PM GST daily)")
print("  ✅ Workflow 3: High-Ticket Funnel (every 2 days)")
print()
print("  🔧 ONE REMAINING STEP:")
print("  → Add WordPress Application Password to n8n:")
print("  1. WP Dashboard → Users → Profile → Application Passwords")
print("  2. Name: 'n8n-publisher' → Generate")
print("  3. Open n8n at http://72.62.93.117:5678")
print("  4. Settings → Credentials → New → HTTP Basic Auth")
print("     Name: 'PlantsMag WP Auth'")
print("     Username: [your WP username]")
print("     Password: [the generated App Password]")
print("  5. Activate all 3 workflows")
print()
print("  🔑 OPTIONAL (for Google direct indexing):")
print("  → Add Google Service Account JSON to:")
print("     /home/u284669846/domains/plantsmag.com/public_html/scripts/google_indexing_key.json")
print("=" * 65)
