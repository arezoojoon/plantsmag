import paramiko, sys, json, time, tempfile, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.62.93.117', port=22, username='root', password="5KT4'ub5B5oD8V9TB#/u", timeout=15)

def run(cmd, timeout=30):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    return out, err

def write_remote(content, remote_path):
    sftp = ssh.open_sftp()
    with sftp.file(remote_path, 'w') as rf:
        rf.write(content)
    sftp.close()

print("=" * 60)
print("PlantsMag n8n — Complete Setup")
print("=" * 60)

# Auth
print("\n1. Authenticating...")
run("""curl -s -c /tmp/n8n_session.txt -X POST http://localhost:5678/rest/login \
  -H 'Content-Type: application/json' \
  -d '{"emailOrLdapLoginId":"plantsmag@gmail.com","password":"PlantsMag2026!"}' -o /dev/null 2>/dev/null""")
chk, _ = run("curl -s -b /tmp/n8n_session.txt http://localhost:5678/rest/workflows 2>/dev/null | python3 -c \"import sys,json;d=json.load(sys.stdin);print('Auth OK, wf count:',len(d.get('data',[])))\"")
print(f"  {chk}")

# Create credential
print("\n2. Creating WordPress credential...")
WP_USER = 'artinmag'
WP_PASS = 'XH18 J5Wq 52Ow oM2M gukl hNcH'
cred_payload = json.dumps({"name":"PlantsMag WP Auth","type":"httpBasicAuth","data":{"user":WP_USER,"password":WP_PASS}})
write_remote(cred_payload, '/tmp/cred.json')
cred_resp, _ = run("curl -s -b /tmp/n8n_session.txt -X POST http://localhost:5678/rest/credentials -H 'Content-Type: application/json' -d @/tmp/cred.json 2>/dev/null")
try:
    cred_data = json.loads(cred_resp)
    cred_id = cred_data.get('data', {}).get('id', '')
    print(f"  Credential created: ID={cred_id}")
except:
    print(f"  Cred response: {cred_resp[:200]}")
    cred_id = ''

# Helper to create and activate a workflow
def create_and_activate(name, nodes, connections):
    payload = json.dumps({"name":name,"nodes":nodes,"connections":connections,"settings":{"executionOrder":"v1"},"staticData":None})
    remote_file = f'/tmp/wf_{name[:10].replace(" ","_")}.json'
    write_remote(payload, remote_file)
    resp, _ = run(f"curl -s -b /tmp/n8n_session.txt -X POST http://localhost:5678/rest/workflows -H 'Content-Type: application/json' -d @{remote_file} 2>/dev/null")
    try:
        wf_data = json.loads(resp).get('data', {})
        wf_id = wf_data.get('id', '')
        wf_name = wf_data.get('name', '?')
        if wf_id:
            # Activate
            act_resp, _ = run(f"curl -s -b /tmp/n8n_session.txt -X PATCH http://localhost:5678/rest/workflows/{wf_id} -H 'Content-Type: application/json' -d '{{\"active\":true}}' -o /dev/null 2>/dev/null")
            return f"✅ Created & Activated: {wf_name} (ID:{wf_id})"
        return f"⚠️ No ID: {resp[:150]}"
    except Exception as e:
        return f"❌ Error: {e} | Response: {resp[:100]}"

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
GEMINI_KEY = "REDACTED_API_KEY"

# ── WF1: US Trend Jacker ─────────────────────────────────────────
print("\n3. Creating WF1 — US Trend Jacker...")

