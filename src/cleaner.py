import os
import shutil
import winreg
import psutil
import win32com.client
from datetime import datetime, timedelta
import subprocess
from typing import List, Dict, Tuple
import logging

class SystemCleaner:
    def __init__(self):
        self.temp_folders = [
            os.path.join(os.environ.get('TEMP')),
            os.path.join(os.environ.get('SYSTEMROOT'), 'Temp'),
            os.path.join(os.environ.get('SYSTEMROOT'), 'Prefetch'),
            os.path.join(os.environ.get('LOCALAPPDATA'), 'Temp')
        ]
        
    def get_inactive_programs(self, days: int = 30) -> List[Dict]:
        """
        Encontra programas que não foram usados nos últimos X dias
        """
        inactive_programs = []
        
        try:
            # Verificar programas instalados através do registro do Windows
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall", 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY) as key:
                for i in range(winreg.QueryInfoKey(key)[0]):
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            try:
                                install_date = winreg.QueryValueEx(subkey, "InstallDate")[0]
                                display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                install_location = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                                uninstall_string = winreg.QueryValueEx(subkey, "UninstallString")[0]
                                
                                # Verificar última modificação do diretório de instalação
                                if os.path.exists(install_location):
                                    last_access = datetime.fromtimestamp(os.path.getatime(install_location))
                                    if datetime.now() - last_access > timedelta(days=days):
                                        inactive_programs.append({
                                            'name': display_name,
                                            'location': install_location,
                                            'last_access': last_access,
                                            'uninstall_string': uninstall_string
                                        })
                            except (WindowsError, ValueError):
                                continue
                    except WindowsError:
                        continue
        except Exception as e:
            logging.error(f"Erro ao buscar programas inativos: {str(e)}")
            
        return inactive_programs
    
    def clean_temp_files(self) -> Tuple[int, List[str]]:
        """
        Limpa arquivos temporários do sistema
        Retorna: (bytes_liberados, lista_de_erros)
        """
        bytes_freed = 0
        errors = []
        
        for folder in self.temp_folders:
            if os.path.exists(folder):
                try:
                    for root, dirs, files in os.walk(folder, topdown=False):
                        for name in files:
                            try:
                                file_path = os.path.join(root, name)
                                bytes_freed += os.path.getsize(file_path)
                                os.unlink(file_path)
                            except Exception as e:
                                errors.append(f"Não foi possível deletar {file_path}: {str(e)}")
                        for name in dirs:
                            try:
                                dir_path = os.path.join(root, name)
                                shutil.rmtree(dir_path, ignore_errors=True)
                            except Exception as e:
                                errors.append(f"Não foi possível deletar diretório {dir_path}: {str(e)}")
                except Exception as e:
                    errors.append(f"Erro ao processar pasta {folder}: {str(e)}")
                    
        return bytes_freed, errors
    
    def optimize_system(self) -> List[str]:
        """
        Executa várias otimizações do sistema
        Retorna: lista de ações realizadas
        """
        actions = []
        
        # Desfragmentação (apenas para HDDs)
        try:
            for disk in psutil.disk_partitions():
                if 'fixed' in disk.opts:  # Skip removable drives
                    # Verificar se é SSD
                    is_ssd = self._is_ssd(disk.device.rstrip('\\'))
                    if not is_ssd:
                        subprocess.run(['defrag', disk.device.rstrip('\\'), '/A'], 
                                    capture_output=True, text=True)
                        actions.append(f"Desfragmentação executada em {disk.device}")
                    else:
                        subprocess.run(['defrag', disk.device.rstrip('\\'), '/O'], 
                                    capture_output=True, text=True)
                        actions.append(f"Otimização TRIM executada em SSD {disk.device}")
        except Exception as e:
            actions.append(f"Erro na desfragmentação: {str(e)}")
            
        # Limpeza do registro
        try:
            subprocess.run(['reg', 'delete', 'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run', '/va', '/f'],
                         capture_output=True, text=True)
            actions.append("Limpeza de entradas de inicialização automática")
        except Exception as e:
            actions.append(f"Erro na limpeza do registro: {str(e)}")
            
        # Desabilitar serviços desnecessários
        unnecessary_services = [
            'DiagTrack',  # Telemetria do Windows
            'dmwappushservice',  # WAP Push Message Routing Service
            'Remote Registry'  # Registro Remoto
        ]
        
        for service in unnecessary_services:
            try:
                subprocess.run(['sc', 'config', service, 'start=disabled'],
                             capture_output=True, text=True)
                subprocess.run(['sc', 'stop', service],
                             capture_output=True, text=True)
                actions.append(f"Serviço {service} desabilitado")
            except Exception as e:
                actions.append(f"Erro ao desabilitar serviço {service}: {str(e)}")
        
        return actions
    
    def uninstall_program(self, uninstall_string: str) -> bool:
        """
        Desinstala um programa usando sua string de desinstalação
        """
        try:
            # Alguns programas usam msiexec
            if 'msiexec' in uninstall_string.lower():
                subprocess.run(uninstall_string, shell=True, check=True)
            else:
                # Outros podem ter seu próprio desinstalador
                subprocess.run(uninstall_string + ' /quiet', shell=True, check=True)
            return True
        except Exception as e:
            logging.error(f"Erro ao desinstalar programa: {str(e)}")
            return False
            
    def _is_ssd(self, drive: str) -> bool:
        """
        Verifica se um drive é SSD
        """
        try:
            wmi = win32com.client.GetObject("winmgmts:")
            for disk in wmi.InstancesOf("Win32_DiskDrive"):
                if drive.lower().startswith(disk.DeviceID.lower()):
                    return "SSD" in disk.MediaType
        except Exception:
            return False
        return False 