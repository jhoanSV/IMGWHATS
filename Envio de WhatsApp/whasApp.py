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


#* Constantes de funcionalidad
# Todo: URL of WhatsApp Web
whatsapp_web_url = "https://web.whatsapp.com/"
options = webdriver.ChromeOptions()
# Todo: Configure Chrome driver option
options.add_experimental_option('excludeSwitches', ['enable-logging'])

#* Lista de variables
#nombre_proyecto = 'pedidos en ruta'
nombre_proyecto = ''
#excel_file_path = './Numero_mensaje_whatsapp.xlsx'
excel_file_path = ''
sheet = None

data_xl = []

message = ""

image_path = r''

'''variables = {
                "@cod":0,
                "@Nombre":1,
                "@Responsable":2,
                "@Cel":3,
                "@ValorFactura":4,
                "@NFactura":5
            }'''
variables = {}
colCelular = 3
nomCli = 2
excel_data = []#data sin encabezados

#* Funciones
def read_excel_file(sheet):
    
    data = []

    for row in sheet.iter_rows(min_row=2, values_only=True):
        '''for col in row:
            if col is not None:
                data.
            print(col)'''
        data.append(row)
    return data


def read_first_row():

    primera_fila = sheet[1]
    data = []
    
    for item in primera_fila:
        if item.value is not None:
            data.append(item.value)

    #print("Excel leído, sus columnas son: ")    
    #for item in data:
    #    print(item)
    return data

'''def funcionjsjs2(data):
    dicc = {}
    print("A continuación asigne el nombre a las variables: ")

    for i, item in enumerate(data):
        col_var = input('Variable de la columna "' + item + '": ')
        dicc['@' + col_var] = [i]
    print(dicc)
    return dicc'''
#def 


def search_file(folder, filename):
    for f in os.listdir(folder):
        if f.startswith(filename):
            return os.path.join(folder, f)
    return None

def set_xl(file):
    global excel_file_path
    global sheet

    excel_file_path = file
    print(excel_file_path)#borrar después
    #global excel_data
    # Todo: Specify la hoja de excel
    wb = openpyxl.load_workbook(excel_file_path)
    sheet = wb.active

def llenarVars(proyecto):
    global excel_file_path
    global message
    global image_path
    global variables
    global colCelular
    global nomCli
    with open("proyectos.json") as archi_json:
        el_json = json.load(archi_json)
    Jvariables = el_json[proyecto]
    excel_file_path = Jvariables['rutaXl']
    message = Jvariables['msj']
    image_path = r''+Jvariables['recurso']
    variables = Jvariables['variables']
    colCelular = Jvariables['colCelular']
    nomCli = Jvariables['NomCli']

def lee_excel():
    # Todo: Read the Excel file and get the data as a dictionary. Currently as an array/list    
    global excel_data
    dict_Xl = {}
    first_row = read_first_row()
    excel_data = read_excel_file(sheet)
    
    for i in range(len(first_row)):
        dict_Xl[i] = {
            "Columnas excel" : first_row[i],
            #"Variables" : first_row[],
            "Celular" : 0,
            "Destino" : 0
        }
    print(dict_Xl)
    return dict_Xl



#cols = funcionjsjs2(first_row(sheet))

#pepe = list(cols.keys())# Todo: estas son solo llaves
#excel_data = read_excel_file(sheet)
#print(excel_data)