wf1_nodes = [
  {"parameters":{"rule":{"interval":[{"field":"cronExpression","expression":"0 13 * * *"}]}},"id":"n1","name":"Daily 8AM EST","type":"n8n-nodes-base.scheduleTrigger","typeVersion":1.2,"position":[180,300]},
  {"parameters":{"jsCode":"const topics=['Spider mites on houseplants: complete guide','Why Monstera leaves turn yellow','Root rot: how to save your plant','Best soil for tropical plants 2026','Orchid care beginner guide','Calathea curling leaves causes','Overwatering vs underwatering signs','Repotting houseplants step by step','Snake plant care complete guide','Pothos varieties comparison 2026'];return {topic:topics[Math.floor(Math.random()*topics.length)]}"},"id":"n2","name":"Select Topic","type":"n8n-nodes-base.code","typeVersion":2,"position":[420,300]},
  {"parameters":{"method":"POST","url":GEMINI_URL,"sendQuery":True,"queryParameters":{"parameters":[{"name":"key","value":GEMINI_KEY}]},"sendHeaders":True,"headerParameters":{"parameters":[{"name":"Content-Type","value":"application/json"}]},"sendBody":True,"contentType":"raw","rawContentType":"application/json","body":"{\"contents\":[{\"parts\":[{\"text\":\"Write a 2500-word SEO article for US plant enthusiasts about: {{ $json.topic }}. Include practical expert advice, H2 sections, FAQ (3 questions), and naturally mention Amazon products (neem oil, moisture meter, grow lights) with affiliate links using tag=plantsmag-20. Use power words in title. Return ONLY valid JSON with keys: title, slug, meta_description, content (HTML with h2 h3 p ul li tags)\"}]}],\"generationConfig\":{\"temperature\":0.8,\"maxOutputTokens\":8192}}"},"id":"n3","name":"Gemini Write US","type":"n8n-nodes-base.httpRequest","typeVersion":4.2,"position":[660,300]},
  {"parameters":{"jsCode":"const r=$input.item.json;let t=r?.candidates?.[0]?.content?.parts?.[0]?.text||'';t=t.replace(/```json\\n?/g,'').replace(/```\\n?/g,'').trim();let a;try{a=JSON.parse(t)}catch(e){const m=t.match(/\\{[\\s\\S]*?\\}/s);if(m)try{a=JSON.parse(m[0])}catch(e2){a=null}}a=a||{title:'Plant Care Guide '+Date.now(),slug:'plant-care-guide-'+Date.now(),meta_description:'Expert plant care advice for US plant lovers',content:t||'<p>Article content</p>'};return {title:String(a.title||'').slice(0,200),slug:String(a.slug||'plant-guide').replace(/[^a-z0-9-]/gi,'-').slice(0,60),meta_description:String(a.meta_description||'').slice(0,155),content:String(a.content||'')}"},"id":"n4","name":"Parse US Article","type":"n8n-nodes-base.code","typeVersion":2,"position":[900,300]},
  {"parameters":{"method":"POST","url":"https://plantsmag.com/wp-json/wp/v2/posts","authentication":"genericCredentialType","genericAuthType":"httpBasicAuth","sendBody":True,"contentType":"json","body":"{\"title\":\"{{ $json.title }}\",\"content\":\"{{ $json.content }}\",\"excerpt\":\"{{ $json.meta_description }}\",\"status\":\"publish\",\"categories\":[1]}","options":{}},"id":"n5","name":"Publish US Post","type":"n8n-nodes-base.httpRequest","typeVersion":4.2,"position":[1140,300],"credentials":{"httpBasicAuth":{"id":cred_id,"name":"PlantsMag WP Auth"}}}
]
wf1_conns = {"Daily 8AM EST":{"main":[[{"node":"Select Topic","type":"main","index":0}]]},"Select Topic":{"main":[[{"node":"Gemini Write US","type":"main","index":0}]]},"Gemini Write US":{"main":[[{"node":"Parse US Article","type":"main","index":0}]]},"Parse US Article":{"main":[[{"node":"Publish US Post","type":"main","index":0}]]}}
print("  " + create_and_activate("WF1 — US Trend Jacker", wf1_nodes, wf1_conns))

