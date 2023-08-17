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
                 **kwargs):
        
        super().__init__(*args, **kwargs)
        self.json_list = json_list
        self.width = width
        self.height = height
        self.Project_name = Project_name
        self.Mainframe = ctk.CTkFrame(self, width= self.width, height= self.height, fg_color='#FFFFFF')
        self.Mainframe.grid(row=0, column=1, padx=0, pady=0 , sticky='nsew')
        self.Mainframe.bind("<Button-1>", self.start_drag)

        whatsappImage = ctk.CTkImage(Image.open('.\Images\WhatsApp.jpeg'), size=(40,40))

        self.ImageWhatsApp = ctk.CTkLabel(self.Mainframe, image = whatsappImage, width= 40, height= 40, text = "")
        self.ImageWhatsApp.grid(row=0, column=0, padx=0, pady=0)
        #self.ImageWhatsApp.bind("<Button-1>", self.start_drag)

        self.Name_Label = ctk.CTkLabel(self.Mainframe, text= self.Project_name, text_color= '#000000')
        self.Name_Label.grid(row=0, column=1, padx=0, pady=0 , sticky='nsew')
        #self.Name_Label.bind("<Button-1>", self.start_drag)

    def start_drag(self, event):
        print('hola')
