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
        
        # Criar layout principal
        self.create_layout()
        
        # Iniciar monitoramento em thread separada
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self.update_metrics, daemon=True)
        self.monitor_thread.start()

    def create_layout(self):
        # Frame principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Frame superior para métricas em tempo real
        self.metrics_frame = ctk.CTkFrame(self)
        self.metrics_frame.grid(row=0, column=0, padx=20, pady=(20,10), sticky="nsew")
        
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
        self.graph_frame = ctk.CTkFrame(self)
        self.graph_frame.grid(row=1, column=0, padx=20, pady=(10,20), sticky="nsew")
        
        # Criar figura do matplotlib
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, figsize=(10, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, self.graph_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        # Configurar gráficos
        self.setup_graphs()

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