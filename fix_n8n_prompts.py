import json
import glob
import re

files = glob.glob('d:/project/plantsmag/workflow_*.json')

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    modified = False
    for node in data.get('nodes', []):
        if 'gemini' in node.get('name', '').lower() and 'httpRequest' in node.get('type', ''):
            if 'parameters' in node and 'body' in node['parameters']:
                body_text = node['parameters']['body']
                
                # Apply replacements to kill the AI footprint
                new_body = body_text.replace('EXACTLY 2500 words', '800-1200 highly useful, concise words. DO NOT produce fluff. Google penalizes fluff.')
                new_body = new_body.replace('5 H2 sections (350 words each)', 'H2 sections (only as many as needed, max 150 words each, no fluff)')
                new_body = new_body.replace('Intro (180 words)', 'Intro (max 60 words)')
                new_body = new_body.replace('Conclusion (120 words)', 'Conclusion (max 60 words)')
                new_body = new_body.replace('Conclusion (150 words)', 'Conclusion (max 60 words)')
                
                if new_body != body_text:
                    node['parameters']['body'] = new_body
                    modified = True
                    
    if modified:
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Fixed AI footprint in: {file}")

print("All workflows updated!")
