import json
import customtkinter as ctk
import tkinter as tk
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageTk
from tkinter import filedialog
from Vcss import  BoxNumber, InputNumber, FlatList, DraggableLabel, ImageContainer, updown_menu
from Components import ItemElement, property_image_bar, property_text_bar, Vincular_excel, property_background_bar

size = width, height = 3000, 3000


class Perzonaliced_image_creator(ctk.CTk):
    def __init__(self,*args,
                 project_name: str = 'proyecto1',
                 up_bar_data: dict = {},
                 **kwargs):
        
        super().__init__(*args, **kwargs)
        #*Configuration
        self.title("Imagenes personalizadas")
        self.geometry("400x150")
        # *variables
        self.project_name = project_name
        self.up_bar_data = up_bar_data
        self.project = {}
        #*Body
        #carga el json
        with open('./projects.json', 'r') as json_file:
            self.image_properties_json = json.load(json_file)
        #Find the project using the name
        if self.project_name != '':
            #Get the list of layers of the project
            self.project = self.image_properties_json[self.project_name]
            #Get the data for the Up_bar
            self.up_bar_data = self.project['Project'][0]
        
        #?Tool bar
        self.Tool_bar = ctk.CTkFrame(self)
        self.Tool_bar.grid(row=0, column=0 ,padx=0, pady=0, sticky="nsew")

        self.Menu_file = updown_menu(self.Tool_bar, json_list=['Guardar', 'Guardar como'], text= 'Archivo', Otros= [self.save, save_As])
        self.Menu_file.grid(row=0, column=0 ,padx=0, pady=0)

        self.Menu_add = updown_menu(self.Tool_bar, json_list=['Image', 'Folder', 'Text'], text= 'Importar', Otros= [New_image, New_folder])
        self.Menu_add.grid(row=0, column=1 ,padx=0, pady=0)

        self.Menu_link = updown_menu(self.Tool_bar, json_list=['Vincular a excel'], text= 'Vincular', Otros=[llamar_vincular_excel])
        self.Menu_link.grid(row=0, column=2 ,padx=0, pady=0)

        self.Menu_Export = updown_menu(self.Tool_bar, json_list=['Unico','Personalizado'], text= 'Exportar', Otros=[llamar_vincular_excel])
        self.Menu_Export.grid(row=0, column=3 ,padx=0, pady=0)
        #?property bar
        print(self.project)
        #self.Up_bar = property_image_bar(self, json_list= self.up_bar_data, Hook = [Relative_to, External_Move, Background_data, External_Rotate, tag_lower, tag_uper])
        #self.Up_bar.grid(row=1, column=0, padx=0, pady=(10, 0), sticky="nsew")

        #self.Up_bar_text = property_text_bar(self, json_list= self.up_bar_data, Hook=[Relative_to, Change_anchor_text, External_Move, Change_color_font, change_text])
        #self.Up_bar_text.grid(row=2, column=0 ,padx=0, pady=(10, 0), sticky="nsew")

        #self.Up_bar_background = property_background_bar(self, json_list= self.up_bar_data, Hook=[])
        #self.Up_bar_background.grid(row=1, column=0 ,padx=0, pady=(10, 0), sticky="nsew")
        
        #self.ElementList = FlatList(self, json_list=self.project, Item = ItemElement, width=200, Otros=[back_one_elements, advance_one_elements])
        #self.ElementList.grid(row=3, column=1 ,padx=5, pady=5)

        self.Image_Container = ImageContainer(self, json_list=self.project['Project'], width= 1000, function = to_image_bar, Hook = [Change_relative_to, to_image_bar])
        self.Image_Container.grid(row=3, column=0 ,padx=5, pady=5)

    #*methods
    #?Toolbar methods
    def save(self):
        #!Save the proyect if there are a active proyect
        #Search the project
        with open('./projects.json', 'r') as json_file:
            projects_json = json.load(json_file)
        #Replace the project with the actual project
        projects_json[self.project_name] = self.project
        #save the project
        with open("./proyectos.json", "w") as json_file:
            json.dump(projects_json, json_file, indent=4)
        print('saved')

    #?Project properties
    def update_project_by_id(self, project_id, new_attributes):
        for layer in self.project['project']:
            if layer["Id"] == project_id:
                #Update project attributes with new values
                layer.update(new_attributes)
                #Update the up_bar_data atributes
                self.up_bar_data.update(new_attributes)
                break

    def to_image_bar(self, lista):
        #!Change the upbar depending on the type of the element active
        self.up_bar_data = lista
        if self.up_bar_data['Type'] == 'image':
            self.Up_bar.update_image_data(self.up_bar_data)
            self.Up_bar_text.grid_forget()
            self.Up_bar_background.grid_forget()
            self.Up_bar.grid(row=1, column=0, padx=0, pady=(10, 0), sticky="nsew")
        elif self.up_bar_data['Type'] == 'text':
            self.Up_bar_text.update_text_data(self.up_bar_data)
            self.Up_bar.grid_forget()
            self.Up_bar_background.grid_forget()
            self.Up_bar_text.grid(row=1, column=0 ,padx=0, pady=(10, 0), sticky="nsew")
        elif self.up_bar_data['Type'] == 'Background':
            self.Up_bar_background.update_text_data(self.up_bar_data)
            self.Up_bar.grid_forget()
            self.Up_bar_text.grid_forget()
            self.Up_bar_text.grid(row=1, column=0 ,padx=0, pady=(10, 0), sticky="nsew")

