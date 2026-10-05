import platform

import psutil

try:
    import pynvml
except ImportError:
    pynvml = None

# A primeira leitura do Psutil serve apenas para inicializar o contador.
psutil.cpu_percent(interval=None)
_nvml_handle = None
_nvml_error = None


def getCpuUsage():
    return psutil.cpu_percent(interval=None)


def getRamUsage():
    memory = psutil.virtual_memory()
    return {"percent": memory.percent, "used_gb": round(memory.used / (1024**3), 2)}


def getGpuUsage():
    global _nvml_handle, _nvml_error
    if pynvml is None:
        return {"usage": None, "temp": None, "name": None, "note": "GPU não suportada por este provedor"}
    try:
        if _nvml_handle is None and _nvml_error is None:
            pynvml.nvmlInit()
            _nvml_handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        if _nvml_error:
            raise RuntimeError(_nvml_error)
        name = pynvml.nvmlDeviceGetName(_nvml_handle)
        if isinstance(name, bytes):
            name = name.decode(errors="replace")
        utilization = pynvml.nvmlDeviceGetUtilizationRates(_nvml_handle)
        try:
            temperature = pynvml.nvmlDeviceGetTemperature(_nvml_handle, pynvml.NVML_TEMPERATURE_GPU)
        except Exception:
            temperature = None
        return {
            "usage": utilization.gpu,
            "temp": temperature,
            "name": name,
            "note": None,
        }
    except Exception as error:
        _nvml_error = str(error)
        return {"usage": None, "temp": None, "name": None, "note": str(error)}


def getPlatformNote():
    if platform.system() != "Windows":
        return "Uso de CPU, memória e discos disponível. Sensores de GPU variam por sistema e fabricante."
    if pynvml is None:
        return "Uso de CPU e memória disponível. Métricas da GPU exigem NVIDIA NVML e driver compatível."
    return None
