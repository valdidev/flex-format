import tkinter as tk
from tkinter import ttk
from ui.styles import setup_dark_theme
from utils.validation import validate_input
from utils.file_operations import copy_to_clipboard, save_to_file
from converters import json_converter, xml_converter, yaml_converter

class FormatConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("FlexFormat")
        self.root.geometry("1000x800")
        self.root.minsize(900, 700)
        self.root.configure(bg="#2b2b2b")
        
        self.formats = ["JSON", "XML", "YAML"]
        self.is_input_valid = False
        self.tooltip = None
        
        setup_dark_theme()
        self.create_widgets()

    def create_widgets(self):
        format_frame = ttk.Frame(self.root)
        format_frame.pack(pady=15, padx=10, fill="x")

        format_inner_frame = ttk.Frame(format_frame)
        format_inner_frame.pack(anchor="center")

        ttk.Label(format_inner_frame).pack(side="left", padx=10)
        self.input_format = tk.StringVar(value=self.formats[0])
        input_combo = ttk.Combobox(format_inner_frame, textvariable=self.input_format, 
                                 values=self.formats, state="readonly", width=15)
        input_combo.pack(side="left", padx=10)
        input_combo.bind("<<ComboboxSelected>>", self.validate_on_format_change)

        ttk.Label(format_inner_frame).pack(side="left", padx=10)
        self.output_format = tk.StringVar(value=self.formats[1])
        output_combo = ttk.Combobox(format_inner_frame, textvariable=self.output_format, 
                                  values=self.formats, state="readonly", width=15)
        output_combo.pack(side="left", padx=10)

        self.input_label = ttk.Label(self.root, text=f"→ {self.input_format.get()}")
        self.input_label.pack(pady=5, padx=10, anchor="w")
        self.input_text = tk.Text(self.root, 
                                 height=10, 
                                 width=80, 
                                 bg="#3c3f41", 
                                 fg="#ffffff", 
                                 insertbackground="#ffffff",
                                 font=("Consolas", 10),
                                 relief="flat",
                                 borderwidth=1)
        self.input_text.pack(pady=5, padx=10, fill="both", expand=True)
        self.input_text.bind("<<Modified>>", self.validate_input)

        self.input_format.trace("w", lambda *args: self.input_label.config(text=f"→ {self.input_format.get()}"))

        self.validation_label = ttk.Label(self.root, 
                                        text="⌛ Esperando entrada", 
                                        foreground="#1e90ff")
        self.validation_label.pack(pady=5)

        self.output_label = ttk.Label(self.root, text=f"← {self.output_format.get()}")
        self.output_label.pack(pady=5, padx=10, anchor="w")
        self.output_text = tk.Text(self.root, 
                                  height=10, 
                                  width=80, 
                                  bg="#3c3f41", 
                                  fg="#ffffff", 
                                  insertbackground="#ffffff",
                                  font=("Consolas", 10),
                                  relief="flat",
                                  borderwidth=1)
        self.output_text.pack(pady=5, padx=10, fill="both", expand=True)

        self.output_format.trace("w", lambda *args: self.output_label.config(text=f"← {self.output_format.get()}"))

        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=15, padx=10)

        convert_frame = ttk.Frame(button_frame)
        convert_frame.pack(pady=10)
        ttk.Button(convert_frame, 
                  text="Convertir", 
                  command=self.convert, 
                  style="Convert.TButton",
                  cursor="hand2").pack()

        icon_frame = ttk.Frame(button_frame)
        icon_frame.pack(pady=5)

        copy_button = ttk.Button(icon_frame, 
                               text="📋", 
                               command=lambda: copy_to_clipboard(self), 
                               style="Icon.TButton",
                               width=4,
                               cursor="hand2")
        copy_button.pack(side="left", padx=5)
        copy_button.bind("<Enter>", lambda e: self.show_tooltip(copy_button, "Copiar al Portapapeles"))
        copy_button.bind("<Leave>", lambda e: self.hide_tooltip())

        save_button = ttk.Button(icon_frame, 
                               text="💾", 
                               command=lambda: save_to_file(self), 
                               style="Icon.TButton",
                               width=4,
                               cursor="hand2")
        save_button.pack(side="left", padx=5)
        save_button.bind("<Enter>", lambda e: self.show_tooltip(save_button, "Guardar como Archivo"))
        save_button.bind("<Leave>", lambda e: self.hide_tooltip())

    def show_tooltip(self, widget, text):
        if self.tooltip:
            self.tooltip.destroy()
        x, y, _, _ = widget.bbox("insert")
        x += widget.winfo_rootx() + 25
        y += widget.winfo_rooty() + 25
        self.tooltip = tk.Toplevel(widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, 
                        text=text, 
                        background="#4a4a4a", 
                        foreground="#ffffff", 
                        relief="solid", 
                        borderwidth=1,
                        font=("Segoe UI", 8))
        label.pack()

    def hide_tooltip(self):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

    def validate_input(self, event=None):
        input_text = self.input_text.get("1.0", tk.END).strip()
        input_format = self.input_format.get()
        result, is_valid = validate_input(input_text, input_format)
        self.validation_label.config(text=result["text"], foreground=result["color"])
        self.is_input_valid = is_valid
        self.input_text.edit_modified(False)

    def validate_on_format_change(self, event=None):
        self.validate_input()

    def convert(self):
        from tkinter import messagebox
        input_format = self.input_format.get()
        output_format = self.output_format.get()
        input_text = self.input_text.get("1.0", tk.END).strip()

        if not input_text:
            messagebox.showwarning("Error", "Por favor, ingresa código para convertir.")
            return

        if input_format == output_format:
            messagebox.showwarning("Error", "El formato de entrada y salida deben ser diferentes.")
            return

        if not self.is_input_valid:
            messagebox.showwarning("Error", "El código de entrada no es válido. Corrige el formato.")
            return

        try:
            data = {
                "JSON": json_converter.parse,
                "XML": xml_converter.parse,
                "YAML": yaml_converter.parse
            }[input_format](input_text)

            result = {
                "JSON": json_converter.convert,
                "XML": xml_converter.convert,
                "YAML": yaml_converter.convert
            }[output_format](data)

            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, result)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo convertir: {str(e)}")