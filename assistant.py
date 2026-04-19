import os
import threading
import tkinter as tk
import speech_recognition as sr
import pyttsx3
import ctypes
import webbrowser
import requests
import json
import sys
import winreg as reg

# --- GESTION DE LA CONFIGURATION (Mémoire de la case) ---
CONFIG_FILE = "config.json"

def save_config(auto_start):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"auto_start": auto_start}, f)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f).get("auto_start", False)
    return False

# --- LOGIQUE DE DÉMARRAGE WINDOWS ---
def set_autostart(action="on"):
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    app_name = "WinAssistant"
    # Utilise pythonw pour ne pas avoir de console noire au démarrage
    executable = sys.executable.replace("python.exe", "pythonw.exe")
    script_path = os.path.realpath(sys.argv[0])
    try:
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_ALL_ACCESS)
        if action == "on":
            reg.SetValueEx(key, app_name, 0, reg.REG_SZ, f'"{executable}" "{script_path}"')
        else:
            try: reg.DeleteValue(key, app_name)
            except: pass
        reg.CloseKey(key)
    except Exception as e:
        print(f"Erreur registre : {e}")

# --- LOGIQUE AUDIO ---
def speak(text):
    def _run():
        local_engine = pyttsx3.init()
        local_engine.say(text)
        local_engine.runAndWait()
    threading.Thread(target=_run, daemon=True).start()

class WinAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("WinAssistant")
        self.root.geometry("500x850")
        self.root.configure(bg="#1a1b26")
        
        # --- LOGO (SÉCURITÉ MAXIMALE) ---
        if os.path.exists("logo.ico"):
            try:
                self.root.iconbitmap("logo.ico")
                # Fix pour la barre des tâches
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("winassistant.final.v1")
            except: pass

        self.history = []
        
        tk.Label(root, text="WinAssistant", font=("Segoe UI", 22, "bold"), fg="#7aa2f7", bg="#1a1b26").pack(pady=15)
        
        self.log_box = tk.Text(root, height=12, width=50, bg="#24283b", fg="#c0caf5", font=("Consolas", 10), bd=0, padx=15, pady=15)
        self.log_box.pack(pady=10)

        tk.Button(root, text="🎤 CLIQUER POUR PARLER", command=self.manual_listen, bg="#7aa2f7", fg="white", font=("Segoe UI", 12, "bold"), bd=0, pady=10).pack(pady=10, padx=30, fill="x")

        self.user_entry = tk.Entry(root, bg="#414868", fg="white", font=("Segoe UI", 12), bd=0, insertbackground="white")
        self.user_entry.pack(pady=10, padx=30, fill="x", ipady=10)
        self.user_entry.bind("<Return>", lambda e: self.process_command(self.user_entry.get()))

        # --- OPTION DÉMARRAGE AVEC MÉMOIRE ---
        self.auto_start_var = tk.BooleanVar(value=load_config())
        self.check_auto = tk.Checkbutton(root, text="Lancer au démarrage de Windows", variable=self.auto_start_var, 
                                        command=self.toggle_startup, bg="#1a1b26", fg="#565f89", selectcolor="#24283b", activebackground="#1a1b26")
        self.check_auto.pack(pady=5)

        tk.Button(root, text="ARRÊTER LA VOIX", command=lambda: pyttsx3.init().stop(), bg="#f7768e", fg="white", bd=0).pack(pady=5)
        
        self.status_label = tk.Label(root, text="Prêt", fg="#565f89", bg="#1a1b26")
        self.status_label.pack(pady=5)

        # Applique l'état sauvegardé au lancement
        if self.auto_start_var.get():
            set_autostart("on")

        threading.Thread(target=self.continuous_listening, daemon=True).start()

    def log(self, msg):
        self.log_box.insert(tk.END, f"> {msg}\n")
        self.log_box.see(tk.END)

    def toggle_startup(self):
        state = self.auto_start_var.get()
        save_config(state) # Sauvegarde dans le fichier JSON
        set_autostart("on" if state else "off")
        self.log(f"Démarrage auto : {'Activé' if state else 'Désactivé'}")

    def manual_listen(self):
        threading.Thread(target=self.listen_once, daemon=True).start()

    def listen_once(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.status_label.config(text="Écoute...", fg="#7ef19d")
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
                cmd = r.recognize_google(audio, language="fr-FR")
                self.process_command(cmd)
            except: pass
            self.status_label.config(text="Prêt", fg="#565f89")

    def process_command(self, text):
        raw_text = text.lower()
        self.log(f"MOI : {text}")
        self.user_entry.delete(0, tk.END)

        if "vidéo" in raw_text or "lien" in raw_text:
            search = raw_text.replace("vidéo", "").strip()
            webbrowser.open(f"https://www.youtube.com/results?search_query={search}")
        elif "verrouille" in raw_text:
            ctypes.windll.user32.LockWorkStation()
        elif "éteins" in raw_text or "arret" in raw_text:
            os.system("shutdown /s /t 1")
        else:
            threading.Thread(target=self.ask_ollama, args=(text,), daemon=True).start()

    def ask_ollama(self, prompt):
        self.history.append({"role": "user", "content": prompt})
        try:
            res = requests.post("http://localhost:11434/api/chat", 
                                json={"model": "llama3.2:1b", "messages": self.history, "stream": False}, timeout=15)
            answer = res.json()['message']['content']
            self.history.append({"role": "assistant", "content": answer})
            self.log(f"IA : {answer}")
            speak(answer)
        except:
            self.log("Ollama non détecté.")

    def continuous_listening(self):
        r = sr.Recognizer()
        while True:
            try:
                with sr.Microphone() as source:
                    audio = r.listen(source, phrase_time_limit=3)
                    if "assistant" in r.recognize_google(audio, language="fr-FR").lower():
                        speak("Oui ?")
                        self.listen_once()
            except: continue

if __name__ == "__main__":
    root = tk.Tk()
    app = WinAssistant(root)
    root.mainloop()