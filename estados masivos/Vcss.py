import customtkinter as ctk
from typing import Union, Callable
import re
from PIL import ImageTk, Image
import json
from typing import Optional
import tkinter as tk
import numpy as np

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
    
class DraggableLabel(ctk.CTkFrame):
    def __init__(self, *args,
                 x: int = 100,
                 y: int = 100,
                 image: Image = None,  # for a CTkimage object
                 resize_width: int = None,
                 resize_height: int = None,
                 transform: bool = False,
                 **kwargs):
        
        # Set default text to an empty string
        #kwargs.setdefault("text", "")
        #kwargs.setdefault("fg_color", "red")
        #kwargs.setdefault("bg_color", "#FFFFff00")
        super().__init__(*args, **kwargs)
        self.configure(fg_color='transparent', bg_color='transparent')
        self.image = image
        self.image_width, self.image_height = self.image.size
        self.image_tk = ctk.CTkImage(self.image, size=(self.image.size))
        self.x = x
        self.y = y
        
        if self.image is not None:
            size = 5, 5
            self.square_image = Image.new('RGB', size, 'black')
            self.square = ctk.CTkImage(self.square_image, size= size)
            
            #* Draggable effect
            self.ImageDraggable = ctk.CTkLabel(self, image= self.image_tk, text="", fg_color= "transparent", bg_color="transparent")
            self.ImageDraggable.grid(row=1, column=1)
            self.ImageDraggable.bind("<Button-1>", self.start_drag)
            self.ImageDraggable.bind("<ButtonRelease-1>", self.stop_drag)
            self.ImageDraggable.bind("<B1-Motion>", self.on_drag)

            # * resize square
            self.Psi = ctk.CTkLabel(self, image= self.square, text="", width=5, height=5)
            self.Psi.grid(row=0,column=0)
            self.Psi.bind("<Button-1>", self.start_drag)
            self.Psi.bind("<B1-Motion>", lambda event: self.on_resize(event, move_x=1, move_y=1, sign = -1,  anchor_x = 1, anchor_y = 1))
            self.Psi.bind("<ButtonRelease-1>", self.stop_drag)
            self.pointreference = {"x": 0, "y": 0}

            # Punto superior central
            self.Psc = ctk.CTkLabel(self, image= self.square, text="", width=5, height=5)
            self.Psc.grid(row=0,column=1)
            self.Psc.bind("<Button-1>", self.start_drag)
            self.Psc.bind("<B1-Motion>", lambda event: self.on_resize(event, move_x=0, move_y=-1, anchor_y = 1))
            self.Psc.bind("<ButtonRelease-1>", self.stop_drag)
            
            # Punto superior derecho
            self.Psd = ctk.CTkLabel(self, image= self.square, text="", width=5, height=5)
            self.Psd.grid(row=0,column=2)
            self.Psd.bind("<Button-1>", self.start_drag)
            self.Psd.bind("<B1-Motion>", lambda event: self.on_resize(event, move_x=1, move_y=1, anchor_y = 1))
            self.Psd.bind("<ButtonRelease-1>", self.stop_drag)
            self.pointreference = {"x": 0, "y": 0}

            # Punto inferior izquierdo
            self.Pii = ctk.CTkLabel(self, image= self.square, text="", width=5, height=5)
            self.Pii.grid(row=2,column=0)
            self.Pii.bind("<Button-1>", self.start_drag)
            self.Pii.bind("<B1-Motion>", lambda event: self.on_resize(event, move_x=1, move_y=1, sign = -1, anchor_x = 1 ))
            self.Pii.bind("<ButtonRelease-1>", self.stop_drag)
            self.pointreference = {"x": 0, "y": 0}

            # Punto inferior central
            self.Pic = ctk.CTkLabel(self, image= self.square, text="", width=5, height=5)
            self.Pic.grid(row=2,column=1)
            self.Pic.bind("<Button-1>", self.start_drag)
            self.Pic.bind("<B1-Motion>", lambda event: self.on_resize(event, move_x=0, move_y=1))
            self.Pic.bind("<ButtonRelease-1>", self.stop_drag)

            # Punto inferior derecho
            self.Pid = ctk.CTkLabel(self, image= self.square, text="", width=5, height=5)
            self.Pid.grid(row=2,column=2)
            self.Pid.bind("<Button-1>", self.start_drag)
            self.Pid.bind("<B1-Motion>", lambda event: self.on_resize(event, move_x=1, move_y=1))
            self.Pid.bind("<ButtonRelease-1>", self.stop_drag)
            self.pointreference = {"x": 0, "y": 0}

            # Punto lateral izquierdo
            self.Pli = ctk.CTkLabel(self, image= self.square, text="", width=5, height=5)
            self.Pli.grid(row=1,column=0)
            self.Pli.bind("<Button-1>", self.start_drag)
            self.Pli.bind("<B1-Motion>", lambda event: self.on_resize(event, move_x=-1, move_y=0, anchor_x=1))
            self.Pli.bind("<ButtonRelease-1>", self.stop_drag)

            # Punto lateral derecho
            self.Pld = ctk.CTkLabel(self, image= self.square, text="", width=5, height=5)
            self.Pld.grid(row=1,column=2)
            self.Pld.bind("<Button-1>", self.start_drag)
            self.Pld.bind("<B1-Motion>", lambda event: self.on_resize(event, move_x=1, move_y=0))
            self.Pld.bind("<ButtonRelease-1>", self.stop_drag)
            self.drag_data = {"x": 0, "y": 0}

            #print('el tamaño es ' + str(self.image_width) + str(self.image_height))

    def start_drag(self, event):
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        self.pointreference["x"] = event.x
        self.pointreference["y"] = event.y

    def stop_drag(self, event):
        self.drag_data = {"x": 0, "y": 0}
        self.pointreference = {"x": 0, "y": 0}

    def on_drag(self, event):
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]
        new_x = self.winfo_x() + dx
        new_y = self.winfo_y() + dy
        self.place(x=new_x, y=new_y)
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def on_resize(self, event, move_x=0, move_y=0, sign = 1, anchor_x = 0, anchor_y = 0):
        # *for the anchor
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]
        
        if move_x != 0 and move_y != 0:
            aspect_ratio = (self.image_width + (sign*dx))/ self.image_width
            size_x = int(np.around(aspect_ratio * self.ImageDraggable.winfo_width()))
            size_y = int(np.around(aspect_ratio * self.ImageDraggable.winfo_height()))
        else:
            drag_x = move_x * dx
            drag_y = move_y * dy
            size_x = self.ImageDraggable.winfo_width() + drag_x
            size_y = self.ImageDraggable.winfo_height() + drag_y

        new_x = self.winfo_x() + (anchor_x * dx)
        new_y = self.winfo_y() + (anchor_y * dy)
        self.place(x=new_x, y=new_y)

        if size_x <=0:
            size_x = 1
        if size_y <=0:
            size_y = 1
        #* resizin the image
        resized_image = self.image.resize((size_x, size_y), Image.ANTIALIAS)
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.ImageDraggable.configure(image=self.image_tk, width=size_x, height=size_y)
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def On_Resize(self, width = 0, height = 0):
        size_x = self.ImageDraggable.winfo_width()
        size_y = self.ImageDraggable.winfo_height()
        if width != 0:
            size_x = width
        if height != 0:
            size_y = height
        resized_image = self.image.resize((size_x, size_y), Image.ANTIALIAS)
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.ImageDraggable.configure(image=self.image_tk, width=size_x, height=size_y)

    def On_Reposition(self, position_x = 0 , position_y = 0):
        new_x = self.winfo_x()
        new_y = self.winfo_y()
        if position_x != 0:
            new_x = position_x
        if position_y != 0:
            new_y = position_y
        self.place(x=new_x, y=new_y)

    def get_data(self):
        return {"Width": self.ImageDraggable.winfo_width(),
                "Height": self.ImageDraggable.winfo_height(),
                "Rotate": 0,
                "x_position": self.winfo_x(),
                "y_position": self.winfo_y(),
                "xCenter": True,
                "yCenter": True}
    
    def On_rotate(self, rotate):
        rotated_image = self.image.rotate(rotate, expand = True)
        size_x, size_y = rotated_image.size
        self.image_tk = ImageTk.PhotoImage(rotated_image)
        self.ImageDraggable.configure(image=self.image_tk, width=size_x, height=size_y)

def relative_position(anchor_x, anchor_y, x, y):
    relative_x = x - anchor_x
    relative_y = y - anchor_y
    return relative_x, relative_y
