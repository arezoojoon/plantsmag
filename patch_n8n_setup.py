import re

file_path = 'd:/project/plantsmag/setup_n8n_complete.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all instances of 2500-word fluff with concise 800-1200 word prompt
content = re.sub(
    r'Write a 2500-word',
    'Write a concise 800-1200 word (no fluff)',
    content
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated setup_n8n_complete.py with shorter, fluff-free prompts.")
