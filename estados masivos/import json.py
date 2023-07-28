import json
from PIL import Image
import os 

# *JSON image properties
image_properties_json = '[{"name": "caminar.jpg", "width": 300, "high": 300, "rotate": 90, "x_position": 0, "y_position":0, "xCenter": true, "yCenter": true}, {"name": "LOGOS FERRETERIAS", "width": 300, "high": 300, "rotate": 60, "x_position": 0, "y_position":0, "xCenter" : false, "yCenter": false}]'
# *List of Clients
CLient = ['17','27','28','46','140','433']
# *Create a background image with the required size 
size = width, height = 3000, 3000

def search_file(folder, filename):
    for f in os.listdir(folder):
        if f.startswith(filename):
            return os.path.join(folder, f)
    return None

#Create a image with the properties of each item in the list of properties
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

# !background_image = Image.new('RGB',size, 'white')
I_properties = json.loads(image_properties_json)

#For each Client crete a new image
for cli in CLient:
    #apliying the properties to each image on the list of properties
    background_image = Image.new('RGB',size, 'white')
    for ImageProperty in I_properties:
        # *Variables for each image
        x = ImageProperty['x_position']
        y = ImageProperty['y_position']
        if ImageProperty['name'].endswith('jpg') or ImageProperty['name'].endswith('png'):
           image1 = properties(ImageProperty['name'],ImageProperty)
        else:
            fil = search_file(ImageProperty['name'],cli)
            image1 = properties(fil,ImageProperty)
        # Load the PNG image and convert it to RGBA
        #png_image = image1.convert('RGBA')

        # Create a new RGBA image with the same size as the PNG image
        #new_image = Image.new('RGBA', png_image.size, (0, 0, 0, 0))

        # Paste the PNG image on the new RGBA image with the alpha channel as the mask
        #new_image.paste(png_image, (0, 0), mask=png_image.split()[3])

        # *Check if the RGBA image have to be at the center in the x position or in the y position
        if ImageProperty['xCenter'] == True:
            x = int(round((size[0] - ImageProperty['width'])/2))
        if ImageProperty['yCenter'] == True:
            y = int(round((size[1] - ImageProperty['high'])/2))

        # * Paste the new RGBA image with the PNG image on top of the background image
        background_image.paste(image1, (x, y), image1)
        #print('aqui si entro')
    background_image.save('pruebas/{}.jpg'.format(cli))
