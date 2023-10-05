import tkinter as tk
from tkinter import filedialog, ttk, colorchooser
#from tkinter.ttk import Combobox
import customtkinter as ctk
from PIL import ImageTk, Image
from Vcss import DraggableLabel, InputNumber, List_of_fonts, Icon_button, CustomComboBox
from typing import Union, Callable
from typing import Optional
import os

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
    def __init__(self, *args,
                 width: int = 100,
                 command: Callable = None,
                 images: str = "Default/No_image.jpg",
                 json_list: dict = None,
                 on_press: Optional[callable] = None,
                 Otros: Optional[any] = None,
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
        self.configure(width=80, height=50)

        self.FrameButons = ctk.CTkFrame(self)
        self.FrameButons.configure(fg_color=("gray78", "gray28")) 

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.FrameButons.grid(row=0, column=0)
        
        # * frame scheme Input
        
        self.frameMove = ctk.CTkLabel(self.FrameButons, image=self.smallMove, width=30, text="")
        self.frameMove.grid(row=0, column=0, padx=1, pady=1)

        self.frameImage = ctk.CTkLabel(self.FrameButons, image=self.smallImage, width=30, text="")
        self.frameImage.grid(row=0, column=1, padx=1, pady=1)

        self.frameInfomation = ctk.CTkFrame(self.FrameButons)
        self.frameInfomation.grid(row=0, column=2, padx=1, pady=1)
        
        if self.json_list['Type'] == 'image':
            self.Name_Label = ctk.CTkLabel(self.frameInfomation, text= "Name: " + os.path.basename(self.json_list['Name']))
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

    def get_itemData(self):
        
        return
    
    def update_row(self, n_list):
        self.json_list = n_list
        return

class property_image_bar(ctk.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 command: Callable = None,
                 json_list: dict = None,
                 Hook: Optional[any] = None,
                 **kwargs):
        
        super().__init__(*args, **kwargs)
        self.json_list = json_list
        self.Hook = Hook
        self.relative_x, self.relative_y = self.Hook[0]
        self.External_Move = self.Hook[1]
        self.background_data = self.Hook[2]
        self.External_Rotate = self.Hook[3]
        self.Id = self.json_list['Id']
        # *Barra de propiedades de formatos imagenes
        
        self.tools_image_frame = ctk.CTkFrame(self)
        self.tools_image_frame.grid(row=0, column=0, padx=0, pady=(10, 0), sticky="nsew")

        self.label_x_position = ctk.CTkLabel(self.tools_image_frame, text= "X:")
        self.label_x_position.grid(row=0, column=0, padx=5, pady=5)

        self.Input_x_position = InputNumber(self.tools_image_frame, width=50, step_size=1, Hook = self.Update_image_move_x)
        self.Input_x_position.set(self.json_list['x_position'] - self.relative_x)
        self.Input_x_position.grid(row=0, column=1 , padx=5, pady=5)

        self.label_y_position = ctk.CTkLabel(self.tools_image_frame, text= "Y:")
        self.label_y_position.grid(row=0, column=2, padx=5, pady=5)

        self.Input_y_position = InputNumber(self.tools_image_frame, width=50, step_size=1, Hook = self.Update_image_move_y)
        self.Input_y_position.set(self.json_list['y_position'] - self.relative_y)
        self.Input_y_position.grid(row=0, column=3 , padx=5, pady=5)

        self.label_width = ctk.CTkLabel(self.tools_image_frame, text= "W:")
        self.label_width.grid(row=0, column=4, padx=5, pady=5)

        self.Input_width = InputNumber(self.tools_image_frame, width=50, step_size=1, Hook= self.Update_image_size_x)
        self.Input_width.set(self.json_list['Width'])
        self.Input_width.grid(row=0, column=5 , padx=5, pady=5)

        self.label_heid = ctk.CTkLabel(self.tools_image_frame, text= "H:")
        self.label_heid.grid(row=0, column=6, padx=5, pady=5)

        self.Input_heid = InputNumber(self.tools_image_frame, width=50, step_size=1, Hook= self.Update_image_size_y)
        self.Input_heid.set(self.json_list['Height'])
        self.Input_heid.grid(row=0, column=7 , padx=5, pady=5)

        self.label_rotate = ctk.CTkLabel(self.tools_image_frame, text= "Girar:")
        self.label_rotate.grid(row=0, column=8, padx=5, pady=5)

        self.Input_rotate = InputNumber(self.tools_image_frame, width=50, step_size=1, ciclic= True, max=360, Hook = self.Update_rotate)
        self.Input_rotate.set(self.json_list['Rotate'])
        self.Input_rotate.grid(row=0, column=9 ,padx=5, pady=5)

        checkbox_xCentro = ctk.CTkCheckBox(self.tools_image_frame, text= "xCentro:")
        #checkbox_xCentro.
        checkbox_xCentro.grid(row=0, column=11, padx=5, pady=5)

        checkbox_yCentro = ctk.CTkCheckBox(self.tools_image_frame, text= "yCentro:")
        
        checkbox_yCentro.grid(row=0, column=12, padx=5, pady=5)

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
    
    def update_image_data(self, updated_data):
        if self.json_list['Type'] == 'image':
            self.json_list = updated_data
            self.Input_x_position.set(self.json_list['x_position'] - self.relative_x)
            self.Input_y_position.set(self.json_list['y_position'] - self.relative_y)
            self.Input_width.set(self.json_list['Width'])
            self.Input_heid.set(self.json_list['Height'])
            self.Input_rotate.set(self.json_list['Rotate'])
        #print('se actualizo la data')

class property_text_bar(ctk.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 command: Callable = None,
                 json_list: dict = None,
                 Hook: Optional[any] = None,
                 **kwargs):
        
        super().__init__(*args, **kwargs)
        self.json_list = json_list
        self.Hook = Hook
        self.Id = self.json_list['Id']
        self.relative_x, self.relative_y = self.Hook[0]
        self.Change_anchor_text = self.Hook[1]
        self.Fonts_list = List_of_fonts('C:\Windows\Fonts')
        #print(self.Fonts_list)

        self.label_x_position = ctk.CTkLabel(self, text= "X:")
        self.label_x_position.grid(row=0, column=0, padx=5, pady=5)

        self.Input_x_position = InputNumber(self, width=50, step_size=1)
        self.Input_x_position.set(self.json_list['x_position'] - self.relative_x)
        self.Input_x_position.grid(row=0, column=1 , padx=5, pady=5)

        self.label_y_position = ctk.CTkLabel(self, text= "Y:")
        self.label_y_position.grid(row=0, column=2, padx=5, pady=5)

        self.Input_y_position = InputNumber(self, width=50, step_size=1)
        self.Input_y_position.set(self.json_list['y_position'] - self.relative_y)
        self.Input_y_position.grid(row=0, column=3 , padx=5, pady=5)

        self.label_width = ctk.CTkLabel(self, text= "W:")
        self.label_width.grid(row=0, column=4, padx=5, pady=5)

        self.Input_width = InputNumber(self, width=50, step_size=1)
        self.Input_width.set(self.json_list['Width'])
        self.Input_width.grid(row=0, column=5 , padx=5, pady=5)

        self.label_heid = ctk.CTkLabel(self, text= "H:")
        self.label_heid.grid(row=0, column=6, padx=5, pady=5)

        self.Input_heid = InputNumber(self, width=50, step_size=1)
        self.Input_heid.set(self.json_list['Height'])
        self.Input_heid.grid(row=0, column=7 , padx=5, pady=5)

        self.Cb_Font_text = CustomComboBox(self, values=self.Fonts_list)
        self.Cb_Font_text.grid(row=0, column=8, padx=5, pady=5)
        
        self.Cb_Font_size = ctk.CTkComboBox(self, values=['8','9','10','11','12','14','16','18','20','22','24','26','28','36','48','72'])
        self.Cb_Font_size.grid(row=0, column=9, padx=5, pady=5)

        self.Bt_color_choose = Icon_button(self, Icon_image = './Default/color_font.png', Function= self.anchor_left )
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
            print('intenta actualizar')
            self.json_list = updated_data
            self.Id = self.json_list['Id']

    def choose_color(self):
        # variable to store hexadecimal code of color
        color_code = tk.colorchooser.askcolor(title ="Choose color")
        print(color_code)