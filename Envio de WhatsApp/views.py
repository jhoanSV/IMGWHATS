import customtkinter as ctk
import tkinter
from tkinter import filedialog
import whasApp
import json
from Vcss import FlatList, El_Tab_view
from components import ItemProject, Table, El_Item
from Pages import Los_proyectos, Vars

class colorsitos:
    def __init__(self) -> None:
        pass


class view(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.xl_path = None
        #self.cols = ['Columnas encontradas','Variables','celular','Nombre Destinatario']
        current = None        

        self.geometry("1024x728+200+5")
        self.minsize(900,640)

        #*Colores
        self.CGreen = "#1C9F80"
        self.CGreen_hov = "#115e45"

        #*configuración de la ventana 
        self.title("Wapp Sender")
        self.configure(fg_color = self.CGreen)
        
        #*root - contenedor verde principal
        self.main_container = ctk.CTkFrame(self, corner_radius=8, fg_color=self.CGreen)
        self.main_container.pack(fill=tkinter.BOTH, expand=True)

        #*Configuración del Tab_view principal
        self.main_tabV = El_Tab_view(self.main_container, num_frames=3, fg_color='transparent')
        self.main_tabV.pack(side='bottom', fill='both', expand=True)

        #Barra de navegación

        #self.nav_bar = Nav_bar(self.main_container)
        
        self.Nav_bar = ctk.CTkFrame(self.main_container, fg_color=self.CGreen, corner_radius = 0, height=77)

        self.btn_vars = ctk.CTkButton(self.Nav_bar, text="Variables", text_color=self.CGreen, corner_radius=0,
            fg_color='white', hover_color='white', font=('', 18), width=140, command=lambda: self.main_tabV.show_frame(1))
        self.btn_vars.place(x=0, rely=1, anchor='sw')

        self.btn_env = ctk.CTkButton(self.Nav_bar, text="Envío", text_color='white', corner_radius=0,
            fg_color=self.CGreen, hover_color=self.CGreen_hov, font=('', 18), width=140,
            command=lambda: self.main_tabV.show_frame(2))
        self.btn_env.place(x=140, rely=1, anchor='sw')

        #*frame1 - frame1 proyectos----------------------------------------------------------------------------
        #self.Frame_proy = Los_proyectos(self.main_tabV)
        #self.main_tabV.add_frame(0, self.Frame_proy)
        self.main_tabV.add_frame(0, Los_proyectos, self.siguiente)
        

        #frame2 - frame2 del program----------------------------------------------------------------------------
        self.main_tabV.add_frame(1, Vars)
        #self.Frame2 = ctk.CTkFrame(self.main_container, fg_color="white", corner_radius = 0)
        
        #whasApp.set_xl(r'C:\Users\pc\Desktop\Numero_mensaje_whatsapp.xlsx')
        #self.lista = whasApp.read_first_row()
        #self.La_tablajs = Table(self.Frame2, t_lista=self.lista, width=900)

        #self.leTable = ctk.CTkFrame(self.Frame2, fg_color="blue")
        #self.leTable.pack(padx=50, pady=50, fill='x', expand=True, anchor='n')

        #frame3 - frame3 del program----------------------------------------------------------------------------
        self.Frame3 = ctk.CTkFrame(self.main_container, fg_color="white", corner_radius = 0)
        
        '''self.jsjs = El_Tab_view(self.Frame3)
        self.jsjs.pack(fill='both', expand=True)

        frame_prueba = ctk.CTkFrame(self.jsjs, fg_color='blue')
        frame_prueba2 = ctk.CTkFrame(self.jsjs, fg_color='green')
        self.jsjs.add_frame(0, frame_prueba2)
        self.jsjs.add_frame(1, frame_prueba)

        btn_mientras = ctk.CTkButton(self.jsjs, text='btn', command=lambda: self.jsjs.toggle_frame_by_id(1))
        btn_mientras2 = ctk.CTkButton(self.jsjs, text='btn', command=lambda: self.jsjs.toggle_frame_by_id(0))
        btn_mientras.pack()
        btn_mientras2.pack()'''

    #funciones de vista

    def siguiente(self):
        self.main_tabV.show_frame(1)
        #if self.el_entry.get() != '':
            #whasApp.set_xl(self.el_entry.get())
            #print(self.el_entry.get())
            #whasApp.lee_excel()
            #self.create_table(whasApp.read_first_row())
            #self.Frame1.pack_forget()
            #self.Frame2.pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=True)
        self.Nav_bar.pack(side=tkinter.TOP, fill=tkinter.X, expand=False)

    def vars(self):
        self.Frame3.pack_forget()
        self.Frame2.pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=True)
        self.btn_env.configure(fg_color=self.CGreen, hover_color=self.CGreen_hov, text_color='white')
        self.btn_vars.configure(fg_color='white', hover_color='white', text_color=self.CGreen)

    def env(self):
        self.Frame2.pack_forget()
        self.Frame3.pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=True)
        self.btn_vars.configure(fg_color=self.CGreen, hover_color=self.CGreen_hov, text_color='white')
        self.btn_env.configure(fg_color='white', hover_color='white', text_color=self.CGreen)
    
    #Funciones de archivo

    def buscar_xl(self):
        self.file_name = filedialog.askopenfilename(title='Seleccionar Excel', filetypes=(('Archivo Excel', '*.xlsx'), ('Todos los archivos', '*')))
        self.xl_path = self.file_name
        print(type(self.xl_path))
        self.el_entry.delete(0, "end")  # Limpiar el contenido del Entry
        self.el_entry.insert(0, self.xl_path)

v = view()
v.mainloop()