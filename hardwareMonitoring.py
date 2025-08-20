import psutil
try:
    import pynvml
except ImportError:
    pynvml = None

def getCpuUsage():
    return psutil.cpu_percent(interval=1)

def getRamUsage():
    """Retorna a porcentagem de uso atual da RAM."""
    return psutil.virtual_memory().percent

def getGpuUsage():
    if pynvml is None:
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