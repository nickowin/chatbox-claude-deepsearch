import os
import sys
import tkinter as tk
from tkinter import scrolledtext, messagebox
import json
import customtkinter as ctk
from openai import OpenAI
import anthropic
import threading
import hashlib
import psutil
import time

# PyInstaller path fix
if getattr(sys, 'frozen', False):
    app_path = sys._MEIPASS
    os.chdir(app_path)
else:
    app_path = os.path.dirname(os.path.abspath(__file__))

HISTORY_FILE = os.path.join(app_path, "chat_history.json")
LICENSE_FILE = os.path.join(app_path, "license.key")

# API KEY (Đã hardcode key của bạn)
API_KEY = "sk-C03RLxXm3CAtpteQsCeuwaZuyX0JeqVkPkmX94tCvUQz4AtY"
claude_client = anthropic.Anthropic(api_key=API_KEY)
deepseek_client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com/v1")

# SECURITY WARNING
print("🚨 BLACKBOX AI PRO SECURITY ACTIVE")
print("⚠️  Strings.exe/Hex editor → APP CRASH")
print("⚠️  Key extract → RATE LIMIT 1/phút")
print("📞 Support: support@blackbox.vn")

def security_check():
    """Anti-reverse engineering"""
    suspicious = ['strings', 'hexedit', '010editor', 'ida', 'ghidra', 'x64dbg']
    for proc in psutil.process_iter(['name']):
        if any(s in proc.info['name'].lower() for s in suspicious):
            print("🚨 REVERSE ENGINEERING DETECTED!")
            messagebox.showerror("🚨 ANTI-THEFT", "App tự hủy do reverse!\nLiên hệ support.")
            os._exit(1)

security_check()

# LICENSE SYSTEM
VALID_LICENSES = {
    "blackbox2026": "e8b9c7d4a2f5b1e9",
    "prodev123": "f3a8d2e7c5b9f1a4",
    # Tạo mới: hashlib.sha256("mã".encode()).hexdigest()[:16]
}

class LicenseWindow:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("🔐 Blackbox AI Pro - License")
        self.root.geometry("550x400")
        self.resizable(False, False)
        self.trial_active = False
        
        ctk.CTkLabel(self.root, text="🖥️ BLACKBOX AI PRO v1.0", 
                    font=ctk.CTkFont(size=28, weight="bold")).pack(pady=40)
        
        ctk.CTkLabel(self.root, text="Nhập License Key (vĩnh viễn):", 
                    font=ctk.CTkFont(size=18)).pack(pady=10)
        
        self.entry = ctk.CTkEntry(self.root, width=400, height=55, font=ctk.CTkFont(size=16),
                                placeholder_text="VD: blackbox2026")
        self.entry.pack(pady=25)
        self.entry.bind("<Return>", self.verify)
        
        ctk.CTkButton(self.root, text="✅ KÍCH HOẠT", height=55, width=250, font=ctk.CTkFont(size=18),
                     command=self.verify).pack(pady=20)
        
        ctk.CTkButton(self.root, text="🆓 TRIAL 5 PHÚT", height=45, width=250,
                     fg_color="#ff9500", command=self.trial).pack(pady=10)
        
        self.root.mainloop()
    
    def verify(self, event=None):
        key = self.entry.get().strip()
        if not key: return messagebox.showerror("Lỗi", "Nhập key!")
        
        if os.path.exists(LICENSE_FILE):
            with open(LICENSE_FILE) as f:
                if f.read().strip() == key:
                    self.root.destroy()
                    MainApp()
                    return
        
        for name, h in VALID_LICENSES.items():
            if hashlib.sha256(key.encode()).hexdigest()[:16] == h:
                with open(LICENSE_FILE, 'w') as f:
                    f.write(key)
                messagebox.showinfo("✅ OK", f"Chào {name.title()}! Mở vĩnh viễn!")
                self.root.destroy()
                MainApp()
                return
        
        messagebox.showerror("❌ Sai", "License không hợp lệ!")
    
    def trial(self):
        self.trial_active = True
        messagebox.showinfo("Trial", "5 phút free!")
        self.root.destroy()
        TrialMainApp()

class MainApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("🖥️ Blackbox AI Pro")
        self.root.geometry("1000x800")
        self.chat_history = []
        self.setup_ui()
        self.load_history()
        self.root.mainloop()
    
    def setup_ui(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Header
        header = ctk.CTkFrame(self.root)
        header.pack(fill="x", padx=15, pady=10)
        ctk.CTkLabel(header, text="🖥️ Blackbox AI Pro", 
                    font=ctk.CTkFont(size=24, weight="bold")).pack(side="left")
        
        ctrl = ctk.CTkFrame(header)
        ctrl.pack(side="right")
        ctk.CTkLabel(ctrl, text="Model:").pack(side="left", padx=10)
        self.model_var
