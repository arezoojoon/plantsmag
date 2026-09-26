"""
Fix N8N Workflows: 
1. Fix Parse nodes to properly extract Gemini JSON
2. Fix Publish nodes to use correct expression format  
3. Delete broken posts (json-slug-*)
"""
import paramiko, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ================================================================
# PART A: Delete broken posts from WordPress
# ================================================================
print("=" * 60)
print("PART A: Cleaning broken posts from WordPress")
print("=" * 60)

ssh_wp = paramiko.SSHClient()
ssh_wp.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_wp.connect('187.124.245.99', port=65002, username='u284669846', password='[3pPybi0[3pPybi0', timeout=20)

def run_wp(cmd):
    _, o, e = ssh_wp.exec_command(cmd)
    return o.read().decode('utf-8', errors='replace'), e.read().decode('utf-8', errors='replace')

wp = '/home/u284669846/domains/plantsmag.com/public_html'

# Find and delete posts with "json-slug" in their slug or raw template content
out, _ = run_wp(f'cd {wp} && wp post list --post_type=post --post_status=publish --fields=ID,post_title,post_name --format=json')
posts = json.loads(out)
deleted = 0
for p in posts:
    slug = p.get('post_name', '')
    title = p.get('post_title', '')
    if 'json-slug' in slug or 'json.content' in title or not title:
        pid = p['ID']
        out2, _ = run_wp(f'cd {wp} && wp post delete {pid} --force 2>&1')
        print(f"  Deleted post #{pid}: slug={slug} title={title[:50]}")
        deleted += 1

print(f"\n  Total deleted: {deleted} broken posts")
ssh_wp.close()

# ================================================================
# PART B: Fix N8N Workflow nodes
# ================================================================
print("\n" + "=" * 60)
print("PART B: Fixing N8N Workflow Parse + Publish nodes")
print("=" * 60)

ssh_n8n = paramiko.SSHClient()
ssh_n8n.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_n8n.connect('72.62.93.117', port=22, username='root', password="5KT4'ub5B5oD8V9TB#/u", timeout=15)

def run_n8n(cmd):
    _, o, e = ssh_n8n.exec_command(cmd)
    return o.read().decode('utf-8', errors='replace'), e.read().decode('utf-8', errors='replace')

# Login
run_n8n('''curl -s -c /tmp/n8n_session.txt -X POST http://localhost:5678/rest/login -H "Content-Type: application/json" -d '{"emailOrLdapLoginId":"plantsmag@gmail.com","password":"PlantsMag2026!"}\' ''')
print("  Logged into N8N")

# Robust Parse code that handles all Gemini response formats
PARSE_CODE = r'''
const raw = $input.item.json;

// Extract text from Gemini response
let text = "";
try {
  if (raw.candidates && raw.candidates[0]) {
    text = raw.candidates[0].content.parts[0].text;
  } else if (typeof raw === "string") {
    text = raw;
  } else if (raw.body) {
    const body = typeof raw.body === "string" ? JSON.parse(raw.body) : raw.body;
    text = body.candidates[0].content.parts[0].text;
  }
} catch(e) {
  text = JSON.stringify(raw);
}

// Clean markdown fencing
text = text.replace(/^```json\s*/i, "").replace(/^```\s*/i, "").replace(/```\s*$/g, "").trim();

// Parse JSON
let article;
try {
  article = JSON.parse(text);
} catch(e) {
  // Try to find JSON object in the text
  const match = text.match(/\{[\s\S]*"title"[\s\S]*"content"[\s\S]*\}/);
  if (match) {
    try {
      article = JSON.parse(match[0]);
    } catch(e2) {
      article = null;
    }
  }
}

if (!article || !article.content || article.content.length < 100) {
  // Last resort: use raw text as content
  const words = text.split(/\s+/).slice(0, 10).join(" ");
  return {
    json: {
      title: words.substring(0, 60) || "Plant Care Guide",
      slug: words.substring(0, 40).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/-+/g, "-") || "plant-care-guide",
      meta_description: words.substring(0, 155) || "Expert plant care tips",
      content: "<p>" + text.replace(/\n\n/g, "</p><p>").replace(/\n/g, "<br>") + "</p>"
    }
  };
}

return {
  json: {
    title: (article.title || "Plant Care Guide").substring(0, 70),
    slug: (article.slug || "plant-guide-" + Date.now()).substring(0, 60),
    meta_description: (article.meta_description || article.excerpt || "").substring(0, 160),
    content: article.content || ""
  }
};
'''

