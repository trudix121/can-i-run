import psutil
import subprocess
from pynvml import *
import re
import torch
import platform
def get_size(bytes=0):
    return round(bytes / (1024 ** 3), 2)

def get_gpu_memory():
    total_memory_gb = 0
    system = platform.system()

    # 1. NVIDIA via PyTorch (Linux/Windows)
    try:
        import torch
        if torch.cuda.is_available():
            for i in range(torch.cuda.device_count()):
                props = torch.cuda.get_device_properties(i)
                mem_gb = props.total_memory / (1024 ** 3)
                total_memory_gb += mem_gb
    except Exception:
        pass

    # 2. AMD & Intel on Windows via WMI
    if system == "Windows":
        try:
            import wmi
            w = wmi.WMI()
            gpus = w.Win32_VideoController()
            for gpu in gpus:
                if gpu.AdapterRAM:
                    mem_gb = int(gpu.AdapterRAM) / (1024 ** 3)
                    if mem_gb < 0:
                        mem_gb *= -1
                    total_memory_gb += mem_gb
        except Exception:
            pass

    # 3. AMD on Linux via pyamdgpuinfo
    elif system == "Linux":
        try:
            import pyamdgpuinfo
            if pyamdgpuinfo.detect_gpus():
                count = pyamdgpuinfo.get_gpu_count()
                for i in range(count):
                    vram = pyamdgpuinfo.get_vram_total(i)
                    mem_gb = vram / (1024 ** 3)
                    total_memory_gb += mem_gb
        except Exception:
            pass

        # 4. Intel or other via clinfo (Linux)
        try:
            result = subprocess.run(["clinfo"], capture_output=True, text=True)
            blocks = result.stdout.split("Platform Name")
            for block in blocks:
                if "Device Type: GPU" in block:
                    matches = re.findall(r'Global memory size:\s+(\d+)', block)
                    for m in matches:
                        mem_gb = int(m) / (1024 ** 3)
                        total_memory_gb += mem_gb
        except Exception:
            pass

    if total_memory_gb < 0:
        return round(total_memory_gb * -1, 2)
    return round(total_memory_gb, 2)

def get_memory_size():
    size = 0
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            size += round(get_size(usage.free), 0)
        except PermissionError:
            pass
    return size

def get_ram():
    ram = psutil.virtual_memory()
    return get_size(ram.total)

def get_components():
    cpu_freq = psutil.cpu_freq().max / 1000
    cpu_cores = psutil.cpu_count()
    gpu_memory = get_gpu_memory()
    size = get_memory_size()
    ram = get_ram()
    return size, cpu_freq, cpu_cores, gpu_memory, ram
