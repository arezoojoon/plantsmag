"""
TECHNIQUE 2: Update N8N Workflow Prompts for GEO
(Generative Engine Optimization)

Adds <table> and <details><summary> structured tags to generated articles
so Google prioritizes them for Rich Snippets and AI Overview answers.
"""
import paramiko, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.62.93.117', port=22, username='root', password="5KT4'ub5B5oD8V9TB#/u", timeout=15)

def run(cmd):
    _, o, e = ssh.exec_command(cmd)
    return o.read().decode('utf-8', errors='replace'), e.read().decode('utf-8', errors='replace')

# Login to N8N
run('''curl -s -c /tmp/n8n_session.txt -X POST http://localhost:5678/rest/login -H "Content-Type: application/json" -d '{"emailOrLdapLoginId":"plantsmag@gmail.com","password":"PlantsMag2026!"}\' ''')
print("Logged into N8N\n")

# GEO-optimized prompt template
GEO_PROMPT_US = """Write a comprehensive, expert-level 2500+ word SEO article about: {{ $json.selectedTopic }}.

Target audience: US plant enthusiasts and indoor gardeners.

CRITICAL STRUCTURE REQUIREMENTS (for Google Rich Snippets and AI Overview):

1. Use H2 and H3 subheadings for logical structure
2. Include at least ONE HTML <table> comparing key data points (e.g., plant varieties, care requirements, product comparisons). Format as proper HTML: <table><thead><tr><th>...</th></tr></thead><tbody><tr><td>...</td></tr></tbody></table>
3. Include a FAQ section at the end using HTML <details><summary> tags for each Q&A pair. Format: <details><summary>Question here?</summary><p>Answer here.</p></details>
4. Naturally mention useful Amazon products (moisture meters, grow lights, soil mixes, pots) with descriptive anchor text
5. Include practical, actionable step-by-step advice using <ol> ordered lists
6. Write in an authoritative yet friendly expert tone
7. Include at least 3 internal linking opportunities using descriptive anchor text

Return your response as valid JSON with these exact keys:
{
  "title": "SEO-optimized article title (55-60 chars, include power word)",
  "slug": "url-friendly-slug-with-dashes-max-60-chars",
  "meta_description": "Compelling meta description under 155 characters with call-to-action",
  "content": "Full HTML article with h2, h3, p, ul, ol, li, table, details, summary tags"
}

IMPORTANT: Return ONLY the JSON object. No markdown code fences. No extra text."""

GEO_PROMPT_UAE = """Write a comprehensive 2500+ word SEO article about: {{ $json.selectedTopic }}.

Target audience: UAE-based plant enthusiasts, expat gardeners, and Amazon.ae shoppers.

CRITICAL STRUCTURE REQUIREMENTS (for Google Rich Snippets and AI Overview):

1. Use H2 and H3 subheadings for logical structure
2. Include at least ONE HTML <table> comparing products, care schedules, or plant varieties. Use proper HTML table markup with thead/tbody.
3. Include a FAQ section using HTML <details><summary> tags for 3-5 common questions.
4. Reference Amazon.ae products naturally (indoor planters, grow lights for UAE climate, humidity trays)
5. Consider UAE climate challenges: extreme heat, air conditioning effects, indoor humidity
6. Include actionable tips in <ol> ordered lists
7. Write with authority — reference botanical names and specific care data

Return JSON: {"title": "...", "slug": "...", "meta_description": "...", "content": "..."}
Return ONLY JSON. No markdown fences."""

GEO_PROMPT_FUNNEL = """Write a comprehensive 2500+ word high-value SEO article about: {{ $json.selectedTopic }}.

Target audience: Serious US plant collectors willing to invest in premium equipment and rare plants.

CRITICAL STRUCTURE REQUIREMENTS:

1. Premium, authoritative tone — position as expert consultation
2. Include HTML <table> comparing premium products with pricing tiers
3. Include FAQ section with <details><summary> HTML tags
4. Reference high-ticket items: professional grow light systems ($200+), premium soil mixes, rare plant varieties
5. Include ROI calculations or cost-benefit analysis where relevant
6. Use data-driven arguments with specific numbers
7. Include <ol> step-by-step guides for complex procedures

Return JSON: {"title": "...", "slug": "...", "meta_description": "...", "content": "..."}
Return ONLY JSON. No markdown fences."""

# Workflow configs: ID -> (prompt, node_name)
WORKFLOWS = {
    'CpyU2cf01DdtpfWo': ('WF1 - US Trend Jacker', 'Gemini 2.5 Write', GEO_PROMPT_US),
    'UKegbNpPIBkkNUrd': ('WF2 - UAE Amazon Market', 'Gemini UAE', GEO_PROMPT_UAE),
    'SLgAkWAL2NBVzZ7U': ('WF3 - High-Ticket Funnel', 'Gemini Write', GEO_PROMPT_FUNNEL),
}

for wf_id, (wf_name, gemini_node_name, new_prompt) in WORKFLOWS.items():
    print(f"\n{'='*50}")
    print(f"Updating: {wf_name}")
    print(f"{'='*50}")
    
    # Get current workflow
    wf_out, _ = run(f'curl -s -b /tmp/n8n_session.txt http://localhost:5678/rest/workflows/{wf_id}')
    wf_data = json.loads(wf_out).get('data', {})
    
    modified = False
    for node in wf_data.get('nodes', []):
        if node['name'] == gemini_node_name and node['type'] == 'n8n-nodes-base.httpRequest':
            # Update the prompt in the body
            old_body = node['parameters'].get('body', '')
            
            # The body is a JSON string containing the Gemini API payload
            # We need to update just the text prompt inside it
            new_body = '={"contents":[{"parts":[{"text":"' + new_prompt.replace('"', '\\"').replace('\n', '\\n') + '"}]}],"generationConfig":{"temperature":0.7,"maxOutputTokens":8192}}'
            
            node['parameters']['body'] = new_body
            modified = True
            print(f"  Updated prompt for node: {gemini_node_name}")
            print(f"  New prompt length: {len(new_prompt)} chars")
    
    if modified:
        # Save back to N8N
        update_payload = json.dumps({"nodes": wf_data['nodes']})
        
        sftp = ssh.open_sftp()
        remote_path = f'/tmp/wf_update_{wf_id}.json'
        with sftp.open(remote_path, 'w') as f:
            f.write(update_payload)
        sftp.close()
        
        result, _ = run(f'curl -s -b /tmp/n8n_session.txt -X PATCH http://localhost:5678/rest/workflows/{wf_id} -H "Content-Type: application/json" -d @{remote_path}')
        if '"updatedAt"' in result:
            print(f"  SUCCESS: Workflow updated!")
        else:
            print(f"  Result: {result[:200]}")
    else:
        print(f"  WARNING: Could not find Gemini node '{gemini_node_name}'")

ssh.close()
print("\n\nTECHNIQUE 2 COMPLETE: All N8N prompts updated with GEO optimization!")
print("New articles will now include <table> and <details><summary> for Rich Snippets.")