# Todo: Iterate over the message properties and send messages
def envio_msj(msj, image_path, variables, colCelular, colDestino):#?Recibir excel_data, msj, col_num, col_destino, variables
    # Todo: Initialize Chrome driver with options
    
    driver = webdriver.Chrome(options=options)
    # Open WhatsApp Web and wait for QR code scan
    driver.get(whatsapp_web_url)
    print("Scan the QR code and press enter")
    input()
    # Todo: Wait for the WhatsApp Web interface to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.title_contains("WhatsApp"))

    print(image_path)
    print("excel_data:")
    print(excel_data)
    
    if nombre_proyecto != '':
       llenarVars(nombre_proyecto)
    for contacto in excel_data:
        #//*[@id="app"]/div/div/div[3]/div[1]/span/div/span/div/div[2]/div/div/div/div[1]/div
        chat_element_path = '//*[@id="app"]/div/div/div[3]/div[1]/span/div/span/div/div[2]/div/div/div'
        text = msj
        try:
            # Todo: Here we change the text with the name of the store
            #?text = message.replace("@NOMBRE", contacto['Ferreteria']).replace("@NFactura", contacto['Nfactura'])
            # Todo: The next loop begins selecting each key/var, and if it exists in the message, change it
            for i, key in enumerate(variables):#Pepe es una lista de claves
                text = text.replace(key, contacto[i])
            print("Vista previa del mensaje: ")
            print(text)
                            
            # Search for the chat by phone number
            #search_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]')))#'//div[@class="_2_1wd"]//div[@contenteditable="true"][@data-tab="3"]')))
            search_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div[4]/header/div[2]/div/span/div[last()-1]')))
            search_btn.click()
            search_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div[3]/div[1]/span/div/span/div/div[1]/div/div[2]/div/div[1]')))        
                                                                                
            #//*[@id="app"]/div/div/div[3]/div[1]/span/div/span/div/div[2]/div/div/div/div[1]/div
            #search_input.clear()
            search_input.send_keys('+57'+contacto[colCelular])
            time.sleep(3)

            # Click on the chat to open it
            #chat_element = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="pane-side"]/div[1]/div/div')))
            #chat_element = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="app"]/div/div/div[3]/div[1]/span/div/span/div/div[2]/div/div/div/div[2]/div')))
            chat_element = wait.until(EC.presence_of_element_located((By.XPATH, chat_element_path)))
            chat_element.click()
            time.sleep(5)
        except Exception as e:
            print("An error occurred:", str(e));
            print('Ocurrio un error con '+ contacto[nomCli] + ' al seleccionar contacto')
            print(e)
            # Click on the button to errace the //*[@id="app"]/div/div/div[3]/div[1]/span/div/span/div/div[1]/div/span/button
            #chat_element = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="side"]/div[1]/div/div/span/button')))
            #chat_element = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="app"]/div/div/div[3]/div[1]/span/div/span/div/header/div/div[1]/div')))
            chat_element = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="app"]/div/div/div[3]/div[1]/span/div/span/div/header/div/div[1]/div/span')))
                                                                                  
            chat_element.click()
            continue
        if image_path == '':
            try:
                # Send the message with the number of the contact that we want to contact ///Este es para wapp business
                message_input = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')
                message_input.send_keys(text)
                message_input.send_keys(Keys.ENTER)
                time.sleep(2)
                
                #Give a random number from 2 and 8 to send the next message.
                random_number = random.randint(2, 8)
                time.sleep(random_number)
            except Exception as e:            
                print('Ocurrio un error con '+ contacto[colDestino] + ' En envio 1')
                print(e)
                '''
                # Click on the button to errace the 
                chat_element = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="side"]/div[1]/div/div/span/button')))
                #chat_element = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="pane-side"]/div[1]/div/div/div[3]')))
                chat_element.click()
                '''
                continue
        elif image_path.endswith('.jpg') or image_path.endswith('.png') or image_path.endswith('.mp4'):
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
                print('Ocurrio un error con '+ contacto[nomCli] + ' En envio 2')
                # Click on the button to errace the
                '''
                chat_element = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="side"]/div[1]/div/div/span/button')))
                chat_element.click()
                '''
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
                print('Ocurrio un error con '+ contacto['Ferreteria'] + ' En envio 3')
                # Click on the button to errace the 
                '''
                chat_element = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="side"]/div[1]/div/div/span/button')))
                chat_element.click()
                '''
                continue

    #para cerrar la sesion del whatapp %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    send_button = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="app"]/div/div/div[4]/header/div[2]/div/span/div[4]/div')))#'//*[@id="main"]/footer/div[1]/div/div/div[2]/button')))
    send_button.click()

    #send_button = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="app"]/div/div/div[4]/header/div[2]/div/span/div[4]/span/div/ul/li[8]')))#'//*[@id="app"]/div/div/div[4]/header/div[2]/div/span/div[4]/span/div/ul/li[7]')))#'//*[@id="main"]/footer/div[1]/div/div/div[2]/button')))
    send_button = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="app"]/div/div/div[4]/header/div[2]/div/span/div[4]/span/div/ul/li[last()]')))
    send_button.click()
    time.sleep(1)

    send_button = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div[3]/div/button[2]')))#'//*[@id="main"]/footer/div[1]/div/div/div[2]/button')))
    send_button.click()
    time.sleep(7)

    #click to send the message

    # Close the browser
    driver.quit()

#envio_msj()