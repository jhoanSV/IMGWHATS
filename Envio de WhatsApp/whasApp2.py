import json
import time
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.service import Service as BraveService
from subprocess import CREATE_NO_WINDOW
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
import openpyxl
import random
import os
import shutil
from typing import Optional
import pywhatkit as kit
from selenium.common.exceptions import NoSuchElementException

class Send_Wapp:
    def __init__(self,
                 msj: str='',
                 image_path: str='',
                 variables: dict=None,
                 colCelular: int=None,
                 colDestino: int=None,
                 file_path: str='',
                 Hook: Optional[any] = None):
        
        self.msj = msj
        self.image_path = image_path
        self.variables = variables
        self.colCelular = colCelular
        self.colDestino = colDestino
        self.excel_file_path = file_path
        self.Add_error = Hook
        self.indices = []
        self.excel_data = None

        #* Constantes de funcionalidad
        # Todo: URL of WhatsApp Web
        self.whatsapp_web_url = "https://web.whatsapp.com/"        
        self.brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
        self.options = webdriver.ChromeOptions()
        self.options.binary_location = self.brave_path
        # Todo: Configure Chrome driver option
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super().__init__()
        #self.envio_msj()

    def read_excel_file(self):
        #lee las filas del excel y las retorna en una lista
        wb = openpyxl.load_workbook(self.excel_file_path)
        sheet = wb.active
        data = []
        self.indices = []
        for i, row in enumerate(sheet.iter_rows(min_row=2, values_only=True)):
            data.append(row)
            self.indices.append(i)
        return data
    

    def update_vars(self, msj, image_path, variables, colCelular, colDestino, file_path, la_funcion, la_funcion2):
        self.msj = msj
        self.image_path = image_path
        self.variables = variables
        self.colCelular = colCelular
        self.colDestino = colDestino
        self.excel_file_path = file_path
        self.Add_error = la_funcion
        self.show_end = la_funcion2

    def envio_msj(self, re=None):
        
        self.enviados = 0
        self.errados = 0
        wait_time = 30
        poll_frequency = 2
        text = self.msj
        #service.creation_flags = CREATE_NO_WINDOW#*Para que no muestre ventana de cmd
        tk.messagebox.showinfo(message="Se está comprobando la compatibilidad de su versión de Chrome. Este proceso puede tardar unos segundos")
        service = BraveService(ChromeDriverManager().install())
        service.creation_flags = CREATE_NO_WINDOW#*Para que no muestre ventana de cmd
        # Todo: Initialize Chrome driver with options
        # Open WhatsApp Web and wait for QR code scan
        driver = webdriver.Chrome(service=service, options=self.options)
        
        driver.get(self.whatsapp_web_url)
                
        # Espera hasta que la variable cambie
        #WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div')))
        WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]')))
        time.sleep(6)

        # Todo: Wait for the WhatsApp Web interface to load
        wait = WebDriverWait(driver, 10)
        wait.until(EC.title_contains("WhatsApp"))
        self.excel_data = self.read_excel_file()
        if re is not None: self.indices = re #si "re" no es None, o se le envió un valor, toma el lugar de self.indices

        def verificar_chat(driver, xpath, texto_no_encontrado, timeout=10):
            try:
                # Esperar a que el elemento con el XPath esté presente
                elemento = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                # Obtener el texto del elemento
                texto_elemento = elemento.text
                print(f"Texto del elemento encontrado: {texto_elemento}")
                
                # Verificar si el texto coincide con el mensaje de "No se encontraron resultados"
                if texto_no_encontrado in texto_elemento:
                    print("El chat no existe.")
                    return [False, None]
                else:
                    print("El chat existe.")
                    return [True, elemento]
            except TimeoutException:
                print("No se pudo encontrar el elemento dentro del tiempo límite.")
                return [False, None]

        def comprobar_xpath(driver, xpath, timeout=10):
            try:
                # Verificar si el elemento está presente en el DOM
                WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))

                # Verificar si el elemento es visible
                elemento_visible = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))

                # Verificar si el elemento es clickeable
                elemento_clickeable = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                print("Si encontro el chat")
                return [True, elemento_clickeable]  # Devuelve el elemento si se encuentra
            except TimeoutException:
                print(f"Timeout: No se pudo encontrar el elemento con XPath: {xpath} después de {timeout} segundos.")
                return [False, None]  # Devuelve None si el elemento no se encuentra dentro del tiempo límite
            except NoSuchElementException:
                print(f"Error: No se encontró un elemento con el XPath: {xpath}.")
                return [False, None]  # Manejo adicional por si el elemento no está presente en el DOM
            except Exception as e:
                print(f"Se produjo un error inesperado: {str(e)}")
                return [False, None]  # Captura de errores generales para diagnósticos
    
        for indice in self.indices:
            #enviado = False
            #!This button is to find the searcher of the cell numbers
            new_chat_btn = '//*[@id="side"]/div[1]/div/div[2]/button/div[2]/span'
            #!This is to whrite the cellnumber
            text_box = '//*[@id="side"]/div[1]/div/div[2]/div[2]/div/div/p'
            #text_box = '//*[@id="app"]/div/div[2]/div[2]/div[1]/span/div/span/div/div[1]/div[2]/div[2]/div/div[1]'
            #!This path is to select the chat
            #//*[@id="pane-side"]/div/div/div/div[1]
            chat_element_path = '//*[@id="pane-side"]/div/div/div/div[2]/div/div'

            xpaths = [
                "//*[@id='pane-side']/div/div/div/div[1]/div/div",
                "//*[@id='pane-side']/div/div/div/div[2]/div/div"
            ]

            element = "//*[@id='pane-side']/div/div/div/div[2]/div/div"
            for xpath in xpaths:
                try:
                    #element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
                    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                    break  # Detener el bucle si encuentra el elemento
                except TimeoutException:
                    continue
            #Button to star again a new search
            arrow_back_but = '//*[@id="app"]/div/div[2]/div[2]/div[1]/span/div/span/div/header//span[@data-icon="back"]'
            text = self.msj
            try:
                # Todo: Here we change the text with the name of the store
                #?text = message.replace("@NOMBRE", contacto['Ferreteria']).replace("@NFactura", contacto['Nfactura'])
                # Todo: The next loop begins selecting each key/var, and if it exists in the message, change it
                for i, key in enumerate(self.variables):
                    #text = text.replace(key, str(contacto[i]))
                    text = text.replace(key, str(self.excel_data[indice][i]))
                lineas = text.split("\n")
                                
                # ?Search for the chat by phone number
                #search_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]')))#'//div[@class="_2_1wd"]//div[@contenteditable="true"][@data-tab="3"]')))
                search_btn = wait.until(EC.presence_of_element_located((By.XPATH, new_chat_btn)))
                search_btn.click()
                search_input = wait.until(EC.presence_of_element_located((By.XPATH, text_box)))

                #//*[@id="app"]/div/div/div[3]/div[1]/span/div/span/div/div[2]/div/div/div/div[1]/div
                #search_input.clear()
                search_input.send_keys('+57'+ str(self.excel_data[indice][self.colCelular]))
                el_texto = '//*[@id="app"]//span[contains(text(), "No se encontraron resultados para '+'\'+57'+str(self.excel_data[indice][self.colCelular])+"'\")]"
                
                time.sleep(3)
                search_researcher = comprobar_xpath(driver, element)
                if search_researcher[0]:
                    #? Click on the chat contact no added to open it
                    search_researcher[1].click()
                    time.sleep(1)
                    print('esta entrando a la busqueda inicial')
                else:
                    print('Inció un nuevo chat')
                    search_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[3]/div/div[3]/header/header/div/span/div/div[1]/button')))
                    search_btn.click()
                    time.sleep(1)

                    #//*[@id="app"]/div/div[3]/div/div[2]/div[1]/span/div/span/div/div[1]/div[2]/div[2]/div/div/p
                    search_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[3]/div/div[2]/div[1]/span/div/span/div/div[1]/div[2]/div[2]/div/div/p')))
                    search_input.send_keys('+57'+ str(self.excel_data[indice][self.colCelular]))
                    time.sleep(2)
                    # Suponiendo que el número está en este formato: 3116032121
                    numero_sin_formato = str(self.excel_data[indice][self.colCelular])

                    # Formatear el número con espacios
                    numero_con_espacios = f"+57 {numero_sin_formato[:3]} {numero_sin_formato[3:]}"
                    #search_chat = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="pane-side"]/div/div/div/div[2]/div/div')))
                                  #//*[@id="app"]/div/div[3]/div/div[2]/div[1]/span/div/span/div/div[2]/div/div/span
                    xpathSearch = '//*[@id="app"]/div/div[3]/div/div[2]/div[1]/span/div/span/div/div[2]/div/div' #f"//span[contains(text(), '{numero_con_espacios}')]"

                    texto_no_encontrado = "No se encontraron resultados para"
                    resultado, elemento = verificar_chat(driver, xpathSearch, texto_no_encontrado)
                    if resultado:
                        elemento.click()
                    else:
                        self.errados += 1
                        print('Ocurrio un error con '+ str(self.excel_data[indice][self.colDestino]) + ' En envio')
                        #if not enviado: self.Add_error({indice:str(self.excel_data[indice][self.colDestino])})
                        self.Add_error({indice:str(self.excel_data[indice][self.colDestino])})
                        print('No hay contacto con ese número')
                        back = '//span[@data-icon="back"]'
                        #back = '//span[@aria-label="atras"]'
                        search_btn = wait.until(EC.presence_of_element_located((By.XPATH, back)))
                        search_btn.click()
                        continue
                    time.sleep(2)
            except Exception as e:
                print('Ocurrio un error con '+ str(self.excel_data[indice][self.colDestino]) + ' En envio 3')
                self.Add_error({indice:str(self.excel_data[indice][self.colDestino])})
                continue


            if self.image_path == '':
                try:
                    #?Send the message with the number of the contact that we want to contact
                    #*Busca la kja de texto y le asigna el msj
                    #//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div[2]/div[1]/p
                    search_tb = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div[2]/div[1]/p')))
                    search_tb.click()
                    #message_input = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]')
                    message_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div[2]/div/p')))
                    #message_input.send_keys(text.rstrip())#.rstrip para eliminar el "Enter" que tienen los strings al final
                    if (len(lineas) > 1):
                        for l, lines in enumerate(lineas):
                            message_input.send_keys(lineas[l].rstrip())
                            message_input.send_keys(Keys.SHIFT, Keys.ENTER)
                    else:
                        message_input.send_keys(text.rstrip())
                    
                    message_input.send_keys(Keys.ENTER)
                    time.sleep(2)
                    #enviado = True
                    
                    #*Give a random number from 2 and 8 to send the next message.
                    random_number = random.randint(2, 8)
                    time.sleep(random_number)
                    self.enviados += 1
                    
                    #if not enviado: self.Add_error({indice:str(self.excel_data[indice][self.colDestino])})
                except Exception as e:
                    self.errados += 1
                    print('Ocurrio un error con '+ str(self.excel_data[indice][self.colDestino]) + ' En envio')
                    print(e)
                    #if not enviado: self.Add_error({indice:str(self.excel_data[indice][self.colDestino])})
                    self.Add_error({indice:str(self.excel_data[indice][self.colDestino])})
                    continue
            elif self.image_path.endswith('.jpg') or self.image_path.endswith('.png'):
                try:                    
                    #*esta es la parte para enviar la imagen
                    #//*[@id="main"]/footer/div[1]/div/span/div/div[1]/div/button
                    #attachment_button = wait.until(EC.presence_of_element_located((By.XPATH, '//span[@data-icon="attach-menu-plus"]')))
                    attachment_button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[1]/div/button')))
                    attachment_button.click()                    
                    time.sleep(1)

                    #*selecciona la imagen
                    attach_image_option = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')))
                    attach_image_option.send_keys(self.image_path)
                    time.sleep(4)

                    #*escribe el mensaje
                    #To write the message that it will send with the image                                        
                    message_input = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="app"]//p[contains(@class, "selectable-text")]')))                                       
                    
                    if (len(lineas) > 1):
                        print('entro a lineas')
                        for l, lines in enumerate(lineas):
                            message_input.send_keys(lineas[l].rstrip())
                            message_input.send_keys(Keys.SHIFT, Keys.ENTER)
                    else:
                        print('No entro a lineas')
                        message_input.send_keys(text.rstrip())
                    
                    message_input.send_keys(Keys.ENTER)
                    #input("errorhptaaaaaaaaaaaaaaaaaaaaa")                    
                    time.sleep(5)

                    #*Give a random number from 2 and 8 to send the next message.
                    random_number = random.randint(2, 8)
                    time.sleep(random_number)
                    self.enviados += 1
                except Exception as e:
                    self.errados += 1
                    print(e)
                    print('Ocurrio un error con '+ str(self.excel_data[indice][self.colDestino]) + ' En envio 2')
                    self.Add_error({indice:str(self.excel_data[indice][self.colDestino])})
                    continue
            elif self.image_path.endswith('.mp4'):
                try:
                    #esta es la parte para enviar la imagen                
                    attachment_button = wait.until(EC.presence_of_element_located((By.XPATH, '//span[@data-icon="plus"]')))
                    attachment_button.click()
                    time.sleep(1)

                    #prueba para seleccionar la imagen
                    attach_image_option = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')))
                    attach_image_option.send_keys(self.image_path)
                    time.sleep(7)

                    #To write the message that it will send with the image                                        
                    message_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[3]/div/div[2]/div[2]/span/div/div/div/div[2]/div/div[1]/div[3]/div/div[1]/div[1]/div[1]/p')))
                    #message_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[2]/span/div/span//div[@role="textbox"]')))
                    if (len(lineas) > 1):
                        for l, lines in enumerate(lineas):
                            message_input.send_keys(lineas[l].rstrip())
                            message_input.send_keys(Keys.SHIFT, Keys.ENTER)
                    else:
                        message_input.send_keys(text.rstrip())
                    
                    message_input.send_keys(Keys.ENTER)
                    time.sleep(5)

                    #Give a random number from 2 and 8 to send the next message.
                    random_number = random.randint(2, 8)
                    time.sleep(random_number)
                    self.enviados += 1
                except Exception as e:
                    #print("An error occurred:", str(e))
                    self.errados += 1
                    print(e)
                    print('Ocurrio un error con '+ str(self.excel_data[indice][self.colDestino]) + 'Envio Video')
                    self.Add_error({indice:str(self.excel_data[indice][self.colDestino])})
                    continue
            else:
                try:
                    #image = search_file(self.image_path, str(contacto['Cod']))#!Esto va a botar error
                    image = 5
                    
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
                    message_input = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[3]/div[2]/span/div/span/div/div/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[1]')#'//div[@contenteditable="true"][@data-tab="6"]')
                    message_input.send_keys(text)
                    message_input.send_keys(Keys.ENTER)
                    time.sleep(5)

                    #fin de la prueba para seleccionar la imaen a mandar
                    #Give a random number from 2 and 8 to send the next message.
                    random_number = random.randint(2, 8)
                    time.sleep(random_number)
                except Exception as e:
                    print('Ocurrio un error con '+ str(self.excel_data[indice][self.colDestino]) + ' En envio 3')
                    self.Add_error({indice:str(self.excel_data[indice][self.colDestino])})
                    continue
        #para cerrar la sesion del whatapp %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


        try:
            #close_button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/header/div[2]/div/span/div[last()]/div')))
            
            #close_button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/header/div[2]/div/span//span[@data-icon="menu"]')))
            close_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-icon="menu"]')))
            #close_button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[3]/div[3]/header/div[2]/div/span//span[@data-icon="menu"]')))
            close_button.click()
            close_button = wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Cerrar sesión")]')))
            #close_button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/header//div[contains(text(), "Cerrar sesión")]')))
            close_button.click()
            time.sleep(1)
            #//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div[2]/div/button[2]
            close_button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div[2]/div/button[2]')))
            driver.implicitly_wait(3)
            close_button.click()
            time.sleep(7)
        except Exception as e:
            print("No se pudo cerrar sesión ", e)
        
        # Close the browser
        driver.quit()
        self.show_end(self.enviados, self.errados)
        
        