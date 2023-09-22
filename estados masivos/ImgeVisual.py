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

def to_image_bar(lista):
    list_property_bar = lista
    Up_bar.update_image_data(list_property_bar)
    
def Buscar():
    '''Desplega el cuadro de busqueda para seleccionar imagenes de
       formato jpg, png y carpetas, descartando otros tipos de documentos 
    '''
    app.filename = filedialog.askopenfilename(title='Buscar recurso')

    def handle_click(event):
        x, y = event.x, event.y
        Image_Container.canvas.unbind("<Button-1>")  # Unbind the event after capturing the coordinates
        add_image(app.filename, x, y)
        activate_element(len(Actual_project)-1)
        Image_Container.Update_list(Actual_project)
        ElementList.Update_list(Actual_project)

    Image_Container.canvas.bind("<Button-1>", handle_click)

def Change_relative_to(New_relative_to):
    Relative_to = New_relative_to
    #print(Relative_to)

def External_Move(Id, value, axis):
    Image_Container.External_Move(Id, value, axis)

app = ctk.CTk()
app.title("Imagenes personalizadas")
app.geometry("400x150")
button = ctk.CTkButton(app, text="Subir", command=Buscar)
button.grid(row=1, column=0, padx=10, pady=10)

# *Barra de propiedades de formatos imagenes
list_property_bar = {"Id": 2,
                    "Width": 0,
                    "Height": 0,
                    "Rotate": 0,
                    "x_position": 0,
                    "y_position": 0,
                    "xCenter": False,
                    "yCenter": False}

Actual_project = image_properties_json['proyecto1']

Relative_to = [0,0]


#spinbox_1 = ItemElement(app, json_list=image_properties_json['proyecto1'])
#spinbox_1.grid(row=2, column=0 ,padx=5, pady=5)

ElementList = FlatList(app, json_list=Actual_project, Item = ItemElement, width=300)
ElementList.grid(row=3, column=1 ,padx=5, pady=5)

Image_Container = ImageContainer(app, json_list=Actual_project, width= 1000, function = to_image_bar, Hook = [Change_relative_to, to_image_bar])
Image_Container.grid(row=3, column=0 ,padx=5, pady=5)

Up_bar = property_image_bar(app, json_list= list_property_bar, Hook = [Relative_to, External_Move])
Up_bar.grid(row=0, column=0, padx=0, pady=(10, 0), sticky="nsew")

background_image = Image.new('RGB',size, 'white')
#image_tk = ctk.CTkImage(background_image, size=background_image.size)

#frameImage = ctk.CTkLabel(ImageContainer, image=image_tk, text="")
#frameImage = DraggableLabel(app, image=background_image)
#frameImage.place(x=300, rely=5)


def capture_click_coordinates(event,x, y):
    # Get the x and y coordinates of the click
    x, y = event.x, event.y
    #return (x,y)

def add_image(path, x , y):
    Actual_project.append({
                        "Id": len(Actual_project),
                        "Type": "image",
                        "Name": path,
                        "Width": 150,
                        "Height": 150,
                        "Rotate": 0,
                        "x_position": x,
                        "y_position": y,
                        "xCenter": False,
                        "yCenter": False,
                        "active": True
                        })

def activate_element(Id):
    for element in Actual_project:
        if element['Id'] == Id:
            element['active'] = True
        elif element['Id'] != Id:
            element['active'] = False

def comparing_elemts(List1, List2):
    symmetric_diff = list(set(List1) ^ set(List2))

    print("Symmetric Difference:", symmetric_diff)


app.mainloop()