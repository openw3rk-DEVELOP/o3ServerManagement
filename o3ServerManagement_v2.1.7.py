import os
import shutil
import subprocess
import sys
import psutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import platform
import socket
import webbrowser

# ----------------------------------------------------------------

# **********************************************************
# * ----- o3ServerManagement -----   Version: 2.1.7  ----- *
# **********************************************************

# **********************************
# * Copyright (c) openw3rk INVENT  *
# * - Licensed under MIT-License - * 
# **********************************

# ----------------------------------------------------------------

required_packages = {
    'psutil': ('psutil', '5.9.1')
}

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_and_install_packages():
    for package, version in required_packages.items():
        try:
            __import__(package)
        except ImportError:
            print(f"{package} is not installed. installing {package}.")
            install(package)

check_and_install_packages()

class openw3rkServerManagement:
    def create_portscanner_tab(self):
        self.tab_ports = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_ports, text="Port Scan")
        tk.Label(self.tab_ports, text="Port Scan", font=("Arial", 16), bg="slategray3").pack(pady=10)
        frame = tk.Frame(self.tab_ports)
        frame.pack(pady=10)
        tk.Label(frame, text="IP / Hostname:").grid(row=0, column=0, sticky="e")
        self.portscan_host = tk.Entry(frame, width=30)
        self.portscan_host.grid(row=0, column=1, padx=5)
        tk.Label(frame, text="Port range (example 20-100):").grid(row=1, column=0, sticky="e")
        self.portscan_range = tk.Entry(frame, width=30)
        self.portscan_range.grid(row=1, column=1, padx=5)
        tk.Button(self.tab_ports, text="Start Scan", command=self.run_portscan).pack(pady=5)
        self.portscan_output = tk.Text(self.tab_ports, width=100, height=25, bg="black", fg="lime", font=("Courier", 10))
        self.portscan_output.pack(pady=10)
        self.portscan_output.tag_config("open_port", foreground="orange")
        self.portscan_output.tag_config("closed_port", foreground="lime")
        self.portscan_output.tag_config("panic_warn", foreground="tomato")
    def run_portscan(self):
        import socket
        host = self.portscan_host.get()
        port_range = self.portscan_range.get()

        self.portscan_output.config(state=tk.NORMAL)
        self.portscan_output.delete("1.0", tk.END)
        self.portscan_output.insert(tk.END, "Starting scan, please wait...\n\n", "info")
        self.portscan_output.update()

        try:
            if "-" in port_range:
                start_port, end_port = map(int, port_range.split("-"))
            else:
                start_port = end_port = int(port_range)

            self.portscan_output.insert(tk.END, f"Scan {host} from Port {start_port} to {end_port}...\n")

            for port in range(start_port, end_port + 1):
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(0.9)
                    result = sock.connect_ex((host, port))
                    if result == 0:
                        self.portscan_output.insert(tk.END, f"[open  ] Port {port}\n", "open_port")
                    else:
                        self.portscan_output.insert(tk.END, f"[closed] Port {port}\n", "closed_port")
        except Exception as e:
            self.portscan_output.insert(tk.END, "[PANIC] ! PORT RANGE IS NOT DEFINED !\n", "panic_warn")

        self.portscan_output.config(state=tk.DISABLED)
    def __init__(self, root):
        self.root = root
        self.root.title("openw3rk-ServerManagement")
        self.root.geometry("1800x850")
        icon = tk.PhotoImage(file="o3ServerManagement_logo.png")
        root.iconphoto(True, icon)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")
        self.tab_monitoring = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_monitoring, text="System monitoring")
        self.create_monitoring_tab()
        self.tab_backup = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_backup, text="Backup-Management")
        self.create_backup_tab()
        self.tab_shell = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_shell, text="Terminal")
        self.create_shell_tab()
        self.tab_info = ttk.Frame(self.notebook)
        self.create_portscanner_tab()
        self.notebook.add(self.tab_info, text="Info")
        self.create_info_tab()
        self.update_monitoring()


    def create_monitoring_tab(self):
        self.monitoring_label = tk.Label(self.tab_monitoring, text="System monitoring", bg="slategray3", font=("Arial", 16))
        self.monitoring_label.pack(pady=10)
        self.cpu_label = tk.Label(self.tab_monitoring, text="CPU usage: ")
        self.cpu_label.pack()
        self.ram_label = tk.Label(self.tab_monitoring, text="RAM usage: ")
        self.ram_label.pack()
        self.disk_label = tk.Label(self.tab_monitoring, text="Hard drive usage: ")
        self.disk_label.pack()
        self.network_label = tk.Label(self.tab_monitoring, text="Network usage: ")
        self.network_label.pack()
        self.temp_label = tk.Label(self.tab_monitoring, text="CPU temperature: ")
        self.temp_label.pack()
        self.sysinfo_label = tk.Label(self.tab_monitoring, text="System information: ")
        self.sysinfo_label.pack()
    def update_monitoring(self):
        cpu_percent = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        net_io = psutil.net_io_counters()
        self.cpu_label.config(text=f"CPU usage: {cpu_percent}%")
        self.ram_label.config(text=f"RAM usage: {ram.percent}% of {self.bytes_to_gb(ram.total)} GB")
        self.disk_label.config(text=f"Hard drive usage: {disk.percent}% of {self.bytes_to_gb(disk.total)} GB")
        self.network_label.config(text=f"Network: {self.bytes_to_gb(net_io.bytes_sent)} GB outgoing, {self.bytes_to_gb(net_io.bytes_recv)} GB incoming")
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                for name, entries in temps.items():
                    for entry in entries:
                        if entry.label == 'Package id 0' or entry.label == '':
                            self.temp_label.config(text=f"CPU temperature: {entry.current}°C")
                            break
                    else:
                        self.temp_label.config(text="CPU temperature: n/a")
            else:
                self.temp_label.config(text="CPU temperature: n/a")
        except Exception:
            self.temp_label.config(text="CPU temperature: n/a")
        sys_info = f"{platform.system()} {platform.release()} ({platform.machine()})"
        self.sysinfo_label.config(text=f"System monitoring: {sys_info}")
        self.root.after(2000, self.update_monitoring)

    def bytes_to_gb(self, bytes_value):
        return round(bytes_value / (1024 ** 3), 2)

    def create_backup_tab(self):
        self.backup_label = tk.Label(self.tab_backup, text="Backup-Management", bg="slategray3", font=("Arial", 16))
        self.backup_label.pack(pady=10)
        self.source_label = tk.Label(self.tab_backup, text="Select source directory:")
        self.source_label.pack(pady=5)
        self.source_entry = tk.Entry(self.tab_backup, width=50, bg="azure3", fg="black")
        self.source_entry.pack(pady=5)
        self.source_button = tk.Button(self.tab_backup, text="Browse", command=self.select_source)
        self.source_button.pack(pady=5)
        self.dest_label = tk.Label(self.tab_backup, text="Select destination directory:")
        self.dest_label.pack(pady=5)
        self.dest_entry = tk.Entry(self.tab_backup, width=50, bg="azure3", fg="black")
        self.dest_entry.pack(pady=5)
        self.dest_button = tk.Button(self.tab_backup, text="Browse", command=self.select_dest)
        self.dest_button.pack(pady=5)
        self.backup_button = tk.Button(self.tab_backup, text="Start Backup", command=self.start_backup)
        self.backup_button.pack(pady=10)
        self.show_backups_button = tk.Button(self.tab_backup, text="Show existing backups", command=self.show_backups)
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
            messagebox.showwarning("Backup PANIC!", "Please select both the source and destination directories!")
            return
        try:
            backup_name = os.path.join(dest, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            self.copy_files(source, backup_name)
            messagebox.showinfo("Successfully", f"Backup Successfully: {backup_name}")
        except Exception as e:
            messagebox.showerror("BACKUP PANIC!", f"Backup failed (corrupted files of wrong Path?): {str(e)}")

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
            messagebox.showwarning("SELECTION PANIC!", "Please select a target directory!")
            return
        backups = [d for d in os.listdir(dest) if os.path.isdir(os.path.join(dest, d)) and d.startswith("backup_")]
        if backups:
            backup_list = "\n".join(backups)
            messagebox.showinfo("Existing Backups", f"The following Backups exist:\n{backup_list}")
        else:
            messagebox.showinfo("Show existing Backups", "No Backups found.")

    def create_shell_tab(self):
        self.shell_label = tk.Label(self.tab_shell, text="Terminal", bg="slategray3", font=("Arial", 16))
        self.shell_label.pack(pady=10)
        self.shell_text = tk.Text(self.tab_shell, height=40, width=130, bg="black", fg="white", font=("Courier New", 10))
        self.shell_text.pack(pady=10)
        self.shell_text.config(state=tk.NORMAL, insertontime=0)
        self.show_ascii_art()
        self.shell_label = tk.Label(self.tab_shell, text="Enter command:", font=("Arial", 10))
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
        self.shell_text.insert(tk.END, "\nWelcome\no3ServerManagementTerminal\nCommandlist: 'help --show'\n***************************\n\n  ")

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
            self.shell_text.insert(tk.END, f"Unknow command: {command_input}\n\n")
            self.shell_text.config(state=tk.DISABLED)

    def handle_backup_command(self, command):
        parts = command.split()
        if len(parts) < 4 or parts[1] != "--make" or parts[2][:6] != "-from:" or parts[3][:4] != "-to:":
            self.shell_text.config(state=tk.NORMAL)
            self.shell_text.insert(tk.END, "Invalid arguments! Use: backup --make -from:<Quellort> -to:<Zielort>\n")
            self.shell_text.config(state=tk.DISABLED)
            return

        source = parts[2][6:]  
        dest = parts[3][4:]    

        try:
            backup_name = os.path.join(dest, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            self.copy_files(source, backup_name)
            self.shell_text.config(state=tk.NORMAL)
            self.shell_text.insert(tk.END, f"Backup successful from '{source}' to '{dest}' created!\n")
            self.shell_text.config(state=tk.DISABLED)
        except Exception as e:
            self.shell_text.config(state=tk.NORMAL)
            self.shell_text.insert(tk.END, f"Backup FAILED: {str(e)}\n")
            self.shell_text.config(state=tk.DISABLED)

    def show_system_info_in_shell(self):
        cpu_percent = psutil.cpu_percent()
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        system_info = (
            f"CPU usage: {cpu_percent}%\n"
            f"RAM usage: {ram.percent}% of {self.bytes_to_gb(ram.total)} GB\n"
            f"Hard disk usage: {disk.percent}% of {self.bytes_to_gb(disk.total)} GB\n\n"
        )
        self.shell_text.config(state=tk.NORMAL)
        self.shell_text.insert(tk.END, system_info)
        self.shell_text.config(state=tk.DISABLED)

    def show_info_in_shell(self):
        help_text = (
            "\nINFORMATION:\n\n"  
            "Application: o3ServerManagement\n"
            "-------------------------------\n\n"
            "------------------\n"
            "* Version: 2.1.7 *\n"
            "------------------\n\n"
            "URL: https://o3sm.openw3rk.de\n"
            "or: https://openw3rk.de\n"
            "SourceCode: https://github.com/openw3rk-DEVELOP/o3ServerManagement\n\n"
            "Copyright (c) openw3rk INVENT\n\n"
            "The openw3rkServerManagement application is Open Source.\nLicensed under the MIT-License.\n"
            "-------------------------------------------------------------------\n\n"
        )
        self.shell_text.config(state=tk.NORMAL)
        self.shell_text.insert(tk.END, help_text)
        self.shell_text.config(state=tk.DISABLED)

    def show_help_in_shell(self):
        help_text = (
            "Available commands:\n"
            "- 'backup --make -from:<source location> -to:<destination location>' Creates a backup\n"
            "- 'system -meta --show' Displays system information\n"
            "- 'help --show' Displays this help\n"
            "- 'info --show' Displays application information\n"
            "- 'exit' Exits the program\n\n"
            "The port scanner is not available at the command line.\nPlease use the 'Port Scan' tab.\n\n"
            "---------------------------------------------------------------------------------------\n"
        )
        self.shell_text.config(state=tk.NORMAL)
        self.shell_text.insert(tk.END, help_text)
        self.shell_text.config(state=tk.DISABLED)
    def create_info_tab(self):
        self.info_label = tk.Label(self.tab_info, text="openw3rk-ServerManagement ", bg="slategray3", font=("Arial", 16))
        self.info_label.pack(pady=10)

        info_text = (
            "\nApplication: o3ServerManagement\n"
            "Developer: openw3rk / openw3rk INVENT\n\n"
            "------------------\n"
            "* Version: 2.1.7 *\n"
            "------------------\n\n"
            "Copyright (c) openw3rk INVENT\n\n"
            "The openw3rkServerManagement application is Open Source.\nLicensed under the MIT-License."
        )

        self.info_display = tk.Text(self.tab_info, height=20, width=80, wrap=tk.WORD)
        self.info_display.pack(pady=20)
        self.info_display.insert(tk.END, info_text + "\n\n")
        urls = {
            "https://o3sm.openw3rk.de": "https://o3sm.openw3rk.de",
            "https://openw3rk.de": "https://openw3rk.de", 
            "SourceCode": "https://github.com/openw3rk-DEVELOP/o3ServerManagement"
    }
        for url_text, url_link in urls.items():
            start_index = self.info_display.index(tk.END)
            self.info_display.insert(tk.END, url_text + "\n")
            end_index = self.info_display.index(tk.END)
            self.info_display.tag_add(url_text, f"{float(start_index) - 1} linestart", f"{float(end_index) - 1} linestart")
            self.info_display.tag_config(url_text, foreground="blue", underline=1)
            self.info_display.tag_bind(url_text, "<Button-1>", lambda e, link=url_link: webbrowser.open(link))
        self.info_display.config(state=tk.DISABLED)

if __name__ == "__main__":
    check_and_install_packages()  
    root = tk.Tk()
    app = openw3rkServerManagement(root)
    root.mainloop()
