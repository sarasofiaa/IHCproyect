from tkinter import *

root = Tk()

framesNum = 2 # Numero de frames que tiene el gif, si no lo conoces ir haciendo tentativos.
archivo = r"C:\Users\Toshiba\Documents\git\IHC(grupos)\prueba2\IHCproyect\images\juego4\insecto1.gif"

# Lista de todas las imagenes del gif
frames = [PhotoImage(file=archivo, format='gif -index %i' %(i)) for i in range(framesNum)]

# Obtener las dimensiones de la primera imagen del gif
width = frames[0].width()
height = frames[0].height()

# Crear el canvas con las dimensiones de la imagen
canvas = Canvas(root, width=width, height=height)
canvas.pack()


def update(ind):
    """ Actualiza la imagen gif """
    frame = frames[ind]
    ind += 1
    if ind == framesNum:
        ind = 0
    canvas.create_image(0, 0, image=frame, anchor=NW)
    root.after(20, update, ind) # Numero que regula la velocidad del gif

root.after(0, update, 0)
root.mainloop()