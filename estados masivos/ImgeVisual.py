import json
import customtkinter as ctk
import tkinter as tk
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageTk
from tkinter import filedialog
from Vcss import  BoxNumber, InputNumber, FlatList, DraggableLabel, ImageContainer, updown_menu
from Components import ItemElement, property_image_bar, property_text_bar, Vincular_excel, property_background_bar
import numpy as np
import openpyxl
import os

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
        self.project_layers = []
        #*Body
        #carga el json
        with open('./projects.json', 'r') as json_file:
            self.image_properties_json = json.load(json_file)
        #Find the project using the name
        if self.project_name != '':
            #Get the list of layers of the project
            self.project = image_properties_json[project_name]
            self.project_layers = project['Project']
            #Get the data for the Up_bar
            self.up_bar_data = project['Project'][0]
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
        #print(self.project)
        #self.Up_bar = property_image_bar(self, json_list= self.up_bar_data, Hook = [Relative_to, External_Move, self.project['Project'][0], External_Rotate, tag_lower, tag_uper])
        #self.Up_bar.grid(row=1, column=0, padx=0, pady=(10, 0), sticky="nsew")

        #self.Up_bar_text = property_text_bar(self, json_list= self.up_bar_data, Hook=[Relative_to, Change_anchor_text, External_Move, Change_color_font, change_text])
        #self.Up_bar_text.grid(row=2, column=0 ,padx=0, pady=(10, 0), sticky="nsew")

        self.Up_bar_background = property_background_bar(self, json_list= self.up_bar_data, Hook=[])
        self.Up_bar_background.grid(row=1, column=0 ,padx=0, pady=(10, 0), sticky="nsew")
        
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

#* PROGRAM %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# *variables
project_name = 'proyecto1'
project_layers = []
up_bar_data = {}
project = {}
Relative_to = [0,0]
#*Initialization
with open('./projects.json', 'r') as json_file:
        image_properties_json = json.load(json_file)
        #Find the project using the name
        if project_name != '':
            #Get the list of layers of the project
            project = image_properties_json[project_name]
            project_layers = project['Project']
            #Get the data for the Up_bar
            up_bar_data = project['Project'][0]
# *JSON image properties
'''with open('./projects.json', 'r') as json_file:
    image_properties_json = json.load(json_file)'''

#*Functions
def update_project(new_project):
    new_project_id = new_project['Id']
    for i in range(len(project_layers)):
        if project_layers[i]['Id'] == new_project_id:
            project['Project'][i] = new_project

