"""
Boost N8N: Change schedules so each workflow runs 3x/day
Total output: 9 articles per day

WF1 - US Trend Jacker: 08:00, 14:00, 20:00 UTC (12:00, 18:00, 00:00 GST)
WF2 - UAE Amazon:      06:00, 12:00, 18:00 UTC (10:00, 16:00, 22:00 GST)
WF3 - High-Ticket:     07:00, 13:00, 19:00 UTC (11:00, 17:00, 23:00 GST)
"""
import paramiko, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('72.62.93.117', port=22, username='root', password="5KT4'ub5B5oD8V9TB#/u", timeout=15)

def run(cmd):
    _, o, _ = ssh.exec_command(cmd)
    return o.read().decode('utf-8', errors='replace')

run('''curl -s -c /tmp/n8n_session.txt -X POST http://localhost:5678/rest/login -H "Content-Type: application/json" -d '{"emailOrLdapLoginId":"plantsmag@gmail.com","password":"PlantsMag2026!"}\' ''')
print("Logged into N8N\n")

# New schedules: 3x per day each
SCHEDULE_UPDATES = {
    'CpyU2cf01DdtpfWo': {
        'name': 'WF1 - US Trend Jacker',
        'trigger_node': 'Daily 8AM EST',
        'cron': '0 8,14,20 * * *',  # 3x daily
    },
    'UKegbNpPIBkkNUrd': {
        'name': 'WF2 - UAE Amazon Market',
        'trigger_node': '14:00 GST Daily',
        'cron': '0 6,12,18 * * *',  # 3x daily
    },
    'SLgAkWAL2NBVzZ7U': {
        'name': 'WF3 - High-Ticket Funnel',
        'trigger_node': 'Every 2 Days',
        'cron': '0 7,13,19 * * *',  # 3x daily (was every 2 days!)
    },
}

# Also expand topic lists so we don't get duplicates
EXPANDED_TOPICS_WF1 = """return {selectedTopic: [
  'Spider mites on houseplants identification treatment and prevention',
  'Monstera yellowing leaves causes and solutions',
  'Root rot rescue guide for indoor plants',
  'Best soil for tropical houseplants DIY mix recipes',
  'Orchid care mistakes beginners make',
  'Snake plant propagation methods water vs soil',
  'Pothos golden vs marble queen vs neon comparison',
  'How to propagate houseplants in water step by step',
  'Best grow lights for indoor plants LED comparison 2026',
  'Calathea care humidity requirements and brown edges fix',
  'Fiddle leaf fig brown spots causes and treatment',
  'ZZ plant complete care guide for beginners',
  'Peace lily not blooming how to force flowers',
  'Succulent overwatering vs underwatering signs',
  'Alocasia polly losing leaves winter dormancy guide',
  'String of pearls care watering and propagation',
  'Philodendron types for beginners easy care varieties',
  'Indoor herb garden setup kitchen windowsill guide',
  'Rubber plant pruning and shaping guide',
  'Bird of paradise indoor care getting it to bloom',
  'Hoya carnosa care trailing plant guide',
  'Pilea peperomioides propagation sharing pups',
  'Anthurium care guide blooming tips',
  'Croton plant light requirements color guide',
  'Ficus audrey vs fiddle leaf fig comparison',
  'Indoor plant pest identification chart guide',
  'Drainage layer myth do indoor pots need rocks',
  'Self watering pots pros and cons for houseplants',
  'Neem oil for houseplants safe usage guide',
  'Bottom watering vs top watering which is better'
][Math.floor(Math.random()*30)]}"""

EXPANDED_TOPICS_WF2 = """return {selectedTopic: [
  'Best indoor plants for Dubai apartments hot climate',
  'AC safe houseplants that survive air conditioning UAE',
  'Desert rose adenium care guide for UAE gardens',
  'Indoor herb growing in UAE kitchen apartments',
  'Snake plant benefits for UAE bedrooms air quality',
  'Money tree pachira aquatica feng shui UAE homes',
  'ZZ plant perfect office plant for Dubai',
  'Pothos golden devil ivy balcony UAE shade plant',
  'Bougainvillea care Dubai garden pruning guide',
  'Indoor plant delivery services UAE comparison',
  'Jasmine growing guide Arabian jasmine UAE balcony',
  'Date palm indoor miniature varieties UAE homes',
  'Aloe vera growing UAE medicinal uses skincare',
  'Succulent arrangements for UAE tabletops gift ideas',
  'Monstera deliciosa thriving in UAE apartments'
][Math.floor(Math.random()*15)]}"""

