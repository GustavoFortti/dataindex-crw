import os
import subprocess

from src.lib.utils.log import message

LOCAL = os.getenv('LOCAL')

GIT_CONF = {
    "username": "Gustavo Fortti",
    "email": "gustavofortti@gmail.com",
    "remote_name": "origin",
    "remote_url": "https://github.com/GustavoFortti/dataindex-img.git",
    "dataindex_img_url": "https://raw.githubusercontent.com/GustavoFortti/dataindex-img/master/imgs/"
}


def configure_image_server():
    os.environ['DATAINDEX_IMG_PATH'] = os.path.join(LOCAL, '..', 'image-server')
    os.environ['DATAINDEX_IMG_URL'] = GIT_CONF["dataindex_img_url"]

    img_path = os.environ.get('DATAINDEX_IMG_PATH')
    if os.path.isdir(img_path):
        message(f"{img_path} Ok")
    else:
        clone_repository(GIT_CONF["remote_url"])
        setup_git_config(img_path, GIT_CONF['username'], GIT_CONF['email'], GIT_CONF['remote_name'], GIT_CONF['remote_url'])


def clone_repository(remote_url):
    try:
        original_dir = os.getcwd()

        os.chdir(LOCAL + "/..")
        subprocess.check_call(['git', 'clone', remote_url])

        message(f"Repositório clonado em {LOCAL}")

    except subprocess.CalledProcessError as e:
        message(f"Erro ao executar o comando Git: {e}")
    except Exception as e:
        message(f"Erro ao clonar o repositório: {e}")
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
            message(f"Remote '{remote_name}' already exists.")

        message("Git user configuration and remote added successfully.")
        
        subprocess.check_call(['git', 'pull', remote_name, 'master'])

    except subprocess.CalledProcessError as e:
        message(f"Error executing Git command: {e}")
    except Exception as e:
        message(f"Error creating the directory: {e}")
    finally:
        os.chdir(original_dir)
