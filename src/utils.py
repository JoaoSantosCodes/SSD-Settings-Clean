import psutil
import platform
import os
from datetime import datetime

def get_system_info():
    """Retorna informações detalhadas do sistema."""
    return {
        'system': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'machine': platform.machine(),
        'processor': platform.processor(),
        'physical_cores': psutil.cpu_count(logical=False),
        'total_cores': psutil.cpu_count(logical=True),
        'ram_total': round(psutil.virtual_memory().total / (1024.0 ** 3), 2),  # GB
        'disk_total': round(psutil.disk_usage('/').total / (1024.0 ** 3), 2)  # GB
    }

def get_disk_info():
    """Retorna informações detalhadas sobre os discos."""
    disks = []
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_info = {
                'device': partition.device,
                'mountpoint': partition.mountpoint,
                'fstype': partition.fstype,
                'total': round(usage.total / (1024.0 ** 3), 2),  # GB
                'used': round(usage.used / (1024.0 ** 3), 2),  # GB
                'free': round(usage.free / (1024.0 ** 3), 2),  # GB
                'percent': usage.percent
            }
            disks.append(disk_info)
        except:
            continue
    return disks

def get_process_info():
    """Retorna informações sobre os processos em execução."""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            proc_info = proc.info
            proc_info['cpu_percent'] = proc.cpu_percent()
            proc_info['memory_percent'] = proc.memory_percent()
            processes.append(proc_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)

def format_bytes(bytes):
    """Formata bytes para uma string legível."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} PB" 