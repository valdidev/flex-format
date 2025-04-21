from tkinter import ttk

def setup_dark_theme():
    style = ttk.Style()
    style.theme_use("clam")
    
    dark_bg = "#2b2b2b"
    dark_fg = "#ffffff"
    dark_field_bg = "#3c3f41"
    dark_select_bg = "#4a4a4a"
    accent_color = "#0078d7"
    
    style.configure("TFrame", background=dark_bg)
    style.configure("TLabel", background=dark_bg, foreground=dark_fg, font=("Segoe UI", 12))
    style.configure("TCombobox", 
                    fieldbackground=dark_field_bg, 
                    background=dark_select_bg, 
                    foreground=dark_fg,
                    selectbackground=accent_color,
                    selectforeground=dark_fg,
                    font=("Segoe UI", 12))
    style.map("TCombobox", 
              fieldbackground=[("readonly", dark_field_bg)],
              selectbackground=[("readonly", dark_select_bg)],
              selectforeground=[("readonly", dark_fg)])
    
    style.configure("TButton", 
                    background=dark_select_bg, 
                    foreground=dark_fg, 
                    font=("Segoe UI", 10),
                    padding=5)
    style.map("TButton",
              background=[("active", accent_color)],
              foreground=[("active", dark_fg)])
    
    style.configure("Convert.TButton",
                    background=accent_color,
                    foreground=dark_fg,
                    font=("Segoe UI", 12, "bold"),
                    padding=10)
    style.map("Convert.TButton",
              background=[("active", "#005ea6")],
              foreground=[("active", dark_fg)])
    
    style.configure("Icon.TButton",
                    background=dark_select_bg,
                    foreground=dark_fg,
                    font=("Segoe UI", 12),
                    padding=5)
    style.map("Icon.TButton",
              background=[("active", accent_color)],
              foreground=[("active", dark_fg)])