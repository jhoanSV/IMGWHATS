import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import openpyxl
import random
import os

def read_excel_file(file_path):
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active
    
    data = []
    
    for row in sheet.iter_rows(min_row=2, values_only=True):
        cod = row[0]
        company = row[1]
        in_charge = row[2]
        number = row[3]
        value = row[4]
        Nfactura = row[5]
        if cod is not None and company is not None and in_charge is not None and number is not None and value is not None and Nfactura is not None:
            data.append({'Cod': cod, 'Ferreteria': company, 'Encargado': in_charge, 'whatsapp': number, 'ValorFactura': value, 'Nfactura': Nfactura})
    return data

def search_file(folder, filename):
    for f in os.listdir(folder):
        if f.startswith(filename):
            return os.path.join(folder, f)
    return None


# Specify the path to your Excel file
excel_file_path = './Numero_mensaje_whatsapp.xlsx'

# Read the Excel file and get the data as a dictionary
excel_data = read_excel_file(excel_file_path)
#print(excel_data)

# Path to your Chrome driver executable
chromedriver_path = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"

# URL of WhatsApp Web
whatsapp_web_url = "https://web.whatsapp.com/"

# Configure Chrome driver options
options = webdriver.ChromeOptions() 
options.add_experimental_option('excludeSwitches', ['enable-logging']) 

# Initialize Chrome driver with options
#driver = webdriver.Chrome(executable_path = chromedriver_path, options=options)
driver = webdriver.Chrome(options=options)

# Open WhatsApp Web and wait for QR code scan
driver.get(whatsapp_web_url)
print("Scan the QR code and press enter")
input()

# Wait for the WhatsApp Web interface to load
wait = WebDriverWait(driver, 10)
wait.until(EC.title_contains("WhatsApp"))

# Iterate over the message properties and send messages
#for properties in message_properties:
# "¡Hola @NOMBRE!¡Quería recordarte que tu pedido número @NFactura está en ruta! Nos esforzamos por brindarte la mejor experiencia de compra y queremos que sepas que valoramos tu confianza en nosotros. Si tienes alguna pregunta o necesitas cualquier tipo de asistencia, no dudes en ponerte en contacto. Estaremos encantados de ayudarte en todo lo que necesites."
# "¡Hola @NOMBRE! Queríamos informarles que hemos realizado cambios en nuestro equipo de asesores comerciales. Les presentamos a Derwin Valencia un profesional altamente capacitado y amplia experiencia en el campo de Ferretería. En los próximos días, Derwin los visitará para conocer sus necesidades y ofrecer soluciones personalizadas. También pueden revisar nuestras promociones y productos en nuestra página web www.ferresierra.com Tus aliados estratégicos."
message = "¡Hola @NOMBRE!¡Quería recordarte que tu pedido número @NFactura está en ruta! Nos esforzamos por brindarte la mejor experiencia de compra y queremos que sepas que valoramos tu confianza en nosotros. Si tienes alguna pregunta o necesitas cualquier tipo de asistencia, no dudes en ponerte en contacto. Estaremos encantados de ayudarte en todo lo que necesites."

#image_path = r'C:\Users\pc\Documents\proyectos empresa\Envio de WhatsApp\pikachu.png'
image_path = r''#'C:\Users\pc\Dropbox\Instalador sierra\envio whatsapp\Envio de WhatsApp\Imagen derwin.jpg'#'C:\Users\pc\Documents\proyectos empresa\IMGWHATS\Envio de WhatsApp\LOGOS FERRETERIAS'

print(image_path)

