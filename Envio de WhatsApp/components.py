from typing import Optional, Tuple, Union
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
                 Project_name: str = None,
                 On_press: callable = None,
                 index: int | str | None = None,
                 **kwargs):
        
        super().__init__(*args, **kwargs)
        self.json_list = json_list
        self.width = width
        self.height = height
        self.Project_name = Project_name
        self.On_press = On_press
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

    def start_drag(self, event):
        if self.On_press:
            self.On_press

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
                 t_lista: list = None,
                 la_var: int=1, 
                 **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, **kwargs)
        self.la_var = la_var
        #self.width = width
        self.t_lista = t_lista
        self.pack(padx=55, pady=55, fill='x', expand=False, anchor='n')

        #*Crea cabecera de tabla----------------------------------
        self.t_head = ctk.CTkFrame(self, fg_color='white', height=40)
        self.t_head.pack(fill='x')
        self.cols = ['Columnas encontradas','Variables','celular','Nombre Destinatario']
        #Crea las 4 columnas de la cabecera
        self.f1, self.l1 = self.create_frame_and_label(self.t_head, text=self.cols[0], width=320)
        self.f2, self.l2 = self.create_frame_and_label(self.t_head, text=self.cols[1], width=310)
        self.f2, self.l2 = self.create_frame_and_label(self.t_head, text=self.cols[2], width=86)
        self.f2, self.l2 = self.create_frame_and_label(self.t_head, text=self.cols[3], width=132)

        #*Crea cuerpo o filas de tabla-----------------------------
        self.t_body = FlatList(self, width=908, height=500, json_list=self.t_lista, Item=El_Item)
        self.t_body.pack(side='bottom', fill='both')
    
    #!Esta funcion es para las filas de la tabla        
    def create_frame_and_label(self, parent, text, width):

        frame = ctk.CTkFrame(parent, fg_color="gray", width=width, height=40, border_width=1, corner_radius=0)
        frame.pack(side='left', expand=False, anchor='n')
        
        label = ctk.CTkLabel(frame, text_color='black', text=text, font=('',15))
        label.place(relx=0.5, rely=0.5, anchor='center')
        #label.pack()
    
        return frame, label

class El_Item(ctk.CTkFrame):
    #def __init__(self, master, destino, mob_num, val, label_text):
    def __init__(self, *args,                
                 json_list: str = 'NotFound',
                 Project_name: str=None,
                 index: int | str | None = None,
                 **kwargs):
        super().__init__(*args, **kwargs)

        self.mob_num = ctk.IntVar()
        self.destino = ctk.IntVar()
        self.valor = index
        #self.Proyect_name = Proyect_name
        self.nom_col = json_list
        self.configure(fg_color='green')
        self.pack(fill='x')

        #* Label con el nombre de col
        self.lf = ctk.CTkFrame(self, fg_color='white', width=320, height=40, corner_radius=0, border_width=1)
        self.lf.pack(side='left', fill='x', expand=True, anchor='n')
        self.l = ctk.CTkLabel(self.lf, text=self.nom_col, text_color='black', font=('', 12), fg_color='transparent')
        self.l.place(relx=0.05, rely=0.05)

        #* Entry para la variable
        self.ef = ctk.CTkFrame(self, fg_color='white', width=310, height=40, corner_radius=0, border_width=1)
        self.ef.pack(side='left', fill='x', expand=True, anchor='n')
        self.e = ctk.CTkEntry(self.ef, fg_color="#D9D9D9", font=('', 12), placeholder_text='@example',
            text_color='black', height=40)
        self.e.place(relx=0, rely=0, anchor='nw')

        #* RadioButton1
        self.r1f = ctk.CTkFrame(self, fg_color='white', width=86, height=40, corner_radius=0, border_width=1)
        self.r1f.pack(side='left', fill='x', expand=True, anchor='n')
        self.r1 = ctk.CTkRadioButton(self.r1f, variable=self.mob_num, value=self.valor, width=20,
            text='')
        self.r1.place(relx=0.5, rely=0.1, anchor='nw')
        
        #* RadioButton2
        self.r2f = ctk.CTkFrame(self, fg_color='white', width=132, height=40, corner_radius=0, border_width=1)
        self.r2f.pack(side='left', fill='x', expand=True, anchor='n')
        self.r2 = ctk.CTkRadioButton(self.r2f, variable=self.destino, value=self.valor, width=20,
            text='')
        self.r2.place(relx=0.5, rely=0.1, anchor='nw')

        self.dik = {self.nom_col:self.e.get()}
        print(self.dik)