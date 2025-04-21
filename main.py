import tkinter as tk
from ui.splash_screen import show_splash_screen
from ui.format_converter import FormatConverter

def start_app(root):
    app = FormatConverter(root)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    show_splash_screen(root, start_app)
    root.mainloop()