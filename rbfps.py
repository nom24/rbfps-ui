import os
import json
import sys
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox

def install_module(module_name):
    """
    Function to install a Python module using pip.
    """
    try:
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', module_name])
    except Exception as e:
        messagebox.showerror("Error", f"Error installing {module_name} module: {e}")
        sys.exit(1)

def check_and_install_module(module_name):
    try:
        __import__(module_name)
    except ImportError:
        messagebox.showinfo("Info", f"{module_name} module not found. Installing...")
        install_module(module_name)

required_modules = ['colorama']
for module in required_modules:
    check_and_install_module(module)

from colorama import init, Fore

init(autoreset=True)

def get_integer_input(prompt):
    value = simpledialog.askinteger("Input", prompt)
    if value is None:
        sys.exit()
    return value

def log(message, success=True):
    time_now = datetime.now().strftime("%H:%M:%S")
    if success:
        messagebox.showinfo("Info", f"[{time_now}] successful | {message}")
    else:
        messagebox.showerror("Error", f"[{time_now}] unsuccessful | {message}")

root = tk.Tk()
root.withdraw()

fps_limit = get_integer_input("Enter FPS limit (eg. 144): ")

def find_folder_with_exe(directory, target_exe):
    try:
        for root, dirs, files in os.walk(directory):
            if target_exe in files:
                return root
    except OSError as e:
        log(f"Error: {e}", success=False)

def create_client_settings(folder):
    client_settings_folder = os.path.join(folder, "ClientSettings")
    os.makedirs(client_settings_folder, exist_ok=True)
    json_data = {
        "DFIntTaskSchedulerTargetFps": fps_limit
    }
    json_file_path = os.path.join(client_settings_folder, "ClientAppSettings.json")
    try:
        with open(json_file_path, "w") as json_file:
            json.dump(json_data, json_file, indent=4)
        log("ClientSettings folder and config file created successfully.")
    except Exception as e:
        log(f"Error creating JSON file: {e}", success=False)

directory = os.path.expanduser(r'~\AppData\Local\Roblox\Versions')
target_exe = "RobloxPlayerBeta.exe"

folder = find_folder_with_exe(directory, target_exe)
if folder:
    log(f"Folder containing 'RobloxPlayerBeta.exe' found: {folder}")
    create_client_settings(folder)
else:
    log("No folder containing 'RobloxPlayerBeta.exe' found in the specified directory.", success=False)

messagebox.showinfo("Info", "Please note that your game must restart for the FPS unlocker to take effect. If any further help is needed, it can be found in the documentation.")
messagebox.showinfo("Info", "Press OK to close this window.")
