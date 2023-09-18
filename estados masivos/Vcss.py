import customtkinter as ctk
from typing import Union, Callable
import re
from PIL import ImageTk, Image, ImageGrab
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
                 background_color: str = '#FFFFFF', # Default to
                 adaptable: bool = False, #For adaptability of the width and height
                 Otros: Optional[any] = None,
                 **kwargs):
        
        super().__init__(*args, width=width, height=height, **kwargs)
        # *variables
        self.otros = Otros
        self.width = width
        self.height = height
        self.json_list = json_list
        self.Item = Item
        self.si_list = True
        self.frames = {}
        self.items = []
        self.prev = None
        if (type(self.json_list) == dict):
            self.Key_List = list(self.json_list.keys())
            self.si_list = False
        else:
            self.Key_List = self.json_list
        #self.Key_List = list(json_list.keys())
        self.background_color = background_color
        self.configure(fg_color='transparent')
        
        # *frame configuration
        #self.configure(fg_color=("gray78", "gray28"))  # set frame color
        
        self.FrameList = ctk.CTkScrollableFrame(self, width=width, height=height, fg_color='transparent')
        #self.FrameList.configure(fg_color=("gray78", "gray28")) 
        self.FrameList.configure(fg_color=self.background_color) 
        
        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.FrameList.grid(row=0, column=0)
        
        #self.crear()
        # * frame scheme Input
        #for i in range(self.Number_of_items()):
        for i in range(len(self.Key_List)):
            FrameItem = ctk.CTkFrame(self.FrameList, fg_color='transparent')
            FrameItem.grid(row=i, column=0 )
            if self.Item is not None:
                if self.si_list:
                    key = i
                else:
                    key = self.Key_List[i]
                #item_instance = self.Item(FrameItem, json_list= self.json_list[key], Project_name = str(key),
                #    width = self.width, height = self.height)
                #print(callable(self.otros))
                item_instance = self.Item(FrameItem, json_list= self.json_list[key], Otros={'Project_name': str(key), 'Hook': self.otros},
                    width = self.width, height = self.height)
                self.items.append(item_instance.get_itemData())
                item_instance.grid(row = 0, column = 0)
                item_instance.update_row(self.json_list[key])
                self.frames[i] = item_instance
            else:
                print('is none')            
        # *default value

    def Update_list(self, new_list):
        self.json_list = new_list
        
        # Elimina las filas que ya no están presentes en la nueva lista
        for i in range(len(self.json_list), len(self.frames)):
            self.frames[i].destroy()
            del self.frames[i]
        
        # Actualiza o crea las filas existentes en la nueva lista
        for i in range(len(self.json_list)):
            if self.si_list:
                key = i
            else:
                key = self.Key_List[i]
            value = self.json_list[key]
            if i < len(self.frames):
                self.frames[i].update_row(value)
            else:
                FrameItem = ctk.CTkFrame(self.FrameList, fg_color='transparent')
                FrameItem.grid(row=i, column=0)
                if self.Item is not None:
                    item_instance = self.Item(FrameItem, json_list=value, Otros={'Project_name': str(key), 'Hook': self.otros},
                                            width=self.width, height=self.height)
                    self.items.append(item_instance.get_itemData())
                    item_instance.grid(row=0, column=0)
                    item_instance.update_row(value)
                    self.frames[i] = item_instance
                else:
                    print('is none')


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
        num_items = len(self.Key_List)
        return num_items
    
    def otro_get(self):
        return self.items
    
'''class FlatList(ctk.CTkFrame):
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
        return num_items'''

'''class FlatList(ctk.CTkFrame):
    def _init_(self, *args,
                width: int = 100,
                height: int = 100,
                json_list: Union[list, dict] = None,  # Use dict for JSON object
                Item: Optional[Callable] = None, # Default to None
                background_color: str = '#FFFFFF', # Default to
                adaptable: bool = False, #For adaptability of the width and height
                Otros: Optional[any] = None,
                **kwargs):
        
        super().__init__(*args, width=width, height=height, **kwargs)
        # *variables
        self.otros = Otros
        self.width = width
        self.height = height
        self.json_list = json_list
        self.Item = Item
        self.si_list = True
        self.frames = {}
        self.items = []
        self.prev = None
        if (type(self.json_list) == dict):
            self.Key_List = list(self.json_list.keys())
            self.si_list = False
        else:
            self.Key_List = self.json_list
        #self.Key_List = list(json_list.keys())
        self.background_color = background_color
        self.configure(fg_color='transparent')
        
        # *frame configuration
        #self.configure(fg_color=("gray78", "gray28"))  # set frame color
        
        self.FrameList = ctk.CTkScrollableFrame(self, width=width, height=height, fg_color='transparent')
        #self.FrameList.configure(fg_color=("gray78", "gray28")) 
        self.FrameList.configure(fg_color=self.background_color) 
        
        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.FrameList.grid(row=0, column=0)
        
        #self.crear()
        # * frame scheme Input
        #for i in range(self.Number_of_items()):
        for i in range(len(self.Key_List)):
            FrameItem = ctk.CTkFrame(self.FrameList, fg_color='transparent')
            FrameItem.grid(row=i, column=0 )
            if self.Item is not None:
                if self.si_list:
                    key = i
                else:
                    key = self.Key_List[i]
                #item_instance = self.Item(FrameItem, json_list= self.json_list[key], Project_name = str(key),
                #    width = self.width, height = self.height)
                #print(callable(self.otros))
                item_instance = self.Item(FrameItem, json_list= self.json_list[key], Otros={'Project_name': str(key), 'Hook': self.otros},
                    width = self.width, height = self.height)
                self.items.append(item_instance.get_itemData())
                item_instance.grid(row = 0, column = 0)
                item_instance.update_row(self.json_list[key])
                self.frames[i] = item_instance
            else:
                print('is none')            
        # *default value

    def update_list(self, new_list):
        self.json_list = new_list
        for i in self.frames:
            self.frames[i].update_row(new_list[i])

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
        num_items = len(self.Key_List)
        return num_items
    
    def otro_get(self):
        return self.items'''