#* PROGRAM
# *variables
project_name = 'proyecto1'
up_bar_data = {}
project = {}
#*Initialization
with open('./projects.json', 'r') as json_file:
        image_properties_json = json.load(json_file)
        #Find the project using the name
        if project_name != '':
            #Get the list of layers of the project
            project = image_properties_json[project_name]
            #Get the data for the Up_bar
            up_bar_data = project['Project'][0]
# *JSON image properties
'''with open('./projects.json', 'r') as json_file:
    image_properties_json = json.load(json_file)'''


def llamar_vincular_excel():
    Vincular_excel(app)


def button_callback():
    print("button pressed")

def to_image_bar(lista):
    up_bar_data = lista
    if up_bar_data['Type'] == 'image':
        Up_bar.update_image_data(up_bar_data)
        Up_bar_text.grid_forget()
        Up_bar_background.grid_forget()
        Up_bar.grid(row=1, column=0, padx=0, pady=(10, 0), sticky="nsew")
    elif up_bar_data['Type'] == 'text':
        Up_bar_text.update_text_data(up_bar_data)
        Up_bar.grid_forget()
        Up_bar_background.grid_forget()
        Up_bar_text.grid(row=1, column=0 ,padx=0, pady=(10, 0), sticky="nsew")
    elif up_bar_data['Type'] == 'Background':
        Up_bar_background.update_text_data(up_bar_data)
        Up_bar.grid_forget()
        Up_bar_text.grid_forget()
        Up_bar_text.grid(row=1, column=0 ,padx=0, pady=(10, 0), sticky="nsew")
    
def New_image():
    '''Desplega el cuadro de busqueda para seleccionar imagenes de
       formato jpg, png y carpetas, descartando otros tipos de documentos 
    '''
    filetypes = [("PNG files", "*.png"), ("JPG files", "*.jpg")]
    app.filename = filedialog.askopenfilename(title='Buscar recurso', filetypes=filetypes)

    def handle_click(event):
        x, y = event.x, event.y
        Image_Container.canvas.unbind("<Button-1>")  # Unbind the event after capturing the coordinates
        add_image(app.filename, x, y)
        activate_element(len(Actual_project)-1)
        Image_Container.Update_list(Actual_project)
        ElementList.Update_list(Actual_project)

    Image_Container.canvas.bind("<Button-1>", handle_click)

