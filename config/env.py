import os
import subprocess
import time

LOCAL = os.getenv("LOCAL")

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
        os.environ['ES_HOSTS'] = "http://192.168.0.102:9200"
        os.environ['ES_USER'] = "elastic"
        os.environ['ES_PASS'] = "123456"
    else:
        os.environ['ES_HOSTS'] = "https://dataindex-elk-1.ngrok.app/"
        os.environ['ES_USER'] = "elastic"
        os.environ['ES_PASS'] = "RJ6XXwfjHzYICKfGRTSn"

def configure_images_path():
    os.environ['DATAINDEX_IMG_PATH'] = os.path.join(LOCAL, '..', 'dataindex-img')
    os.environ['DATAINDEX_IMG_URL'] = "https://raw.githubusercontent.com/GustavoFortti/dataindex-img/master/imgs/"

    img_path = os.environ.get('DATAINDEX_IMG_PATH')
    if os.path.isdir(img_path):
        print(f"{img_path} Ok")
    else:
        print(f"Error: path does not exist {img_path}")

def configure_env(args):

    job_type = args.job_type
    if (job_type == "extract"):
        configure_display()
    
    configure_elasticsearch(args.mode)
    configure_images_path()