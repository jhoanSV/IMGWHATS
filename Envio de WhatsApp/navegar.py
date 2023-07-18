from tkinter import *

ventana = Tk()

ventana.title("Envio whatsapp")

#Entrada de texto
e_recurso = Entry(ventana, font=("Calibri 20"))
e_recurso.grid(row=0, column=1, columnspan= 4, padx= 50, pady= 5)

#botones
boton = Button(ventana, text="Buscar", width=5, height= 2)

#agregar botones en pantalla
boton.grid( row=0, column=0, padx= 10, pady=5)
ventana.mainloop()

