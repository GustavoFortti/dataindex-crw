import os
import pandas as pd
import subprocess
import shutil

def data_ingestion(conf):
    global CONF
    CONF = conf

    file_path = CONF['data_path']

    images_path = file_path + "/img_csl/"
    dataindex_img_path = os.getenv('DATAINDEX_IMG_PATH')
    images_server_path = dataindex_img_path + "/imgs"

    if not os.path.exists(images_server_path):
        os.makedirs(images_server_path)

    for file_name in os.listdir(images_path):
        source_file = os.path.join(images_path, file_name)
        
        if os.path.isfile(source_file):
            destination_file = os.path.join(images_server_path, file_name)
            shutil.copy(source_file, destination_file)
    
    execute_git_commands(dataindex_img_path)

    # https://raw.githubusercontent.com/GustavoFortti/dataindex-img/master/imgs/04ba683b.webp

def execute_git_commands(dataindex_img_path):
    # Change to the repository directory
    os.chdir(dataindex_img_path)

    try:
        # Stage all modified files
        subprocess.run(['git', 'add', '.'], check=True)
        
        # Check if there are changes to commit
        status_result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
        if status_result.stdout.strip():  # If there's output, there are changes to commit
            # Commit the changes
            subprocess.run(['git', 'commit', '-m', 'Automated commit from data ingestion script'], check=True)
            
            # Push the changes to the remote repository, setting upstream if necessary
            push_result = subprocess.run(['git', 'push'], stderr=subprocess.PIPE, text=True)
            if "no upstream" in push_result.stderr:
                print("Setting upstream branch...")
                subprocess.run(['git', 'push', '--set-upstream', 'origin', 'master'], check=True)
        else:
            print("No changes to commit.")
        
        print("Changes successfully committed and pushed.")
        
    except subprocess.CalledProcessError as e:
        print(f"Error executing git commands: {e}")