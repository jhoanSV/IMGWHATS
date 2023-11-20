import json
import tkinter as tk
from tkinter import filedialog, ttk, colorchooser
#from tkinter.ttk import Combobox
import customtkinter as ctk
from PIL import ImageTk, Image
from Vcss import DraggableLabel, InputNumber, List_of_fonts, Icon_button, CustomComboBox, FlatList
from typing import Union, Callable
from typing import Optional
import os
import openpyxl

class ImageContainer(ctk.CTkCanvas):
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
        self.configure(width=self.width, height=self.height)
        #num_items = len(self.json_list)

        #canvas = tk.Canvas
        size = (self.Background_image_width, self.Background_image_height)
        ImageContainer = ctk.CTkFrame(self, width= self.width, height= self.height, fg_color='#D9D9D9')
        ImageContainer.pack(fill= None)
        ImageContainer.lower()

        for Item in  self.json_list:
            if Item['Type'] == 'Background':
                size_background = Item['Width'], Item['Height']
                background_color = Item['BackgroundColor']
                on_x = (self.width - Item['Width'])/2
                on_y = (self.height - Item['Height'])/2
                background_image = Image.new('RGB',size_background, background_color)
                Bg_image = ctk.CTkImage(background_image, size = size_background)
                background_continer = ctk.CTkLabel(self, image= Bg_image, text="", width=Item['Width'], height=Item['Height'])
                background_continer.place(x=on_x, y=on_y)
                #background_continer.lower()
            elif Item['Type'] == 'image':
                picture = Image.open(Item['Name'])
                frameImage = DraggableLabel(self, image=picture)
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
                new_image_tk = ctk.CTkImage(new_image)
                child.configure(image=new_image_tk)
                child.image_tk = new_image_tk
                child.image_width = new_width
                child.image_height = new_height

   