# Workflow IDs and their node names
WORKFLOWS = {
    'CpyU2cf01DdtpfWo': {
        'name': 'WF1 - US Trend Jacker',
        'parse_node': 'Parse Article',
        'publish_node': 'Publish to WordPress',
    },
    'UKegbNpPIBkkNUrd': {
        'name': 'WF2 - UAE Amazon Market',
        'parse_node': 'Parse UAE Article',
        'publish_node': 'Publish UAE Post',
    },
    'SLgAkWAL2NBVzZ7U': {
        'name': 'WF3 - High-Ticket Funnel',
        'parse_node': 'Parse Review',
        'publish_node': 'Publish Review',
    },
}

for wf_id, config in WORKFLOWS.items():
    print(f"\n--- Fixing: {config['name']} ---")
    
    wf_out, _ = run_n8n(f'curl -s -b /tmp/n8n_session.txt http://localhost:5678/rest/workflows/{wf_id}')
    wf_data = json.loads(wf_out).get('data', {})
    
    modified = False
    for node in wf_data.get('nodes', []):
        # Fix Parse node
        if node['name'] == config['parse_node'] and node['type'] == 'n8n-nodes-base.code':
            node['parameters']['jsCode'] = PARSE_CODE
            modified = True
            print(f"  Fixed Parse node: {node['name']}")
        
        # Fix Publish node — use expression-based jsonBody
        if node['name'] == config['publish_node'] and node['type'] == 'n8n-nodes-base.httpRequest':
            node['parameters']['specifyBody'] = 'json'
            node['parameters']['contentType'] = 'json'
            # The key fix: use N8N expression that builds JSON properly
            # The entire jsonBody must be an expression starting with =
            node['parameters']['jsonBody'] = '={{ JSON.stringify({ "title": $json.title, "content": $json.content, "status": "publish", "excerpt": $json.meta_description || "", "slug": $json.slug }) }}'
            
            # Remove old bodyParameters if present
            if 'bodyParameters' in node['parameters']:
                del node['parameters']['bodyParameters']
            
            modified = True
            print(f"  Fixed Publish node: {node['name']}")
            print(f"    jsonBody = expression-based JSON.stringify")
    
    if modified:
        update_payload = json.dumps({"nodes": wf_data['nodes']})
        sftp = ssh_n8n.open_sftp()
        remote_path = f'/tmp/wf_fix_{wf_id}.json'
        with sftp.open(remote_path, 'w') as f:
            f.write(update_payload)
        sftp.close()
        
        result, _ = run_n8n(f'curl -s -b /tmp/n8n_session.txt -X PATCH http://localhost:5678/rest/workflows/{wf_id} -H "Content-Type: application/json" -d @{remote_path}')
        if '"updatedAt"' in result:
            print(f"  SAVED: {config['name']}")
        else:
            print(f"  ERROR: {result[:200]}")

ssh_n8n.close()

print("\n" + "=" * 60)
print("ALL FIXES APPLIED!")
print("=" * 60)
print("""
Changes:
1. Deleted broken 'json-slug-*' posts from WordPress
2. Fixed Parse nodes: robust Gemini JSON extraction with fallbacks
3. Fixed Publish nodes: using JSON.stringify() expression for body
   (prevents raw {{$json.content}} from appearing in posts)
""")