def llamar_vincular_excel():
    V_excel = Vincular_excel(app, F_vincular= vincular_a_excel, data_link=project['Link'])


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
        Up_bar_background.Update_bg_data(up_bar_data)
        Up_bar.grid_forget()
        Up_bar_text.grid_forget()
        Up_bar_background.grid(row=1, column=0 ,padx=0, pady=(10, 0), sticky="nsew")
    update_project(up_bar_data)
    
    
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
        activate_element(len(project)-1)
        Image_Container.Update_list(project)
        ElementList.Update_list(project)

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
        project.append({
                        "Id": len(project),
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
        activate_element(len(project)-1)
        Image_Container.Update_list(project)
        ElementList.Update_list(project)


    Image_Container.canvas.bind("<Button-1>", handle_click)

def Change_relative_to(New_relative_to):
    global Relative_to 
    Relative_to = New_relative_to
    Up_bar.Change_relative_to(Relative_to)
    Up_bar_text.Change_relative_to(Relative_to)
    print(Relative_to)

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
        index = next(i for i, element in enumerate(project_layers) if element['Id'] == Id and element['Id'] not in (0, 1))
        if index > 0:
            project_layers[index - 1], project_layers[index] = project_layers[index], project_layers[index - 1]
            project_layers[index - 1]['tags'], project_layers[index]['tags'] = project_layers[index]['tags'], project_layers[index - 1]['tags']
            Image_Container.advance_one_element(index-1)
            ElementList.Update_list(project_layers)
            project['Project'] = project_layers
        else:
            print("Cannot move the element further back.")
    except StopIteration:
        print(f"Element with Id {Id} not found in Actual_project.")

def advance_one_elements(Id):
    try:
        index = next(i for i, element in enumerate(project_layers) if element['Id'] == Id and element['Id'] not in (0, len(project_layers)-1))
        if index > 0:
            project_layers[index], project_layers[index + 1] = project_layers[index + 1], project_layers[index]
            project_layers[index]['tags'], project_layers[index + 1]['tags'] = project_layers[index + 1]['tags'], project_layers[index]['tags']
            Image_Container.advance_one_element(index)
            ElementList.Update_list(project_layers)
            project['Project'] = project_layers
        else:
            print("Cannot move the element further back.")
    except StopIteration:
        print(f"Element with Id {Id} not found in Actual_project.")

def save_As():
    Guardado = False
    while Guardado == False:
        name_proj = tk.simpledialog.askstring("Guardar", "Ingrese un nombre para el proyecto:")

        #*Si se le asigna nombre continua codigo, si se da a cancelar solo sale de la funcion
        if name_proj:

            with open('./projects.json', 'r') as json_file:
                projects_json = json.load(json_file)
            names = list(projects_json.keys())
            #* Condicional para validar proyecto ya guardado
            proyecto_encontrado = False
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

                        with open("./projects.json", "w") as json_file:
                            json.dump(projects_json, json_file, indent=4)
                        Guardado = True
                else:
                    continue

            #* Si no se encontró el proyecto, agrégalo
            if not proyecto_encontrado:
                projects_json[str(name_proj)] = project

                with open("./projects.json", "w") as json_file:
                    json.dump(projects_json, json_file, indent=4)
                Guardado = True
        else:
            return


def save():
    #Search the project
    with open('./projects.json', 'r') as json_file:
        projects_json = json.load(json_file)
    #Replace the project with the actual project
    projects_json[project_name] = project
    #save the project
    with open("./projects.json", "w") as json_file:
        json.dump(projects_json, json_file, indent=4)
    print('saved')

def vincular_a_excel(Datos):
    #Change the link to the given data 
    project['Link'] = Datos

def Bg_change_size(size, value):
    Image_Container.change_size_Bg(size, value)
    

def Bg_change_color():
    Image_Container.bg_color()

#? Functions to export the image #################################
#! This function is the most important to change the image's properties
def properties(image, property):
    i = Image.open(image)
    #resize the image
    resized_image = i.resize((property['Width'], property['Height']))
    #Rotate the image
    image_rotated = resized_image.rotate(property['Rotate'], expand=True)
    # Load the PNG image and convert it to RGBA
    png_image = image_rotated.convert('RGBA')
    # Create a new RGBA image with the same size as the PNG image
    new_image = Image.new('RGBA', png_image.size, (0, 0, 0, 0))
    # Paste the PNG image on the new RGBA image with the alpha channel as the mask
    new_image.paste(png_image, (0, 0), mask=png_image.split()[3])
    return new_image

# *This function compute the size of the font to the text fits into the box
def TextBoxSize(width, height, text, font):
    windowsPath = font
    for size in range(1, np.maximum(width, height)):
        arial = ImageFont.FreeTypeFont(windowsPath, size=size)
        x_min, y_min, x_max, y_max = arial.getbbox(text)
        w = x_max - x_min
        h = y_max - y_min
        if w > width or h > height:
            break
    return [size, w, h]

def exportar_unico():
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=(("PNG files", "*.png"), ("JPEG files", "*.jpg")))
    if save_path:
        print('salvaria como', save_path)
        for Item in project['Project']:
            if Item['Type'] == 'Background':
                background_image = Image.new('RGB',(Item['Width'], Item['Height']), Item['BackgroundColor'])
            elif Item['Type'] == 'image':
                image1 = properties(Item['Name'], Item)
                # * Compute the position of the image
                x = Item['x_position']- Relative_to[0]
                y = Item['y_position']- Relative_to[1]
                # * Paste the new RGBA image with the PNG image on top of the background image
                background_image.paste(image1, (int(x),int(y)), image1)
            elif Item['Type'] == 'text':
                # *put the text into the image
                fontType = 'C:\\Windows\\Fonts\\' + 'Arial' + '.ttf'
                print(fontType)

                fontColor = tuple(map(int, Item['color'].strip('()').split(',')))
                fontSizeBox = TextBoxSize(Item['boxWidth'], Item['boxHeight'], Item['text'], fontType)
                font = ImageFont.truetype(fontType, fontSizeBox[0])
                draw = ImageDraw.Draw(background_image)

                draw.multiline_text((Item['x_position']- Relative_to[0], Item['y_position'] - Relative_to[1]), Item['text'], font=font, fill=fontColor, align=Item['align'])
        
        background_image.save(save_path)

def search_file(folder, filename):
    for f in os.listdir(folder):
        if f.startswith(filename):
            return os.path.join(folder, f)
    return None

def Exportar_personalizado():
    if project['Link']['Type'] == '':
        print('No esta vinculado a datos')
    elif project['Link']['Type'] == 'Excel':
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=(("PNG files", "*.png"), ("JPEG files", "*.jpg")))
        #save_path = filedialog.askdirectory()
        # get the data from the excel's sheet
        Data = project['Link']
        wb = openpyxl.load_workbook(Data['Path'])
        sheet = wb[Data['Sheet']]
        data = []
        Cell = Data['Cell']
        Cell_number = 0
        indices = []
        j=0

        for i, row in enumerate(sheet.iter_rows(min_row=2, values_only=True)):
            data.append(row)
            indices.append(i)

        #print(data)
        for name in {name: 0 for name in [item.value for item in sheet[1] if item.value is not None]}:
            temp_name = name.lower()
            if Cell.lower() == temp_name:
                Cell_number = j
                break
            j+=1
        if save_path:
            for row in data:

                for Item in project['Project']:
                    if Item['Type'] == 'Background':
                        background_image = Image.new('RGB',(Item['Width'], Item['Height']), Item['BackgroundColor'])
                    elif Item['Type'] == 'image':
                        image1 = properties(Item['Name'], Item)
                        # * Compute the position of the image
                        x = Item['x_position']- Relative_to[0]
                        y = Item['y_position']- Relative_to[1]
                        # * Paste the new RGBA image with the PNG image on top of the background image
                        background_image.paste(image1, (int(x),int(y)), image1)
                    elif Item['Type'] == 'text':
                        # *put the text into the image
                        fontType = 'C:\\Windows\\Fonts\\' + 'Arial' + '.ttf'
                        #print(fontType)
                        fontColor = tuple(map(int, Item['color'].strip('()').split(',')))
                        fontSizeBox = TextBoxSize(Item['boxWidth'], Item['boxHeight'], Item['text'], fontType)
                        font = ImageFont.truetype(fontType, fontSizeBox[0])
                        draw = ImageDraw.Draw(background_image)

                        draw.multiline_text((Item['x_position']- Relative_to[0], Item['y_position'] - Relative_to[1]), Item['text'], font=font, fill=fontColor, align=Item['align'])
                    elif Item['Type'] == 'Folder':
                        #for row in data:
                        fil = search_file(os.path.dirname(Item['Name']),row[Cell_number])
                        image1 = properties(fil,Item)
                        # * Compute the position of the image
                        x = Item['x_position']- Relative_to[0]
                        y = Item['y_position']- Relative_to[1]
                        # * Paste the new RGBA image with the PNG image on top of the background image
                        background_image.paste(image1, (int(x),int(y)), image1)
                #+ '/' + str(New_image[Cell_number]) + str(os.path.splitext(save_path)[1])
                #print(os.path.dirname(save_path)+ '/' + str(row[Cell_number])+ str(os.path.splitext(save_path)[1]))
                background_image.save(os.path.dirname(save_path)+ '/' + str(row[Cell_number])+ str(os.path.splitext(save_path)[1]))