# ── WF2: UAE Amazon Market ───────────────────────────────────────
print("\n4. Creating WF2 — UAE Amazon Market...")
wf2_nodes = [
  {"parameters":{"rule":{"interval":[{"field":"cronExpression","expression":"0 10 * * *"}]}},"id":"w2a","name":"14:00 GST Daily","type":"n8n-nodes-base.scheduleTrigger","typeVersion":1.2,"position":[180,300]},
  {"parameters":{"jsCode":"const topics=['Best indoor plants for UAE apartments with extreme heat','How to water plants in Dubai dry climate','Spider mite crisis in Gulf region guide','Top 10 low-maintenance plants for UAE beginners','Snake plant care in UAE: survival guide','ZZ plant care Abu Dhabi climate','Orchid care UAE humid summer tips','Monstera care Dubai apartment guide'];const products=[{name:'Organic Neem Oil Spray',asin:'B07M983S9B',price:'$18'},{name:'LEVOIT Humidifier',asin:'B08L73ZT3N',price:'$79'},{name:'Soil Moisture Meter',asin:'B07KBKXZL1',price:'$12'},{name:'Spider Farmer Grow Light',asin:'B08B486YQK',price:'$189'}];const t=topics[Math.floor(Math.random()*topics.length)];const p=products[Math.floor(Math.random()*products.length)];return {topic:t,product:p}"},"id":"w2b","name":"Select UAE Topic","type":"n8n-nodes-base.code","typeVersion":2,"position":[420,300]},
  {"parameters":{"method":"POST","url":GEMINI_URL,"sendQuery":True,"queryParameters":{"parameters":[{"name":"key","value":GEMINI_KEY}]},"sendHeaders":True,"headerParameters":{"parameters":[{"name":"Content-Type","value":"application/json"}]},"sendBody":True,"contentType":"raw","rawContentType":"application/json","body":"{\"contents\":[{\"parts\":[{\"text\":\"Write a 2500-word SEO article for UAE/Gulf English-speaking plant enthusiasts about: {{ $json.topic }}. Feature product: {{ $json.product.name }} (ASIN {{ $json.product.asin }}, {{ $json.product.price }}) with Amazon UAE purchase link (https://www.amazon.ae/dp/{{ $json.product.asin }}?tag=plantsmag-ae-21). Include UAE climate context: extreme heat 40-50C summers, very low humidity, mostly indoor plants. Use Dubai/Abu Dhabi references. Include H2 sections, FAQ, strong CTA. Return ONLY valid JSON: {title, slug, meta_description, content}\"}]}],\"generationConfig\":{\"temperature\":0.75,\"maxOutputTokens\":8192}}"},"id":"w2c","name":"Gemini UAE","type":"n8n-nodes-base.httpRequest","typeVersion":4.2,"position":[660,300]},
  {"parameters":{"jsCode":"const r=$input.item.json;let t=r?.candidates?.[0]?.content?.parts?.[0]?.text||'';t=t.replace(/```json\\n?/g,'').replace(/```\\n?/g,'').trim();let a;try{a=JSON.parse(t)}catch(e){const m=t.match(/\\{[\\s\\S]*?\\}/s);if(m)try{a=JSON.parse(m[0])}catch(e2){a=null}}a=a||{title:'UAE Plant Guide '+Date.now(),slug:'uae-plant-guide-'+Date.now(),meta_description:'Plant care for UAE',content:t||'<p>Article</p>'};return {title:String(a.title||'').slice(0,200),slug:String(a.slug||'uae-guide').replace(/[^a-z0-9-]/gi,'-').slice(0,60),meta_description:String(a.meta_description||'').slice(0,155),content:String(a.content||'')}"},"id":"w2d","name":"Parse UAE Article","type":"n8n-nodes-base.code","typeVersion":2,"position":[900,300]},
  {"parameters":{"method":"POST","url":"https://plantsmag.com/wp-json/wp/v2/posts","authentication":"genericCredentialType","genericAuthType":"httpBasicAuth","sendBody":True,"contentType":"json","body":"{\"title\":\"{{ $json.title }}\",\"content\":\"{{ $json.content }}\",\"excerpt\":\"{{ $json.meta_description }}\",\"status\":\"publish\",\"categories\":[1]}","options":{}},"id":"w2e","name":"Publish UAE Post","type":"n8n-nodes-base.httpRequest","typeVersion":4.2,"position":[1140,300],"credentials":{"httpBasicAuth":{"id":cred_id,"name":"PlantsMag WP Auth"}}}
]
wf2_conns = {"14:00 GST Daily":{"main":[[{"node":"Select UAE Topic","type":"main","index":0}]]},"Select UAE Topic":{"main":[[{"node":"Gemini UAE","type":"main","index":0}]]},"Gemini UAE":{"main":[[{"node":"Parse UAE Article","type":"main","index":0}]]},"Parse UAE Article":{"main":[[{"node":"Publish UAE Post","type":"main","index":0}]]}}
print("  " + create_and_activate("WF2 — UAE Amazon Market", wf2_nodes, wf2_conns))

