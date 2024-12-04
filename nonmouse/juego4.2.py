from tkinter import *

root = Tk()

framesNum = 2 # Número de frames que tiene el gif
archivo = r"C:\Users\Toshiba\Documents\git\IHC(grupos)\prueba2\IHCproyect\images\juego4\insecto1.gif"

# Lista de todas las imágenes del gif
frames = [PhotoImage(file=archivo, format='gif -index %i' %(i)) for i in range(framesNum)]

# Obtener las dimensiones de la primera imagen del gif
width = frames[0].width()
height = frames[0].height()

# Crear el canvas con las dimensiones de la imagen
canvas = Canvas(root, width=width, height=height)
canvas.pack()

# Colocar un fondo de color (ejemplo: fondo blanco)
canvas.create_rectangle(0, 0, width, height, fill="lightblue", outline="")

def update(ind):
    """ Actualiza la imagen gif """
    frame = frames[ind]
    ind += 1
    if ind == framesNum:
        ind = 0
    # Actualizar la imagen en el canvas, con el fondo ya dibujado
    canvas.create_image(0, 0, image=frame, anchor=NW)
    root.after(20, update, ind) # Número que regula la velocidad del gif

root.after(0, update, 0)
root.mainloop()