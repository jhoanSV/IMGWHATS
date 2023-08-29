import json
import customtkinter as ctk
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageTk
from tkinter import filedialog
from Vcss import  BoxNumber, InputNumber, FlatList, DraggableLabel, ImageContainer
from Components import ItemElement, property_image_bar #ImageContainer

size = width, height = 3000, 3000
# *JSON image properties
with open('./projects.json', 'r') as json_file:
    image_properties_json = json.load(json_file)


def button_callback():
    
    print("button pressed")

def Buscar():
    '''Desplega el cuadro de busqueda para seleccionar imagenes de
       formato jpg, png y carpetas, descartando otros tipos de documentos 
    '''
    global img_Tk
    app.filename = filedialog.askopenfilename(title='Buscar recurso')
    img = Image.open(app.filename)
    img_Tk = ImageTk.PhotoImage(img)
    label2 = ctk.CTkLabel(app, image=img_Tk)
    label2.grid(row=1, column=2, padx=20, pady=20)

app = ctk.CTk()
app.title("Imagenes personalizadas")
app.geometry("400x150")

button = ctk.CTkButton(app, text="Subir", command=Buscar)
button.grid(row=1, column=0, padx=10, pady=10)

# *Barra de propiedades de formatos imagenes
Up_bar = property_image_bar(app, json_list= {"Width": 200,
                                            "Height": 150,
                                            "Rotate": 6,
                                            "x_position": 17,
                                            "y_position": 7,
                                            "xCenter": True,
                                            "yCenter": True})
Up_bar.grid(row=0, column=0, padx=0, pady=(10, 0), sticky="nsew")


#spinbox_1 = ItemElement(app, json_list=image_properties_json['proyecto1'])
#spinbox_1.grid(row=2, column=0 ,padx=5, pady=5)

ElementList = FlatList(app, json_list=image_properties_json['proyecto1'], Item = ItemElement, width=300)
ElementList.grid(row=3, column=1 ,padx=5, pady=5)

Image_Container = ImageContainer(app, json_list=image_properties_json['proyecto1'], width= 1000)
Image_Container.grid(row=3, column=0 ,padx=5, pady=5)

background_image = Image.new('RGB',size, 'white')
#image_tk = ctk.CTkImage(background_image, size=background_image.size)

#frameImage = ctk.CTkLabel(ImageContainer, image=image_tk, text="")
#frameImage = DraggableLabel(app, image=background_image)
#frameImage.place(x=300, rely=5)



app.mainloop()