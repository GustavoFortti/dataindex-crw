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

def configure_env():
    configure_display()