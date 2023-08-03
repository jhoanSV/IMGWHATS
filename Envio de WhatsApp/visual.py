import customtkinter as ctk
from PIL import Image

class list_button(ctk.CTkFrame):
    def __init__(self,
                 *args,
                 lista,
                 logo,
                 function,
                 width= 100,
                 height = 50):
        
        self.lista = lista
        self.logo = Image.open(logo)
        self.function = function
        
        super().__init__(*args, width=width, height=height)
        