EXPANDED_TOPICS_WF3 = """return {selectedTopic: [
  'Best professional grow light systems for indoor gardens review',
  'Premium aroid soil mix recipe professional growers use',
  'Rare monstera varieties collectors guide Thai constellation vs albo',
  'Professional greenhouse setup for apartment balcony',
  'High end self watering planter systems comparison review',
  'Tissue culture plants buying guide for collectors',
  'Professional humidity control system for plant rooms',
  'Rare philodendron species investment guide 2026',
  'Premium fertilizer comparison for tropical houseplants',
  'Professional plant propagation station setup guide',
  'Best terrarium kits for bioactive setups premium review',
  'Rare alocasia species collectors growing guide',
  'Professional pest management IPM for indoor gardens',
  'Premium moss pole systems for climbing aroids comparison',
  'High end plant monitoring systems smart sensors review'
][Math.floor(Math.random()*15)]}"""

TOPIC_UPDATES = {
    'CpyU2cf01DdtpfWo': ('Select Topic', EXPANDED_TOPICS_WF1),
    'UKegbNpPIBkkNUrd': ('Select UAE Topic', EXPANDED_TOPICS_WF2),
    'SLgAkWAL2NBVzZ7U': ('Select High-Ticket', EXPANDED_TOPICS_WF3),
}

for wf_id, config in SCHEDULE_UPDATES.items():
    print(f"--- Updating: {config['name']} ---")
    
    wf_out = run(f'curl -s -b /tmp/n8n_session.txt http://localhost:5678/rest/workflows/{wf_id}')
    wf_data = json.loads(wf_out).get('data', {})
    
    for node in wf_data.get('nodes', []):
        # Update schedule trigger
        if 'scheduleTrigger' in node['type']:
            node['parameters'] = {
                "rule": {
                    "interval": [
                        {
                            "field": "cronExpression",
                            "expression": config['cron']
                        }
                    ]
                }
            }
            print(f"  Schedule: {config['cron']} (3x daily)")
        
        # Update topic selector
        if wf_id in TOPIC_UPDATES:
            topic_node_name, new_code = TOPIC_UPDATES[wf_id]
            if node['name'] == topic_node_name and node['type'] == 'n8n-nodes-base.code':
                node['parameters']['jsCode'] = new_code
                print(f"  Topics: expanded to 15-30 unique topics")
    
    # Save
    update_payload = json.dumps({"nodes": wf_data['nodes']})
    sftp = ssh.open_sftp()
    with sftp.open(f'/tmp/wf_sched_{wf_id}.json', 'w') as f:
        f.write(update_payload)
    sftp.close()
    
    result = run(f'curl -s -b /tmp/n8n_session.txt -X PATCH http://localhost:5678/rest/workflows/{wf_id} -H "Content-Type: application/json" -d @/tmp/wf_sched_{wf_id}.json')
    if '"updatedAt"' in result:
        print(f"  SAVED!\n")
    else:
        print(f"  Error: {result[:150]}\n")

# Deactivate and reactivate all 3 to reset their cron timers
print("Restarting workflows to apply new schedules...")
for wf_id in SCHEDULE_UPDATES:
    run(f'curl -s -b /tmp/n8n_session.txt -X POST http://localhost:5678/rest/workflows/{wf_id}/deactivate')
    run(f'curl -s -b /tmp/n8n_session.txt -X POST http://localhost:5678/rest/workflows/{wf_id}/activate')
    print(f"  Restarted: {SCHEDULE_UPDATES[wf_id]['name']}")

ssh.close()

print(f"""
{'='*60}
SCHEDULE UPDATE COMPLETE!
{'='*60}

New daily output:
  WF1 (US Trend Jacker):    3 articles/day (08:00, 14:00, 20:00 UTC)
  WF2 (UAE Amazon Market):  3 articles/day (06:00, 12:00, 18:00 UTC)
  WF3 (High-Ticket Funnel): 3 articles/day (07:00, 13:00, 19:00 UTC)
  ─────────────────────────────────────────────
  TOTAL:                    9 articles per day!

Topic pools expanded to 15-30 unique topics per workflow.
Next execution: within the next few hours based on new cron.
""")