class ItemElement(ctk.CTkFrame):
    def __init__(self, master, *args,
                 width: int = 100,
                 command: Callable = None,
                 images: str = "Default/No_image.jpg",
                 json_list: dict = None,
                 on_press: Optional[callable] = None,
                 Otros: Optional[any] = None,
                 **kwargs):
        
        super().__init__(master, *args, **kwargs)
        # *variables
        self.width = width
        self.master = master
        self.command = command
        self.images = images
        self.json_list = json_list
        self.Hook = Otros['Hook']
        self.smallImage = ctk.CTkImage(Image.new('RGBA', (30,30), '#FFFFFF'))
        self.Name = ''
        if self.json_list['Type' ] == 'image':
            self.smallImage = ctk.CTkImage(Image.open(self.json_list['Name']), size=(30,30))
            self.Name = os.path.basename(self.json_list['Name'])
        elif self.json_list['Type' ] == 'text':
            self.smallImage = ctk.CTkImage(Image.open('Default/Text_Icon.png'), size=(30,30))
        elif self.json_list['Type'] == 'folder':
            self.smallImage = ctk.CTkImage(Image.open(self.json_list['Name']), size=(30,30))
        self.smallMove = ctk.CTkImage(light_image=Image.open("Default/bars_dark.png"), dark_image=Image.open("Default/bars_dark.png"), size=(30, 30))
        self.back_one_elements, self.advance_one_elements = self.Hook[0],  self.Hook[1]

        # *frame configuration
        self.configure(fg_color=("gray78", "gray28"))  # set frame color
        self.configure(width=self.width, height=50)
        #self.configure(fill=False)
        self.FrameButons = ctk.CTkFrame(self)
        self.FrameButons.configure(fg_color=("gray78", "gray28")) 

        self.grid(sticky='ew')
        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands
        self.grid_columnconfigure(2, weight=3)  # entry expands

        self.FrameButons.grid(row=0, column=0)
        
        # * frame scheme Input

        self.frameMove = ctk.CTkLabel(self.FrameButons, image=self.smallMove, width=30, text="")
        self.frameMove.grid(row=0, column=0, padx=1, pady=1)
        self.frameMove.bind("<Button-1>", self.activate_element)

        self.frameImage = ctk.CTkLabel(self.FrameButons, image=self.smallImage, width=30, text="")
        self.frameImage.grid(row=0, column=1, padx=1, pady=1)

        self.frameInfomation = ctk.CTkFrame(self.FrameButons)
        self.frameInfomation.grid(row=0, column=2, padx=1, pady=1, sticky='ew')
        
        self.Name_image = ctk.CTkLabel(self.frameInfomation, text= "Name: " + self.Name)
        self.Name_image.grid(row=0, column=0, padx=0, pady=0)

        self.Name_Label = ctk.CTkLabel(self.frameInfomation, text= "Type: " + self.json_list['Type'])
        self.Name_Label.grid(row=1, column=0, padx=0, pady=0)

        self.frameChangeOrder = ctk.CTkFrame(self.FrameButons)
        self.frameChangeOrder.grid(row=0, column=3, padx=1, pady=1)

        self.Bt_uper_order = Icon_button(self.frameChangeOrder, Icon_image = './Default/up-arrow.png', Function= self.tag_lower)
        self.Bt_uper_order.grid(row=0, column=0, padx=0, pady=0)

        self.Bt_change_order = Icon_button(self.frameChangeOrder, Icon_image = './Default/down-arrow.png', Function= self.tag_uper)
        self.Bt_change_order.grid(row=1, column=0, padx=0, pady=0)

    def activate_element(self, event):
        self.Hook[2](self.json_list['Id'])

    def tag_uper(self):
        if self.json_list['Type'] != 'Background':
            self.advance_one_elements(self.json_list['Id'])

    def tag_lower(self):
        if self.json_list['Type'] != 'Background':
            self.back_one_elements(self.json_list['Id'])

    def get(self) -> Union[float, None]:
        try:
            return float(self.entry.get())
        except ValueError:
            return None

    def set(self, value: float):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(float(value)))

    def get_itemData(self):
        
        return
    
    def update_row(self, n_list):
        self.json_list = n_list
        self.Name_Label.configure(text= "Type: " + self.json_list['Type'])
        if self.json_list['Type' ] == 'image':
            self.smallImage = ctk.CTkImage(Image.open(self.json_list['Name']), size=(30,30))
            self.Name_image.configure(text= "Name: " + os.path.basename(self.json_list['Name']))
        elif self.json_list['Type' ] == 'text':
            self.smallImage = ctk.CTkImage(Image.open('Default/Text_Icon.png'), size=(30,30))
            self.Name_image.configure(text= "Name: ")
        elif self.json_list['Type'] == 'folder':
            self.smallImage = ctk.CTkImage(Image.open(self.json_list['Name']), size=(30,30))
            self.Name_image.configure(text= "Name: ")
        self.frameImage.configure(image= self.smallImage)

