import customtkinter as ctk
import tkinter
from tkinter import filedialog
from PIL import Image, ImageTk

class ItemProject(ctk.CTkFrame):
    def __init__(self, *args,
                 width: int = 700,
                 height: int = 500,
                 json_list: dict = None,  # Use dict for JSON object
                 Project_name: str = None,
                 On_press: callable = None,
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
