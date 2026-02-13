import platform
import psutil

# Só importa o pynvml se o sistema for Windows
if platform.system() == "Windows":
    try:
        import pynvml
    except ImportError:
        pynvml = None
else:
    pynvml = None

def getCpuUsage():
    return psutil.cpu_percent(interval=1)

def getRamUsage():
    return psutil.virtual_memory().percent

def getGpuUsage():
    # Se não for Windows, retorna N/A e para.
    if platform.system() != "Windows" or pynvml is None:
        return {"usage": "N/A", "temp": "N/A"}
    try:
        pynvml.nvmlInit()
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
        temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
        pynvml.nvmlShutdown()
        return {"usage": f"{utilization.gpu}%", "temp": f"{temp}°C"}
    except Exception:
        return {"usage": "N/A", "temp": "N/A"}