class property_image_bar(ctk.CTkFrame):
    def __init__(self, master, *args,
                 width: int = 100,
                 command: Callable = None,
                 json_list: dict = None,
                 Hook: Optional[any] = None,
                 **kwargs):
        
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.json_list = json_list
        self.Hook = Hook
        self.relative_x, self.relative_y = self.Hook[0]
        self.External_Move = self.Hook[1]
        self.background_data = self.Hook[2]
        self.External_Rotate = self.Hook[3]
        self.tags_lower = self.Hook[4]
        self.tags_uper = self.Hook[5]
        self.Id = self.json_list['Id']
        # *Barra de propiedades de formatos imagenes
        if self.json_list['Type'] == 'image':
            self.label_x_position = ctk.CTkLabel(self, text= "X:")
            self.label_x_position.grid(row=0, column=0, padx=5, pady=5)

            self.Input_x_position = InputNumber(self, width=50, step_size=1, Hook = self.Update_image_move_x)
            self.Input_x_position.set(self.json_list['x_position'] - self.relative_x)
            self.Input_x_position.grid(row=0, column=1 , padx=5, pady=5)

            self.label_y_position = ctk.CTkLabel(self, text= "Y:")
            self.label_y_position.grid(row=0, column=2, padx=5, pady=5)

            self.Input_y_position = InputNumber(self, width=50, step_size=1, Hook = self.Update_image_move_y)
            self.Input_y_position.set(self.json_list['y_position'] - self.relative_y)
            self.Input_y_position.grid(row=0, column=3 , padx=5, pady=5)

            self.label_width = ctk.CTkLabel(self, text= "W:")
            self.label_width.grid(row=0, column=4, padx=5, pady=5)

            self.Input_width = InputNumber(self, width=50, step_size=1, Hook= self.Update_image_size_x)
            self.Input_width.set(self.json_list['Width'])
            self.Input_width.grid(row=0, column=5 , padx=5, pady=5)

            self.label_heid = ctk.CTkLabel(self, text= "H:")
            self.label_heid.grid(row=0, column=6, padx=5, pady=5)

            self.Input_heid = InputNumber(self, width=50, step_size=1, Hook= self.Update_image_size_y)
            self.Input_heid.set(self.json_list['Height'])
            self.Input_heid.grid(row=0, column=7 , padx=5, pady=5)

            self.label_rotate = ctk.CTkLabel(self, text= "Girar:")
            self.label_rotate.grid(row=0, column=8, padx=5, pady=5)

            self.Input_rotate = InputNumber(self, width=50, step_size=1, ciclic= True, max=360, Hook = self.Update_rotate)
            self.Input_rotate.set(self.json_list['Rotate'])
            self.Input_rotate.grid(row=0, column=9 ,padx=5, pady=5)

            checkbox_xCentro = ctk.CTkCheckBox(self, text= "xCentro:")
            checkbox_xCentro.grid(row=0, column=11, padx=5, pady=5)

            checkbox_yCentro = ctk.CTkCheckBox(self, text= "yCentro:")
            checkbox_yCentro.grid(row=0, column=12, padx=5, pady=5)

            self.Bt_color_choose = Icon_button(self, Icon_image = './Default/color_font.png', Function= self.tag_uper )
            self.Bt_color_choose.grid(row=0, column=10, padx=5, pady=5)

        else:
            self.label_x_position = ctk.CTkLabel(self, text= "X:")
            self.label_x_position.grid(row=0, column=0, padx=5, pady=5)

            self.Input_x_position = InputNumber(self, width=50, step_size=1, Hook = self.Update_image_move_x)
            self.Input_x_position.set(0 - self.relative_x)
            self.Input_x_position.grid(row=0, column=1 , padx=5, pady=5)

            self.label_y_position = ctk.CTkLabel(self, text= "Y:")
            self.label_y_position.grid(row=0, column=2, padx=5, pady=5)

            self.Input_y_position = InputNumber(self, width=50, step_size=1, Hook = self.Update_image_move_y)
            self.Input_y_position.set(0 - self.relative_y)
            self.Input_y_position.grid(row=0, column=3 , padx=5, pady=5)

            self.label_width = ctk.CTkLabel(self, text= "W:")
            self.label_width.grid(row=0, column=4, padx=5, pady=5)

            self.Input_width = InputNumber(self, width=50, step_size=1, Hook= self.Update_image_size_x)
            self.Input_width.set(0)
            self.Input_width.grid(row=0, column=5 , padx=5, pady=5)

            self.label_heid = ctk.CTkLabel(self, text= "H:")
            self.label_heid.grid(row=0, column=6, padx=5, pady=5)

            self.Input_heid = InputNumber(self, width=50, step_size=1, Hook= self.Update_image_size_y)
            self.Input_heid.set(0)
            self.Input_heid.grid(row=0, column=7 , padx=5, pady=5)

            self.label_rotate = ctk.CTkLabel(self, text= "Girar:")
            self.label_rotate.grid(row=0, column=8, padx=5, pady=5)

            self.Input_rotate = InputNumber(self, width=50, step_size=1, ciclic= True, max=360, Hook = self.Update_rotate)
            self.Input_rotate.set(0)
            self.Input_rotate.grid(row=0, column=9 ,padx=5, pady=5)

            checkbox_xCentro = ctk.CTkCheckBox(self, text= "xCentro:")
            checkbox_xCentro.grid(row=0, column=11, padx=5, pady=5)

            checkbox_yCentro = ctk.CTkCheckBox(self, text= "yCentro:")
            checkbox_yCentro.grid(row=0, column=12, padx=5, pady=5)

            self.Bt_color_choose = Icon_button(self, Icon_image = './Default/color_font.png', Function= self.tag_uper )
            self.Bt_color_choose.grid(row=0, column=10, padx=5, pady=5)

    def Update_image_move_x(self, value):
        if self.json_list['Type'] == 'image':
            self.External_Move(self.Id, value, 'x')

    def Update_image_move_y(self, value):
        if self.json_list['Type'] == 'image':
            self.External_Move(self.Id, value, 'y')

    def Update_image_size_x(self, value):
        if self.json_list['Type'] == 'image':
            self.External_Move(self.Id, value, 'Width')

    def Update_image_size_y(self, value):
        if self.json_list['Type'] == 'image':
            self.External_Move(self.Id, value, 'Height')

    def Centering_in_x(self):
        if self.json_list['Type'] == 'image':
            New_X = self.background_data['x_position'] + self.background_data['Width']/2 - self.json_list['Width']/2
            self.External_Move(self.Id, New_X, 'x')

    def Update_rotate(self, value):
        if self.json_list['Type'] == 'image':
            self.External_Rotate(self.Id, value)

    def tag_lower(self):
        if self.json_list['Type'] == 'image':
            #print('entro al tag lower', self.Id)
            self.tags_lower(self.Id)

    def tag_uper(self):
        if self.json_list['Type'] == 'image':
            #print('entro al tag lower', self.Id)
            self.tags_uper(self.Id)
    
    def update_image_data(self, updated_data):
        self.json_list = updated_data
        if self.json_list['Type'] == 'image':
            self.Input_x_position.set(self.json_list['x_position'] - self.relative_x)
            self.Input_y_position.set(self.json_list['y_position'] - self.relative_y)
            self.Input_width.set(self.json_list['Width'])
            self.Input_heid.set(self.json_list['Height'])
            self.Input_rotate.set(self.json_list['Rotate'])
            self.Id = self.json_list['Id']

    def Change_relative_to(self, value):
        self.relative_x, self.relative_y = value[0], value[1]

