import tkinter as tk
from tkinter import messagebox
import os, subprocess, sys

# Detecta la ruta real donde está este script
RUTA_BASE = os.path.dirname(os.path.abspath(__file__))

def ejecutar_script(carpeta, script_nombre="main.py", ruta_base=RUTA_BASE):
    ruta_script = os.path.join(ruta_base, carpeta, script_nombre)
    if os.path.isfile(ruta_script):
        subprocess.Popen([sys.executable, ruta_script], cwd=os.path.join(ruta_base, carpeta))
    else:
        messagebox.showerror("Error", f"No se encontró '{script_nombre}' en {carpeta}")

def crear_menu(ruta_base=RUTA_BASE, script_nombre="main.py"):
    carpetas = [f for f in os.listdir(ruta_base) if os.path.isdir(os.path.join(ruta_base, f))]
    ventana = tk.Tk()
    ventana.title("Selector de Juego")
    tk.Label(ventana, text="Selecciona un módulo para ejecutar:", font=("Arial", 14)).pack(pady=10)

    for carpeta in carpetas:
        boton = tk.Button(
            ventana,
            text=carpeta,
            width=30,
            command=lambda c=carpeta: ejecutar_script(c, script_nombre, ruta_base)
        )
        boton.pack(pady=5)

    ventana.mainloop()

if __name__ == "__main__":
    crear_menu()