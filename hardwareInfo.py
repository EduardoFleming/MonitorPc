import platform
import psutil # Excelente para leitura dos discos

# Só importa o WMI se o sistema for Windows
if platform.system() == "Windows":
    import wmi
    import pythoncom

def getCpuInfo():
    if platform.system() != "Windows":
        return "Disponível apenas no Windows"
    try:
        pythoncom.CoInitialize()
        c = wmi.WMI()
        processador = c.Win32_Processor()[0].Name.strip()
        return processador
    except Exception:
        return "Erro ao obter CPU"

def getGpuInfo():
    if platform.system() != "Windows":
        return "Disponível apenas no Windows"
    try:
        pythoncom.CoInitialize()
        c = wmi.WMI()
        gpuInfo = c.Win32_VideoController()
        
        if not gpuInfo:
            return "Nenhuma GPU encontrada"
        
        # --- LÓGICA DE PRIORIDADE ---
        for gpu in gpuInfo:
            if "NVIDIA" in gpu.Name.upper():
                return gpu.Name
                
        for gpu in gpuInfo:
            if "AMD" in gpu.Name.upper() and "GRAPHICS" not in gpu.Name.upper():
                 return gpu.Name

        return gpuInfo[0].Name
    except Exception:
        return "Erro ao obter GPU"

def getMotherboardInfo():
    if platform.system() != "Windows":
        return "Disponível apenas no Windows"
    try:
        pythoncom.CoInitialize()
        c = wmi.WMI()
        # Win32_BaseBoard é a exata chave que o msinfo32 usa para "Produto BaseBoard"
        board_info = c.Win32_BaseBoard()[0]
        
        fabricante = board_info.Manufacturer.strip()
        produto = board_info.Product.strip()
        
        if produto.upper().startswith(fabricante.upper()):
            return produto
        else:
            return f"{fabricante} {produto}"
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
                continue 
        return diskInfo
    except Exception:
        return ["Erro ao obter informações de disco"]
