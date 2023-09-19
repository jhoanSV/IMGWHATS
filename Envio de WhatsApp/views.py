import customtkinter as ctk
import tkinter
from tkinter import filedialog
import whasApp
import json
from Vcss import FlatList, El_Tab_view
from components import ItemProject, Table, El_Item
from Pages import Los_proyectos, Vars, Send

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
        self.main_tabV.pack(side='bottom', fill='both', expand=True, padx=55, pady=55)
        
        self.Nav_bar = ctk.CTkFrame(self.main_container, fg_color=self.CGreen, corner_radius = 0, height=77)

        self.btn_vars = ctk.CTkButton(self.Nav_bar, text="Variables", text_color=self.CGreen, corner_radius=0,
            fg_color='white', hover_color='white', font=('', 18), width=140,
            command=lambda: self.switch_tab(1))
        self.btn_vars.place(x=0, rely=1, anchor='sw')

        self.btn_env = ctk.CTkButton(self.Nav_bar, text="Envío", text_color='white', corner_radius=0,
            fg_color=self.CGreen, hover_color=self.CGreen_hov, font=('', 18), width=140,
            command=lambda: self.switch_tab(2))
        self.btn_env.place(x=140, rely=1, anchor='sw')

        #*frame1 - frame1 proyectos----------------------------------------------------------------------------
        self.proyectos = Los_proyectos(self.main_tabV, El_metodo=self.siguiente)
        self.main_tabV.add_frame(0, self.proyectos)
        self.main_tabV.toggle_frame_by_id(0)

        #frame3 - frame3 del program----------------------------------------------------------------------------
        self.Frame3 = ctk.CTkFrame(self.main_container, fg_color="white", corner_radius = 0)

    #funciones de vista

    def siguiente(self, tab, data_proj=None):
            #try:
                #*Crea el frame de variables                
                self.variables  = Vars(master=self.main_tabV, path = self.proyectos.el_entry.get(), El_metodo=self.reload_switch)
                self.main_tabV.add_frame(1, self.variables)
                self.envio = Send(master=self.main_tabV, data_proj=data_proj)
                self.main_tabV.add_frame(2, self.envio)
                #self.main_tabV.toggle_frame_by_id(tab)
                self.switch_tab(tab)
                self.Nav_bar.pack(side='top', fill='x', expand=False)
                self.main_tabV.pack_configure(padx=0, pady=0)
            #except Exception as e:
                #print("error---------------------------jiji")
                #print(e)
                #crea un label para avisar del error
                error = 'No se ha podido abrir el excel\npor favor verifique c:'
                #error = 'Error: ' + str(e)
                #print(e)
                self.warn_file = ctk.CTkLabel(self.proyectos.frame_der,text=error,text_color="black",font=('', 20))
                self.warn_file.place(relx=0.9, rely=0.8, anchor='se')

    def switch_tab(self, tab):
        self.main_tabV.toggle_frame_by_id(tab)
        if tab == 1:
            self.btn_env.configure(fg_color=self.CGreen, hover_color=self.CGreen_hov, text_color='white')
            self.btn_vars.configure(fg_color='white', hover_color='white', text_color=self.CGreen)
        elif tab == 2:
            self.btn_vars.configure(fg_color=self.CGreen, hover_color=self.CGreen_hov, text_color='white')
            self.btn_env.configure(fg_color='white', hover_color='white', text_color=self.CGreen)
    
    def reload_switch(self, tab, new_dataP):
         self.envio.update_data(new_dataP)
         #self.variables.update_table() que acutalice los checkboxes cuando sea un proyecto ya guardado
         self.switch_tab(tab)

v = view()
v.mainloop()