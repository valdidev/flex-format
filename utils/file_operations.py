import tkinter as tk
from tkinter import messagebox, filedialog

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