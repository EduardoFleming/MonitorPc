import sys
import subprocess
import importlib.util
import platform
import os
import time
import threading
import socket

# ==========================================
# 1. VERIFICAÇÃO E INSTALAÇÃO
# ==========================================
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
        print(f"📦 Instalando {pip_name}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name])
            print(f"✅ {pip_name} instalado!")
        except Exception as e:
            print(f"❌ Erro ao instalar {pip_name}: {e}")

# ==========================================
# 2. IMPORTAÇÃO NA THREAD PRINCIPAL
# ==========================================
import webview 

# ==========================================
# 3. FUNÇÕES DO SISTEMA
# ==========================================
SCRIPT_NAME = "main.py"

def get_free_port():
    """Pede ao sistema operacional uma porta de rede livre."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def run_streamlit_background(port):
    """Roda o servidor do Streamlit."""
    file_path = os.path.join(os.path.dirname(__file__), SCRIPT_NAME)
    cmd = [
        sys.executable, "-m", "streamlit", "run", file_path,
        "--server.headless=true", 
        f"--server.port={port}"
    ]
    subprocess.run(cmd)

def main():
    print("\n🚀 Iniciando Sistema...")

    porta_dinamica = get_free_port()
    print(f"🔌 Porta alocada: {porta_dinamica}")

    # Inicia o Streamlit em segundo plano
    t = threading.Thread(target=run_streamlit_background, args=(porta_dinamica,))
    t.daemon = True 
    t.start()

    # Dá tempo para o Streamlit ligar
    time.sleep(3)

    # Inicia a Janela
    try:
        webview.create_window(
            "Monitor PC", 
            f"http://localhost:{porta_dinamica}",
            width=1000, 
            height=800,
            text_select=True 
        )
        webview.start()
    except Exception as e:
        print(f"❌ Erro ao abrir janela: {e}")

    print("👋 Encerrando aplicação...")
    sys.exit()

if __name__ == "__main__":
    main()