import os
import subprocess
import time

from .env import (ELASTICSEARCH_CONF as es_conf, 
                  GIT_CONF as git_conf,
                  LOCAL)


def configure_display():
    display_values = [":0", ":1", ":0.0"]
    chrome_command = "/usr/local/bin/chrome"

    for display in display_values:
        print(f"Testing DISPLAY={display}")
        os.environ["DISPLAY"] = display
        process = subprocess.Popen([chrome_command, "--no-sandbox", "--disable-gpu", "--dump-dom", "about:blank"],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        time.sleep(2)

        try:
            process.poll()
            if process.returncode is None:
                print(f"Chrome started successfully with DISPLAY={display}")
                process.terminate()
                return True
            else:
                print(f"Failed to start Chrome with DISPLAY={display}")
        except Exception as e:
            print(f"Failed to start Chrome with DISPLAY={display} due to an error: {e}")

    print("Failed to configure DISPLAY for Chrome")
    return False

def configure_elasticsearch(env):
    if env == "dev":
        os.environ['ES_HOSTS'] = es_conf["hosts_dev"]
        os.environ['ES_USER'] = es_conf["user_dev"]
        os.environ['ES_PASS'] = es_conf["password_dev"]
    else:
        os.environ['ES_HOSTS'] = es_conf["hosts_prd"]
        os.environ['ES_USER'] = es_conf["user_prd"]
        os.environ['ES_PASS'] = es_conf["password_prd"]

def configure_images_path():
    os.environ['DATAINDEX_IMG_PATH'] = os.path.join(LOCAL, '..', 'dataindex-img')
    os.environ['DATAINDEX_IMG_URL'] = git_conf["dataindex_img_url"]

    img_path = os.environ.get('DATAINDEX_IMG_PATH')
    if os.path.isdir(img_path):
        print(f"{img_path} Ok")
    else:
        clone_repository(git_conf["remote_url"])
        setup_git_config(img_path, git_conf['username'], git_conf['email'], git_conf['remote_name'], git_conf['remote_url'])

def clone_repository(remote_url):
    try:
        original_dir = os.getcwd()

        os.chdir(LOCAL + "/..")
        subprocess.check_call(['git', 'clone', remote_url])

        print(f"Repositório clonado em {LOCAL}")

    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando Git: {e}")
    except Exception as e:
        print(f"Erro ao clonar o repositório: {e}")
    finally:
        os.chdir(original_dir)

def setup_git_config(project_dir, username, email, remote_name, remote_url):
    try:
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)

        original_dir = os.getcwd()
        os.chdir(project_dir)

        subprocess.check_call(['git', 'config', 'init.defaultBranch', 'master'])
        subprocess.check_call(['git', 'config', 'user.name', username])
        subprocess.check_call(['git', 'config', 'user.email', email])

        remote_check = subprocess.check_output(['git', 'remote']).decode('utf-8').strip()
        if remote_name not in remote_check.split():
            subprocess.check_call(['git', 'remote', 'add', remote_name, remote_url])
        else:
            print(f"Remote '{remote_name}' already exists.")

        print("Git user configuration and remote added successfully.")
        
        subprocess.check_call(['git', 'pull', remote_name, 'master'])

    except subprocess.CalledProcessError as e:
        print(f"Error executing Git command: {e}")
    except Exception as e:
        print(f"Error creating the directory: {e}")
    finally:
        os.chdir(original_dir)

def configure_env(args):

    job_type = args.job_type
    if (job_type == "extract"):
        configure_display()
    
    configure_elasticsearch(args.mode)
    configure_images_path()