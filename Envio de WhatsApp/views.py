import customtkinter as ctk
#from whasApp import envio_msj

class view(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1152x819")

        #Colores
        self.CGreen = "#1C9F80"

        self.title("Wapp Sender")
        self.configure(fg_color = self.CGreen, padx=80, pady=80)
        self.rowconfigure(0, weight=1)  # configure grid system
        self.columnconfigure(0, weight=1)
        #view.create_frame(self)
        Frame1 = ctk.CTkFrame(self, fg_color="white", corner_radius=0)
        Frame1.rowconfigure(0, weight=1)  # configure grid system
        Frame1.columnconfigure(0, weight=1)
        Frame1.columnconfigure(1, weight=1)
        Frame1.grid(row = 0, column = 0, sticky = 'nsew')

        frame_left = ctk.CTkFrame(Frame1, fg_color="transparent")
        frame_left.grid(row = 0,column = 0)
        frame_left.rowconfigure(0, weight=1)
        frame_left.columnconfigure(0, weight=1)
        
        unTexto = ctk.CTkLabel(Frame1,text="Proyectos",text_color="black")
        unTexto.grid(row=0,column=0,sticky='nw', padx = 46, pady = 90)

        frame_rigth = ctk.CTkFrame(Frame1, fg_color="transparent")
        frame_rigth.grid(row = 0,column = 1)
        frame_rigth.rowconfigure(0, weight=1)
        '''frame_rigth.rowconfigure(1, weight=1)
        frame_rigth.rowconfigure(2, weight=1)'''
        frame_rigth.columnconfigure(0, weight=1)

        unTexto2 = ctk.CTkLabel(frame_rigth,text="Nuevo Proyecto",text_color="black")
        unTexto2.grid(row=0,column=0)
        el_entry = ctk.CTkEntry(frame_rigth, placeholder_text="Seleccionar Excel", fg_color="#D9D9D9")
        el_entry.grid(row=1,column=0)
        el_btn = ctk.CTkButton(frame_rigth, text="Envio mensaje", command=view.button_event)
        el_btn.grid(row=2,column=0)
    
    def button_event():
        print("button pressed")
    '''def frame1(self):
        myFrame = ctk.CTkFrame(self, fg_color="green")
        myFrame.grid(row=0,col=0)'''

v = view()



v.mainloop()