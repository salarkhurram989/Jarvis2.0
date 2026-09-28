import json, os, re, subprocess, threading, urllib.request, urllib.error
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

API_URL = "https://jarvis-flax-pi.vercel.app/api/chat"
APP_NAME = "JARVIS 2.0"
CONFIG = Path.home() / ".jarvis2_config.json"

def open_item(path):
    p = Path(path)
    if not p.exists():
        return False, "I couldn't find that item."
    try:
        os.startfile(str(p))
        return True, f"Opening {p.name}."
    except Exception:
        return False, "Windows couldn't open that item."

def search_files(query, limit=25):
    q = query.lower().strip().strip('"').strip("'")
    roots = []
    home = Path.home()
    for p in (home/"Desktop", home/"Documents", home/"Downloads"):
        if p.exists(): roots.append(p)
    for letter in "CDEFGHIJKLMNOPQRSTUVWXYZ":
        p = Path(f"{letter}:\\")
        if p.exists(): roots.append(p)

    skip = {
        "Windows", "ProgramData", "$Recycle.Bin", "System Volume Information",
        "Recovery", "PerfLogs", "node_modules", ".git", "__pycache__"
    }
    results = []
    for root in roots:
        try:
            for current, dirs, files in os.walk(root):
                dirs[:] = [d for d in dirs if d not in skip and not d.startswith(".")]
                for name in files:
                    if q in name.lower():
                        results.append(str(Path(current) / name))
                        if len(results) >= limit:
                            return results
        except (PermissionError, OSError):
            continue
    return results

def find_app(name):
    q = name.lower().replace(".exe", "").strip()
    places = [
        Path(os.environ.get("APPDATA", "")) / "Microsoft/Windows/Start Menu/Programs",
        Path(os.environ.get("PROGRAMDATA", "")) / "Microsoft/Windows/Start Menu/Programs",
        Path(os.environ.get("USERPROFILE", "")) / "Desktop",
        Path(os.environ.get("PUBLIC", "")) / "Desktop",
    ]
    matches = []
    for base in places:
        if not base.exists(): continue
        try:
            for p in base.rglob("*"):
                if p.is_file() and p.suffix.lower() in (".lnk", ".exe") and q in p.stem.lower():
                    matches.append(p)
                    if len(matches) >= 8:
                        return matches
        except (PermissionError, OSError):
            continue
    return matches

def ai_reply(message):
    body = json.dumps({"message": message}).encode("utf-8")
    req = urllib.request.Request(API_URL, data=body, headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req, timeout=20) as response:
        data = json.loads(response.read().decode("utf-8"))
    return data.get("answer", "I didn't receive an answer.")

def handle_local_command(text):
    t = text.lower().strip()

    if t.startswith(("find ", "search for ", "search ")):
        q = re.sub(r"^(find|search for|search)\s+", "", text, flags=re.I)
        results = search_files(q)
        if not results:
            return "I couldn't find any matching files.", None
        return "I found:\n" + "\n".join(results[:20]), results

    m = re.match(r"^(open|launch|start)\s+(?:the\s+)?(.+)$", text, re.I)
    if m:
        target = m.group(2).strip()
        # Explicit paths are opened directly.
        if (":" in target or target.startswith("\\") or "/" in target or "\\" in target):
            ok, msg = open_item(target)
            return msg, None
        apps = find_app(target)
        if apps:
            ok, msg = open_item(apps[0])
            return msg, None

    return None, None

class JarvisApp:
    def __init__(self, root):
        self.root = root
        root.title(APP_NAME)
        root.geometry("940x650")
        root.minsize(720, 520)
        root.configure(bg="#02070c")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", padding=9)

        header = tk.Frame(root, bg="#06131c", height=70)
        header.pack(fill="x")
        tk.Label(header, text="J A R V I S   2 . 0", fg="#8eeaf4", bg="#06131c",
                 font=("Segoe UI", 20, "bold")).pack(side="left", padx=22, pady=17)
        self.status = tk.Label(header, text="LOCAL PC • READY", fg="#46f0b0", bg="#06131c",
                               font=("Segoe UI", 9))
        self.status.pack(side="right", padx=22)

        main = tk.Frame(root, bg="#02070c")
        main.pack(fill="both", expand=True, padx=18, pady=18)

        self.log = tk.Text(main, bg="#050f18", fg="#cceff5", insertbackground="white",
                           relief="flat", font=("Consolas", 11), wrap="word")
        self.log.pack(fill="both", expand=True, pady=(0,12))
        self.log.insert("end",
            "JARVIS 2.0 online.\n"
            "AI: connected to your existing JARVIS API\n"
            "PC tools: file search + app/file opening\n\n"
        )

        bar = tk.Frame(main, bg="#02070c")
        bar.pack(fill="x")
        self.entry = tk.Entry(bar, bg="#081722", fg="white", insertbackground="white",
                              relief="flat", font=("Segoe UI", 11))
        self.entry.pack(side="left", fill="x", expand=True, ipady=12, padx=(0,8))
        self.entry.bind("<Return>", lambda e: self.run())
        ttk.Button(bar, text="ASK JARVIS", command=self.run).pack(side="left")

        tk.Label(main,
                 text='Try: "find my PDFs"  •  "open Chrome"  •  "open C:\\Games\\game.exe"  •  ask any normal AI question',
                 fg="#54727d", bg="#02070c", font=("Segoe UI", 9)).pack(anchor="w", pady=(10,0))

    def say(self, text, who="JARVIS"):
        self.log.insert("end", f"{who}: {text}\n\n")
        self.log.see("end")

    def run(self):
        q = self.entry.get().strip()
        if not q: return
        self.entry.delete(0, "end")
        self.say(q, "YOU")
        self.status.config(text="WORKING…", fg="#ffd166")
        threading.Thread(target=self.process, args=(q,), daemon=True).start()

    def process(self, q):
        try:
            local_msg, _ = handle_local_command(q)
            if local_msg:
                self.root.after(0, lambda m=local_msg: self.say(m))
            else:
                answer = ai_reply(q)
                self.root.after(0, lambda a=answer: self.say(a))
        except urllib.error.HTTPError as e:
            self.root.after(0, lambda: self.say("The JARVIS API returned an error. Check that the original JARVIS site is working."))
        except Exception:
            self.root.after(0, lambda: self.say("I couldn't reach the JARVIS API. Check your internet connection."))
        finally:
            self.root.after(0, lambda: self.status.config(text="LOCAL PC • READY", fg="#46f0b0"))

if __name__ == "__main__":
    root = tk.Tk()
    JarvisApp(root)
    root.mainloop()
