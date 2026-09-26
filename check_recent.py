import json
try:
    with open('d:/project/plantsmag/recent_execs.json', encoding='utf-8') as f:
        d = json.load(f)
    execs = d.get('data', {}).get('results', [])
    for e in execs:
        print(f"WF: {e.get('workflowName')} | Status: {e.get('status')} | Time: {e.get('startedAt')}")
except Exception as e:
    print(f"Error: {e}")
