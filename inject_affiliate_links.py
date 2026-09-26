import subprocess
import re

# High Payout Link
LECHUZA_LINK = "https://amzn.to/4tll8BC"
# Volume Payout Link
QRRICA_LINK = "https://amzn.to/4exPwoG"

box_a_html = f"""<div class="pm-affiliate-box" style="border: 2px solid #2ecc71; padding: 20px; border-radius: 8px; margin: 20px 0; background-color: #f9f9f9;">
    <h3 style="margin-top: 0; color: #2ecc71;">🌱 Top Recommended Plant Gear</h3>
    <p>Ensure your plants never dry out. We highly recommend the <strong><a href="{LECHUZA_LINK}" target="_blank" rel="nofollow noopener" style="color: #e67e22; font-weight: bold;">LECHUZA Self Watering Plant Pot CLASSICO</a></strong> for ultimate moisture control and professional aesthetic.</p>
    <a href="{LECHUZA_LINK}" target="_blank" rel="nofollow noopener" style="display: inline-block; background: #f39c12; color: #fff; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">Check Price on Amazon</a>
</div>"""

box_b_html = f"""<div class="pm-affiliate-box" style="border: 2px solid #2ecc71; padding: 20px; border-radius: 8px; margin: 20px 0; background-color: #f9f9f9;">
    <h3 style="margin-top: 0; color: #2ecc71;">🌱 Great Value Plant Gear</h3>
    <p>Need multiple pots for your growing collection? We recommend the <strong><a href="{QRRICA_LINK}" target="_blank" rel="nofollow noopener" style="color: #e67e22; font-weight: bold;">QRRICA Self Watering Pots (Set of 5)</a></strong>. Excellent value and reliable drainage.</p>
    <a href="{QRRICA_LINK}" target="_blank" rel="nofollow noopener" style="display: inline-block; background: #f39c12; color: #fff; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">Check Price on Amazon</a>
</div>"""

posts = {
    784: box_a_html, # Bioactive Terrariums (Important/Newest) -> High Payout
    782: box_a_html, # Tissue Culture (Important/Newest) -> High Payout
    780: box_a_html, # Fungus Gnats -> High Payout
    774: box_b_html, # Goth Plants -> Value
    772: box_b_html, # Ficus Audrey -> Value
    770: box_b_html  # Hydroponics -> Value
}

ssh_base = 'ssh -p 65002 u284669846@187.124.245.99 "wp --path=/home/u284669846/domains/plantsmag.com/public_html'

for post_id, affiliate_html in posts.items():
    print(f"Processing Post ID {post_id}...")
    
    # Get Content
    cmd_get = f'{ssh_base} post get {post_id} --field=post_content"'
    res = subprocess.run(cmd_get, shell=True, capture_output=True, text=True)
    
    if res.returncode != 0:
        print(f"Error getting post {post_id}: {res.stderr}")
        continue
        
    content = res.stdout
    
    # Replace existing pm-affiliate-box div
    # Uses regex to match <div class="pm-affiliate-box">...</div>
    new_content = re.sub(r'<div[^>]*class="pm-affiliate-box"[^>]*>.*?</div>', affiliate_html, content, flags=re.DOTALL)
    
    # If no pm-affiliate-box was found, append it to the end before the last closing tag (or just append)
    if new_content == content:
        print("No pm-affiliate-box found, appending to end of article.")
        new_content = content + "\n" + affiliate_html
        
    # Write to local temp file to safely transfer
    local_file = f"tmp_content_{post_id}.txt"
    with open(local_file, "w", encoding="utf-8") as f:
        f.write(new_content)
        
    # Upload via SCP
    remote_file = f"/home/u284669846/domains/plantsmag.com/public_html/tmp_upload/tmp_content_{post_id}.txt"
    subprocess.run(f'scp -P 65002 {local_file} u284669846@187.124.245.99:{remote_file}', shell=True)
    
    # Update post
    cmd_update = f'{ssh_base} post update {post_id} {remote_file}"'
    res_update = subprocess.run(cmd_update, shell=True, capture_output=True, text=True)
    if res_update.returncode == 0:
        print(f"Successfully updated post {post_id}")
    else:
        print(f"Failed to update post {post_id}: {res_update.stderr}")
        
    # Cleanup
    subprocess.run(f'{ssh_base} --eval=\\"unlink(\'{remote_file}\');\\""', shell=True)
    import os
    if os.path.exists(local_file):
        os.remove(local_file)

print("Flushing cache...")
subprocess.run(f'{ssh_base} cache flush"', shell=True)
subprocess.run(f'{ssh_base} litespeed-purge all"', shell=True)
print("Done!")
