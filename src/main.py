import customtkinter as ctk
import psutil
import platform
from PIL import Image
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time
from cleaner import SystemCleaner
from utils import format_bytes, get_system_info

class SystemMonitor(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuração da janela principal
        self.title("SSD Settings Clean - Monitor de Sistema")
        self.geometry("1200x800")
        
        # Definir tema escuro por padrão
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Variáveis para armazenar dados históricos
        self.cpu_history = []
        self.ram_history = []
        self.disk_history = []
        
        # Inicializar sistema de limpeza
        self.cleaner = SystemCleaner()
        
        # Criar layout principal
        self.create_layout()
        
        # Iniciar monitoramento em thread separada
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self.update_metrics, daemon=True)
        self.monitor_thread.start()

    def create_layout(self):
        # Criar notebook para abas
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)

        # Aba de monitoramento
        self.tab_monitor = self.tabview.add("Monitor")
        self.create_monitor_tab()

        # Aba de limpeza e otimização
        self.tab_clean = self.tabview.add("Limpeza e Otimização")
        self.create_clean_tab()

    def create_monitor_tab(self):
        # Frame superior para métricas em tempo real
        self.metrics_frame = ctk.CTkFrame(self.tab_monitor)
        self.metrics_frame.pack(fill="x", padx=20, pady=10)
        
        # CPU Info
        self.cpu_label = ctk.CTkLabel(self.metrics_frame, text="CPU Usage", font=("Roboto", 16, "bold"))
        self.cpu_label.grid(row=0, column=0, padx=20, pady=10)
        self.cpu_progress = ctk.CTkProgressBar(self.metrics_frame, width=200)
        self.cpu_progress.grid(row=1, column=0, padx=20, pady=5)
        self.cpu_progress.set(0)
        
        # RAM Info
        self.ram_label = ctk.CTkLabel(self.metrics_frame, text="RAM Usage", font=("Roboto", 16, "bold"))
        self.ram_label.grid(row=0, column=1, padx=20, pady=10)
        self.ram_progress = ctk.CTkProgressBar(self.metrics_frame, width=200)
        self.ram_progress.grid(row=1, column=1, padx=20, pady=5)
        self.ram_progress.set(0)
        
        # Disk Info
        self.disk_label = ctk.CTkLabel(self.metrics_frame, text="Disk Usage", font=("Roboto", 16, "bold"))
        self.disk_label.grid(row=0, column=2, padx=20, pady=10)
        self.disk_progress = ctk.CTkProgressBar(self.metrics_frame, width=200)
        self.disk_progress.grid(row=1, column=2, padx=20, pady=5)
        self.disk_progress.set(0)

        # Frame para gráficos
        self.graph_frame = ctk.CTkFrame(self.tab_monitor)
        self.graph_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Criar figura do matplotlib
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, figsize=(10, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, self.graph_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        # Configurar gráficos
        self.setup_graphs()

    def create_clean_tab(self):
        # Frame para ações de limpeza
        clean_frame = ctk.CTkFrame(self.tab_clean)
        clean_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Título
        title = ctk.CTkLabel(clean_frame, text="Limpeza e Otimização do Sistema", 
                            font=("Roboto", 20, "bold"))
        title.pack(pady=20)

        # Botão de limpeza de arquivos temporários
        self.temp_button = ctk.CTkButton(clean_frame, text="Limpar Arquivos Temporários",
                                       command=self.clean_temp_files)
        self.temp_button.pack(pady=10)

        # Botão de otimização
        self.optimize_button = ctk.CTkButton(clean_frame, text="Otimizar Sistema",
                                           command=self.optimize_system)
        self.optimize_button.pack(pady=10)

        # Frame para programas inativos
        inactive_frame = ctk.CTkFrame(clean_frame)
        inactive_frame.pack(fill="x", padx=20, pady=20)

        inactive_label = ctk.CTkLabel(inactive_frame, text="Programas Inativos (>30 dias)",
                                    font=("Roboto", 16, "bold"))
        inactive_label.pack(pady=10)

        # Lista de programas inativos
        self.inactive_listbox = ctk.CTkTextbox(inactive_frame, height=200)
        self.inactive_listbox.pack(fill="x", padx=20, pady=10)

        # Botão para atualizar lista de programas inativos
        refresh_button = ctk.CTkButton(inactive_frame, text="Atualizar Lista",
                                     command=self.update_inactive_programs)
        refresh_button.pack(pady=10)

        # Área de log
        self.log_area = ctk.CTkTextbox(clean_frame, height=150)
        self.log_area.pack(fill="x", padx=20, pady=20)

    def clean_temp_files(self):
        self.temp_button.configure(state="disabled")
        self.log_area.delete("1.0", "end")
        self.log_area.insert("end", "Limpando arquivos temporários...\n")
        
        def clean():
            bytes_freed, errors = self.cleaner.clean_temp_files()
            
            self.log_area.insert("end", f"\nEspaço liberado: {format_bytes(bytes_freed)}\n")
            if errors:
                self.log_area.insert("end", "\nErros encontrados:\n")
                for error in errors:
                    self.log_area.insert("end", f"- {error}\n")
            
            self.temp_button.configure(state="normal")
        
        threading.Thread(target=clean, daemon=True).start()

    def optimize_system(self):
        self.optimize_button.configure(state="disabled")
        self.log_area.delete("1.0", "end")
        self.log_area.insert("end", "Otimizando sistema...\n")
        
        def optimize():
            actions = self.cleaner.optimize_system()
            
            self.log_area.insert("end", "\nAções realizadas:\n")
            for action in actions:
                self.log_area.insert("end", f"- {action}\n")
            
            self.optimize_button.configure(state="normal")
        
        threading.Thread(target=optimize, daemon=True).start()

    def update_inactive_programs(self):
        self.inactive_listbox.delete("1.0", "end")
        self.inactive_listbox.insert("end", "Buscando programas inativos...\n")
        
        def update():
            programs = self.cleaner.get_inactive_programs()
            
            self.inactive_listbox.delete("1.0", "end")
            if not programs:
                self.inactive_listbox.insert("end", "Nenhum programa inativo encontrado.\n")
                return
            
            for prog in programs:
                self.inactive_listbox.insert("end", 
                    f"Nome: {prog['name']}\n"
                    f"Local: {prog['location']}\n"
                    f"Último acesso: {prog['last_access'].strftime('%d/%m/%Y %H:%M:%S')}\n"
                    f"{'='*50}\n")
        
        threading.Thread(target=update, daemon=True).start()

    def setup_graphs(self):
        self.ax1.set_title('CPU Usage Over Time')
        self.ax1.set_ylim(0, 100)
        self.ax1.grid(True)

        self.ax2.set_title('RAM Usage Over Time')
        self.ax2.set_ylim(0, 100)
        self.ax2.grid(True)

        self.ax3.set_title('Disk Usage Over Time')
        self.ax3.set_ylim(0, 100)
        self.ax3.grid(True)

    def update_metrics(self):
        while self.monitoring:
            # Coletar métricas
            cpu_percent = psutil.cpu_percent()
            ram_percent = psutil.virtual_memory().percent
            disk_percent = psutil.disk_usage('/').percent

            # Atualizar histórico
            self.cpu_history.append(cpu_percent)
            self.ram_history.append(ram_percent)
            self.disk_history.append(disk_percent)

            # Manter apenas os últimos 60 pontos
            if len(self.cpu_history) > 60:
                self.cpu_history.pop(0)
                self.ram_history.pop(0)
                self.disk_history.pop(0)

            # Atualizar interface
            self.after(0, self.update_ui, cpu_percent, ram_percent, disk_percent)
            
            time.sleep(1)

    def update_ui(self, cpu, ram, disk):
        # Atualizar barras de progresso
        self.cpu_progress.set(cpu/100)
        self.cpu_label.configure(text=f"CPU Usage: {cpu:.1f}%")
        
        self.ram_progress.set(ram/100)
        self.ram_label.configure(text=f"RAM Usage: {ram:.1f}%")
        
        self.disk_progress.set(disk/100)
        self.disk_label.configure(text=f"Disk Usage: {disk:.1f}%")

        # Atualizar gráficos
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()

        self.setup_graphs()

        self.ax1.plot(self.cpu_history, color='blue')
        self.ax2.plot(self.ram_history, color='green')
        self.ax3.plot(self.disk_history, color='red')

        self.fig.canvas.draw()

if __name__ == "__main__":
    app = SystemMonitor()
    app.mainloop() 