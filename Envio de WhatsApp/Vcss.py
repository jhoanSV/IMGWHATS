import customtkinter as ctk
from typing import Union, Callable
import re
from PIL import ImageTk, Image
import json
from typing import Optional

class BoxNumber(ctk.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 step_size: Union[int, float] = 1,
                 command: Callable = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command

        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = ctk.CTkButton(self, text="-", width=height-6, height=height-6,
                                                       command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = ctk.CTkEntry(self, width=width-(2*height), height=height-6, border_width=0)
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.add_button = ctk.CTkButton(self, text="+", width=height-6, height=height-6,
                                                  command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        # default value
        self.entry.insert(0, "0.0")

    def add_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = float(self.entry.get()) + self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def subtract_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = float(self.entry.get()) - self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def get(self) -> Union[float, None]:
        try:
            return float(self.entry.get())
        except ValueError:
            return None

    def set(self, value: float):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(float(value)))

class ImageBox(ctk.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 xPosition: int = 0,
                 yPosition: int = 0,
                 command: Callable = None,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.command = command

        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = ctk.CTkButton(self, text="-", width=height-6, height=height-6,
                                                       command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = ctk.CTkEntry(self, width=width-(2*height), height=height-6, border_width=0)
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.add_button = ctk.CTkButton(self, text="+", width=height-6, height=height-6,
                                                  command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        # default value
        self.entry.insert(0, "0.0")

class InputNumber(ctk.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 step_size: Union[int, float] = 1,
                 command: Callable = None,
                 ciclic: bool = False,
                 min: int = 0,
                 max: int = 10,
                 **kwargs):
        def tamaño(width):
            if width < 50:
                return 50
            else:
                return width
        
        super().__init__(*args, width=tamaño(width), height=tamaño(width)*0.66, **kwargs)
        self.step_size = step_size
        self.ciclic = ciclic
        self.command = command
        self.min = min
        self.max = max
        self.configure(fg_color=("gray78", "gray28"))  # set frame color
        
        self.FrameButons = ctk.CTkFrame(self)
        self.FrameButons.configure(fg_color=("gray78", "gray28")) 

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        # ! intento 2
        self.entry = ctk.CTkEntry(self, width=width*0.80, height=width*0.70, border_width=0)
        self.entry.bind('<Key>', self.Float_input)
        self.entry.bind('<Leave>', self.Leave_input)
        # ! Fin intento 2

        self.entry.grid(row=0, column=0, columnspan=1, padx=1, pady=1, sticky="ew")
        self.FrameButons.grid(row=0, column=2)
        # * botones de cambio de cantidad
        
        self.add_button = ctk.CTkButton(self.FrameButons, text="+", width=width*0.3, height=width*0.3,
                                                  command= lambda: self.ciclico(1))
        self.add_button.grid(row=0, column=0, padx=1, pady=1)
        
        self.subtract_button = ctk.CTkButton(self.FrameButons, text="-", width=width*0.3, height=width*0.3,
                                                       command=lambda: self.ciclico(-1))
        self.subtract_button.grid(row=1, column=0, padx=1, pady=1)

        # *default value
        self.entry.insert(0, float(0))

    def ciclico(self, sign):
        if self.command is not None:
            self.command()
        
        if self.entry.get() == '':
            self.entry.delete(0, "end")
            self.entry.insert(0, float(0))
        elif self.ciclic == True:
            try:
                value = float(self.entry.get()) + (float(sign)*self.step_size)
                if value < self.min:
                    self.entry.delete(0, "end")
                    self.entry.insert(0, float(self.max-0.1))
                elif value >= self.max:
                    self.entry.delete(0, "end")
                    self.entry.insert(0, float(self.min))
                else:
                    self.entry.delete(0, "end")
                    self.entry.insert(0, value)
            except ValueError:
                return
        elif self.ciclic == False:
            try:
                value = float(self.entry.get()) + (float(sign)*self.step_size)
                self.entry.delete(0, "end")
                self.entry.insert(0, value)
            except ValueError:
                return

    def get(self) -> Union[float, None]:
        try:
            return float(self.entry.get())
        except ValueError:
            return None

    def set(self, value: float):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(float(value)))
    
    def es_flotante(self, texto):
        try:
            float(texto)
            return True
        except ValueError:
            return False
    
    def Float_input(self, event):
        P = event.widget.get()  # Get the text from the entry widget
        c = event.char
        if not self.es_flotante(c) and c != '' and c != '.' and event.keysym not in ('BackSpace', 'Delete'):
            if P != "":
                return "break"  # Prevent the key press from being processed
        return True
    
    def Leave_input(self, event):
        if event.widget.get() == '':
            self.entry.delete(0, "end")
            self.entry.insert(0, str(float(0)))

    
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

        self.Name_Label = ctk.CTkLabel(self.frameInfomation, text= "Name: " + self.json_list['Name'])
        self.Name_Label.grid(row=0, column=0, padx=0, pady=0)

        self.Name_Label = ctk.CTkLabel(self.frameInfomation, text= "Type: " + self.json_list['Type'])
        self.Name_Label.grid(row=1, column=0, padx=0, pady=0)
        # *default value


    def get(self) -> Union[float, None]:
        try:
            return float(self.entry.get())
        except ValueError:
            return None

    def set(self, value: float):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(float(value)))
    
class FlatList(ctk.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 100,
                 json_list: dict = None,  # Use dict for JSON object
                 Item: Optional[Callable] = None, # Default to None
                 **kwargs):
        
        super().__init__(*args, width=width, height=height, **kwargs)
        # *variables
        self.width = width
        self.height = height
        self.json_list = json_list
        self.Item = Item
        
        # *frame configuration
        self.configure(fg_color=("gray78", "gray28"))  # set frame color
        
        self.FrameList = ctk.CTkScrollableFrame(self, width=width, height=height)
        self.FrameList.configure(fg_color=("gray78", "gray28")) 

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.FrameList.grid(row=0, column=0)
        
        # * frame scheme Input
        for i in range(self.Number_of_items()):
            FrameItem = ctk.CTkFrame(self.FrameList)
            FrameItem.grid(row=i, column=0 )
            
            if self.Item is not None:
                item_instance = self.Item(FrameItem, json_list= self.json_list[i])
                item_instance.grid(row = 0, column = 0)
            else:
                print('is none')

        # *default value


    def get(self) -> Union[float, None]:
        try:
            return float(self.entry.get())
        except ValueError:
            return None

    def set(self, value: float):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(float(value)))

    def Number_of_items(self):
        #json_data = json.loads(self.json_list)
        num_items = len(self.json_list)
        return num_items

class DraggableLabel(ctk.CTkLabel):
    def __init__(self, *args,
                 x: int = 100,
                 y: int = 100,
                 image: ctk.CTkImage = None,  # for a CTkimage object
                 **kwargs):
        
        super().__init__(*args, **kwargs)
        self.image = image
        self.x = x
        self.y = y

        if self.image is not None:
            self.ImageDraggable = ctk.CTkLabel(self, image= self.image, text='')
            self.ImageDraggable.grid(row=0, column=0)
            self.ImageDraggable.bind("<Button-1>", self.start_drag)
            self.ImageDraggable.bind("<ButtonRelease-1>", self.stop_drag)
            self.ImageDraggable.bind("<B1-Motion>", self.on_drag)
            self.drag_data = {"x": 200, "y": 200}

    def start_drag(self, event):
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def stop_drag(self, event):
        self.drag_data = {"x": 0, "y": 0}

    def on_drag(self, event):
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]
        new_x = self.winfo_x() + dx
        new_y = self.winfo_y() + dy
        self.place(x=new_x, y=new_y)
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y