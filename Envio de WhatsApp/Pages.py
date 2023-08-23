import customtkinter as ctk
import tkinter
from typing import Tuple, Callable
from Vcss import FlatList, El_Tab_view
from components import ItemProject, Table
import whasApp
import json

#*colores
CGreen = "#1C9F80"
CGreen_hov = "#115e45"

#*Frame de proyectos-------------------------------------------------------
class Los_proyectos(ctk.CTkFrame):
    def __init__(self, 
                 master: any,
                 El_metodo: Callable = None,
                 width: int = 200,
                 height: int = 200,
                 corner_radius: int | str | None = 0,
                 fg_color: str | Tuple[str, str] | None = None,
                 *args,
                 **kwargs):
        super().__init__(master, *args, width=width, height=height, corner_radius=corner_radius,
                    fg_color=fg_color, **kwargs)

        self.next = El_metodo

        #*Colores
        self.CGreen = "#1C9F80"
        self.CGreen_hov = "#115e45"

        self.configure(fg_color="white", width = 1018)
        self.pack(padx=55, pady=55)

        #panel izquierdo
        self.frame_iz = ctk.CTkFrame(self, fg_color = 'transparent', border_width=0, 
            border_color='black')#394
        self.frame_iz.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

        self.unTexto = ctk.CTkLabel(self.frame_iz, text="Proyectos", text_color="black", font=('', 24))
        self.unTexto.place(relx=0.1, rely=0.1, anchor='nw')

        with open('./proyectos.json', 'r') as json_file:
            projects_json = json.load(json_file)

        self.ListaDeProyectos = FlatList(self.frame_iz, json_list=projects_json, Item=ItemProject, width= 200)
        self.ListaDeProyectos.pack(side=tkinter.LEFT, expand=True)


        #panel derecho
        self.frame_der = ctk.CTkFrame(self, fg_color = 'transparent', border_width=0,
            border_color='black')#394
        self.frame_der.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=True)

        self.unTexto2 = ctk.CTkLabel(self.frame_der,text="Nuevo Proyecto",text_color="black",font=('', 24))
        self.unTexto2.place(relx=0.1, rely=0.1, anchor='nw')

        self.el_entry = ctk.CTkEntry(self.frame_der, placeholder_text="Seleccionar Excel", fg_color="#D9D9D9",
            text_color='black', font=('', 18), border_width=0, corner_radius=0)
        self.el_entry.place(relx=0.1, rely=0.17, relwidth=0.7, relheight=0.06, anchor='nw')

        self.el_btn = ctk.CTkButton(self.frame_der, text="Buscar", corner_radius=0, fg_color=self.CGreen,
            hover_color="#115e45", font=('', 18), command='self.buscar_xl')
        self.el_btn.place(relx=0.1, rely=0.25, anchor='nw')

        self.Separador = ctk.CTkLabel(self, fg_color=self.CGreen, text='', width=0)
        self.Separador.place(relx=0.49, rely=0.08, relwidth=0.005, relheight=0.84, anchor='n')

        self.btn_sig = ctk.CTkButton(self.frame_der, text="Siguiente", corner_radius=0, fg_color=self.CGreen,
            hover_color='#115e45', font=('', 18), command=self.btn_sig_funct)
        self.btn_sig.place(relx=0.9, rely=0.92, anchor='se')

    def btn_sig_funct(self):
        if self.el_entry.get() != '':
            whasApp.set_xl(self.el_entry.get())
            #lista = whasApp.read_first_row()
            #La_tablajs = Table(self.Frame2, t_lista=lista, width=900)
        self.next()

class Vars(ctk.CTkFrame):
    def __init__(self,
                 *args,
                 master: any,
                 El_metodo: Callable = None,
                 width: int = 200,
                 height: int = 200,
                 corner_radius: int | str | None = 0,
                 fg_color: str | Tuple[str, str] | None = None,
                 **kwargs):
        super().__init__(master, *args, width=width, height=height, corner_radius=corner_radius,
                fg_color=fg_color, **kwargs)

        self.configure(fg_color='white')

        #whasApp.set_xl(r'C:\Users\pc\Desktop\Numero_mensaje_whatsapp.xlsx')
        #self.lista = whasApp.read_first_row()
        #self.La_tablajs = Table(self, t_lista=self.lista, width=900)
    
