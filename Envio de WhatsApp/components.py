from typing import Optional, Tuple, Callable
import customtkinter as ctk
import tkinter
from tkinter import filedialog
from PIL import Image, ImageTk
from Vcss import FlatList
import json

class Wapp_Nav_bar(ctk.CTkFrame):
    def __init__():
        super().__init__()


class ItemProject(ctk.CTkFrame):
    def __init__(self, *args,
                 width: int = 700,
                 height: int = 500,
                 json_list: dict = None,  # Use dict for JSON object
                 #Project_name: str = None,
                 On_press: Optional[Callable] = None,
                 Otros: Optional[any] = None,
                 **kwargs):
        
        super().__init__(*args, **kwargs)
        self.json_list = json_list
        self.width = width
        self.height = height
        self.Project_name = Otros["Project_name"]
        self.On_press = Otros['Hook'][0]
        self.Delete = Otros['Hook'][1]
        self.configure(width=self.width, fg_color='transparent')
        self.pack()

        self.Mainframe = ctk.CTkFrame(self, width= self.width, height= self.height, fg_color='transparent')
        self.Mainframe.pack(fill='both', expand=True)
        self.Mainframe.bind("<Button-1>", self.start_drag)

        whatsappImage = ctk.CTkImage(Image.open('.\Images\WhatsApp.jpeg'), size=(40,40))

        self.ImageWhatsApp = ctk.CTkLabel(self.Mainframe, image=whatsappImage, text = "")
        self.ImageWhatsApp.pack(side='left' , fill='x', expand=True)
        self.ImageWhatsApp.bind("<Button-1>", self.start_drag)

        self.Name_Label = ctk.CTkLabel(self.Mainframe, text= self.Project_name, width= self.width - 40, text_color= '#000000', anchor='w')
        self.Name_Label.pack(side='left', fill='x', anchor='w')
        self.Name_Label.bind("<Button-1>", self.start_drag)

        self.btn_quitar = ctk.CTkButton(self.Mainframe, text='X', text_color='white', font=('', 20),
            fg_color='#BB1D1D', width=20, command=lambda: self.borrar_proyecto())
        self.btn_quitar.place(relx=1, rely=0, anchor='ne')

    def start_drag(self, event):
        if self.On_press:
            self.On_press(self.json_list['rutaXl'], self.json_list)

    def borrar_proyecto(self):        

        pregunta = tkinter.messagebox.askquestion(
            "Precaución", "Se eliminará el proyecto \"" + str(self.Project_name) + "\" ¿Desea continuar con esta acción?"
        )        

        if pregunta == "yes":
            print("Función para que se borre el proyecto")
            self.Delete(self.Project_name)
        else:
            return

    def get_data(self):        
        return self.json_list, self.Project_name
    
    def get_itemData(self):
        return
    
    def update_row(self, key ,val):        
        self.Name_Label.configure(text=key)
        self.json_list = val

class ErrorItem(ctk.CTkFrame):
    def __init__(self, *args,
                 width: int = 0,
                 height: int = 0,
                 json_list: dict = None,  # Use dict for JSON object
                 #Project_name: str = None,
                 On_press: Optional[Callable] = None,
                 Otros: Optional[any] = None,
                 **kwargs):
        
        super().__init__(*args, **kwargs)

        self.configure(fg_color='transparent', height=30, width =200)
        self.width = width
        self.height = height
        llave = next(iter(json_list))
        self.name = json_list[llave]
        self.delete = Otros['Hook']
        self.deleted = Otros['Project_name']
        
        self.el_label = ctk.CTkLabel(self, text=self.name, text_color='black', font=('', 18))
        self.el_label.place(relx=0, rely=0)

        self.btn_quitar = ctk.CTkButton(self, text='X', text_color='white', font=('', 20),
            fg_color='#BB1D1D', width=20, command=lambda: self.delete(self.deleted))
        self.btn_quitar.place(relx=1, rely=0, anchor='ne')

    def get_data(self):
        return #self.json_list, self.Project_name
    
    def get_itemData(self):
        return
    
    def update_row(self, key, val):
        llave = next(iter(val))
        texto = val[llave]
        self.el_label.configure(text=texto)
        self.deleted = key
        #self.name = texto