class property_text_bar(ctk.CTkFrame):
    def __init__(self, master, *args,
                 width: int = 100,
                 command: Callable = None,
                 json_list: dict = None,
                 Hook: Optional[any] = None,
                 **kwargs):
        
        super().__init__(master, *args, **kwargs)
        #*Variables
        self.master = master
        self.json_list = json_list
        self.Hook = Hook
        self.Id = self.json_list['Id']
        self.relative_x, self.relative_y = self.Hook[0]
        self.Change_anchor_text = self.Hook[1]
        self.External_Move = self.Hook[2]
        self.Change_color_font = self.Hook[3]
        self.change_text = self.Hook[4]
        self.Fonts_list = List_of_fonts('C:\Windows\Fonts')
        #print(self.Fonts_list)
        #*Body
        if self.json_list['Type'] == 'text':
            self.label_x_position = ctk.CTkLabel(self, text= "X:")
            self.label_x_position.grid(row=0, column=0, padx=5, pady=5)

            self.Input_x_position = InputNumber(self, width=50, step_size=1, Hook= self.Update_text_move_x)
            self.Input_x_position.set(self.json_list['x_position'] - self.relative_x)
            self.Input_x_position.grid(row=0, column=1 , padx=5, pady=5)

            self.label_y_position = ctk.CTkLabel(self, text= "Y:")
            self.label_y_position.grid(row=0, column=2, padx=5, pady=5)

            self.Input_y_position = InputNumber(self, width=50, step_size=1, Hook= self.Update_text_move_y)
            self.Input_y_position.set(self.json_list['y_position'] - self.relative_y)
            self.Input_y_position.grid(row=0, column=3 , padx=5, pady=5)

            self.label_width = ctk.CTkLabel(self, text= "W:")
            self.label_width.grid(row=0, column=4, padx=5, pady=5)

            self.Input_width = InputNumber(self, width=50, step_size=1, Hook= self.Update_text_size_x)
            self.Input_width.set(self.json_list['Width'])
            self.Input_width.grid(row=0, column=5 , padx=5, pady=5)

            self.label_heid = ctk.CTkLabel(self, text= "H:")
            self.label_heid.grid(row=0, column=6, padx=5, pady=5)

            self.Input_heid = InputNumber(self, width=50, step_size=1, Hook= self.Update_text_size_y)
            self.Input_heid.set(self.json_list['Height'])
            self.Input_heid.grid(row=0, column=7 , padx=5, pady=5)

            self.Cb_Font_text = CustomComboBox(self, values=self.Fonts_list, Function= self.Change_font)
            self.Cb_Font_text.grid(row=0, column=8, padx=5, pady=5)
            
            self.Cb_Font_size = ctk.CTkComboBox(self, values=['8','9','10','11','12','14','16','18','20','22','24','26','28','36','48','72'])
            self.Cb_Font_size.grid(row=0, column=9, padx=5, pady=5)

            self.Bt_color_choose = Icon_button(self, Icon_image = './Default/color_font.png', Function= self.choose_color )
            self.Bt_color_choose.grid(row=0, column=10, padx=5, pady=5)

            self.Bt_left_text = Icon_button(self, Icon_image = './Default/left_text.png', Function= self.anchor_left)
            self.Bt_left_text.grid(row=0, column=11, padx=5, pady=5)

            self.Bt_center_text = Icon_button(self, Icon_image = './Default/center_text.png', Function= self.anchor_center)
            self.Bt_center_text.grid(row=0, column=12, padx=5, pady=5)

            self.Bt_right_text = Icon_button(self, Icon_image = './Default/right_text.png', Function= self.anchor_right)
            self.Bt_right_text.grid(row=0, column=13, padx=5, pady=5)

        else:
            self.label_x_position = ctk.CTkLabel(self, text= "X:")
            self.label_x_position.grid(row=0, column=0, padx=5, pady=5)

            self.Input_x_position = InputNumber(self, width=50, step_size=1, Hook= self.Update_text_move_x)
            self.Input_x_position.set(0 - self.relative_x)
            self.Input_x_position.grid(row=0, column=1 , padx=5, pady=5)

            self.label_y_position = ctk.CTkLabel(self, text= "Y:")
            self.label_y_position.grid(row=0, column=2, padx=5, pady=5)

            self.Input_y_position = InputNumber(self, width=50, step_size=1, Hook= self.Update_text_move_y)
            self.Input_y_position.set(0 - self.relative_y)
            self.Input_y_position.grid(row=0, column=3 , padx=5, pady=5)

            self.label_width = ctk.CTkLabel(self, text= "W:")
            self.label_width.grid(row=0, column=4, padx=5, pady=5)

            self.Input_width = InputNumber(self, width=50, step_size=1, Hook= self.Update_text_size_x)
            self.Input_width.set(0)
            self.Input_width.grid(row=0, column=5 , padx=5, pady=5)

            self.label_heid = ctk.CTkLabel(self, text= "H:")
            self.label_heid.grid(row=0, column=6, padx=5, pady=5)

            self.Input_heid = InputNumber(self, width=50, step_size=1, Hook= self.Update_text_size_y)
            self.Input_heid.set(0)
            self.Input_heid.grid(row=0, column=7 , padx=5, pady=5)

            self.Cb_Font_text = CustomComboBox(self, values=self.Fonts_list, Function= self.Change_font)
            self.Cb_Font_text.grid(row=0, column=8, padx=5, pady=5)
            
            self.Cb_Font_size = ctk.CTkComboBox(self, values=['8','9','10','11','12','14','16','18','20','22','24','26','28','36','48','72'])
            self.Cb_Font_size.grid(row=0, column=9, padx=5, pady=5)

            self.Bt_color_choose = Icon_button(self, Icon_image = './Default/color_font.png', Function= self.choose_color )
            self.Bt_color_choose.grid(row=0, column=10, padx=5, pady=5)

            self.Bt_left_text = Icon_button(self, Icon_image = './Default/left_text.png', Function= self.anchor_left)
            self.Bt_left_text.grid(row=0, column=11, padx=5, pady=5)

            self.Bt_center_text = Icon_button(self, Icon_image = './Default/center_text.png', Function= self.anchor_center)
            self.Bt_center_text.grid(row=0, column=12, padx=5, pady=5)

            self.Bt_right_text = Icon_button(self, Icon_image = './Default/right_text.png', Function= self.anchor_right)
            self.Bt_right_text.grid(row=0, column=13, padx=5, pady=5)

    def anchor_left(self):
        self.Change_anchor_text(self.Id, 'left')

    def anchor_center(self):
        print('entro al center')
        self.Change_anchor_text(self.Id, 'center')

    def anchor_right(self):
        print('entro al derecho')
        self.Change_anchor_text(self.Id, 'right')

    def update_text_data(self, updated_data):
        if updated_data['Type'] == 'text':
            self.json_list = updated_data
            self.Id = self.json_list['Id']
            self.Input_x_position.set(self.json_list['x_position'] - self.relative_x)
            self.Input_y_position.set(self.json_list['y_position'] - self.relative_y)
            self.Input_width.set(self.json_list['boxWidth'])
            self.Input_heid.set(self.json_list['boxHeight'])
            self.Cb_Font_text.set(self.json_list['fontType'])

    def Update_text_move_x(self, value):
        if self.json_list['Type'] == 'text':
            self.External_Move(self.Id, value, 'x')

    def Update_text_move_y(self, value):
        if self.json_list['Type'] == 'text':
            self.External_Move(self.Id, value, 'y')

    def Update_text_size_x(self, value):
        if self.json_list['Type'] == 'text':
            self.External_Move(self.Id, value, 'Width')

    def Update_text_size_y(self, value):
        if self.json_list['Type'] == 'text':
            self.External_Move(self.Id, value, 'Height')

    def choose_color(self):
        # variable to store hexadecimal code of color
        self.Change_color_font(self.Id)
        #color_code = tk.colorchooser.askcolor(title ="Choose color")
        #print(color_code[1])

    def Change_font(self, text):
        self.change_text(self.Id, 'font', text)

    def Change_relative_to(self, value):
        self.relative_x, self.relative_y = value[0], value[1]