def activate_element(Id):
    for element in project_layers:
        if element['Id'] == Id:
            element['active'] = True
        elif element['Id'] != Id:
            element['active'] = False
    Image_Container.activate_element(Id)
    project['Project'] = project_layers

app = ctk.CTk()
app.title("Imagenes personalizadas")
app.geometry("400x150")



#*Tool bar
Tool_bar = ctk.CTkFrame(app)
Tool_bar.grid(row=0, column=0 ,padx=0, pady=0, sticky="nsew")

Menu_file = updown_menu(Tool_bar, json_list=['Guardar', 'Guardar como'], text= 'Archivo', Otros= [save, save_As])
Menu_file.grid(row=0, column=0 ,padx=0, pady=0)

Menu_add = updown_menu(Tool_bar, json_list=['Image', 'Folder', 'Text'], text= 'Importar', Otros= [New_image, New_folder])
Menu_add.grid(row=0, column=1 ,padx=0, pady=0)

Menu_link = updown_menu(Tool_bar, json_list=['Vincular a excel'], text= 'Vincular', Otros=[llamar_vincular_excel])
Menu_link.grid(row=0, column=2 ,padx=0, pady=0)

Menu_Export = updown_menu(Tool_bar, json_list=['Unico','Personalizado'], text= 'Exportar', Otros=[exportar_unico, Exportar_personalizado])
Menu_Export.grid(row=0, column=3 ,padx=0, pady=0)
#*property bar
Up_bar = property_image_bar(app, json_list= up_bar_data, Hook = [Relative_to, External_Move, project['Project'][0], External_Rotate, tag_lower, tag_uper])
#Up_bar.grid(row=1, column=0, padx=0, pady=(10, 0), sticky="nsew")

