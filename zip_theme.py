import os
import zipfile

def create_wp_zip(source_dir, zip_name):
    if os.path.exists(zip_name):
        os.remove(zip_name)
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # We need to make sure the root folder inside the zip matches the plugin/theme name
        root_folder_name = os.path.basename(os.path.normpath(source_dir))
        
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Get relative path inside the folder
                rel_path = os.path.relpath(file_path, source_dir)
                
                # Prepend the root folder name to make it WordPress compatible
                arcname = f"{root_folder_name}/{rel_path}"
                
                # Force forward slashes for WordPress upload!
                arcname = arcname.replace("\\", "/") 
                
                zipf.write(file_path, arcname)
    
    print(f"Created {zip_name} successfully with forward slashes.")

# Create Theme Zip
create_wp_zip('plantsmag-premium', 'plantsmag-premium_v8.zip')

# Create Plugin Zip
create_wp_zip(os.path.join('plugins', 'plantsmag-tools'), 'plantsmag-tools_v8.zip')

print("All done!")
