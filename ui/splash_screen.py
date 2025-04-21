import tkinter as tk
from PIL import Image, ImageTk  # Necesitarás instalar Pillow: pip install Pillow

def show_splash_screen(root, callback):
    splash = tk.Toplevel(root)
    splash.overrideredirect(True)  # Remove window borders
    splash.configure(bg="#2b2b2b")

    # Aumentamos un poco el tamaño para acomodar la imagen
    splash_width = 400
    splash_height = 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - splash_width) // 2
    y = (screen_height - splash_height) // 2
    splash.geometry(f"{splash_width}x{splash_height}+{x}+{y}")

    try:
        # Cargar la imagen
        img = Image.open("flexformat.png")  # Asegúrate de que la imagen está en el mismo directorio
        img = img.resize((80, 80), Image.Resampling.LANCZOS)  # Redimensionar si es necesario
        logo = ImageTk.PhotoImage(img)
        
        # Crear un frame para organizar los elementos
        frame = tk.Frame(splash, bg="#2b2b2b")
        frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Mostrar la imagen
        logo_label = tk.Label(frame, image=logo, bg="#2b2b2b")
        logo_label.image = logo  # Guardar referencia para evitar que la imagen sea eliminada por el garbage collector
        logo_label.pack(side='top', pady=(0, 10))
        
        # Añadir el texto
        label = tk.Label(
            frame,
            text="FlexFormat",
            bg="#2b2b2b",
            fg="#ffffff",
            font=("Segoe UI", 24, "bold")
        )
        label.pack(side='top')
        
    except Exception as e:
        print(f"No se pudo cargar la imagen: {e}")
        # Si hay error, mostrar solo el texto
        label = tk.Label(
            splash,
            text="FlexFormat",
            bg="#2b2b2b",
            fg="#ffffff",
            font=("Segoe UI", 24, "bold")
        )
        label.pack(expand=True)

    # Destroy splash and start main app after 2000ms
    root.after(2000, lambda: [splash.destroy(), root.deiconify(), callback(root)])