import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from converters import json_converter, xml_converter, yaml_converter

class FormatConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("FlexFormat")
        self.root.geometry("800x600")
        
        # Formatos soportados
        self.formats = ["JSON", "XML", "YAML"]
        
        # Estado de validación
        self.is_input_valid = False
        
        # Interfaz gráfica
        self.create_widgets()

    def create_widgets(self):
        # Frame para selección de formatos
        format_frame = tk.Frame(self.root)
        format_frame.pack(pady=10, fill="x")

        tk.Label(format_frame, text="Formato de Entrada:").pack(side="left", padx=5)
        self.input_format = tk.StringVar(value=self.formats[0])
        input_combo = ttk.Combobox(format_frame, textvariable=self.input_format, 
                                 values=self.formats, state="readonly", width=10)
        input_combo.pack(side="left", padx=5)
        input_combo.bind("<<ComboboxSelected>>", self.validate_on_format_change)

        tk.Label(format_frame, text="Formato de Salida:").pack(side="left", padx=5)
        self.output_format = tk.StringVar(value=self.formats[1])
        output_combo = ttk.Combobox(format_frame, textvariable=self.output_format, 
                                  values=self.formats, state="readonly", width=10)
        output_combo.pack(side="left", padx=5)

        # Área de texto para entrada
        tk.Label(self.root, text="Código de Entrada:").pack(pady=5)
        self.input_text = tk.Text(self.root, height=10, width=80)
        self.input_text.pack(pady=5)
        self.input_text.bind("<<Modified>>", self.validate_input)

        # Etiqueta para mostrar estado de validación
        self.validation_label = tk.Label(self.root, text="Estado: Esperando entrada", 
                                       foreground="blue")
        self.validation_label.pack(pady=5)

        # Área de texto para salida (vista previa)
        tk.Label(self.root, text="Resultado Convertido:").pack(pady=5)
        self.output_text = tk.Text(self.root, height=10, width=80)
        self.output_text.pack(pady=5)

        # Botones
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Convertir", command=self.convert).pack(side="left", padx=5)
        tk.Button(button_frame, text="Copiar al Portapapeles", command=self.copy_to_clipboard).pack(side="left", padx=5)
        tk.Button(button_frame, text="Guardar como Archivo", command=self.save_to_file).pack(side="left", padx=5)

    def validate_input(self, event=None):
        input_text = self.input_text.get("1.0", tk.END).strip()
        input_format = self.input_format.get()

        if not input_text:
            self.validation_label.config(text="Estado: Entrada vacía", foreground="blue")
            self.is_input_valid = False
            return

        try:
            if input_format == "JSON":
                json_converter.parse(input_text)
                self.validation_label.config(text="Estado: JSON válido", foreground="green")
                self.is_input_valid = True
            elif input_format == "XML":
                xml_converter.parse(input_text)
                self.validation_label.config(text="Estado: XML válido", foreground="green")
                self.is_input_valid = True
            elif input_format == "YAML":
                yaml_converter.parse(input_text)
                self.validation_label.config(text="Estado: YAML válido", foreground="green")
                self.is_input_valid = True
        except Exception as e:
            self.validation_label.config(text=f"Estado: Formato inválido ({str(e)})", 
                                      foreground="red")
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