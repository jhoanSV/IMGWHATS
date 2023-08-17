from tkinter import filedialog
import customtkinter as ctk
from PIL import ImageTk, Image
from Vcss import DraggableLabel
from typing import Union, Callable
import tkinter as tk
class ImageContainer(ctk.CTkFrame):
    def __init__(self, *args,
                 width: int = 700,
                 height: int = 500,
                 Background_image_width: int = 500,
                 Background_image_height: int = 200,
                 json_list: dict = None,  # Use dict for JSON object   
                 **kwargs):
        
        super().__init__(*args, **kwargs)
        self.Background_image_width = Background_image_width
        self.Background_image_height = Background_image_height
        self.json_list = json_list
        self.width = width
        self.height = height
        num_items = len(self.json_list)

        size = (self.Background_image_width, self.Background_image_height)
        ImageContainer = ctk.CTkFrame(self, width= self.width, height= self.height, fg_color='#D9D9D9')
        ImageContainer.pack(fill= None)

        for Item in  self.json_list:
            if Item['Type'] == 'Background':
                size_background = Item['Width'], Item['Height']
                background_color = Item['BackgroundColor']

                background_image = Image.new('RGB',size_background, background_color)
                Bg_image = ctk.CTkImage(background_image, size = size_background)
                background_continer = ctk.CTkLabel(self, image= Bg_image, text="", width=Item['Width'], height=Item['Height'])
                background_continer.place(x=0, y=0)
            elif Item['Type'] == 'image':
                picture = Image.open(Item['Name'])

                frameImage = DraggableLabel(ImageContainer, image=picture)
                frameImage.place(x=0, rely=0)
        #image_tk = ctk.CTkImage(background_image, size=size)

        
        #frameImage = DraggableLabel(ImageContainer, image=background_image)
        #frameImage.place(x=0, rely=0)
        # Add a scale (slider) widget for zooming
        self.zoom_var = tk.DoubleVar(value=1.0)
        self.zoom_scale = tk.Scale(self, from_=0.1, to=5.0, resolution=0.1, orient="horizontal", variable=self.zoom_var, label="Zoom")
        self.zoom_scale.pack(side="bottom")
        
        # Bind the zoom scale change event
        self.zoom_var.trace_add("write", self.update_image_size)

    def update_image_size(self, *args):
        zoom_level = self.zoom_var.get()

        # Update the size of each image in the container based on zoom level
        for child in self.winfo_children():
            if isinstance(child, DraggableLabel):
                new_width = int(child.image_width * zoom_level)
                new_height = int(child.image_height * zoom_level)
                new_image = child.image.resize((new_width, new_height))
                new_image_tk = ImageTk.PhotoImage(new_image)
                child.configure(image=new_image_tk)
                child.image_tk = new_image_tk
                child.image_width = new_width
                child.image_height = new_height

   
class ItemElement(ctk.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 command: Callable = None,
                 images: str = "Default/No_image.jpg",
                 json_list: dict = None,
                 **kwargs):
        
        super().__init__(*args, **kwargs)
        # *variables
        self.command = command
        self.images = images
        self.json_list = json_list
        self.smallImage = ctk.CTkImage(Image.open('caminar.jpg'), size=(30,30))
        self.smallMove = ctk.CTkImage(light_image=Image.open("Default/bars_dark.png"), dark_image=Image.open("Default/bars_dark.png"), size=(30, 30))


        # *frame configuration
        self.configure(fg_color=("gray78", "gray28"))  # set frame color
        
        self.FrameButons = ctk.CTkFrame(self)
        self.FrameButons.configure(fg_color=("gray78", "gray28")) 

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.FrameButons.grid(row=0, column=0)
        
        # * frame scheme Input
        
        self.frameMove = ctk.CTkLabel(self.FrameButons, image=self.smallMove, width=30, text="")
        self.frameMove.grid( row=0, column=0, padx=1, pady=1)

        self.frameImage = ctk.CTkLabel(self.FrameButons, image=self.smallImage, width=30, text="")
        self.frameImage.grid(row=0, column=1, padx=1, pady=1)

        self.frameInfomation = ctk.CTkFrame(self.FrameButons)
        self.frameInfomation.grid(row=0, column=2, padx=1, pady=1)
        if self.json_list['Type'] == 'image':
            self.Name_Label = ctk.CTkLabel(self.frameInfomation, text= "Name: " + self.json_list['Name'])
            self.Name_Label.grid(row=0, column=0, padx=0, pady=0)

            self.Name_Label = ctk.CTkLabel(self.frameInfomation, text= "Type: " + self.json_list['Type'])
            self.Name_Label.grid(row=1, column=0, padx=0, pady=0)
            # *default value
        elif self.json_list['Type'] == 'Background':
            self.Name_Label = ctk.CTkLabel(self.frameInfomation, text= "Type: " + self.json_list['Type'])
            self.Name_Label.grid(row=0, column=0, padx=0, pady=0)
        elif self.json_list['Type'] == 'text':
            self.Name_Label = ctk.CTkLabel(self.frameInfomation, text= "Type: " + self.json_list['Type'])
            self.Name_Label.grid(row=0, column=0, padx=0, pady=0)


    def get(self) -> Union[float, None]:
        try:
            return float(self.entry.get())
        except ValueError:
            return None

    def set(self, value: float):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(float(value)))
 