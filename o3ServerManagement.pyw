import os
import shutil
import subprocess
import sys
import psutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

# ----------------------------------------------------------------

# ***********************************************************
# * ----- o3ServerManagement ----- Version: Alpha 1.0 ----- *
# ***********************************************************

# *******************************************************
# * Copyright (c) openw3rk INVENT, All Rights reserved. *
# * Copyright (c) openw3rk, All Rights reserved.        *
# *******************************************************

# ----------------------------------------------------------------


required_packages = {
    'psutil': '5.9.1'
}

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
def check_and_install_packages():
    for package, version in required_packages.items():
        try:
            __import__(package)  
        except ImportError:
            print(f"{package} ist nicht installiert. Installiere {package}.")
            install(package)

check_and_install_packages()

class openw3rkServerManagement:

    def __init__(self, root):
        self.root = root
        self.root.title("openw3rkServerManagement")
        self.root.geometry("1800x850")
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")
        self.tab_monitoring = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_monitoring, text="Systemüberwachung")
        self.create_monitoring_tab()
        self.tab_backup = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_backup, text="Backup-Management")
        self.create_backup_tab()
        self.tab_shell = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_shell, text="Terminal")
        self.create_shell_tab()
        self.tab_info = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_info, text="Info")
        self.create_info_tab()
        self.update_monitoring()

    def create_monitoring_tab(self):
        self.monitoring_label = tk.Label(self.tab_monitoring, text="Systemüberwachung", bg="slategray3", font=("Arial", 16))
        self.monitoring_label.pack(pady=10)
        self.cpu_label = tk.Label(self.tab_monitoring, text="CPU-Auslastung: ")
        self.cpu_label.pack()
        self.ram_label = tk.Label(self.tab_monitoring, text="RAM-Auslastung: ")
        self.ram_label.pack()

        self.disk_label = tk.Label(self.tab_monitoring, text="Festplatten-Auslastung: ")
        self.disk_label.pack()

        self.network_label = tk.Label(self.tab_monitoring, text="Netzwerk-Auslastung: ")
        self.network_label.pack()

    def update_monitoring(self):
        cpu_percent = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        net_io = psutil.net_io_counters()
        self.cpu_label.config(text=f"CPU-Auslastung: {cpu_percent}%")
        self.ram_label.config(text=f"RAM-Auslastung: {ram.percent}% von {self.bytes_to_gb(ram.total)} GB")
        self.disk_label.config(text=f"Festplatten-Auslastung: {disk.percent}% von {self.bytes_to_gb(disk.total)} GB")
        self.network_label.config(text=f"Netzwerk: {self.bytes_to_gb(net_io.bytes_sent)} GB gesendet, {self.bytes_to_gb(net_io.bytes_recv)} GB empfangen")
        
        self.root.after(2000, self.update_monitoring)

    def bytes_to_gb(self, bytes_value):
        return round(bytes_value / (1024 ** 3), 2)

    def create_backup_tab(self):
        self.backup_label = tk.Label(self.tab_backup, text="Backup-Management", bg="slategray3", font=("Arial", 16))
        self.backup_label.pack(pady=10)
        self.source_label = tk.Label(self.tab_backup, text="Quellverzeichnis auswählen:")
        self.source_label.pack(pady=5)

        self.source_entry = tk.Entry(self.tab_backup, width=50, bg="azure3", fg="black")
        self.source_entry.pack(pady=5)

        self.source_button = tk.Button(self.tab_backup, text="Durchsuchen", command=self.select_source)
        self.source_button.pack(pady=5)
        self.dest_label = tk.Label(self.tab_backup, text="Zielverzeichnis auswählen:")
        self.dest_label.pack(pady=5)
        self.dest_entry = tk.Entry(self.tab_backup, width=50, bg="azure3", fg="black")
        self.dest_entry.pack(pady=5)
        self.dest_button = tk.Button(self.tab_backup, text="Durchsuchen", command=self.select_dest)
        self.dest_button.pack(pady=5)

        self.backup_button = tk.Button(self.tab_backup, text="Backup starten", command=self.start_backup)
        self.backup_button.pack(pady=10)

        self.show_backups_button = tk.Button(self.tab_backup, text="Vorhandene Backups anzeigen", command=self.show_backups)
        self.show_backups_button.pack(pady=10)

    def select_source(self):
        source_dir = filedialog.askdirectory()
        self.source_entry.delete(0, tk.END)
        self.source_entry.insert(0, source_dir)

    def select_dest(self):
        dest_dir = filedialog.askdirectory()
        self.dest_entry.delete(0, tk.END)
        self.dest_entry.insert(0, dest_dir)

    def start_backup(self):
        source = self.source_entry.get()
        dest = self.dest_entry.get()

        if not source or not dest:
            messagebox.showwarning("Fehler", "Bitte wählen Sie sowohl das Quell- als auch das Zielverzeichnis aus!")
            return

        try:
            backup_name = os.path.join(dest, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            self.copy_files(source, backup_name)
            messagebox.showinfo("Erfolg", f"Backup erfolgreich erstellt: {backup_name}")
        except Exception as e:
            messagebox.showerror("Fehler", f"Backup fehlgeschlagen: {str(e)}")

    def copy_files(self, source, dest):
        if not os.path.exists(dest):
            os.makedirs(dest)

        for item in os.listdir(source):
            s = os.path.join(source, item)
            d = os.path.join(dest, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, False, None)
            else:
                shutil.copy2(s, d)

    def show_backups(self):
        dest = self.dest_entry.get()

        if not dest:
            messagebox.showwarning("Fehler", "Bitte wählen Sie ein Zielverzeichnis aus!")
            return

        backups = [d for d in os.listdir(dest) if os.path.isdir(os.path.join(dest, d)) and d.startswith("backup_")]

        if backups:
            backup_list = "\n".join(backups)
            messagebox.showinfo("Vorhandene Backups", f"Folgende Backups sind vorhanden:\n{backup_list}")
        else:
            messagebox.showinfo("Vorhandene Backups", "Keine Backups gefunden.")

    def create_shell_tab(self):
        self.shell_label = tk.Label(self.tab_shell, text="Terminal", bg="slategray3", font=("Arial", 16))
        self.shell_label.pack(pady=10)

        self.shell_text = tk.Text(self.tab_shell, height=40, width=130, bg="black", fg="white", font=("Courier New", 10))
        self.shell_text.pack(pady=10)
        self.shell_text.config(state=tk.NORMAL, insertontime=0)  
        self.show_ascii_art()
        #eingabefeld
        self.shell_label = tk.Label(self.tab_shell, text="Type command:", font=("Arial", 10))
        self.shell_label.pack(pady=5)
        self.shell_entry = tk.Entry(self.tab_shell, width=100, bg="azure3", fg="black", font=("Courier New", 10), insertontime=500)
        self.shell_entry.pack(pady=7)
        self.shell_entry.bind("<Return>", lambda event: self.process_command())
        self.shell_entry.focus_set()  
        self.shell_text.config(state=tk.DISABLED)

    def show_ascii_art(self):
        ascii_art = r"""
                                   ____     __     _____  ___   _______  ________
         ___  ___  ___ ___ _    __|_  /____/ /__  /  _/ |/ / | / / __/ |/ /_  __/
        / _ \/ _ \/ -_) _ \ |/|/ //_ </ __/  '_/ _/ //    /| |/ / _//    / / /   
        \___/ .__/\__/_//_/__,__/____/_/ /_/\_\ /___/_/|_/ |___/___/_/|_/ /_/    
            /_/  Copyright (c) openw3rk INVENT                                                                 
        """
        self.shell_text.insert(tk.END, ascii_art)
        self.shell_text.insert(tk.END, "\nWillkommen\no3ServerManagementTerminal\nCommandlist: 'help --show'\n***************************\n\n  ")

    def process_command(self):
        command_input = self.shell_entry.get().strip()
        self.shell_entry.delete(0, tk.END)  

        if command_input == "help --show":
            self.show_help_in_shell()
        elif command_input == "system -meta --show":
            self.show_system_info_in_shell()
        elif command_input.startswith("backup --make"):
            self.handle_backup_command(command_input)
        elif command_input == "info --show":
            self.show_info_in_shell()
        elif command_input == "exit":
            self.root.quit()
        else:
            self.shell_text.config(state=tk.NORMAL)
            self.shell_text.insert(tk.END, f"Unbekannter Befehl: {command_input}\n\n")
            self.shell_text.config(state=tk.DISABLED)

    def handle_backup_command(self, command):
        parts = command.split()
        if len(parts) < 4 or parts[1] != "--make" or parts[2][:6] != "-from:" or parts[3][:4] != "-to:":
            self.shell_text.config(state=tk.NORMAL)
            self.shell_text.insert(tk.END, "Ungültige Argumente. Benutze: backup --make -from:<Quellort> -to:<Zielort>\n")
            self.shell_text.config(state=tk.DISABLED)
            return

        source = parts[2][6:]  
        dest = parts[3][4:]    

        try:
            backup_name = os.path.join(dest, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            self.copy_files(source, backup_name)
            self.shell_text.config(state=tk.NORMAL)
            self.shell_text.insert(tk.END, f"Backup erfolgreich von '{source}' nach '{dest}' erstellt!\n")
            self.shell_text.config(state=tk.DISABLED)
        except Exception as e:
            self.shell_text.config(state=tk.NORMAL)
            self.shell_text.insert(tk.END, f"Backup fehlgeschlagen: {str(e)}\n")
            self.shell_text.config(state=tk.DISABLED)

    def show_system_info_in_shell(self):
        cpu_percent = psutil.cpu_percent()
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        system_info = (
            f"CPU-Auslastung: {cpu_percent}%\n"
            f"RAM-Auslastung: {ram.percent}% von {self.bytes_to_gb(ram.total)} GB\n"
            f"Festplatten-Auslastung: {disk.percent}% von {self.bytes_to_gb(disk.total)} GB\n\n"
        )
        self.shell_text.config(state=tk.NORMAL)
        self.shell_text.insert(tk.END, system_info)
        self.shell_text.config(state=tk.DISABLED)

    def show_info_in_shell(self):
        help_text = (
            "\n Application: o3ServerManagement\n"
            "Version: Alpha 1.0\n"
            "URL: https://o3sm.openw3rk.de\n"
            "or: https://openw3rk.de\n\n"
            "Copyright (c) openw3rk INVENT, All Rights reserved\n"
            "Copyright (c) openw3rk, All Rights reserved\n\n"
        )
        self.shell_text.config(state=tk.NORMAL)
        self.shell_text.insert(tk.END, help_text)
        self.shell_text.config(state=tk.DISABLED)

    def show_help_in_shell(self):
        help_text = (
            "Verfügbare Befehle:\n"
            "- 'backup --make -from:<Quellort> -to:<Zielort>' Erstellt ein Backup\n"
            "- 'system -meta --show' Zeigt Systeminformationen an\n"
            "- 'help --show' Zeigt diese Hilfe an\n"
            "- 'info --show' Zeigt Informationen zur Application an\n"
            "- 'exit' Beendet das Programm\n\n"
        )
        self.shell_text.config(state=tk.NORMAL)
        self.shell_text.insert(tk.END, help_text)
        self.shell_text.config(state=tk.DISABLED)

    def create_info_tab(self):
        self.info_label = tk.Label(self.tab_info, text="openw3rkServerManagement ", bg="slategray3", font=("Arial", 16))
        self.info_label.pack(pady=10)

        info_text = ( 
            #""
            "\nApplication: o3ServerManagement\n"
            "Entwickeler/developer: openw3rk / openw3rk INVENT\n"
            "----------------------\n"
            "* Version: Alpha 1.0 *\n"
            "----------------------\n"
            "English version coming soon\n\n\n"
            
            "Copyright(c) openw3rk INVENT, All Rights reserved\n"
            "Copyright(c) openw3rk, All Rights reserved\n"
           
        )
        self.info_display = tk.Text(self.tab_info, height=20, width=80, wrap=tk.WORD)
        self.info_display.pack(pady=20)
        self.info_display.insert(tk.END, info_text)
        self.info_display.config(state=tk.DISABLED)  

if __name__ == "__main__":
    check_and_install_packages()  
    root = tk.Tk()
    app = openw3rkServerManagement(root)
    root.mainloop()
