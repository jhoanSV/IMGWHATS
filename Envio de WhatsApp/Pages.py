import customtkinter as ctk
import tkinter
from tkinter import filedialog
from typing import Tuple, Callable, Optional
from Vcss import FlatList, El_Tab_view
from components import ItemProject, Table
import whasApp
import json

#*colores
CGreen = "#1C9F80"
CGreen_hov = "#115e45"

#*Frame de proyectos-------------------------------------------------------
class Los_proyectos(ctk.CTkFrame):
    lista = []
    def __init__(self, 
                 master: any,
                 El_metodo: Callable = None,
                 width: int = 200,
                 height: int = 200,
                 corner_radius: int | str | None = 0,
                 fg_color: str | Tuple[str, str] | None = None,
                 path: str=None,
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
            self.projects_json = json.load(json_file)

        self.ListaDeProyectos = FlatList(self.frame_iz, json_list=self.projects_json, Item=ItemProject, width= 200, Otros=self.proj_selection)
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
            hover_color="#115e45", font=('', 18), command=self.buscar_xl)
        self.el_btn.place(relx=0.1, rely=0.25, anchor='nw')

        self.Separador = ctk.CTkLabel(self, fg_color=self.CGreen, text='', width=0)
        self.Separador.place(relx=0.49, rely=0.08, relwidth=0.005, relheight=0.84, anchor='n')

        self.btn_sig = ctk.CTkButton(self.frame_der, text="Siguiente", corner_radius=0, fg_color=self.CGreen,
            hover_color='#115e45', font=('', 18), command=self.btn_sig_funct)
        self.btn_sig.place(relx=0.9, rely=0.92, anchor='se')

    def btn_sig_funct(self):
        self.next(1)

    def buscar_xl(self):
        self.file_name = filedialog.askopenfilename(title='Seleccionar Excel', filetypes=(('Archivo Excel', '*.xlsx'), ('Todos los archivos', '*')))
        self.xl_path = self.file_name
        print(type(self.xl_path))
        self.el_entry.delete(0, "end")  # Limpiar el contenido del Entry
        self.el_entry.insert(0, self.xl_path)

    def proj_selection(self, rutXl, json):
        self.el_entry.delete(0, "end")
        self.el_entry.insert(0, rutXl)
        self.next(2, json)

class Vars(ctk.CTkFrame):
    def __init__(self,
                 *args,
                 master: any,
                 El_metodo: Callable = None,
                 width: int = 200,
                 height: int = 200,
                 corner_radius: int | str | None = 0,
                 fg_color: str | Tuple[str, str] | None = None,
                 path: str=None,
                 **kwargs):
        super().__init__(master, *args, width=width, height=height, corner_radius=corner_radius,
                fg_color=fg_color, **kwargs)

        self.path = r''+path
        self.configure(fg_color='white')
        whasApp.set_xl(self.path)
        #self.lista = whasApp.read_first_row()
        self.lista = whasApp.lee_excel()
        self.La_tablajs = Table(self, t_lista=self.lista, width=908)

        self.save_btn = ctk.CTkButton(self, text="Guardar", corner_radius=0, fg_color=CGreen,
            hover_color='#115e45', font=('', 18), command=self.save)
        self.save_btn.place(relx=0.8, rely=0.8, anchor='se')

    def save(self):
        print("guardar")

    #def get(self):
        

class Send(ctk.CTkFrame):
    def __init__(self,
                 *args,
                 master: any,
                 width: int = 200,
                 height: int = 200,
                 corner_radius: int | str | None = 0,
                 fg_color: str | Tuple[str, str] | None = None,
                 data_proj: Optional[dict] = None,
                 **kwargs):
        super().__init__(master, *args, width=width, height=height, corner_radius=corner_radius,
                fg_color=fg_color, **kwargs)
        
        self.data_proj = data_proj

        #self.El_metodo = El_metodo
        
        self.configure(fg_color='white')

        self.label1 = ctk.CTkLabel(self, text='Adjuntar archivos multimedia', text_color=CGreen,
            font=('', 20))
        self.label1.place(relx=0.05, rely=0.09)

        self.search_btn = ctk.CTkButton(self, text="Buscar", corner_radius=0, fg_color=CGreen,
            hover_color='#115e45', font=('', 18), command='laFuncion')
        self.search_btn.place(relx=0.05, rely=0.15, anchor='nw')
        self.entry_media = ctk.CTkEntry(self, placeholder_text="Foto/s, Video/s, carpeta", fg_color="#D9D9D9",
            text_color='black', font=('', 18), border_width=0, corner_radius=0)
        self.entry_media.place(relx=0.2, rely=0.15, relwidth=0.7, relheight=0.06, anchor='nw')

        self.label2 = ctk.CTkLabel(self, text='Mensaje', text_color=CGreen,
            font=('', 20))
        self.label2.place(relx=0.05, rely=0.25)

        self.entry_msj = ctk.CTkTextbox(self, fg_color="#D9D9D9", text_color='black',
            font=('', 18), border_width=0, corner_radius=0)
        self.entry_msj.place(relx=0.05, rely=0.3, relwidth=0.9, relheight=0.5, anchor='nw')

        self.send_btn = ctk.CTkButton(self, text="Enviar", corner_radius=0, fg_color=CGreen,
            hover_color='#115e45', font=('', 18), command=lambda: self.enviar_msj())
        self.send_btn.place(relx=0.05, rely=0.84, anchor='nw')

        #Llena entrys
        if self.data_proj:
            print(self.data_proj['msj'])
            self.entry_media.delete(0, "end")
            self.entry_media.insert(0, self.data_proj['recurso'])
            self.entry_msj.delete(0.0, "end")
            self.entry_msj.insert(0.0, self.data_proj['msj'])
    
    def enviar_msj(self):

        whasApp.envio_msj(msj=self.entry_msj.get("0.0", "end"), image_path=self.entry_media.get(), 
            variables=self.data_proj["variables"], colCelular=self.data_proj["colCelular"],
            colDestino=self.data_proj["colDestino"])