class DraggableLabel(ctk.CTkFrame):
    def __init__(self, *args,
                 x: int = 100,
                 y: int = 100,
                 image: Image = None,  # for a CTkimage object
                 resize_width: int = None,
                 resize_height: int = None,
                 transform: bool = False,
                 x_container: int = 0,
                 y_container: int = 0,
                 **kwargs):
        
        # Set default text to an empty string
        #kwargs.setdefault("bg", "")
        #kwargs.setdefault("fg_color", "SystemTransparent")
        #kwargs.setdefault("bg_color", "SystemTransparent")
        #kwargs.setdefault("bg", "")  # Set background to empty string for transparency
        self.image = image
        self.image_width, self.image_height = self.image.size
        self.x_container = x_container
        self.y_container = y_container
        #self.image_tk = ctk.CTkImage(self.image, size=(self.image.size))
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.x = x
        self.y = y
        super().__init__(*args, **kwargs)
        #self.configure(image = self.background)
        
        if self.image is not None:
            self.background = self.capture_screenshot(self.x, self.y, self.image_width + 10, self.image_height + 10)
            size = 5, 5
            self.square_image = Image.new('RGB', size, 'black')
            self.square = ctk.CTkImage(self.square_image, size= size)
            
            #* Draggable effect
            self.ImageDraggable = ctk.CTkCanvas(self, width = self.image_width, height = self.image_height)
            self.background_item = self.ImageDraggable.create_image(0,0, anchor="nw", image=self.background)
            self.ImageDraggable.create_image(0,0, anchor="nw", image=self.image_tk)

            self.ImageDraggable.grid(row=1, column=1)
            self.ImageDraggable.bind("<Button-1>", self.start_drag)
            self.ImageDraggable.bind("<B1-Motion>", self.on_drag)
            self.ImageDraggable.bind("<ButtonRelease-1>", self.stop_drag)

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
        self.place_forget()
        if self.winfo_ismapped() == False:
            self.background = self.capture_screenshot(new_x, new_y, self.image_width, self.image_height)
            self.ImageDraggable.itemconfig(self.background_item, image=self.background)
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

    def capture_screenshot(self, x, y, width, height):
        relative_x = self.winfo_rootx()
        relative_y = self.winfo_rooty()
        screenshot = ImageGrab.grab(bbox=(relative_x, relative_y, x + width, y + height))
        bg_screenshot = ImageTk.PhotoImage(screenshot)
        return bg_screenshot
        