def New_folder():
    '''Desplega el cuadro de busqueda para seleccionar imagenes de
       formato jpg, png y carpetas, descartando otros tipos de documentos 
    '''
    filetypes = [("PNG files", "*.png"), ("JPG files", "*.jpg")]
    app.filename = filedialog.askopenfilename(title='Buscar recurso', filetypes=filetypes)

    def handle_click(event):
        x, y = event.x, event.y
        Image_Container.canvas.unbind("<Button-1>")  # Unbind the event after capturing the coordinates
        Actual_project.append({
                        "Id": len(Actual_project),
                        "Type": "Folder",
                        "Name": app.filename,
                        "Width": 150,
                        "Height": 150,
                        "Rotate": 0,
                        "x_position": x,
                        "y_position": y,
                        "xCenter": False,
                        "yCenter": False,
                        "active": True
                        })
        activate_element(len(Actual_project)-1)
        Image_Container.Update_list(Actual_project)
        ElementList.Update_list(Actual_project)

    Image_Container.canvas.bind("<Button-1>", handle_click)

def Change_relative_to(New_relative_to):
    Relative_to = New_relative_to
    #print(Relative_to)

def External_Move(Id, value, axis):
    Image_Container.External_Move(Id, value, axis)

def External_Rotate(Id, angle):
    Image_Container.External_Rotate(Id, angle)

def Change_anchor_text(Id, aling):
    Image_Container.Change_anchor(Id, aling)

def Change_color_font(Id):
    Image_Container.Change_color_font(Id)

def tag_lower(Id):
    Image_Container.tag_lower(Id)
    back_one_elements(Id)

def tag_uper(Id):
    Image_Container.tag_Uper(Id)
    advance_one_elements(Id)

def change_text(Id, Type, Text):
    Image_Container.change_text(Id, Type, Text)

def back_one_elements(Id):
    try:
        index = next(i for i, element in enumerate(Actual_project) if element['Id'] == Id and element['Id'] not in (0, 1))
        if index > 0:
            Actual_project[index - 1], Actual_project[index] = Actual_project[index], Actual_project[index - 1]
            Actual_project[index - 1]['tags'], Actual_project[index]['tags'] = Actual_project[index]['tags'], Actual_project[index - 1]['tags']
            Image_Container.advance_one_element(index-1)
            ElementList.Update_list(Actual_project)
            #print(Actual_project)
        else:
            print("Cannot move the element further back.")
    except StopIteration:
        print(f"Element with Id {Id} not found in Actual_project.")

def advance_one_elements(Id):
    try:
        index = next(i for i, element in enumerate(Actual_project) if element['Id'] == Id and element['Id'] not in (0, len(Actual_project)-1))
        if index > 0:
            Actual_project[index], Actual_project[index + 1] = Actual_project[index + 1], Actual_project[index]
            Actual_project[index]['tags'], Actual_project[index + 1]['tags'] = Actual_project[index + 1]['tags'], Actual_project[index]['tags']
            Image_Container.advance_one_element(index)
            ElementList.Update_list(Actual_project)
        else:
            print("Cannot move the element further back.")
    except StopIteration:
        print(f"Element with Id {Id} not found in Actual_project.")

def save_As(project):
    Guardado = False
    while Guardado == False:
        name_proj = tk.simpledialog.askstring("Guardar", "Ingrese un nombre para el proyecto:")

        #*Si se le asigna nombre continua codigo, si se da a cancelar solo sale de la funcion
        if name_proj:

            with open('./projects.json', 'r') as json_file:
                projects_json = json.load(json_file)
            names = list(projects_json.keys())
            #* Condicional para validar proyecto ya guardado
            for name in names:
                temp_name = name.lower()
                if name_proj.lower() == temp_name:
                    proyecto_encontrado = True # Coincidencia encontrada
                    preguntaGuardado = tk.messagebox.askquestion("Precaución", "El proyecto " + name_proj +
                        " ya existe" + "¿Desea reemplazar el proyecto existente?")                        

                    if preguntaGuardado == "yes":
                        #* Borra el que ya existe primero, luego guarda el nuevo
                        del projects_json[name]  # Elimina la clave existente
                        projects_json[name] = project  # Agrega el nuevo proyecto

                        with open("./proyectos.json", "w") as json_file:
                            json.dump(projects_json, json_file, indent=4)
                        Guardado = True
                else:
                    continue

            #* Si no se encontró el proyecto, agrégalo
            if not proyecto_encontrado:
                projects_json[str(name_proj)] = project

                with open("./proyectos.json", "w") as json_file:
                    json.dump(projects_json, json_file, indent=4)
                Guardado = True
        else:
            return


