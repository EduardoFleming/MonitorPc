import sys
import subprocess
import importlib.util
import platform
import os
import time
import threading
import socket
import webview 

# --- VERIFICAÇÃO DE DEPENDÊNCIAS ---
required_libraries = {
    "streamlit": "streamlit",
    "psutil": "psutil",
    "google-generativeai": "google.generativeai",
    "pywebview": "webview"
}

if platform.system() == "Windows":
    required_libraries["wmi"] = "wmi"
    required_libraries["pywin32"] = "win32com"
    required_libraries["nvidia-ml-py"] = "pynvml"

print("🔍 Verificando dependências...")
for pip_name, import_name in required_libraries.items():
    if importlib.util.find_spec(import_name) is None:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name])
        except:
            pass

SCRIPT_NAME = "main.py"

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def run_streamlit_background(port):
    file_path = os.path.join(os.path.dirname(__file__), SCRIPT_NAME)
    cmd = [
        sys.executable, "-m", "streamlit", "run", file_path,
        "--server.headless=true", f"--server.port={port}"
    ]
    subprocess.run(cmd)

def main():
    porta_dinamica = get_free_port()
    t = threading.Thread(target=run_streamlit_background, args=(porta_dinamica,))
    t.daemon = True 
    t.start()
    time.sleep(3)

    try:
        webview.create_window("Monitor PC", f"http://localhost:{porta_dinamica}", width=1000, height=800)
        webview.start()
    except Exception as e:
        print(f"Erro: {e}")
    sys.exit()

if __name__ == "__main__":
    main()