class Table(ctk.CTkFrame):
    def __init__(self, 
                 master: any, 
                 width: int = 200, 
                 height: int = 200, 
                 corner_radius: int | str | None = None, 
                 border_width: int | str | None = None,
                 bg_color: str | Tuple[str, str] = "transparent", 
                 fg_color: str | Tuple[str, str] | None = 'transparent', 
                 border_color: str | Tuple[str, str] | None = None,                 
                 t_lista: list | dict | None = None,
                 la_var: int=1, 
                 **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, **kwargs)
        self.la_var = la_var
        #self.width = width
        self.t_lista = t_lista #Aquí llega el diccionario de datos de la tabla

        self.pack(padx=55, pady=55, fill='x', expand=False, anchor='n')

        #*Crea cabecera de tabla----------------------------------
        self.t_head = ctk.CTkFrame(self, fg_color='white', height=40)
        self.t_head.pack(fill='x')
        self.cols = ['Columnas encontradas','celular','Nombre Destinatario']
        #Crea las 4 columnas de la cabecera
        self.f1, self.l1 = self.create_frame_and_label(self.t_head, text=self.cols[0], width=320)
        self.f2, self.l2 = self.create_frame_and_label(self.t_head, text=self.cols[1], width=86)
        self.f2, self.l2 = self.create_frame_and_label(self.t_head, text=self.cols[2], width=132)

        #*Crea cuerpo o filas de tabla-----------------------------

        self.t_body = FlatList(self, width=908, height=500, json_list=self.t_lista, Item=El_Item, Otros=self.change)
        self.t_body.pack(side='bottom', fill='both')

    def change(self, numbCol, nomCol, val):
        for i in range(len(self.t_lista)):
            var = self.t_lista[i]
            if int(numbCol) == i:
                var[nomCol] = val
            else:
                var[nomCol] = 0        
        
        self.t_body.update_list(new_list=self.t_lista)

    #!Esta funcion es para las filas de la tabla        
    def create_frame_and_label(self, parent, text, width):

        frame = ctk.CTkFrame(parent, fg_color="gray", width=width, height=40, border_width=1, corner_radius=0)
        frame.pack(side='left', expand=False, anchor='n')
        
        label = ctk.CTkLabel(frame, text_color='black', text=text, font=('',15))
        label.place(relx=0.5, rely=0.5, anchor='center')
        #label.pack()
    
        return frame, label
    
    def get_dataTable(self):
        return self.t_body.otro_get()


class El_Item(ctk.CTkFrame):
    #def __init__(self, master, destino, mob_num, val, label_text):
    def __init__(self, *args,                
                 json_list: str = 'NotFound',
                 Project_name: str=None,
                 Otros: Optional[any] = None,
                 **kwargs):
        super().__init__(*args, **kwargs)

        self.json_list = json_list
        self.nom_col = self.json_list['Columnas excel']
        self.numCol = Otros['Project_name']
        self.change = Otros['Hook']
        #self.entry_text = tkinter.StringVar()
        #self.entry_text.set(json_list['Variables'])
        #self.cel = tkinter.IntVar()
        #self.des = tkinter.IntVar()
        self.cel = tkinter.IntVar()#json_list['Celular']
        self.cel.set(self.json_list['Celular'])
        self.des = tkinter.IntVar()
        self.des.set(self.json_list['Destino'])
        self.configure(fg_color='green')
        self.pack(fill='x')


        #* Label con el nombre de col
        self.lf = ctk.CTkFrame(self, fg_color='white', width=320, height=40, corner_radius=0, border_width=1)
        self.lf.pack(side='left', fill='x', expand=True, anchor='n')
        self.l = ctk.CTkLabel(self.lf, text=self.nom_col, text_color='black', font=('', 12), fg_color='transparent')
        self.l.place(relx=0.05, rely=0.05)

        #* Entry para la variable
        '''self.ef = ctk.CTkFrame(self, fg_color='white', width=310, height=40, corner_radius=0, border_width=1)
        self.ef.pack(side='left', fill='x', expand=True, anchor='n')
        self.e = ctk.CTkEntry(self.ef, fg_color="#D9D9D9", font=('', 12), textvariable=self.entry_text,
            text_color='black', height=40)
        self.e.place(relx=0, rely=0, anchor='nw')'''

        #* Checkbox1
        self.r1f = ctk.CTkFrame(self, fg_color='white', width=86, height=40, corner_radius=0, border_width=1)
        self.r1f.pack(side='left', fill='x', expand=True, anchor='n')
        #self.checkbox1.configure(master=self.r1f)
        #self.checkbox1.place(relx=0.5, rely=0.5, anchor='center')
        self.cb1 = ctk.CTkCheckBox(self.r1f, variable=self.cel, onvalue=1, offvalue=0, width=20, text='',
            command=lambda: self.update_cel())
        self.cb1.place(relx=0.5, rely=0.5, anchor='center')
        
        #* Checkbox2
        self.r2f = ctk.CTkFrame(self, fg_color='white', width=132, height=40, corner_radius=0, border_width=1)
        self.r2f.pack(side='left', fill='x', expand=True, anchor='n')        
        #self.checkbox2.configure(master=self.r1f)
        #self.checkbox2.place(relx=0.5, rely=0.5, anchor='center')
        self.cb2 = ctk.CTkCheckBox(self.r2f, variable=self.des, onvalue=1, offvalue=0, width=20, text='',
            command=lambda: self.update_des())
        self.cb2.place(relx=0.5, rely=0.5, anchor='center')

        #self.get_itemData()

    #def 

    def update_cel(self):
        self.change(self.numCol, 'Celular', self.cb1.get())
        
    def update_des(self):
        self.change(self.numCol, 'Destino', self.cb2.get())

    def update_row(self, key, n_list):
        self.json_list=n_list
        self.cel.set(self.json_list['Celular'])
        self.des.set(self.json_list['Destino'])
        self.cb1.configure(variable=self.cel)
        self.cb2.configure(variable=self.des)

    def get_itemData(self):
        return #self.cel.get(), self.des.get(), self.nom_col


    #def update(self):

class CheckboxGroup:
    def __init__(self, master, checkbox_groups):
        self.var = tkinter.IntVar()
        self.checkbox = ctk.CTkCheckBox(master, text='', variable=self.var, command=self.update_checkboxes, width=20)
        self.checkbox.pack()
        self.checkbox_groups = checkbox_groups

    def update_checkboxes(self):
        for checkbox_group in self.checkbox_groups:
            if checkbox_group is not self:
                checkbox_group.var.set(0)