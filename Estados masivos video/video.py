import json
import cv2
from gtts import gTTS
import numpy as np
import pyttsx3
import moviepy.editor as mp
from moviepy.editor import VideoFileClip, AudioFileClip
import os
from PIL import Image

"""# Create a TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech (words per minute)
engine.setProperty('volume', 0.8)  # Volume (0.0 to 1.0)
voice = engine.getProperty('voices') #get the available voices
engine.setProperty('voice', 'voives')
# Set properties (optional)
engine.setProperty('rate', 150)  # Speed of speech (words per minute)
engine.setProperty('volume', 0.8)  # Volume (0.0 to 1.0)
engine.setProperty('voice', 'es') #language (spanish)
engine.setProperty('voice', voice[0].id) #0 for male 1 form female
# Get the list of available voices
voices = engine.getProperty('voices')
print(voices)


for voice in voices:
    print("ID:", voice.id)
    print("Name:", voice.name)
    print("Languages:", voice.languages)
    print("Gender:", voice.gender)
    print("Age:", voice.age)
    print("\n")
# Text to be converted to speech
text = "Hola pola mira este Charmander, se ve muy bonito ¿no?"

# Convert text to speech
engine.say(text)
engine.save_to_file(text, "output_1.wav") 
# Play the speech
engine.runAndWait()"""


#This function is used to calculate the time to apply the image to the video
def Total_fotogramas(tiempo, fotogramas):
    minutos, segundos = tiempo.split(":")
    total_segundos = int(minutos) * 60 + int(segundos)
    Total_de_fotogramas =  fotogramas * total_segundos
    return Total_de_fotogramas

def search_file(folder, filename):
    for f in os.listdir(folder):
        if f.startswith(filename):
            return os.path.join(folder, f)
    return None

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

# List of Clients
Client = '[{"cod":"17", "Cliente": "ferreteria almirante"}, {"cod":"27", "Cliente": "ferreteria edielectricos"}]'
Clientes = json.loads(Client)

# JSON image properties
image_properties_json = '[{"name": "LOGOS_FERRETERIAS", "width": 500, "high": 500, "rotate": 0, "x_position": 0, "y_position":0, "start_time": "0:03", "end_time": "0:10"}]'
I_properties = json.loads(image_properties_json)

# Load the video
#video = cv2.VideoCapture("./Tips.mp4")

#Text of the video
General_text = "@NOMBRE, Ferredistribuciones sierra piensa en usted y en sus clientes, por eso te traemos, Tip semanal para una empresa exitosa... Crea tu marca. Tu marca es lo que te distingue de tu competencia.Una marca exitosa aumenta las ventas, fideliza clientes y hace que tu empresa perdure en el tiempo... Ferredistribuciones sierra, tus aliados estratégicos."



for fe in Clientes:
    # Load the video
    video = cv2.VideoCapture("./Tips.mp4")
    #Here we change the text with the name of the store
    text = General_text.replace("@NOMBRE", fe['Cliente'])

    # Create gTTS object with Spanish language code
    tts = gTTS(text, lang='es', tld='com.mx')

    # Save the speech as an audio file
    tts.save('output.mp3')

    # Get audio properties
    fps = video.get(cv2.CAP_PROP_FPS)  # Frames per second
    
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(fe['cod']+'.mp4', fourcc, fps , (int(video.get(3)), int(video.get(4))))
    # Define the codec and create VideoWriter object
    # Variables for frame count and timestamp
    frame_count = 0

    while True:
        # Read a frame from the video
        ret, frame = video.read()

        if not ret:
            # End of video
            break
        
        #This code is to put the image over the frame of the video
        for bla in I_properties:
            #this code searches for the logo file
            start_time, end_time = bla['start_time'], bla['end_time']

            
            if Total_fotogramas(start_time, fps ) <= frame_count <= Total_fotogramas(end_time, fps):
                if bla['name'].endswith('jpg') or bla['name'].endswith('png'):
                    image1 = properties(bla['name'],bla)
                else:
                    fil = search_file(bla['name'],fe['cod'])
                    image1 = properties(fil,bla)
                # Convert the frame to PIL image
                frame_pil = Image.fromarray(frame)
                # Paste the image onto the frame
                frame_pil.paste(image1, (bla['x_position'], bla['y_position']), image1)
                # Convert the PIL image back to a NumPy array
                frame = np.array(frame_pil)
                #frame_image.paste(image1, (bla['x_position'], bla['y_position']), image1)
 
        frame_count += 1
        # Display the frame
        cv2.imshow("Video", frame)

        # Write the frame to the output video
        out.write(frame)

        # Exit if the user presses 'q'
        if cv2.waitKey(1) == ord("q"):
            break
        
   # Release the video and close the window
    video.release()
    out.release()
    cv2.destroyAllWindows()
        
    #Put de original audio with the voice to the new video 
    cli = mp.VideoFileClip(fe['cod']+'.mp4')
    original_video = mp.VideoFileClip('./Tips.mp4')
    Original_audio = original_video.audio
    audio_bg = mp.AudioFileClip('./output.mp3')
    # Set the volume factor for the additional audio
    volume_factor = 0.05  # Adjust the volume here (0.0 to 1.0)

    # Adjust the volume of the additional audio clip
    Modified_audio = Original_audio.volumex(volume_factor)
    # Combine the original audio and additional audio using CompositeAudioClip
    final_audio = mp.CompositeAudioClip([Modified_audio, audio_bg])

    cli = cli.set_audio(final_audio)
    cli.write_videofile('./Videos_realizados/'+fe['cod']+'.mp4')
    os.remove('./'+fe['cod']+'.mp4')
    os.remove('./output.mp3')
    print('video realizado')
