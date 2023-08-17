from PIL import Image, ImageDraw, ImageFont
from collections import Counter
from transforms import RGBTransform # from source code mentioned above
import customtkinter as ctk

class PImage:
    # Constructor
    def __init__(self, name):
        # Instance attributes
        self.name = name
        self.image = Image.open(name)
    
    def properties(self, property):
        i = self.image
        #resize the image
        resized_image = i.resize((property['width'], property['high']))
        #Rotate the image
        image_rotated = resized_image.rotate(property['rotate'], expand=True)
        # Load the PNG image and convert it to RGBA
        png_image = image_rotated.convert('RGBA')
        # Create a new RGBA image with the same size as the PNG image
        new_image = Image.new('RGBA', png_image.size, (0, 0, 0, 0))
        # Paste the PNG image on the new RGBA image with the alpha channel as the mask
        new_image.paste(png_image, (0, 0), mask=png_image.split()[3])
        return new_image
    
    def get_principal_color(self):
        # Open the image and convert it to RGB mode
        image = self.image.resize((7,7)).convert('RGBA')
        # Get the pixel data as a list of RGB tuples
        pixels = list(image.getdata())
        # Count the occurrences of each color
        color_counts = Counter(pixels)
        # Find the color with the highest count (most common color)
        most_common_color = color_counts.most_common(1)[0][0]
        return most_common_color
    
    def color_filter(self, color):
        lena = self.image
        lena = lena.convert('RGB') # ensure image has 3 channels
        withFilter = RGBTransform().mix_with(color,factor=.30).applied_to(lena)
        return withFilter
    
class PText:
    # Constructor
    def __init__(self, text):
        # Instance attributes
        self.text = text

    def Text_replace(self, variables, replacement):
        text = self.text
        for i, key in enumerate(variables):#Pepe es una lista de claves
            text = text.replace(key, replacement[i])
        return text


    