Up_bar_text = property_text_bar(app, json_list= up_bar_data, Hook=[Relative_to, Change_anchor_text, External_Move, Change_color_font, change_text])
#Up_bar_text.grid(row=2, column=0 ,padx=0, pady=(10, 0), sticky="nsew")

Up_bar_background = property_background_bar(app, json_list= up_bar_data, Hook=[Bg_change_size, to_image_bar, Bg_change_color])
Up_bar_background.grid(row=1, column=0 ,padx=0, pady=(10, 0), sticky="nsew")

#*Container
Project_elements = ctk.CTkFrame(app)
Project_elements.grid(row=2, column=0, sticky="nsew")

ElementList = FlatList(Project_elements, json_list=project_layers, Item = ItemElement, width=200, Otros=[back_one_elements, advance_one_elements, activate_element])
ElementList.grid(row=0, column=1 ,padx=5, pady=5)

Image_Container = ImageContainer(Project_elements, json_list=project_layers, width= 1000, function = to_image_bar, Hook = [Change_relative_to, to_image_bar])
Image_Container.grid(row=0, column=0 ,padx=5, pady=5)

def capture_click_coordinates(event,x, y):
    # Get the x and y coordinates of the click
    x, y = event.x, event.y
    #return (x,y)

def add_image(path, x , y):
    project_layers.append({
                        "Id": len(project_layers),
                        "Type": "image",
                        "Name": path,
                        "Width": 150,
                        "Height": 150,
                        "Rotate": 0,
                        "x_position": x,
                        "y_position": y,
                        "active": True,
                        "tags": len(project_layers)
                        })
    project['Project'] = project_layers




def comparing_elemts(List1, List2):
    symmetric_diff = list(set(List1) ^ set(List2))

    print("Symmetric Difference:", symmetric_diff)

app.mainloop()

#v = Perzonaliced_image_creator()
#v.mainloop()
