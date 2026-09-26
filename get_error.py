import json
with open('d:/project/plantsmag/exec46.json', encoding='utf-8') as f:
    d = json.load(f)

# N8N's /rest/executions/{id} wraps the execution data in d['data']
# but sometimes that might be stringified? Let's check type.
exec_data = d.get('data', {})
if isinstance(exec_data, str):
    exec_data = json.loads(exec_data)

rd = exec_data.get('data', {}).get('resultData', {}).get('runData', {})
found_error = False
for k, v in rd.items():
    if v and isinstance(v, list) and v[0].get('error'):
        print(f"Node: {k}")
        print(f"Error: {v[0]['error'].get('message', '')}")
        found_error = True

if not found_error:
    print("No error found in runData. Full execution data keys:", exec_data.keys())
    if 'data' in exec_data:
        print("exec_data['data'] keys:", exec_data['data'].keys())