class property_background_bar(ctk.CTkFrame):
    def __init__(self, master, *args,
                 width: int = 100,
                 command: Callable = None,
                 json_list: dict = None,
                 Hook: Optional[any] = None,
                 **kwargs):
        
        super().__init__(master, *args, **kwargs)
        #*Variables
        self.json_list = json_list
        self.Hook = Hook
        #*Body
        self.label_width = ctk.CTkLabel(self, text= "W:")
        self.label_width.grid(row=0, column=0, padx=5, pady=5)

        self.Input_width = InputNumber(self, width=50, step_size=1, Hook= self.Update_Width)
        self.Input_width.set(self.json_list['Width'])
        self.Input_width.grid(row=0, column=1, padx=5, pady=5)

        self.label_heid = ctk.CTkLabel(self, text= "H:")
        self.label_heid.grid(row=0, column=2, padx=5, pady=5)

        self.Input_heid = InputNumber(self, width=50, step_size=1, Hook= self.Update_Height)
        self.Input_heid.set(self.json_list['Height'])
        self.Input_heid.grid(row=0, column=3, padx=5, pady=5)

        self.Bt_left_text = Icon_button(self, Icon_image = './Default/change_orientation.png', Function= self.Change_orientation)
        self.Bt_left_text.grid(row=0, column=4, padx=5, pady=5)

        self.Bt_color_choose = Icon_button(self, Icon_image = './Default/color_font.png', Function= self.choose_color)
        self.Bt_color_choose.grid(row=0, column=5, padx=5, pady=5)

    def Update_Width(self, value):
        self.json_list['Width'] = value
        self.Hook[0]('Width', int(self.json_list['Width']))
        self.Input_width.set(self.json_list['Width'])
        return
    
    def Update_Height(self, value):
        self.json_list['Height'] = value
        self.Hook[0]('Height', int(self.json_list['Height']))
        self.Input_width.set(self.json_list['Height'])
        return
    
    def Change_orientation(self):
        New_h = self.json_list['Width']
        New_w = self.json_list['Height']
        self.Hook[0]('Width', New_w)
        self.Hook[0]('Height', New_h)
        return
    
    def choose_color(self):
        self.Hook[2]()
        return
    
    def Update_bg_data(self, data):
        self.json_list = data
        self.Input_width.set(self.json_list['Width'])
        self.Input_heid.set(self.json_list['Height'])


