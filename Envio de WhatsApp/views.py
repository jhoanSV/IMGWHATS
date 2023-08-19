import customtkinter as ctk
import tkinter
from tkinter import filedialog
import whasApp
from Vcss import FlatList, El_Tab_view
import json
from components import ItemProject, Table, El_Item

class colorsitos:
    def __init__(self) -> None:
        pass

'''class El_Item(ctk.CTkFrame):
    #def __init__(self, master, destino, mob_num, val, label_text):
    def __init__(self, *args,                 
                 json_list: dict=None,
                 **kwargs):
        super().__init__(*args, **kwargs)

        self.mob_num = ctk.IntVar()
        self.valor = ctk.IntVar()
        self.destino = ctk.IntVar()
        self.la_columna = ctk.StringVar()
        self.json_list = json_list
        self.configure(fg_color='green')
        self.pack(fill='x')

        #* Label con el nombre de col
        self.lf = ctk.CTkFrame(self, fg_color='white', height=40, corner_radius=0, border_width=1)
        self.lf.pack(side='left', fill='x', expand=True, anchor='n')
        self.l = ctk.CTkLabel(self.lf, text='self.la_columna', text_color='black', font=('', 12), fg_color='transparent')
        self.l.place(relx=0.05, rely=0.05)

        #* Entry para la variable
        self.ef = ctk.CTkFrame(self, fg_color='white', height=40, corner_radius=0, border_width=1)
        self.ef.pack(side='left', fill='x', expand=True, anchor='n')
        self.e = ctk.CTkEntry(self.ef, fg_color="#D9D9D9", font=('', 12), placeholder_text='@example',
            text_color='black', height=40)
        self.e.place(relx=0, rely=0, anchor='nw')

        #* RadioButton1
        self.r1f = ctk.CTkFrame(self, fg_color='white', height=40, corner_radius=0, border_width=1)
        self.r1f.pack(side='left', fill='x', expand=True, anchor='n')
        self.r1 = ctk.CTkRadioButton(self.r1f, variable=self.mob_num, value=self.valor, 
            text='')
        self.r1.place(relx=0.5, rely=0.1, anchor='nw')
        
        #* RadioButton2
        self.r2f = ctk.CTkFrame(self, fg_color='white', height=40, corner_radius=0, border_width=1)
        self.r2f.pack(side='left', fill='x', expand=True, anchor='n')
        self.r2 = ctk.CTkRadioButton(self.r2f, variable=self.destino, value=self.valor, 
            text='')
        self.r2.place(relx=0.5, rely=0.1, anchor='nw')'''


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

        #Barra de navegación
        self.Nav_bar = ctk.CTkFrame(self.main_container, fg_color=self.CGreen, corner_radius = 0, height=77)

        self.btn_vars = ctk.CTkButton(self.Nav_bar, text="Variables", text_color=self.CGreen, corner_radius=0,
            fg_color='white', hover_color='white', font=('', 18), width=140, command=self.vars)
        self.btn_vars.place(x=0, rely=1, anchor='sw')

        self.btn_env = ctk.CTkButton(self.Nav_bar, text="Envío", text_color='white', corner_radius=0,
            fg_color=self.CGreen, hover_color=self.CGreen_hov, font=('', 18), width=140, command=self.env)
        self.btn_env.place(x=140, rely=1, anchor='sw')

        #frame1 - frame1 proyectos----------------------------------------------------------------------------
        self.Frame1 = ctk.CTkFrame(self.main_container, fg_color="white", corner_radius = 0, width = 1018)
        self.Frame1.pack(fill=tkinter.BOTH, expand=True, padx=55, pady=55)

        # TODO: panel izquierdo
        self.frame_iz = ctk.CTkFrame(self.Frame1, fg_color = 'transparent', border_width=0, 
            border_color='black')#394
        self.frame_iz.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

        self.unTexto = ctk.CTkLabel(self.frame_iz, text="Proyectos", text_color="black", font=('', 24))
        self.unTexto.place(relx=0.1, rely=0.1, anchor='nw')

        with open('./proyectos.json', 'r') as json_file:
            projects_json = json.load(json_file)

        self.ListaDeProyectos = FlatList(self.frame_iz, json_list=projects_json, Item= ItemProject, width= 200)
        self.ListaDeProyectos.pack(side=tkinter.LEFT, expand=True)


        #panel derecho
        self.frame_der = ctk.CTkFrame(self.Frame1, fg_color = 'transparent', border_width=0,
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

        self.Separador = ctk.CTkLabel(self.Frame1, fg_color=self.CGreen, text='', width=0)
        self.Separador.place(relx=0.49, rely=0.08, relwidth=0.005, relheight=0.84, anchor='n')

        self.btn_sig = ctk.CTkButton(self.frame_der, text="Siguiente", corner_radius=0, fg_color=self.CGreen,
            hover_color='#115e45', font=('', 18), command=self.siguiente)
        self.btn_sig.place(relx=0.9, rely=0.92, anchor='se')

        #frame2 - frame2 del program----------------------------------------------------------------------------
        self.Frame2 = ctk.CTkFrame(self.main_container, fg_color="white", corner_radius = 0)        

        whasApp.set_xl(r'C:\Users\pc\Desktop\Numero_mensaje_whatsapp.xlsx')
        self.lista = whasApp.read_first_row()
        self.Tablajs = Table(self.Frame2, t_lista=self.lista, width=900)
        '''self.leTable = ctk.CTkFrame(self.Frame2, fg_color="blue")
        self.leTable.pack(padx=50, pady=50, fill='x', expand=True, anchor='n')'''

        #frame3 - frame3 del program----------------------------------------------------------------------------
        self.Frame3 = ctk.CTkFrame(self.main_container, fg_color="white", corner_radius = 0)
        
        self.jsjs = El_Tab_view(self.Frame3)
        self.jsjs.pack(fill='both', expand=True)

        frame_prueba = ctk.CTkFrame(self.jsjs, fg_color='#6d6357')
        frame_prueba2 = ctk.CTkFrame(self.jsjs, fg_color='#e7f392')
        self.jsjs.add_frame(0, frame_prueba2)
        self.jsjs.add_frame(1, frame_prueba)

        btn_mientras = ctk.CTkButton(self.jsjs, text='btn', command=lambda: self.jsjs.toggle_frame_by_id(1))
        btn_mientras2 = ctk.CTkButton(self.jsjs, text='btn', command=lambda: self.jsjs.toggle_frame_by_id(0))
        btn_mientras.pack()
        btn_mientras2.pack()

    #funciones de vista

    def siguiente(self):
        if self.el_entry.get() != '':
            #whasApp.set_xl(self.el_entry.get())
            #whasApp.lee_excel()
            #self.create_table(whasApp.read_first_row())
            self.Frame1.pack_forget()
            self.Frame2.pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=True)
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

    def create_frame_and_label(self, parent, text):

        frame = ctk.CTkFrame(parent, fg_color="gray", height=40, border_width=1, corner_radius=0)
        frame.pack(side=tkinter.LEFT, fill='x', expand=True, anchor='n')
        
        label = ctk.CTkLabel(frame, text_color='black', text=text, font=('',15))
        label.place(relx=0.5, rely=0.5, anchor='center')
        #label.pack()
    
        return frame, label
    
    #Funciones de archivo

    def create_table(self, fr):
        
        #Variables
        print(fr)            
        
        self.t_head = ctk.CTkFrame(self.leTable, fg_color='white', height=40)
        self.t_head.pack(fill='x')
        self.t_body = ctk.CTkFrame(self.leTable, fg_color='white')
        self.t_body.pack(side='bottom', fill='both')

        self.f1, self.l1 = self.create_frame_and_label(self.t_head, text=self.cols[0])
        self.f2, self.l2 = self.create_frame_and_label(self.t_head, text=self.cols[1])
        self.f2, self.l2 = self.create_frame_and_label(self.t_head, text=self.cols[2])
        self.f2, self.l2 = self.create_frame_and_label(self.t_head, text=self.cols[3])

        #self.t_flatlist = FlatList(self.t_body, json_list=fr, Item=El_Item)

        '''self.item_row = El_Item(self.t_body, destino=self.destino, mob_num=self.mob_num, val=0, label_text=fr[0])
        self.item_row2 = El_Item(self.t_body, destino=self.destino, mob_num=self.mob_num, val=1, label_text=fr[1])
        self.item_row3 = El_Item(self.t_body, destino=self.destino, mob_num=self.mob_num, val=2, label_text=fr[2])'''

    def buscar_xl(self):
        self.file_name = filedialog.askopenfilename(title='Seleccionar Excel', filetypes=(('Archivo Excel', '*.xlsx'), ('Todos los archivos', '*')))
        self.xl_path = self.file_name
        print(type(self.xl_path))
        self.el_entry.delete(0, "end")  # Limpiar el contenido del Entry
        self.el_entry.insert(0, self.xl_path)

v = view()
v.mainloop()