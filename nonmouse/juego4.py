import tkinter as tk


def mostrar_instrucciones():
    # Crear ventana para las instrucciones
    root = tk.Tk()
    root.title("Instrucciones")
    root.geometry("370x450")
    tk.Label(root, text='Instrucciones', font=("Arial", 14, "bold")).pack(pady=10)

   

