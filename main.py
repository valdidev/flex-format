import tkinter as tk
from ui.format_converter import FormatConverter

if __name__ == "__main__":
    root = tk.Tk()
    app = FormatConverter(root)
    root.mainloop()