class ImageContainer(tk.Frame):
    def __init__(self, *args,
                 width: int = 700,
                 height: int = 500,
                 Background_image_width: int = 500,
                 Background_image_height: int = 200,
                 json_list: dict = None,  # Use dict for JSON object
                 function: callable = None,
                 Hook: Optional[any]= None,
                 **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.Background_image_width = Background_image_width
        self.Background_image_height = Background_image_height
        self.json_list = json_list
        self.width = width
        self.height = height
        self.configure(width=self.width, height=self.height,)
        self.function = function
        self.Change_point_relative_to = Hook[0]
        #num_items = len(self.json_list)

        self.canvas = tk.Canvas(self, width = self.width, height = self.height, bg='#D9D9D9')
        self.canvas.pack()
        self.image_objects = []

        for Item in  self.json_list:
            if Item['Type'] == 'Background':
                self.size_background = Item['Width'], Item['Height']
                self.background_color = Item['BackgroundColor']
                self.on_x = (self.width - Item['Width'])/2
                self.on_y = (self.height - Item['Height'])/2
                self.background_image = Image.new('RGBA',self.size_background, self.background_color)
                self.Bg_image = ImageTk.PhotoImage(self.background_image)
                self.background_continer = self.canvas.create_image(self.on_x,self.on_y, anchor="nw", image=self.Bg_image)
                self.Change_point_relative_to([self.on_x, self.on_y])
           
            elif Item['Type'] == 'image':
                self.picture = Image.open(Item['Name'])
                x = Item['x_position']
                y = Item['y_position']
                obj = ObjectOnCanvas(self.canvas, x, y, Item['Name'], function = self.function)
                self.image_objects.append(obj)
            
            elif Item['Type'] == 'text':
                x = Item['x_position']
                y = Item['y_position']
                text = TextBox(self.canvas, x, y, Item['text'], Item['boxWidth'], Item['boxHeight'])

    def update_image_size(self, *args):
        zoom_level = self.zoom_var.get()

        # Update the size of each image in the container based on zoom level
        for child in self.winfo_children():
            if isinstance(child, DraggableLabel):
                new_width = int(child.image_width * zoom_level)
                new_height = int(child.image_height * zoom_level)
                new_image = child.image.resize((new_width, new_height))
                new_image_tk = ctk.CTkImage(new_image)
                child.configure(image=new_image_tk)
                child.image_tk = new_image_tk
                child.image_width = new_width
                child.image_height = new_height

    def Container_image(self, image_path):
        image = Image.open(image_path)
        image_tk = ImageTk.PhotoImage(image)
        self.create_image(50, 50, image=image_tk)
        

    def Update_list(self, new_list):
        self.json_list = new_list

class ObjectOnCanvas:
    def __init__(self,
                 canvas, 
                 x, 
                 y, 
                 picture,
                 function: Optional[callable] = any):
        self.canvas = canvas
        self.x = x
        self.y = y
        #self.image = picture
        self.picture = Image.open(picture)
        self.image = ImageTk.PhotoImage(self.picture)
        self.Width = self.image.width()
        self.Height = self.image.height()
        self.state = True
        self.angle = 0
        self.function = function

        super().__init__()
        # *principal image
        #self.angleRsi = Angle_between_vectors(np.array([0,1]), np.array([-self.Width/2,self.Height/2]))
        # Create an image over the canvas
        self.canvas_obj = self.canvas.create_image(self.x, self.y, anchor="nw", image=self.image)
        # Agregar un evento de clic al objeto en el lienzo
        self.canvas.tag_bind(self.canvas_obj,"<Double-Button-1>", self.Change_state)
        self.canvas.tag_bind(self.canvas_obj,"<Button-1>", self.start_drag)
        self.canvas.tag_bind(self.canvas_obj,"<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.canvas_obj,"<ButtonRelease-1>", self.stop_drag)

        self.drag_data = {"x": 0, "y": 0}
        # *Outline resize
        self.Square = Image.new('RGBA',(4,4), '#000000')
        self.square_point = ImageTk.PhotoImage(self.Square)

        #?Punto superior izquierdo
        self.Psi = self.canvas.create_image(self.x,self.y, anchor="nw", image=self.square_point)
        self.canvas.tag_bind(self.Psi,"<Button-1>", self.start_drag)
        self.canvas.tag_bind(self.Psi,"<B1-Motion>", lambda event: self.on_resize(event, move_x=1, move_y=1, sign = -1,  anchor_x = 1, anchor_y = 1))
        self.canvas.tag_bind(self.Psi,"<ButtonRelease-1>", self.stop_drag)
        #?Punto superior central
        self.Psc = self.canvas.create_image(self.x + round((self.Width/2))-2,self.y, anchor="nw", image=self.square_point)
        self.canvas.tag_bind(self.Psc,"<Button-1>", self.start_drag)
        self.canvas.tag_bind(self.Psc,"<B1-Motion>", lambda event: self.on_resize(event, move_x=0, move_y=-1, anchor_y = 1))
        self.canvas.tag_bind(self.Psc,"<ButtonRelease-1>", self.stop_drag)
        #?Punto superior derecho
        self.Psd = self.canvas.create_image(self.x + self.Width - 4,self.y, anchor="nw", image=self.square_point)
        self.canvas.tag_bind(self.Psd,"<Button-1>", self.start_drag)
        self.canvas.tag_bind(self.Psd,"<B1-Motion>", lambda event: self.on_resize(event, move_x=1, move_y=1, anchor_y = 1))
        self.canvas.tag_bind(self.Psd,"<ButtonRelease-1>", self.stop_drag)
        #?Punto inferior izquierdo
        self.Pii = self.canvas.create_image(self.x, self.y + self.Height - 4, anchor="nw", image=self.square_point)
        self.canvas.tag_bind(self.Pii,"<Button-1>", self.start_drag)
        self.canvas.tag_bind(self.Pii,"<B1-Motion>", lambda event: self.on_resize(event, move_x=1, move_y=1, sign = -1, anchor_x = 1 ))
        self.canvas.tag_bind(self.Pii,"<ButtonRelease-1>", self.stop_drag)
        #?Punto inferior central
        self.Pic = self.canvas.create_image(self.x + round((self.Width/2))-2, self.y + self.Height - 4, anchor="nw", image=self.square_point)
        self.canvas.tag_bind(self.Pic,"<Button-1>", self.start_drag)
        self.canvas.tag_bind(self.Pic,"<B1-Motion>", lambda event: self.on_resize(event, move_x=0, move_y=1))
        self.canvas.tag_bind(self.Pic,"<ButtonRelease-1>", self.stop_drag)
        #?Punto inferior derecho
        self.Pid = self.canvas.create_image(self.x + self.Width - 4,self.y + self.Height - 4, anchor="nw", image=self.square_point)
        self.canvas.tag_bind(self.Pid,"<Button-1>", self.start_drag)
        self.canvas.tag_bind(self.Pid,"<B1-Motion>", lambda event: self.on_resize(event, move_x=1, move_y=1))
        self.canvas.tag_bind(self.Pid,"<ButtonRelease-1>", self.stop_drag)
        #?Punto lateral izquierdo
        self.Pli = self.canvas.create_image(self.x,self.y + round((self.Height/2))-2, anchor="nw", image=self.square_point)
        self.canvas.tag_bind(self.Pli,"<Button-1>", self.start_drag)
        self.canvas.tag_bind(self.Pli,"<B1-Motion>", lambda event: self.on_resize(event, move_x=-1, move_y=0, anchor_x=1))
        self.canvas.tag_bind(self.Pli,"<ButtonRelease-1>", self.stop_drag)
        #?Punto lateral derecho
        self.Pld = self.canvas.create_image(self.x + self.Width - 4,self.y + round((self.Height/2))-2, anchor="nw", image=self.square_point)
        self.canvas.tag_bind(self.Pld,"<Button-1>", self.start_drag)
        self.canvas.tag_bind(self.Pld,"<B1-Motion>", lambda event: self.on_resize(event, anchor_x = 1, move_x=1, move_y=0))
        self.canvas.tag_bind(self.Pld,"<ButtonRelease-1>", self.stop_drag)
        self.drag_data = {"x": 0, "y": 0}

        #* Outline for rotate
        self.Rotate_picture = Image.open('./Default/rotare.png')
        self.Rotate_picture = self.Rotate_picture.resize((16, 16), Image.ANTIALIAS)
        #Rotar superior izquiedo
        self.Rotate_pictureSI = self.Rotate_picture.rotate(180)
        self.RotarSI = ImageTk.PhotoImage(self.Rotate_pictureSI)
        self.Rsi = self.canvas.create_image(self.x - 8,self.y - 8, anchor="nw", image=self.RotarSI)
        border_x, border_y = self.canvas.coords(self.Rsi)
        self.canvas.tag_bind(self.Rsi,"<B1-Motion>", lambda event: self.On_rotate(event, border_x = border_x, border_y = border_y))
        #Rotar superior derecho
        self.Rotate_pictureSD = self.Rotate_picture.rotate(90)
        self.RotarSD = ImageTk.PhotoImage(self.Rotate_pictureSD)
        self.Rsd = self.canvas.create_image(self.x + self.Width - 8, self.y - 8 , anchor="nw", image=self.RotarSD)
        border_x, border_y = self.canvas.coords(self.Rsd)
        self.canvas.tag_bind(self.Rsd,"<B1-Motion>", lambda event: self.On_rotate(event, border_x = border_x, border_y = border_y ))
        #Rotar inferior izquierdo
        self.Rotate_pictureII = self.Rotate_picture.rotate(-90)
        self.RotarII = ImageTk.PhotoImage(self.Rotate_pictureII)
        self.Rii = self.canvas.create_image(self.x - 8, self.y + self.Height - 8 , anchor="nw", image=self.RotarII)
        border_x, border_y = self.canvas.coords(self.Rii)
        self.canvas.tag_bind(self.Rii,"<B1-Motion>", lambda event: self.On_rotate(event, border_x = border_x, border_y = border_y ))
        #Rotar inferior derecho
        self.Rotate_pictureID = self.Rotate_picture
        self.RotarID = ImageTk.PhotoImage(self.Rotate_pictureID)
        self.Rid = self.canvas.create_image(self.x + self.Width - 8, self.y + self.Height - 8 , anchor="nw", image=self.RotarID)
        border_x, border_y = self.canvas.coords(self.Rid)
        self.canvas.tag_bind(self.Rid,"<B1-Motion>", lambda event: self.On_rotate(event, border_x = border_x, border_y = border_y ))

        self.rotated_reference = {"x": 0, "y":0}
        self.Show_points(state_resize = 'normal', state_rotate = 'hidden')
        #centered point
        self.Cp = self.canvas.create_image(self.x + round((self.Width/2))-2, self.y + round((self.Height/2))-2 , anchor="nw", image=self.square_point)
        self.canvas.itemconfigure(self.Cp, state='hidden')

    def start_drag(self, event):
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        
    def stop_drag(self, event):
        self.drag_data = {"x": 0, "y": 0}

    def on_drag(self, event):
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]
        new_x = self.x + dx
        new_y = self.y + dy
        # Move the image
        self.canvas.move(self.canvas_obj, dx, dy)
        # Move the reference points to resize
        self.canvas.move(self.Psi, dx, dy)
        self.canvas.move(self.Psc, dx, dy)
        self.canvas.move(self.Psd, dx, dy)
        self.canvas.move(self.Pii, dx, dy)
        self.canvas.move(self.Pic, dx, dy)
        self.canvas.move(self.Pid, dx, dy)
        self.canvas.move(self.Pli, dx, dy)
        self.canvas.move(self.Pld, dx, dy)
        # Move the reference points to rotate
        self.canvas.move(self.Rsi, dx, dy)
        self.canvas.move(self.Rsd, dx, dy)
        self.canvas.move(self.Rii, dx, dy)
        self.canvas.move(self.Rid, dx, dy)
        # Move the centered point
        self.canvas.move(self.Cp, dx, dy)
        # Update the current position
        self.x = new_x
        self.y = new_y

        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

        self.function(self.get())

    def on_resize(self, event, move_x=0, move_y=0, sign = 1, anchor_x = 0, anchor_y = 0):
        # *for the anchor
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]
        
        if move_x != 0 and move_y != 0:
            aspect_ratio = (self.Width + (sign*dx))/ self.Width
            size_x = int(np.around(aspect_ratio * self.Width))
            size_y = int(np.around(aspect_ratio * self.Height))
        else:
            drag_x = move_x * dx
            drag_y = move_y * dy
            size_x = self.Width + drag_x
            size_y = self.Height + drag_y

        new_x = anchor_x * dx #self.x + (anchor_x * dx)
        new_y = anchor_y * dy #self.y + (anchor_y * dy)

        if size_x <=0:
            size_x = 1
        if size_y <=0:
            size_y = 1
        #* resizin the image
        
        resized_image = self.picture.resize((size_x, size_y), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(resized_image)
        self.canvas.itemconfig(self.canvas_obj, image=self.image)
        self.Width = size_x
        self.Height = size_y
        #* Move the image
        #Principal image
        self.canvas.move(self.canvas_obj, new_x, new_y)
        #? Move the reference points to resize the image
        #Punto superior izquierdo
        self.canvas.coords(self.Psi, self.x, self.y)
        #Punto superior central
        self.canvas.coords(self.Psc, self.x + round((self.Width/2))-2,self.y)
        #Punto superior derecho
        self.canvas.coords(self.Psd, self.x + self.Width - 4,self.y)
        #Punto inferior izquierdo
        self.canvas.coords(self.Pii, self.x, self.y + self.Height - 4)
        #Punto inferior central
        self.canvas.coords(self.Pic, self.x + round((self.Width/2))-2, self.y + self.Height - 4)
        #Punto inferior derecho
        self.canvas.coords(self.Pid, self.x + self.Width - 4,self.y + self.Height - 4)
        #Punto lateral izquierdo
        self.canvas.coords(self.Pli, self.x,self.y + round((self.Height/2))-2)
        #Punto lateral derecho
        self.canvas.coords(self.Pld, self.x + self.Width - 4,self.y + round((self.Height/2))-2)
        #Centered point
        self.canvas.coords(self.Cp, self.x + round((self.Width/2))-2, self.y + round((self.Height/2))-2)
        
        #? Move the reference points to rotate the image
        #Rotar superior izquierdo
        self.canvas.coords(self.Rsi,self.x - 8,self.y - 8)
        #Rotar superior derecho
        self.canvas.coords(self.Rsd,self.x + self.Width - 8, self.y - 8 )
        #Rotar inferior izquierdo
        self.canvas.coords(self.Rii,self.x - 8, self.y + self.Height - 8)
        #Rotar inferior derecho
        self.canvas.coords(self.Rid,self.x + self.Width - 8, self.y + self.Height - 8)


        self.x = self.x + new_x
        self.y = self.y + new_y
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        self.function(self.get())

    def Change_state(self, event):
        self.state = not self.state
        if self.state:
            self.state_resize = 'hidden'
            self.state_rotate = 'normal'
        else:
            self.state_resize = 'normal'
            self.state_rotate = 'hidden'
        self.Show_points(state_resize = self.state_resize, state_rotate= self.state_rotate)
        self.function(self.get())
    
    def Show_points(self, state_resize = 'normal', state_rotate = 'hidden'):
        self.canvas.itemconfigure(self.Psi, state=state_resize)
        self.canvas.itemconfigure(self.Psc, state=state_resize)
        self.canvas.itemconfigure(self.Psd, state=state_resize)
        self.canvas.itemconfigure(self.Pii, state=state_resize)
        self.canvas.itemconfigure(self.Pic, state=state_resize)
        self.canvas.itemconfigure(self.Pid, state=state_resize)
        self.canvas.itemconfigure(self.Pli, state=state_resize)
        self.canvas.itemconfigure(self.Pld, state=state_resize)
        # *Reference points to rotate
        # item comfigure to hide and show the rotation.
        self.canvas.itemconfigure(self.Rsi, state=state_rotate)
        self.canvas.itemconfigure(self.Rsd, state=state_rotate)
        self.canvas.itemconfigure(self.Rii, state=state_rotate)
        self.canvas.itemconfigure(self.Rid, state=state_rotate)

    def start_rotated(self, event):
        self.rotated_reference["x"] = event.x
        self.rotated_reference["y"] = event.y

    def end_rotated(self,event):
        self.angle = self.angle + self.new_angle

    def On_rotate(self, event, border_x, border_y):
        Cp_coords = self.canvas.coords(self.Cp)
        self.coords = self.canvas.coords(self.canvas_obj)
        vector1 = (border_x - (Cp_coords[0] + 2), border_y - (Cp_coords[1] + 2))
        Vector2 = (event.x - (Cp_coords[0] + 2), event.y - (Cp_coords[1] + 2))
        #dx = event.x - (Cp_coords[0] + 2) #event.x - (self.coords[0] + self.Width/2)
        #dy = event.y - (Cp_coords[1] + 2) #event.y - (self.coords[1] + self.Height/2)
        # Calculate the angle of rotation based on mouse movement
        #self.new_angle = np.arctan2(dy, dx)
        self.new_angle = Angle_between_vectors(vector1, Vector2)
        #print(Angle_between_vectors(vector1, Vector2))
        # *To rotate de image 
        #Current_width, Current_height = self.image.size
        self.resized_image = self.picture.resize((self.Width, self.Height))
        # Create a new RGBA image with a transparent background
        self.new_image = Image.new('RGBA', self.resized_image.size, (0, 0, 0, 0))
        # Create a mask for the resized image (fully opaque)
        mask = Image.new('L', self.resized_image.size, 255)
        # Paste the loaded JPG image onto the new RGBA image with a mask
        self.new_image.paste(self.resized_image, (0, 0), mask)
        # Rotate the new RGBA image
        self.image_rotated = self.new_image.rotate(-np.degrees(self.new_angle), expand=True)
        # new size of the rotated image
        self.size = self.image_rotated.size
        # Create the new RGBA image
        self.new_rotated_image = self.image_rotated.resize(self.size, Image.ANTIALIAS)
        # Convert the new rotated image to an ImageTk.PhotoImage
        self.image = ImageTk.PhotoImage(self.new_rotated_image)
        # Update the canvas object with the new image
        self.canvas.itemconfig(self.canvas_obj, image=self.image)

        #? Move the reference points to rotate the image
        # Define the distances from the rotated image's center to its corners
        diagonal_length = np.sqrt((self.Width / 2) ** 2 + (self.Height / 2) ** 2)
        angle1 = Angle_between_vectors((1,0), (self.Width,self.Height))#np.arctan2(self.Width / 2,self.Height / 2)
        angle2 = np.pi - angle1
        angles = [
            self.new_angle - angle1, #superior derecho
            self.new_angle + angle1, #inferior derecho
            self.new_angle - angle2, #superior izquierdo
            self.new_angle + angle2, #inferior izquierdo
        ]

        for i, reference_point in enumerate([self.Rsd, self.Rid, self.Rsi, self.Rii]): #, self.Rsi, self.Rii
            #* To move the rotate points around the image_obj
            x = Cp_coords[0] + diagonal_length * np.cos(angles[i]) #self.canvas.coords(self.canvas_obj)[0] + self.Width/2 + diagonal_length * np.cos(angles[i])
            y = Cp_coords[1] + diagonal_length * np.sin(angles[i]) #self.canvas.coords(self.canvas_obj)[1] + self.Height/2 + diagonal_length * np.sin(angles[i])
            self.canvas.coords(reference_point, x - 8, y - 8)
            #* to rotate the image face to the center of the image_obj
            #?Rsd
            self.Rotate_pictureSD = self.Rotate_picture.rotate(-(np.degrees(self.new_angle)) + 90, expand=True)
            self.RotarSD = ImageTk.PhotoImage(self.Rotate_pictureSD)
            self.canvas.itemconfig(self.Rsd, image=self.RotarSD)
            #?Rid
            self.Rotate_pictureID = self.Rotate_picture.rotate(-(np.degrees(self.new_angle)), expand=True)
            self.RotarID = ImageTk.PhotoImage(self.Rotate_pictureID)
            self.canvas.itemconfig(self.Rid, image=self.RotarID)
            #?Rsi
            self.Rotate_pictureSI = self.Rotate_picture.rotate(-(np.degrees(self.new_angle)) + 180, expand=True)
            self.RotarSI = ImageTk.PhotoImage(self.Rotate_pictureSI)
            self.canvas.itemconfig(self.Rsi, image=self.RotarSI)
            #?Rii
            self.Rotate_pictureII = self.Rotate_picture.rotate(-(np.degrees(self.new_angle)) - 90, expand=True)
            self.RotarII = ImageTk.PhotoImage(self.Rotate_pictureII)
            self.canvas.itemconfig(self.Rii, image=self.RotarII)
            New_dx = Cp_coords[0] - (self.size[0]/2)
            New_dy = Cp_coords[1] - (self.size[1]/2)
            self.canvas.coords(self.canvas_obj, New_dx, New_dy)

        #self.angle = self.angle + self.new_angle
        self.rotated_reference["x"] = event.x
        self.rotated_reference["y"] = event.y
        self.angle = self.angle + np.degrees(self.new_angle)
        #print("angle = ", self.angle)
        self.function(self.get())

    def get(self):
        return {"Width": self.Width,
                "Height": self.Height,
                "Rotate": self.angle,
                "x_position": self.x,
                "y_position": self.y,
                "xCenter": False,
                "yCenter": False}
        
class TextBox:
    def __init__(self, canvas, x, y, Text, width, height):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.text = Text
        self.Width = width
        self.Height = height
        self.state = True
        self.angle = 0
        self.editing = False
        self.cursor_position = len(Text) - 1

        super().__init__()
        
        self.text_container = self.canvas.create_rectangle(self.x, self.y, self.x + self.Width, self.Height, outline="#F2F2F2", width=4)

        self.canvas_text = self.canvas.create_text(self.x, self.y, text=self.text, anchor='nw', fill="black", font=('Helvetica 15 bold'))
        # to allow rewrite the text
        self.canvas.tag_bind(self.canvas_text,"<Double-Button-1>", self.DoubleClick)
        # To rewrite the text
        self.canvas.bind("<KeyPress>", self.Re_write)
        self.canvas.bind("<BackSpace>", self.backspace)
        self.canvas.bind("<Left>", self.move_cursor_left)
        self.canvas.bind("<Right>", self.move_cursor_right)
        # To move the text
        self.canvas.tag_bind(self.canvas_text,"<Button-1>", self.start_drag)
        self.canvas.tag_bind(self.canvas_text,"<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.canvas_text,"<ButtonRelease-1>", self.stop_drag)
        # Bind the key press event to the canvas
        #self.canvas.tag_bind(self.canvas_text,"<KeyPress>", self.Re_write)

        self.Square = Image.new('RGBA',(4,4), '#000000')
        self.square_point = ImageTk.PhotoImage(self.Square)
        self.H_line = Image.new('RGBA',(8,4), '#000000')
        self.H_line_point = ImageTk.PhotoImage(self.H_line)
        self.V_line = Image.new('RGBA',(4,8), '#000000')
        self.V_line_point = ImageTk.PhotoImage(self.V_line)
        #?Punto superior izquierdo
        self.Psi = self.canvas.create_image(self.x - 2,self.y - 2, anchor="nw", image=self.square_point)
        self.canvas.tag_bind(self.Psi,"<Button-1>", self.start_drag)
        self.canvas.tag_bind(self.Psi,"<B1-Motion>", lambda event: self.on_resize(event, move_x=1, move_y=1, sign = -1,  anchor_x = 1, anchor_y = 1))
        self.canvas.tag_bind(self.Psi,"<ButtonRelease-1>", self.stop_drag)
        #?Punto superior central
        self.Psc = self.canvas.create_image(self.x + round((self.Width/2))-2,self.y - 2 , anchor="nw", image=self.H_line_point)
        self.canvas.tag_bind(self.Psc,"<Button-1>", self.start_drag)
        self.canvas.tag_bind(self.Psc,"<B1-Motion>", lambda event: self.on_resize(event, move_x=0, move_y=-1, anchor_y = 1))
        self.canvas.tag_bind(self.Psc,"<ButtonRelease-1>", self.stop_drag)
        #?Punto superior derecho
        self.Psd = self.canvas.create_image(self.x + self.Width - 2,self.y - 2, anchor="nw", image=self.square_point)
        self.canvas.tag_bind(self.Psd,"<Button-1>", self.start_drag)
        self.canvas.tag_bind(self.Psd,"<B1-Motion>", lambda event: self.on_resize(event, move_x=1, move_y=1, anchor_y = 1))
        self.canvas.tag_bind(self.Psd,"<ButtonRelease-1>", self.stop_drag)
        #?Punto inferior izquierdo
        self.Pii = self.canvas.create_image(self.x - 2, self.y + self.Height - 2, anchor="nw", image=self.square_point)
        self.canvas.tag_bind(self.Pii,"<Button-1>", self.start_drag)
        self.canvas.tag_bind(self.Pii,"<B1-Motion>", lambda event: self.on_resize(event, move_x=1, move_y=1, sign = -1, anchor_x = 1 ))
        self.canvas.tag_bind(self.Pii,"<ButtonRelease-1>", self.stop_drag)
        #?Punto inferior central
        self.Pic = self.canvas.create_image(self.x + round((self.Width/2))-2, self.y + self.Height - 2, anchor="nw", image=self.H_line_point)
        self.canvas.tag_bind(self.Pic,"<Button-1>", self.start_drag)
        self.canvas.tag_bind(self.Pic,"<B1-Motion>", lambda event: self.on_resize(event, move_x=0, move_y=1))
        self.canvas.tag_bind(self.Pic,"<ButtonRelease-1>", self.stop_drag)
        #?Punto inferior derecho
        self.Pid = self.canvas.create_image(self.x + self.Width - 2,self.y + self.Height - 2, anchor="nw", image=self.square_point)
        self.canvas.tag_bind(self.Pid,"<Button-1>", self.start_drag)
        self.canvas.tag_bind(self.Pid,"<B1-Motion>", lambda event: self.on_resize(event, move_x=1, move_y=1))
        self.canvas.tag_bind(self.Pid,"<ButtonRelease-1>", self.stop_drag)
        #?Punto lateral izquierdo
        self.Pli = self.canvas.create_image(self.x - 2, self.y + round((self.Height/2))-2, anchor="nw", image=self.V_line_point)
        self.canvas.tag_bind(self.Pli,"<Button-1>", self.start_drag)
        self.canvas.tag_bind(self.Pli,"<B1-Motion>", lambda event: self.on_resize(event, move_x=-1, move_y=0, anchor_x=1))
        self.canvas.tag_bind(self.Pli,"<ButtonRelease-1>", self.stop_drag)
        #?Punto lateral derecho
        self.Pld = self.canvas.create_image(self.x + self.Width - 2, self.y + round((self.Height/2))-2, anchor="nw", image=self.V_line_point)
        self.canvas.tag_bind(self.Pld,"<Button-1>", self.start_drag)
        self.canvas.tag_bind(self.Pld,"<B1-Motion>", lambda event: self.on_resize(event, move_x=1, move_y=0))
        self.canvas.tag_bind(self.Pld,"<ButtonRelease-1>", self.stop_drag)
        
        self.drag_data = {"x": 0, "y": 0}


    def start_drag(self, event):
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        
    def stop_drag(self, event):
        self.drag_data = {"x": 0, "y": 0}

    def on_drag(self, event):
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]
        new_x = self.x + dx
        new_y = self.y + dy
        # Move the text
        self.canvas.move(self.canvas_text, dx, dy)
        self.canvas.move(self.text_container, dx, dy)
        self.canvas.move(self.Psi, dx, dy)
        self.canvas.move(self.Psd, dx, dy)
        self.canvas.move(self.Pii, dx, dy)
        self.canvas.move(self.Pid, dx, dy)
        self.canvas.move(self.Psc, dx, dy)
        self.canvas.move(self.Pic, dx, dy)
        self.canvas.move(self.Pli, dx, dy)
        self.canvas.move(self.Pld, dx, dy)
        # Update the current position
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        # Update the current position
        self.x = new_x
        self.y = new_y

    def DoubleClick(self, event):
        self.editing = not self.editing
        self.canvas.focus_set()
        current_focus = self.canvas.focus_get()
        if self.editing:
            self.text = self.text + '|'
            self.cursor_position += 1
            self.canvas.itemconfig(self.canvas_text, text=self.text)
        elif self.editing == False:
            self.text = self.text[:self.cursor_position] + self.text[self.cursor_position + 1:]
            self.canvas.itemconfig(self.canvas_text, text=self.text)
            self.cursor_position = len(self.text)
        '''if current_focus == self.canvas:
            print("The canvas has keyboard focus.")
        else:
            print("Another widget has keyboard focus:", current_focus)'''

    def Re_write(self, event):
        current_focus = self.canvas.focus_get()
        if current_focus == self.canvas:
            key = event.char
            if key:
                if self.size_text()[0]>self.Width:
                    indexes = [i for i, c in enumerate(self.text) if c == ' ']
                    ultimo_indice = indexes[-1]
                    self.text = self.text[:self.cursor_position] + self.text[self.cursor_position + 1:]
                    self.text = self.text[:ultimo_indice] + '\n' + self.text[ultimo_indice:]
                    self.cursor_position += 1
                    self.text = self.text[:self.cursor_position] + '|' +  self.text[self.cursor_position + 1:]
                    self.text = self.text[:self.cursor_position] + key + self.text[self.cursor_position:]
                else:
                    self.text = self.text[:self.cursor_position] + key + self.text[self.cursor_position:]
        
                self.cursor_position += 1
                self.canvas.itemconfig(self.canvas_text, text=self.text)
                

    def move_cursor_left(self, event):
        if self.editing and self.cursor_position > 0:
            if self.cursor_position == len(self.text):
                self.text = self.text[:self.cursor_position-1]
            else:
                self.text = self.text[:self.cursor_position] + self.text[self.cursor_position+1:]
            self.cursor_position -= 1
            self.text = self.text[:self.cursor_position] + "|" + self.text[self.cursor_position:]
            self.canvas.itemconfig(self.canvas_text, text=self.text)

    def move_cursor_right(self, event):
        if self.editing and self.cursor_position < len(self.text):
            self.text = self.text[:self.cursor_position] + self.text[self.cursor_position+1:]
            self.cursor_position += 1
            self.text = self.text[:self.cursor_position] + "|" + self.text[self.cursor_position:]
            self.canvas.itemconfig(self.canvas_text, text=self.text)

    def backspace(self, event):
        if self.editing and self.cursor_position > 0:
            self.text = self.text[:self.cursor_position - 1] + self.text[self.cursor_position:]
            self.cursor_position -= 1
            self.canvas.itemconfig(self.canvas_text, text=self.text)

    def size_text(self):
        bounds = self.canvas.bbox(self.canvas_text)  # returns a tuple like (x1, y1, x2, y2)
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]
        return (width, height)
    
    def on_resize(self, event, move_x=0, move_y=0, sign = 1, anchor_x = 0, anchor_y = 0):
        actual_x, actual_y, actual_width, actual_heigth = self.canvas.coords(self.text_container)
        # *for the anchor
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]
        
        if move_x != 0 and move_y != 0:
            aspect_ratio = (self.Width + (sign*dx))/ self.Width
            size_x = int(np.around(aspect_ratio * self.Width))
            size_y = int(np.around(aspect_ratio * self.Height))
        else:
            drag_x = move_x * dx
            drag_y = move_y * dy
            size_x = self.Width + drag_x
            size_y = self.Height + drag_y

        new_x = actual_x + anchor_x * dx
        new_y = actual_y + anchor_y * dy

        if size_x <=0:
            size_x = 1
        if size_y <=0:
            size_y = 1
        #* resizin the textBox
        new_x2 = new_x + size_x
        new_y2 = new_y + size_y
        self.Width = size_x
        self.Height = size_y
        self.canvas.coords(self.text_container, new_x, new_y, new_x2, new_y2)
        self.canvas.coords(self.canvas_text, new_x, new_y)
        #? Move the reference points to resize the image
        #Punto superior izquierdo
        self.canvas.coords(self.Psi, self.x - 2, self.y - 2)
        #Punto superior central
        self.canvas.coords(self.Psc, self.x + round((self.Width/2)) - 2, self.y - 2)
        #Punto superior derecho
        self.canvas.coords(self.Psd, self.x + self.Width - 2,self.y - 2)
        #Punto inferior izquierdo
        self.canvas.coords(self.Pii, self.x - 2, self.y + self.Height - 2)
        #Punto inferior central
        self.canvas.coords(self.Pic, self.x + round((self.Width/2))-2, self.y + self.Height - 2)
        #Punto inferior derecho
        self.canvas.coords(self.Pid, self.x + self.Width - 2,self.y + self.Height - 2)
        #Punto lateral izquierdo
        self.canvas.coords(self.Pli, self.x - 2,self.y + round((self.Height/2))-2)
        #Punto lateral derecho
        self.canvas.coords(self.Pld, self.x + self.Width - 2,self.y + round((self.Height/2))-2)

        self.x = self.x + anchor_x * dx
        self.y = self.y + anchor_y * dy
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y


def Angle_between_vectors(vector1, vector2):
    # Calculate the angle in radians
    angle_radians = np.arccos(np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2)))

    if vector1[0]*vector2[1]-vector1[1]*vector2[0]<0:
        angle_radians = np.pi + (np.pi - angle_radians)

    return angle_radians

def sum_angles(angle_1, angle_2):
    total_degrees = angle_1 + angle_2
    if total_degrees < 0:
        total_degrees += 360.0
    elif total_degrees >= 360.0:
        total_degrees -= 360.0
    return total_degrees

