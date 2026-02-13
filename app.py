import sys
import subprocess
import importlib.util
import platform
import os
import time
import threading

# --- CONFIGURAÇÃO ---
SCRIPT_NAME = "main.py"

# Lista de bibliotecas necessárias
required_libraries = {
    "streamlit": "streamlit",
    "psutil": "psutil",
    "py-cpuinfo": "cpuinfo",
    "google-generativeai": "google.generativeai",
    "pywebview": "webview"
}

if platform.system() == "Windows":
    required_libraries["wmi"] = "wmi"
    required_libraries["pywin32"] = "win32com"
    required_libraries["nvidia-ml-py"] = "pynvml"

# --- FUNÇÕES DE INSTALAÇÃO ---
def is_installed(package_import_name):
    try:
        return importlib.util.find_spec(package_import_name) is not None
    except ImportError:
        return False

def install_package(package_pip_name):
    print(f"📦 Instalando {package_pip_name}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_pip_name])
        print(f"✅ {package_pip_name} instalado!")
    except subprocess.CalledProcessError:
        print(f"❌ Erro ao instalar {package_pip_name}.")

# --- FUNÇÃO PARA RODAR O STREAMLIT EM SEGUNDO PLANO ---
def run_streamlit_background():
    """Roda o servidor do Streamlit sem abrir o navegador."""
    file_path = os.path.join(os.path.dirname(__file__), SCRIPT_NAME)
    
    # Comando: streamlit run main.py --server.headless=true --server.port=8501
    cmd = [
        sys.executable, "-m", "streamlit", "run", file_path,
        "--server.headless=true", # Não abre o navegador
    ]
    # Inicia o processo
    subprocess.run(cmd)

# --- FLUXO PRINCIPAL ---
def main():
    print("🔍 Verificando dependências...")
    
    # 1. Instalação Automática
    for pip_name, import_name in required_libraries.items():
        if not is_installed(import_name):
            install_package(pip_name)
    
    print("\n🚀 Iniciando Sistema...")

    # 2. Inicia o Streamlit em uma Thread separada (para não travar o código)
    t = threading.Thread(target=run_streamlit_background)
    t.daemon = True # Garante que fecha quando o programa fechar
    t.start()

    # 3. Pequena pausa para garantir que o servidor subiu
    time.sleep(3)

    # 4. Inicia a Janela (PyWebview)
    try:
        import webview
        
        # Cria a janela
        webview.create_window(
            "Monitor de Hardware & IA", 
            f"http://localhost:8501",
            width=1000, 
            height=800,
            text_select=True # Permite selecionar/copiar texto
        )
        webview.start()
        
    except ImportError:
        print("❌ Erro crítico: A biblioteca 'pywebview' não foi carregada corretamente.")
    except Exception as e:
        print(f"❌ Erro ao abrir janela: {e}")

    # Quando fechar a janela, o script encerra
    print("👋 Encerrando aplicação...")
    sys.exit()

if __name__ == "__main__":
    main()