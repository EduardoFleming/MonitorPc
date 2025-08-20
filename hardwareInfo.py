import cpuinfo
import psutil
import wmi
import pythoncom

def getCpuInfo():
    try:
        info = cpuinfo.get_cpu_info()
        return info.get('brand_raw', "Não disponível")
    except Exception as e:
        print(f"Erro em getCpuInfo: {e}")
        return "Erro ao obter CPU"

def getGpuInfo():
    try:
        pythoncom.CoInitialize() 
        
        c = wmi.WMI()
        gpuInfo = c.Win32_VideoController()

        if gpuInfo:
            return gpuInfo[0].Name
        else:
            return "Nenhuma GPU encontrada"
    except Exception as e:
        print(f"Erro ao buscar info da GPU: {e}")
        return "Não foi possível obter informação"

def getMotherboardInfo():
    try:
        pythoncom.CoInitialize() 
        
        c = wmi.WMI()
        board_info = c.Win32_BaseBoard()[0]
        
        manufacturer = board_info.Manufacturer
        product = board_info.Product
        
        return f"{manufacturer} {product}"
    except Exception as e:
        print(f"Erro ao buscar info da Placa-Mãe: {e}")
        return "Não foi possível obter informação"

def getRamInfo():
    try:
        totalRamBytes = psutil.virtual_memory().total
        totalRamGb = totalRamBytes / (1024**3)
        return f"{totalRamGb:.2f} GB"
    except Exception as e:
        print(f"Erro em getRamInfo: {e}")
        return "Não foi possível obter informação"

def getDiskInfo():
    diskInfo = []
    try:
        partitions = psutil.disk_partitions()
        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                total = usage.total / (1024**3)
                used = usage.used / (1024**3)
                diskStr = (
                    f"Disco {partition.device} - Total: {total:.2f} GB "
                    f"| Usado: {used:.2f} GB ({usage.percent}%)"
                )
                diskInfo.append(diskStr)
            except PermissionError:
                continue
        return diskInfo
    except Exception as e:
        print(f"Erro ao buscar info de Disco: {e}")
        return ["Não foi possível obter informação"]