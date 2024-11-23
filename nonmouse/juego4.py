import tkinter as tk
from .__main__ import main  # Importa la función main desde main.py

def mostrar_instrucciones():
    # Crear ventana para las instrucciones
    root = tk.Tk()
    root.title("Instrucciones")
    root.geometry("370x450")
    
    tk.Label(root, text='Instrucciones', font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(root, text='Estas son las instrucciones para continuar.').pack(pady=20)
    
    # Para jecutar el main.py
    def continuar():
        root.destroy()  # Cerrar la ventana de instrucciones
        main()  

    boton_continuar = tk.Button(root, text="Continuar", command=continuar)
    boton_continuar.pack(pady=20)
    
    root.mainloop()  # Mostrar ventana de instrucciones