class Vincular_excel(ctk.CTkToplevel):
    def __init__(self, 
                 master,
                 F_vincular: Optional[callable] = None,
                 data_link: dict = {},
                 *args,
                 **kwargs):
        
        super().__init__(master, *args, **kwargs)
        #*configuración
        self.configure(title="Vincular")
        #*Variables
        self.data_link = data_link
        self.data = {}
        self.F_vincular = F_vincular
        #*Body
        self.Contenedor_buscar = ctk.CTkFrame(self)
        self.Contenedor_buscar.grid(row=0, column=0, padx=0, pady=0)

        self.L_direccion = ctk.CTkLabel(self.Contenedor_buscar, text= 'Dirección')
        self.L_direccion.grid(row=0, column=0, padx=0, pady=0)

        self.I_direccion = ctk.CTkEntry(self.Contenedor_buscar, fg_color='transparent')
        self.I_direccion.grid(row=0, column=1 , padx=0, pady=0)

        self.B_BuscarDireccion = ctk.CTkButton(self.Contenedor_buscar, text="Seleccionar", command=self.Get_columnLabels)
        self.B_BuscarDireccion.grid(row=0, column=2 , padx=0, pady=0)

        self.tabla_vinculada = FlatList(self, json_list= self.data, Item= Item_table, width=200, Otros=[self.shoose_principal])
        self.tabla_vinculada.grid(row=2, column=0, padx=0, pady=0)

        self.Contenedor_botones = ctk.CTkFrame(self)
        self.Contenedor_botones.grid(row=3, column=0, padx=0, pady=0)

        self.B_Cancelar = ctk.CTkButton(self.Contenedor_botones, text="Cancelar", fg_color='#FF3F4A')
        self.B_Cancelar.grid(row=0, column=0, padx=0, pady=0)

        self.B_Vincular = ctk.CTkButton(self.Contenedor_botones, text="Vincular", command= self.Vincular)
        self.B_Vincular.grid(row=0, column=1, padx=0, pady=0)

    def Get_columnLabels(self):
        filetypes = [("Excel Files", "*.xlsx;*.xlsm;*.xltx;*.xltm")]
        self.filename = filedialog.askopenfilename(title='Seleccionar hoja de calculo', filetypes=filetypes)
        self.I_direccion.delete(0, "end")
        self.I_direccion.insert(0, self.filename)
        self.wb = openpyxl.load_workbook(self.filename)
        self.data_link['Type'] = 'Excel'
        self.data_link['Path'] = self.filename
        # Get the list of sheet names
        sheet_names = self.wb.sheetnames
        #print(sheet_names)
        self.select_sheets = ctk.CTkFrame(self)
        self.select_sheets.grid(row=1, column=0, padx=0, pady=0)
        self.label_sheets =ctk.CTkLabel(self.select_sheets, text='Hojas')
        self.label_sheets.grid(row=1, column=0, padx=0, pady=0)
        self.combobox_sheets = ctk.CTkComboBox(self.select_sheets, values=sheet_names, command=self.get_data_sheet)
        self.combobox_sheets.grid(row=1, column=1, padx=0, pady=0)
    
    def get_data_sheet(self, sheet):
        self.data = {name: 0 for name in [item.value for item in self.wb[sheet][1] if item.value is not None]}
        self.tabla_vinculada.Update_list(self.data)
        self.data_link['Sheet'] = sheet
        return self.data

    def shoose_principal(self, key, val):
        for k in self.data.keys():
            if k == key:
                self.data[k] = val
            else:
                self.data[k] = 0
        self.tabla_vinculada.Update_list(self.data)
        self.data_link['Cell'] = key
        
    def Vincular(self):
        self.F_vincular(self.data_link)

class Item_table(ctk.CTkFrame):
    def __init__(self, 
                 master,
                 json_list: list = [],
                 Cell_type: Optional[dict] = {},
                 Otros: Optional[any]= None,
                 *args,
                 **kwargs):
        
        super().__init__(master, *args, **kwargs)
        #*variables
        self.json_list = json_list
        self.Cell_type = Cell_type
        self.check = tk.IntVar()
        self.check.set(0)
        self.Column_name = Otros['Project_name']
        self.Hook = Otros['Hook']
        self.Change = self.Hook[0]
        #*Body
        self.label = ctk.CTkLabel(self, text= self.Column_name)
        self.label.grid(row=0, column=0, padx=0, pady=0, sticky= "nsew")

        self.checkbox = ctk.CTkCheckBox(self, text= '', variable= self.check, onvalue=1, offvalue=0, command=self.Change_checkbox)
        self.checkbox.grid(row=0, column=1, padx=0, pady=0, sticky= "e")

    def get_itemData(self):
        return

    def update_row(self, n_list):
        self.json_list = n_list
        self.check.set(self.json_list)
        self.checkbox.configure(variable=self.check)

    def Change_checkbox(self):
        self.Change(self.Column_name, self.checkbox.get())