# ── WF3: High-Ticket Funnel ──────────────────────────────────────
print("\n5. Creating WF3 — High-Ticket Funnel...")
wf3_nodes = [
  {"parameters":{"rule":{"interval":[{"field":"cronExpression","expression":"0 15 */2 * *"}]}},"id":"w3a","name":"Every 2 Days","type":"n8n-nodes-base.scheduleTrigger","typeVersion":1.2,"position":[180,300]},
  {"parameters":{"jsCode":"const cats=[{cat:'LED Grow Lights',angle:'Best LED Grow Lights for Indoor Plants 2026: Expert Tested',asin:'B08B486YQK',price:'$189',name:'Spider Farmer SF-2000'},{cat:'Plant Humidifiers',angle:'Best Humidifiers for Tropical Houseplants 2026',asin:'B08L73ZT3N',price:'$79',name:'LEVOIT 6L Humidifier'},{cat:'Smart Soil Sensors',angle:'Best Smart Plant Monitors 2026: Honest Expert Review',asin:'B07KBKXZL1',price:'$29',name:'XLUX Soil Sensor'},{cat:'Self-Watering Pots',angle:'Best Self-Watering Planters for Busy Plant Parents 2026',asin:'B07N1CLX3J',price:'$89',name:'LECHUZA CUBICO'},{cat:'Indoor Greenhouses',angle:'Best Mini Indoor Greenhouses 2026: Create Your Plant Paradise',asin:'B07RV3G2PF',price:'$49',name:'Ohuhu Mini Greenhouse'}];return cats[Math.floor(Math.random()*cats.length)]"},"id":"w3b","name":"Select High-Ticket","type":"n8n-nodes-base.code","typeVersion":2,"position":[420,300]},
  {"parameters":{"method":"POST","url":GEMINI_URL,"sendQuery":True,"queryParameters":{"parameters":[{"name":"key","value":GEMINI_KEY}]},"sendHeaders":True,"headerParameters":{"parameters":[{"name":"Content-Type","value":"application/json"}]},"sendBody":True,"contentType":"raw","rawContentType":"application/json","body":"{\"contents\":[{\"parts\":[{\"text\":\"Write a 2500-word high-converting product review article: {{ $json.angle }}. Feature product: {{ $json.name }} ({{ $json.price }}, ASIN {{ $json.asin }}). Structure: 1) AIDA intro (200w) hooking plant parent pain points 2) Quick comparison HTML table of top 3 {{ $json.cat }} products with ratings 3) Detailed review with pros/cons 4) Buying guide 5) FAQ (3 questions) 6) Strong CTA. Include affiliate links: US: https://www.amazon.com/dp/{{ $json.asin }}?tag=plantsmag-20 and UAE: https://www.amazon.ae/dp/{{ $json.asin }}?tag=plantsmag-ae-21. Disclosure at bottom. Return ONLY valid JSON: {title, slug, meta_description, content}\"}]}],\"generationConfig\":{\"temperature\":0.7,\"maxOutputTokens\":8192}}"},"id":"w3c","name":"Gemini Review","type":"n8n-nodes-base.httpRequest","typeVersion":4.2,"position":[660,300]},
  {"parameters":{"jsCode":"const r=$input.item.json;let t=r?.candidates?.[0]?.content?.parts?.[0]?.text||'';t=t.replace(/```json\\n?/g,'').replace(/```\\n?/g,'').trim();let a;try{a=JSON.parse(t)}catch(e){const m=t.match(/\\{[\\s\\S]*?\\}/s);if(m)try{a=JSON.parse(m[0])}catch(e2){a=null}}a=a||{title:'Plant Equipment Review '+Date.now(),slug:'plant-review-'+Date.now(),meta_description:'Expert plant equipment review',content:t||'<p>Review</p>'};return {title:String(a.title||'').slice(0,200),slug:String(a.slug||'plant-review').replace(/[^a-z0-9-]/gi,'-').slice(0,60),meta_description:String(a.meta_description||'').slice(0,155),content:String(a.content||'')}"},"id":"w3d","name":"Parse Review","type":"n8n-nodes-base.code","typeVersion":2,"position":[900,300]},
  {"parameters":{"method":"POST","url":"https://plantsmag.com/wp-json/wp/v2/posts","authentication":"genericCredentialType","genericAuthType":"httpBasicAuth","sendBody":True,"contentType":"json","body":"{\"title\":\"{{ $json.title }}\",\"content\":\"{{ $json.content }}\",\"excerpt\":\"{{ $json.meta_description }}\",\"status\":\"publish\",\"categories\":[1]}","options":{}},"id":"w3e","name":"Publish Review","type":"n8n-nodes-base.httpRequest","typeVersion":4.2,"position":[1140,300],"credentials":{"httpBasicAuth":{"id":cred_id,"name":"PlantsMag WP Auth"}}}
]
wf3_conns = {"Every 2 Days":{"main":[[{"node":"Select High-Ticket","type":"main","index":0}]]},"Select High-Ticket":{"main":[[{"node":"Gemini Review","type":"main","index":0}]]},"Gemini Review":{"main":[[{"node":"Parse Review","type":"main","index":0}]]},"Parse Review":{"main":[[{"node":"Publish Review","type":"main","index":0}]]}}
print("  " + create_and_activate("WF3 — High-Ticket Funnel", wf3_nodes, wf3_conns))

# Final status
print("\n" + "=" * 60)
print("FINAL STATUS:")
wf_json, _ = run("curl -s -b /tmp/n8n_session.txt http://localhost:5678/rest/workflows 2>/dev/null")
wfs = json.loads(wf_json).get('data', [])
print(f"Total workflows: {len(wfs)}")
for w in wfs:
    icon = "🟢" if w.get('active') else "⚫"
    print(f"  {icon} {w['name']}")
print("=" * 60)
ssh.close()
