import platform
import cpuinfo
import psutil

# Só importa o WMI se o sistema for Windows
if platform.system() == "Windows":
    import wmi
    import pythoncom

def getCpuInfo():
    try:
        info = cpuinfo.get_cpu_info()
        return info.get('brand_raw', "Não disponível")
    except Exception:
        return "Erro ao obter CPU"

def getGpuInfo():
    # Se não for Windows, retorna a mensagem e para.
    if platform.system() != "Windows":
        return "Disponível apenas no Windows"
    try:
        pythoncom.CoInitialize()
        c = wmi.WMI()
        gpuInfo = c.Win32_VideoController()
        
        if not gpuInfo:
            return "Nenhuma GPU encontrada"
        
        # --- LÓGICA DE PRIORIDADE ---
        # 1. Procura especificamente por NVIDIA
        for gpu in gpuInfo:
            if "NVIDIA" in gpu.Name.upper():
                return gpu.Name
        
        # 2. Se não achar NVIDIA, procura por AMD (Dedicada)
        # (Evita pegar gráficos integrados genéricos se tiver uma dedicada)
        for gpu in gpuInfo:
            if "AMD" in gpu.Name.upper() and "GRAPHICS" not in gpu.Name.upper():
                 return gpu.Name

        # 3. Se não tiver preferência, retorna a primeira da lista
        return gpuInfo[0].Name

    except Exception:
        return "Erro ao obter GPU"

def getMotherboardInfo():
    # Se não for Windows, retorna a mensagem e para.
    if platform.system() != "Windows":
        return "Disponível apenas no Windows"
    try:
        pythoncom.CoInitialize()
        c = wmi.WMI()
        board_info = c.Win32_BaseBoard()[0]
        return f"{board_info.Manufacturer} {board_info.Product}"
    except Exception:
        return "Erro ao obter Placa-Mãe"

def getRamInfo():
    try:
        totalRamGb = psutil.virtual_memory().total / (1024**3)
        return f"{totalRamGb:.2f} GB"
    except Exception:
        return "Erro ao obter RAM"

def getDiskInfo():
    try:
        partitions = psutil.disk_partitions()
        diskInfo = []
        for p in partitions:
            try:
                usage = psutil.disk_usage(p.mountpoint)
                total = usage.total / (1024**3)
                used = usage.used / (1024**3)
                diskStr = (f"Disco {p.device} - Total: {total:.2f} GB | Usado: {used:.2f} GB ({usage.percent}%)")
                diskInfo.append(diskStr)
            except PermissionError:
                continue # Pula discos que o Windows bloqueou acesso
        return diskInfo
    except Exception:
        return ["Erro ao obter informações de disco"]