'''def save():
    #Search the project
    with open('./projects.json', 'r') as json_file:
        projects_json = json.load(json_file)
    #Replace the project with the actual project
    projects_json[project_name] = image_properties_json
    #save the project
    with open("./proyectos.json", "w") as json_file:
        json.dump(projects_json, json_file, indent=4)
    print('saved')'''



app = ctk.CTk()
app.title("Imagenes personalizadas")
app.geometry("400x150")


# *Barra de propiedades de formatos imagenes
list_property_bar = {"Id": 2,
                    "Type": "image",
                    "Width": 0,
                    "Height": 0,
                    "Rotate": 0,
                    "x_position": 0,
                    "y_position": 0,
                    "xCenter": False,
                    "yCenter": False}

Actual_project = image_properties_json['proyecto1']['Project']

Relative_to = [0,0]

Background_data = {"Id": 0,
                    "Type": "Background",
                    "Name": "caminar.jpg",
                    "Width": 300,
                    "Height": 400,
                    "Rotate": 0,
                    "x_position": 0,
                    "y_position": 0,
                    "xCenter": True,
                    "yCenter": True,
                    "BackgroundColor": "#FFFFFF",
                    "active": False}

#*Tool bar
Tool_bar = ctk.CTkFrame(app)
Tool_bar.grid(row=0, column=0 ,padx=0, pady=0, sticky="nsew")

Menu_file = updown_menu(Tool_bar, json_list=['Guardar', 'Guardar como'], text= 'Archivo', Otros= [save_As, save_As])
Menu_file.grid(row=0, column=0 ,padx=0, pady=0)

Menu_add = updown_menu(Tool_bar, json_list=['Image', 'Folder', 'Text'], text= 'Importar', Otros= [New_image, New_folder])
Menu_add.grid(row=0, column=1 ,padx=0, pady=0)

Menu_link = updown_menu(Tool_bar, json_list=['Vincular a excel'], text= 'Vincular', Otros=[llamar_vincular_excel])
Menu_link.grid(row=0, column=2 ,padx=0, pady=0)

Menu_Export = updown_menu(Tool_bar, json_list=['Unico','Personalizado'], text= 'Exportar', Otros=[llamar_vincular_excel])
Menu_Export.grid(row=0, column=3 ,padx=0, pady=0)
#*property bar
Up_bar = property_image_bar(app, json_list= up_bar_data, Hook = [Relative_to, External_Move, up_bar_data, External_Rotate, tag_lower, tag_uper])
Up_bar.grid(row=1, column=0, padx=0, pady=(10, 0), sticky="nsew")

Up_bar_text = property_text_bar(app, json_list= up_bar_data, Hook=[Relative_to, Change_anchor_text, External_Move, Change_color_font, change_text])
Up_bar_text.grid(row=2, column=0 ,padx=0, pady=(10, 0), sticky="nsew")

Up_bar_background = property_background_bar(app, json_list= up_bar_data, Hook=[])
Up_bar_background.grid(row=1, column=0 ,padx=0, pady=(10, 0), sticky="nsew")

#*Container
ElementList = FlatList(app, json_list=Actual_project, Item = ItemElement, width=200, Otros=[back_one_elements, advance_one_elements])
ElementList.grid(row=3, column=1 ,padx=5, pady=5)

Image_Container = ImageContainer(app, json_list=Actual_project, width= 1000, function = to_image_bar, Hook = [Change_relative_to, to_image_bar])
Image_Container.grid(row=3, column=0 ,padx=5, pady=5)


background_image = Image.new('RGB',size, 'white')



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
                        "active": True,
                        "tags": len(Actual_project)
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

#v = Perzonaliced_image_creator()
#v.mainloop()
