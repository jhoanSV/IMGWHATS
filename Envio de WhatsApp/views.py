import customtkinter as ctk
import tkinter
from tkinter import filedialog
import whasApp

class El_Item(ctk.CTkFrame):
    def __init__(self, *args,
                 master,
                 json_list: dict = None,
                 **kwargs):
        super().__init__(master, *args, **kwargs)

        self.json_list = json_list

        self.configure(fg_color='blue')
        
        self.f = ctk.CTkFrame(self, fg_color='black')
        self.grid(column=0, row=1)

class view(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.xl_path = None
        self.cols = ['Columnas encontradas','Variables','celular','Nombre Destinatario']
        current = None        

        self.geometry("1024x728+200+5")
        self.minsize(900,640)

        #Colores
        self.CGreen = "#1C9F80"
        self.CGreen_hov = "#115e45"

        self.title("Wapp Sender")
        self.configure(fg_color = self.CGreen)
        
        #root - contenedor verde principal
        self.main_container = ctk.CTkFrame(self, corner_radius=8, fg_color=self.CGreen)
        self.main_container.pack(fill=tkinter.BOTH, expand=True)

        self.Nav_bar = ctk.CTkFrame(self.main_container, fg_color=self.CGreen, corner_radius = 0, height=77)

        self.btn_vars = ctk.CTkButton(self.Nav_bar, text="Variables", text_color=self.CGreen, corner_radius=0,
            fg_color='white', hover_color='white', font=('', 18), width=140, command=self.vars)
        self.btn_vars.place(x=0, rely=1, anchor='sw')

        self.btn_env = ctk.CTkButton(self.Nav_bar, text="Envío", text_color='white', corner_radius=0,
            fg_color=self.CGreen, hover_color=self.CGreen_hov, font=('', 18), width=140, command=self.env)
        self.btn_env.place(x=140, rely=1, anchor='sw')

        #self.Nav = ctk.CTkTabview(self.main_container)

        #frame1 - frame1 del program----------------------------------------------------------------------------
        self.Frame1 = ctk.CTkFrame(self.main_container, fg_color="white", corner_radius = 0, width = 1018)
        self.Frame1.pack(fill=tkinter.BOTH, expand=True, padx=55, pady=55)

        #panel izquierdo
        self.frame_iz = ctk.CTkFrame(self.Frame1, fg_color = 'transparent', border_width=0, 
            border_color='black')#394
        self.frame_iz.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

        self.unTexto = ctk.CTkLabel(self.frame_iz, text="Proyectos", text_color="black", font=('', 24))
        self.unTexto.place(relx=0.1, rely=0.1, anchor='nw')

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

        #frame2 - frame1 del program----------------------------------------------------------------------------
        self.Frame2 = ctk.CTkFrame(self.main_container, fg_color="white", corner_radius = 0)        

        self.leTable = ctk.CTkFrame(self.Frame2, fg_color="black")
        #self.leTable.pack(padx=50, pady=50, fill=tkinter.BOTH, expand=True)
        self.leTable.grid(padx=50, pady=50)
        self.leTable.columnconfigure(0, weight=3)
        self.leTable.columnconfigure(1, weight=3)
        self.leTable.columnconfigure(2, weight=1)
        self.leTable.columnconfigure(3, weight=1)

        #frame3 - frame2 del program----------------------------------------------------------------------------
        self.Frame3 = ctk.CTkFrame(self.main_container, fg_color="white", corner_radius = 0)
    
    #funciones de vista

    def siguiente(self):
        if self.el_entry.get() != '':
            whasApp.set_xl(self.el_entry.get())
            #whasApp.lee_excel()
            self.create_table(whasApp.read_first_row())
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

    def create_frame_and_label(self, parent, column, row, text):

        frame = ctk.CTkFrame(parent, fg_color="white", height=40, border_width=1, corner_radius=0)
        frame.grid(column=column, row=row, sticky='wens')
        
        label = ctk.CTkLabel(frame, text_color='black', text=text)
        label.place(relx=0.5, rely=0.5, anchor='center')
    
        return frame, label
    
    #Funciones de archivo

    def create_table(self, fr):
        
        self.item_row = El_Item(master=self.leTable)

        self.f1, self.l1 = self.create_frame_and_label(self.leTable, column=0, row=0, text=self.cols[0])
        self.f2, self.l2 = self.create_frame_and_label(self.leTable, column=1, row=0, text=self.cols[1])
        self.f2, self.l2 = self.create_frame_and_label(self.leTable, column=2, row=0, text=self.cols[2])
        self.f2, self.l2 = self.create_frame_and_label(self.leTable, column=3, row=0, text=self.cols[3])
        self.item_row


    def buscar_xl(self):
        self.file_name = filedialog.askopenfilename(title='Seleccionar Excel', filetypes=(('Archivo Excel', '*.xlsx'), ('Todos los archivos', '*')))
        self.xl_path = self.file_name
        print(type(self.xl_path))
        self.el_entry.delete(0, "end")  # Limpiar el contenido del Entry
        self.el_entry.insert(0, self.xl_path)

v = view()
v.mainloop()