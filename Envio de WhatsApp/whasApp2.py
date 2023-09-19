import json
import time
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import openpyxl
import random
import os
from typing import Optional

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

        #* Constantes de funcionalidad
        # Todo: URL of WhatsApp Web
        self.whatsapp_web_url = "https://web.whatsapp.com/"
        self.options = webdriver.ChromeOptions()
        # Todo: Configure Chrome driver option
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super().__init__()
        #self.envio_msj()

    def read_excel_file(self):
        #lee las filas del excel y las retorna en una lista
        wb = openpyxl.load_workbook(self.excel_file_path)
        sheet = wb.active
        data = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            data.append(row)
        return data
    

    def update_vars(self, msj, image_path, variables, colCelular, colDestino, file_path, la_funcion):
        self.msj = msj
        self.image_path = image_path
        self.variables = variables
        self.colCelular = colCelular
        self.colDestino = colDestino
        self.excel_file_path = file_path
        self.Add_error = la_funcion

    def envio_msj(self):#?Recibir excel_data, msj, col_num, col_destino, variables
        # Todo: Initialize Chrome driver with options
        # Open WhatsApp Web and wait for QR code scan        
        driver = webdriver.Chrome(options=self.options, service=ChromeService(ChromeDriverManager().install()))
        driver.get(self.whatsapp_web_url)
        '''print("Scan the QR code and press enter")
        input()'''
        # Espera hasta que la variable cambie
        #WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div')))
        WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]')))
        time.sleep(6)        
        
        # Todo: Wait for the WhatsApp Web interface to load
        wait = WebDriverWait(driver, 10)
        wait.until(EC.title_contains("WhatsApp"))
        excel_data = self.read_excel_file()
        print(excel_data)
        for contacto in excel_data:
            #//*[@id="app"]/div/div/div[3]/div[1]/span/div/span/div/div[2]/div/div/div/div[1]/div
            chat_element_path = '//*[@id="app"]/div/div/div[3]/div[1]/span/div/span/div/div[2]/div/div/div'
            text = self.msj
            try:
                # Todo: Here we change the text with the name of the store
                #?text = message.replace("@NOMBRE", contacto['Ferreteria']).replace("@NFactura", contacto['Nfactura'])
                # Todo: The next loop begins selecting each key/var, and if it exists in the message, change it
                for i, key in enumerate(self.variables):
                    text = text.replace(key, str(contacto[i]))
                print("Vista previa del mensaje: ")
                print(text)
                                
                # ?Search for the chat by phone number
                #search_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]')))#'//div[@class="_2_1wd"]//div[@contenteditable="true"][@data-tab="3"]')))
                search_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div[4]/header/div[2]/div/span/div[last()-1]')))
                search_btn.click()
                search_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div[3]/div[1]/span/div/span/div/div[1]/div/div[2]/div/div[1]')))        
                                                                                    
                #//*[@id="app"]/div/div/div[3]/div[1]/span/div/span/div/div[2]/div/div/div/div[1]/div
                #search_input.clear()
                search_input.send_keys('+57'+str(contacto[self.colCelular]))
                time.sleep(3)

                # ?Click on the chat to open it                
                chat_element = wait.until(EC.presence_of_element_located((By.XPATH, chat_element_path)))
                chat_element.click()               

                time.sleep(5)
            except Exception as e:
                self.Add_error(contacto, self.colDestino)
                print('Ocurrio un error con '+ str(contacto[self.colDestino]) + ' al seleccionar contacto')
                print(e)
                #set_errors((contacto))
                #oprime una flecha para cancelar el proceso de ingreso de número
                arrow_back = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="app"]/div/div/div[3]/div[1]/span/div/span/div/header/div/div[1]/div/span')))
                arrow_back.click()

                continue
            
            if self.image_path == '':
                try:
                    #?Send the message with the number of the contact that we want to contact
                    #Busca la kja de texto y le asigna el msj 
                    message_input = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')
                    message_input.send_keys(text)
                    #//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span
                    #message_input.send_keys(Keys.ENTER)
                    #send_button = driver.find_element(By.XPATH, '//span[@data-icon="send"]')
                    #?da click en enviar
                    send_button = wait.until(EC.presence_of_element_located((By.XPATH, '//span[@data-icon="send"]')))                        
                    send_button.click()
                    time.sleep(2)
                    
                    #Give a random number from 2 and 8 to send the next message.
                    random_number = random.randint(2, 8)
                    time.sleep(random_number)
                except Exception as e:            
                    print('Ocurrio un error con '+ str(contacto[self.colDestino]) + ' En envio 1')
                    print(e)                
                    '''
                    # Click on the button to errace the 
                    chat_element = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="side"]/div[1]/div/div/span/button')))
                    #chat_element = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="pane-side"]/div[1]/div/div/div[3]')))
                    chat_element.click()
                    '''
                    continue
            elif self.image_path.endswith('.jpg') or self.image_path.endswith('.png'):
                try:
                    #esta es la parte para enviar la imagen                
                    attachment_button = wait.until(EC.presence_of_element_located((By.XPATH, '//span[@data-icon="attach-menu-plus"]')))
                    attachment_button.click()
                    time.sleep(1)

                    #prueba para seleccionar la imagen
                    attach_image_option = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')))
                    attach_image_option.send_keys(self.image_path)
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
                    print('Ocurrio un error con '+ str(contacto[self.colDestino]) + ' En envio 2')
                    # Click on the button to errace the
                    '''
                    chat_element = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="side"]/div[1]/div/div/span/button')))
                    chat_element.click()
                    '''
                    continue
            elif self.image_path.endswith('.mp4'):
                try:
                    #esta es la parte para enviar la imagen                
                    attachment_button = wait.until(EC.presence_of_element_located((By.XPATH, '//span[@data-icon="attach-menu-plus"]')))
                    attachment_button.click()
                    time.sleep(1)                

                    #prueba para seleccionar la imagen
                    attach_image_option = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')))
                    attach_image_option.send_keys(self.image_path)
                    time.sleep(7)

                    #To write the message that it will send with the image
                    # //*[@id="app"]/div/div/div[3]/div[2]/span/div/span/div/div/div[2]/div/div[1]/div[3]/div/div[2]/div[1]/div/p/span
                    message_input = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[3]/div[2]/span/div/span/div/div/div[2]/div/div[1]/div[3]/div/div/div[1]/div[1]/p')#'//*[@id="app"]/div/div/div[3]/div[2]/span/div/span/div/div/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[1]/p')#'//div[@contenteditable="true"][@data-tab="6"]')
                    message_input.send_keys(text)
                    message_input.send_keys(Keys.ENTER)
                    time.sleep(5)

                    #fin de la prueba para seleccionar la imaen a mandar
                    #Give a random number from 2 and 8 to send the next message.
                    random_number = random.randint(2, 8)
                    time.sleep(random_number)
                except Exception as e:
                    #print("An error occurred:", str(e))
                    print('Ocurrio un error con '+ str(contacto[self.colDestino]))
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
                    message_input = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[3]/div[2]/span/div/span/div/div/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[1]/p')#'//div[@contenteditable="true"][@data-tab="6"]')
                    message_input.send_keys(text)
                    message_input.send_keys(Keys.ENTER)
                    time.sleep(5)

                    #fin de la prueba para seleccionar la imaen a mandar
                    #Give a random number from 2 and 8 to send the next message.
                    random_number = random.randint(2, 8)
                    time.sleep(random_number)
                except Exception as e:
                    print('Ocurrio un error con '+ str(contacto[self.colDestino]) + ' En envio 3')
                    continue