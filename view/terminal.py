from time import sleep
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading

class Terminal(threading.Thread):
    def __init__(self, title="Terminal"):
        self.title = title
        self.root = None
        self.scrolled_text = None
        threading.Thread.__init__(self)
        self.daemon = True  # terminate when the main thread terminates
        self.start()

    def close(self):
        self.root.destroy()
        self.root.update()
        self.root = None
        self.scrolled_text = None

    def run(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.title(self.title)
        self.scrolled_text = ScrolledText(self.root)
        self.scrolled_text.pack()
        self.root.mainloop()

    def print(self, text):
        if self.root is None or self.scrolled_text is None:
            return None
        else:
            self.scrolled_text.configure(state="normal")
            self.scrolled_text.see("end")
            self.scrolled_text.insert("end", text)
            self.scrolled_text.insert("end", "\n")
            self.scrolled_text.configure(state="disabled")

