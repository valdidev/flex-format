import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from converters import json_converter, xml_converter, yaml_converter

class FormatConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("FlexFormat")
        self.root.geometry("1000x800")  # Tamaño inicial más grande
        self.root.minsize(900, 700)  # Tamaño mínimo obligatorio
        self.root.configure(bg="#2b2b2b")  # Dark background
        
        # Formatos soportados
        self.formats = ["JSON", "XML", "YAML"]
        
        # Estado de validación
        self.is_input_valid = False
        
        # Configurar estilo oscuro
        self.setup_dark_theme()
        
        # Interfaz gráfica
        self.create_widgets()

    def setup_dark_theme(self):
        style = ttk.Style()
        
        # Configurar tema base
        style.theme_use("clam")
        
        # Colores del tema oscuro
        dark_bg = "#2b2b2b"
        dark_fg = "#ffffff"
        dark_field_bg = "#3c3f41"
        dark_select_bg = "#4a4a4a"
        accent_color = "#0078d7"  # Azul profesional
        
        # Configurar estilos
        style.configure("TFrame", background=dark_bg)
        style.configure("TLabel", background=dark_bg, foreground=dark_fg, font=("Segoe UI", 10))
        style.configure("TCombobox", 
                        fieldbackground=dark_field_bg, 
                        background=dark_select_bg, 
                        foreground=dark_fg,
                        selectbackground=accent_color,
                        selectforeground=dark_fg)
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
        
        # Estilo para el botón Convertir
        style.configure("Convert.TButton",
                        background=accent_color,
                        foreground=dark_fg,
                        font=("Segoe UI", 12, "bold"),
                        padding=10)
        style.map("Convert.TButton",
                  background=[("active", "#005ea6")],
                  foreground=[("active", dark_fg)])
        
        # Estilo para botones de iconos
        style.configure("Icon.TButton",
                        background=dark_select_bg,
                        foreground=dark_fg,
                        font=("Segoe UI", 12),
                        padding=5)
        style.map("Icon.TButton",
                  background=[("active", accent_color)],
                  foreground=[("active", dark_fg)])

    def create_widgets(self):
        # Frame para selección de formatos
        format_frame = ttk.Frame(self.root)
        format_frame.pack(pady=15, padx=10, fill="x")

        ttk.Label(format_frame, text="Formato de Entrada:").pack(side="left", padx=10)
        self.input_format = tk.StringVar(value=self.formats[0])
        input_combo = ttk.Combobox(format_frame, textvariable=self.input_format, 
                                 values=self.formats, state="readonly", width=10)
        input_combo.pack(side="left", padx=10)
        input_combo.bind("<<ComboboxSelected>>", self.validate_on_format_change)

        ttk.Label(format_frame, text="Formato de Salida:").pack(side="left", padx=10)
        self.output_format = tk.StringVar(value=self.formats[1])
        output_combo = ttk.Combobox(format_frame, textvariable=self.output_format, 
                                  values=self.formats, state="readonly", width=10)
        output_combo.pack(side="left", padx=10)

        # Área de texto para entrada
        ttk.Label(self.root, text="Código de Entrada:").pack(pady=5, padx=10, anchor="w")
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

        # Etiqueta para mostrar estado de validación
        self.validation_label = ttk.Label(self.root, 
                                        text="Estado: Esperando entrada", 
                                        foreground="#1e90ff")
        self.validation_label.pack(pady=5)

        # Área de texto para salida (vista previa)
        ttk.Label(self.root, text="Resultado Convertido:").pack(pady=5, padx=10, anchor="w")
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

        # Botones
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=15, padx=10)

        # Botón Convertir (centrado y destacado)
        convert_frame = ttk.Frame(button_frame)
        convert_frame.pack(pady=10)
        ttk.Button(convert_frame, 
                  text="Convertir", 
                  command=self.convert, 
                  style="Convert.TButton",
                  cursor="hand2").pack()

        # Frame para botones de iconos
        icon_frame = ttk.Frame(button_frame)
        icon_frame.pack(pady=5)

        # Botón Copiar al Portapapeles (ícono)
        copy_button = ttk.Button(icon_frame, 
                               text="📋", 
                               command=self.copy_to_clipboard, 
                               style="Icon.TButton",
                               width=4,
                               cursor="hand2")
        copy_button.pack(side="left", padx=5)
        copy_button.bind("<Enter>", lambda e: self.show_tooltip(copy_button, "Copiar al Portapapeles"))
        copy_button.bind("<Leave>", lambda e: self.hide_tooltip())

        # Botón Guardar como Archivo (ícono)
        save_button = ttk.Button(icon_frame, 
                               text="💾", 
                               command=self.save_to_file, 
                               style="Icon.TButton",
                               width=4,
                               cursor="hand2")
        save_button.pack(side="left", padx=5)
        save_button.bind("<Enter>", lambda e: self.show_tooltip(save_button, "Guardar como Archivo"))
        save_button.bind("<Leave>", lambda e: self.hide_tooltip())

        # Configurar tooltip
        self.tooltip = None

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

        if not input_text:
            self.validation_label.config(text="Estado: Entrada vacía", foreground="#1e90ff")
            self.is_input_valid = False
            return

        try:
            if input_format == "JSON":
                json_converter.parse(input_text)
                self.validation_label.config(text="Estado: JSON válido", foreground="#32cd32")
                self.is_input_valid = True
            elif input_format == "XML":
                xml_converter.parse(input_text)
                self.validation_label.config(text="Estado: XML válido", foreground="#32cd32")
                self.is_input_valid = True
            elif input_format == "YAML":
                yaml_converter.parse(input_text)
                self.validation_label.config(text="Estado: YAML válido", foreground="#32cd32")
                self.is_input_valid = True
        except Exception as e:
            self.validation_label.config(text=f"Estado: Formato inválido ({str(e)})", 
                                      foreground="#ff4040")
            self.is_input_valid = False

        # Resetear la bandera de modificación
        self.input_text.edit_modified(False)

    def validate_on_format_change(self, event=None):
        self.validate_input()

    def convert(self):
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
            # Parsear entrada
            if input_format == "JSON":
                data = json_converter.parse(input_text)
            elif input_format == "XML":
                data = xml_converter.parse(input_text)
            elif input_format == "YAML":
                data = yaml_converter.parse(input_text)

            # Convertir a formato de salida
            if output_format == "JSON":
                result = json_converter.convert(data)
            elif output_format == "XML":
                result = xml_converter.convert(data)
            elif output_format == "YAML":
                result = yaml_converter.convert(data)

            # Mostrar resultado
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, result)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo convertir: {str(e)}")

    def copy_to_clipboard(self):
        result = self.output_text.get("1.0", tk.END).strip()
        if result:
            self.root.clipboard_clear()
            self.root.clipboard_append(result)
            self.root.update()
            messagebox.showinfo("Éxito", "Resultado copiado al portapapeles.")
        else:
            messagebox.showwarning("Error", "No hay resultado para copiar.")

    def save_to_file(self):
        result = self.output_text.get("1.0", tk.END).strip()
        if not result:
            messagebox.showwarning("Error", "No hay resultado para guardar.")
            return

        file_ext = {"JSON": ".json", "XML": ".xml", "YAML": ".yaml"}
        ext = file_ext.get(self.output_format.get(), ".txt")
        file_path = filedialog.asksaveasfilename(
            defaultextension=ext,
            filetypes=[(f"{self.output_format.get()} files", f"*{ext}"), 
                      ("All files", "*.*")]
        )
        
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(result)
            messagebox.showinfo("Éxito", f"Resultado guardado en {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FormatConverter(root)
    root.mainloop()