for contacto in excel_data:
    try:
        #Here we change the text with the name of the store
        text = message.replace("@NOMBRE", contacto['Ferreteria']).replace("@NFactura", contacto['Nfactura'])
        # Search for the chat by phone number
        search_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]')))#'//div[@class="_2_1wd"]//div[@contenteditable="true"][@data-tab="3"]')))
        search_input.clear()
        search_input.send_keys('+57'+contacto['whatsapp'])
        time.sleep(3)

        # Click on the chat to open it
        chat_element = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="pane-side"]/div[1]/div/div')))
        chat_element.click()
        time.sleep(5)
    except Exception as e:
        print("An error occurred:", str(e));
        print('Ocurrio un error con '+ contacto['Ferreteria'] + 'num1')
        # Click on the button to errace the 
        chat_element = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="side"]/div[1]/div/div/span/button')))
        chat_element.click()
        continue
    if image_path == '':
        try:
            # Send the message with the number of the contact that we want to contact
            message_input = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')
            message_input.send_keys(text)
            message_input.send_keys(Keys.ENTER)
            time.sleep(2)
            
            #Give a random number from 2 and 8 to send the next message.
            random_number = random.randint(2, 8)
            time.sleep(random_number)
        except Exception as e:
            print('Ocurrio un error con '+ contacto['Ferreteria'] + 'num2')
            print(Exception)
            # Click on the button to errace the 
            chat_element = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="side"]/div[1]/div/div/span/button')))
            chat_element.click()
            continue
    elif image_path.endswith('.jpg') or image_path.endswith('.png'):
        try:
            #esta es la parte para enviar la imagen
            attachment_button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]')))
            attachment_button.click()
            time.sleep(1)

            #prueba para seleccionar la imagen
            attach_image_option = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')))
            attach_image_option.send_keys(image_path)
            time.sleep(6)

            #To write the message that it will send with the image
            message_input = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[3]/div[2]/span/div/span/div/div/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[1]/p')#'//div[@contenteditable="true"][@data-tab="6"]')
            message_input.send_keys(text)
            message_input.send_keys(Keys.ENTER)
            time.sleep(5)

            #fin de la prueba para seleccionar la imaen a mandar
            #Give a random number from 2 and 8 to send the next message.
            random_number = random.randint(2, 8)
            time.sleep(random_number)
        except Exception as e:
            print("An error occurred:", str(e))
            print('Ocurrio un error con '+ contacto['Ferreteria'] + 'num3')
            # Click on the button to errace the 
            chat_element = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="side"]/div[1]/div/div/span/button')))
            chat_element.click()
            continue
    else:
        try:
            image = search_file(image_path, contacto['Cod'])
            
            #esta es la parte para enviar la imagen
            attachment_button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]')))
            attachment_button.click()
            time.sleep(1)

            #prueba para seleccionar la imagen
            # Choose the "Attach an image" option
            attach_image_option = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')))
            attach_image_option.send_keys(image)
            time.sleep(6)

            #To write the message that it will send with the image
            message_input = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[3]/div[2]/span/div/span/div/div/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[1]/p')#'//div[@contenteditable="true"][@data-tab="6"]')
            message_input.send_keys(text)
            message_input.send_keys(Keys.ENTER)
            time.sleep(5)

            #fin de la prueba para seleccionar la imaen a mandar
            #Give a random number from 2 and 8 to send the next message.
            random_number = random.randint(2, 8)
            time.sleep(random_number)
        except Exception as e:
            print("An error occurred:", str(e))
            print('Ocurrio un error con '+ contacto['Ferreteria'] + 'num4')
            # Click on the button to errace the 
            chat_element = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="side"]/div[1]/div/div/span/button')))
            chat_element.click()
            continue
#para cerrar la sesion del whatapp %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
send_button = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="app"]/div/div/div[4]/header/div[2]/div/span/div[4]/div')))#'//*[@id="main"]/footer/div[1]/div/div/div[2]/button')))
send_button.click()

send_button = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="app"]/div/div/div[4]/header/div[2]/div/span/div[4]/span/div/ul/li[8]')))#'//*[@id="app"]/div/div/div[4]/header/div[2]/div/span/div[4]/span/div/ul/li[7]')))#'//*[@id="main"]/footer/div[1]/div/div/div[2]/button')))
send_button.click()
time.sleep(1)

send_button = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div[3]/div/button[2]')))#'//*[@id="main"]/footer/div[1]/div/div/div[2]/button')))
send_button.click()
time.sleep(7)
#click to send the message

# Close the browser
driver.quit()