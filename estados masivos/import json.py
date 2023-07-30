import json
from PIL import Image, ImageDraw, ImageFont
import os
import numpy as np

# *JSON image properties
with open('./proyextos.json', 'r') as json_file:
    image_properties_json = json.load(json_file)
# *List of Clients
CLient = ['17','27','28','46','140','433']
# *Create a background image with the required size 
size = width, height = 3000, 3000

def search_file(folder, filename):
    for f in os.listdir(folder):
        if f.startswith(filename):
            return os.path.join(folder, f)
    return None

# *Create a image with the properties of each item in the list of properties
def properties(image,property):
    #name = image['name']
    i = Image.open(image)
    #width, height = i.size
    #i.thumbnail(size_7000)
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

I_properties =  image_properties_json['proyecto1']



# TODO 
def TextBoxSize(width, height, text, font):
    windowsPath = font
    for size in range(1, np.maximum(width, height)):
        arial = ImageFont.FreeTypeFont(windowsPath, size=size)
        x_min, y_min, x_max, y_max = arial.getbbox(text)
        w = x_max - x_min
        h = y_max - y_min
        if w > width or h > height:
            break
    return [size, w, h]
    
#For each Client crete a new image
for cli in CLient:
    #apliying the properties to each image on the list of properties
    background_image = Image.new('RGB',size, 'white')
    for ImageProperty in I_properties:
        
        if ImageProperty['Type'] == 'image':
            # *Variables for each image
            x = ImageProperty['x_position']
            y = ImageProperty['y_position']
            if ImageProperty['name'].endswith('jpg') or ImageProperty['name'].endswith('png'):
                image1 = properties(ImageProperty['name'],ImageProperty)
            else:
                fil = search_file(ImageProperty['name'],cli)
                image1 = properties(fil,ImageProperty)

            # *Check if the RGBA image have to be at the center in the x position or in the y position
            if ImageProperty['xCenter'] == True:
                x = int(round((size[0] - ImageProperty['width'])/2))
            if ImageProperty['yCenter'] == True:
                y = int(round((size[1] - ImageProperty['high'])/2))

            # * Paste the new RGBA image with the PNG image on top of the background image
            background_image.paste(image1, (x, y), image1)

        elif ImageProperty['Type'] == 'text':
            # *Variables for the text
            x = ImageProperty['x_position']
            y = ImageProperty['y_position']
            fontType = 'C:\\Windows\\Fonts\\' + ImageProperty['fontType']
            fontColor = tuple(map(int, ImageProperty['color'].strip('()').split(',')))
            text = ImageProperty['text']
            alingType = ImageProperty['align']
            bold = ImageProperty['bold']
            italic = ImageProperty['italic']
            fontSize = ImageProperty['fontSize']
            boxWidth = ImageProperty['boxWidth']
            boxHeight = ImageProperty['boxHeight']

            # *Check if the text have to be at the center in the x position or in the y position
            fontSizeBox = TextBoxSize(boxWidth, boxHeight, text, fontType)
            lines = text.splitlines()
            font = ImageFont.truetype(fontType, fontSizeBox[0])
            # Get the width of the bounding box of the longest line.
            w = font.getbbox(max(lines, key=lambda s: len(s)))[2]
            # Get the height of the bounding box of the text.
            h = font.getbbox(text)[1] * len(lines)

            if ImageProperty['xCenter'] == True:
                x = int(round((size[0]- w)/2))
                #x = int(round((size[0]- fontSizeBox[1])/2))
            if ImageProperty['yCenter'] == True:
                y = int(round((size[1]- h)/2))
            # *put the text into the image
            #font = ImageFont.truetype(fontType, fontSizeBox[0])
            draw = ImageDraw.Draw(background_image)
            draw.multiline_text((x, y), text, font=font, fill=fontColor, align=alingType)
            #print(x,y, 'W='+str(fontSizeBox[1]), 'h='+str(fontSizeBox[2]))

        #print('aqui si entro')
    background_image.save('pruebas/{}.jpg'.format(cli))
