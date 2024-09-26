import os
import shutil
import subprocess

def image_ingestion(df, conf):
    global CONF
    CONF = conf

    file_path = CONF['data_path']

    images_path = file_path + "/img_csl/"
    dataindex_img_path = os.getenv('DATAINDEX_IMG_PATH')
    images_server_path = dataindex_img_path + "/imgs"

    git_pull(dataindex_img_path)

    if not os.path.exists(images_server_path):
        os.makedirs(images_server_path)

    files = os.listdir(images_path)
    for file_name in files:
        source_file = os.path.join(images_path, file_name)
        
        if os.path.isfile(source_file):
            destination_file = os.path.join(images_server_path, file_name)
            shutil.copy(source_file, destination_file)
    
    git_push(dataindex_img_path)

    url = os.getenv('DATAINDEX_IMG_URL')
    refs = {file.split(".")[0]: url + file for file in files}

    print("Successfully image ingestion")
    df['image_url_srv'] = df['ref'].map(refs)

    return df

def git_pull(project_dir):
    try:
        original_dir = os.getcwd()
        os.chdir(project_dir)

        subprocess.check_call(['git', 'checkout', '.'])
        subprocess.check_call(['git', 'pull'])

        print("Successful pull.")

    except subprocess.CalledProcessError as e:
        print(f"Error when running Git command: {e}")
    except Exception as e:
        print(f"Error pulling from repository: {e}")
    finally:
        os.chdir(original_dir)

def git_push(project_dir):
    original_dir = os.getcwd()
    
    try:
        os.chdir(project_dir)
        
        if os.system('git add .') != 0:
            print("Error staging files.")
            return

        if os.system('git diff --cached --exit-code') == 0:
            print("No changes to commit.")
            return

        if os.system('git commit -m "Automated commit from data ingestion script"') != 0:
            print("Error committing changes.")
            return

        push_result = os.system('git push')
        if push_result != 0:
            print("Error pushing changes, trying to set upstream...")
            if os.system('git push --set-upstream origin master') != 0:
                print("Error setting upstream and pushing changes.")
                return

        print("Changes successfully committed and pushed.")
    
    finally:
        os.chdir(original_dir)