import customtkinter as ctk
from ctypes import windll, byref, sizeof, c_int

class view(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1152x819")

        #Colores
        self.CGreen = "#1C9F80"
        self.title("Wapp Sender")
        self.configure(fg_color = self.CGreen)    

v = view()
v.mainloop()