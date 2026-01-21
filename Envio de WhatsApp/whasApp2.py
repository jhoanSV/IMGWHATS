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
#from selenium.webdriver.chrome.service import Service as BraveService
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
from selenium.webdriver.common.action_chains import ActionChains

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
        self.chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"  # ahora es Chrome

        self.options = webdriver.ChromeOptions()
        self.options.binary_location = self.chrome_path
        # --- AÑADE ESTAS LÍNEAS ---
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--disable-software-rasterizer')
        self.options.add_argument('--disable-features=VizDisplayCompositor')
        #self.options.add_argument("--disable-impl-side-painting")
        # -------------------------
        # Todo: Configure Chrome driver option
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super().__init__()
        #self.envio_msj()

    def read_excel_file(self):
        try:
            #lee las filas del excel y las retorna en una lista
            wb = openpyxl.load_workbook(self.excel_file_path)
            sheet = wb.active
            data = []
            self.indices = []
            for i, row in enumerate(sheet.iter_rows(min_row=2, values_only=True)):
                data.append(row)
                self.indices.append(i)
            return data
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo Excel -> {self.excel_file_path}")
            return []

        except openpyxl.utils.exceptions.InvalidFileException:
            print(f"Error: El archivo no es un Excel válido -> {self.excel_file_path}")
            return []

        except Exception as e:
            print(f"Error inesperado al leer el Excel: {e}")
            return []
    

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
        service = Service(ChromeDriverManager().install())
        service.creation_flags = CREATE_NO_WINDOW#*Para que no muestre ventana de cmd
        # Todo: Initialize Chrome driver with options
        # Open WhatsApp Web and wait for QR code scan
        driver = webdriver.Chrome(service=service, options=self.options)
        
        driver.get(self.whatsapp_web_url)
                
        # Espera hasta que la variable cambie
        WebDriverWait(driver, 400).until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]')))
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
            new_chat_btn = '//*[@id="side"]/div[1]/div/div[2]/div/div/div[1]' #'//*[@id="side"]/div[1]/div/div[2]/button/div[2]/span'
            #!This is to whrite the cellnumber
            #text_box = '//*[@id="side"]/div[1]/div/div[2]/div[2]/div/div/p'
            text_box = "//*[@id='side']/div[1]/div/div[2]/div/div/div/p"

            xpaths = [
                "//*[@id='side']/div/div/div/div[1]/div/div",
                "//*[@id='side']/div/div/div/div[2]/div/div"
            ]

            element = "//*[@id='pane-side']/div/div/div/div[2]/div/div"
            for xpath in xpaths:
                try:
                    #element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
                    #element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
                    element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@role='gridcell' and @tabindex='0']"))
                    )
                    break  # Detener el bucle si encuentra el elemento
                except TimeoutException:
                    continue
            #Button to star again a new search
            #arrow_back_but = '//*[@id="app"]/div/div[2]/div[2]/div[1]/span/div/span/div/header//span[@data-icon="back"]'
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
                #search_btn = wait.until(EC.presence_of_element_located((By.XPATH, new_chat_btn)))
                #search_btn.click()
                #search_input = wait.until(EC.presence_of_element_located((By.XPATH, text_box)))

                #//*[@id="app"]/div/div/div[3]/div[1]/span/div/span/div/div[2]/div/div/div/div[1]/div
                #search_input.clear()
                #search_input.send_keys('+57'+ str(self.excel_data[indice][self.colCelular]))
                #el_texto = '//*[@id="app"]//span[contains(text(), "No se encontraron resultados para '+'\'+57'+str(self.excel_data[indice][self.colCelular])+"'\")]"
                
                #time.sleep(3)
                #search_researcher = comprobar_xpath(driver, element)
                #if search_researcher[0]:
                #    #? Click on the chat contact no added to open it
                #    search_researcher[1].click()
                #    time.sleep(1)
                #else:
                #!Select the button New Chat
                search_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-icon='new-chat-outline']")))
                search_btn.click()
                #Put the phone number into the search box
                #search_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[3]/div/div[2]/div[1]/span/div/span/div/div[1]/div[2]/div/div/div[1]/p')))
                search_input = wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div[aria-label='Buscar un nombre o número'][contenteditable='true']")
                ))
                search_input.send_keys('+57'+ str(self.excel_data[indice][self.colCelular]))
                time.sleep(2)
                # Suponiendo que el número está en este formato: 3116032121
                numero_sin_formato = str(self.excel_data[indice][self.colCelular])

                # Formatear el número con espacios
                numero_con_espacios = f"+57 {numero_sin_formato[:3]} {numero_sin_formato[3:]}"
                #search_chat = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="pane-side"]/div/div/div/div[2]/div/div')))
                                #//*[@id="app"]/div/div[3]/div/div[2]/div[1]/span/div/span/div/div[1]/div[2]/div/div/div[1]/p
                                #//*[@id="app"]/div/div[3]/div/div[2]/div[1]/span/div/span/div/div[2]/div/div
                #xpathSearch = '//*[@id="app"]/div[1]/div/div[3]/div/div[2]/div[1]/div/span/div/span/div/div[2]/div[2]/div/div/div[2]/div' #'//*[@id="app"]/div[1]/div/div[3]/div/div[2]/div[1]/div/span/div/span/div/div[2]/div[2]/div/div/div[2]/div' #f"//span[contains(text(), '{numero_con_espacios}')]"
                xpathSearch = '//*[@id="app"]/div[1]/div/div[3]/div/div[3]/div[1]/div/span/div/span/div/div[2]/div[2]/div/div/div[2]/div'
                texto_no_encontrado = "No se encontraron resultados para"
                resultado, elemento = verificar_chat(driver, xpathSearch, texto_no_encontrado)
                if resultado:
                    elemento.click()
                # Esperar hasta que haya resultados visibles
                else:
                    print("La lista es 0")
                    self.errados += 1
                    print('Ocurrio un error con '+ str(self.excel_data[indice][self.colDestino]) + ' En envio')
                    #if not enviado: self.Add_error({indice:str(self.excel_data[indice][self.colDestino])})
                    self.Add_error({indice:str(self.excel_data[indice][self.colDestino])})
                    print('No hay contacto con ese número')
                    #back = '//span[@data-icon="back"]'
                    # //*[@id="app"]/div/div[3]/div/div[2]/div[1]/span/div/span/div/header/div/div[1]/div/span
                    #!Clic in the button back to a new search
                    back = '//span[@data-icon="back-refreshed"]'
                    #back = '//span[@aria-label="atras"]'
                    search_btn = wait.until(EC.presence_of_element_located((By.XPATH, back)))
                    search_btn.click()
                    continue
                time.sleep(2)
            except Exception as e:
                print('Ocurrio un error con '+ str(self.excel_data[indice][self.colDestino]) + ' En envio 3: el error es' + str(e))
                self.Add_error({indice:str(self.excel_data[indice][self.colDestino])})
                continue
            if self.image_path == '':
                try:
                    """#?Send the message with the number of the contact that we want to contact
                    #*Busca la kja de texto y le asigna el msj
                    search_tb = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div/div[3]/div[1]')))
                    search_tb.click()
                    message_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div/div[3]/div')))

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
                    
                    #if not enviado: self.Add_error({indice:str(self.excel_data[indice][self.colDestino])})"""
                    # Esperamos a que sea clickable
                    message_input = wait.until(EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "div[data-tab='10'][contenteditable='true']")
                    ))

                    # 2. Forzar el foco con un click físico
                    message_input.click()
                    time.sleep(0.5)

                    # 3. Escribir el mensaje
                    if len(lineas) > 1:
                        print('Escribiendo múltiples líneas...')
                        for l, line in enumerate(lineas):
                            message_input.send_keys(line.rstrip())
                            # Evitar mandar el último Shift+Enter para que no quede un espacio vacío abajo
                            if l < len(lineas) - 1:
                                message_input.send_keys(Keys.SHIFT, Keys.ENTER)
                    else:
                        print('Escribiendo línea única')
                        message_input.send_keys(text.rstrip())

                    # 4. Enviar
                    time.sleep(0.5)
                    message_input.send_keys(Keys.ENTER)
                    time.sleep(2)
                except Exception as e:
                    self.errados += 1
                    print('Ocurrio un error con '+ str(self.excel_data[indice][self.colDestino]) + ' En envio')
                    print(e)
                    #if not enviado: self.Add_error({indice:str(self.excel_data[indice][self.colDestino])})
                    self.Add_error({indice:str(self.excel_data[indice][self.colDestino])})
                    continue
            elif self.image_path.endswith('.jpg') or self.image_path.endswith('.png') or self.image_path.endswith('.mp4'):
                try:                    
                    # 1. Clic en el botón "+" e input de archivo
                    plus_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-icon='plus-rounded']")))
                    plus_btn.click()
                    
                    file_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
                    file_input.send_keys(os.path.abspath(self.image_path))
                    
                    # 2. Esperar la caja de texto de la vista previa
                    message_input = wait.until(EC.element_to_be_clickable(
                        (By.XPATH, "//div[@aria-label='Escribe un mensaje' and @role='textbox']")
                    ))

                    # 2. Dar foco (indispensable)
                    message_input.click()
                    time.sleep(1) # Dale 1 segundo completo para que el cursor se active

                    # 3. Escribir (Usando tu lógica de lineas y send_keys normal)
                    if (len(lineas) > 1):
                        print('entro a lineas')
                        for l, line in enumerate(lineas):
                            message_input.send_keys(line.rstrip())
                            # Shift+Enter para nueva línea dentro del mismo mensaje
                            message_input.send_keys(Keys.SHIFT, Keys.ENTER)
                    else:
                        print('No entro a lineas')
                        message_input.send_keys(text.rstrip())

                    time.sleep(1) # Esperar a que el texto se vea en pantalla

                    # 4. Enviar (Usando el botón verde para evitar el error del cuadro negro)
                    # 1. LOCALIZAR EL BOTÓN (el DIV que me pasaste)
                    # Esperamos a que el botón sea visible y tenga el icono dentro
                    send_btn = wait.until(EC.presence_of_element_located(
                        (By.XPATH, "//div[@role='button' and @aria-label='Enviar']")
                    ))

                    # 2. PAUSA DE SINCRONIZACIÓN (Vital para evitar el cuadro negro)
                    # WhatsApp necesita un momento para que el "blob" de la imagen esté listo para envío
                    time.sleep(2.5) 

                    # 3. EL TRUCO DEFINITIVO: DISPARAR EVENTOS DE MOUSE
                    # En lugar de un simple .click(), disparamos 'mousedown' y 'mouseup' 
                    # Esto engaña a WhatsApp haciéndole creer que un humano presionó y soltó el botón.
                    driver.execute_script("""
                        var btn = arguments[0];
                        var mousedown = new MouseEvent('mousedown', {bubbles: true, cancelable: true, view: window});
                        var mouseup = new MouseEvent('mouseup', {bubbles: true, cancelable: true, view: window});
                        var click = new MouseEvent('click', {bubbles: true, cancelable: true, view: window});
                        btn.dispatchEvent(mousedown);
                        btn.dispatchEvent(mouseup);
                        btn.dispatchEvent(click);
                    """, send_btn)

                    # 4. VERIFICACIÓN DE SALIDA
                    # Esperamos a que el cuadro de texto desaparezca (señal de que se envió)
                    time.sleep(2)
                    
                    # Si el cuadro negro persiste, usamos el ENTER como último recurso de empuje
                    if driver.find_elements(By.XPATH, "//div[@aria-label='Escribe un mensaje']"):
                        print("El cuadro negro persiste, intentando empujar con ENTER...")
                        message_input = driver.find_element(By.XPATH, "//div[@aria-label='Escribe un mensaje']")
                        message_input.send_keys(Keys.ENTER)
                        time.sleep(2)

                    # Si después de todo sigue negro, cerramos con ESC para que no bloquee el bucle
                    if driver.find_elements(By.XPATH, "//div[@aria-label='Escribe un mensaje']"):
                        print("Error de renderizado detectado, limpiando interfaz con ESC")
                        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                        self.errados += 1
                    else:
                        print("Envío exitoso")

                    # Esperar a que la interfaz vuelva a la normalidad
                    random_number = random.randint(3, 6)
                    time.sleep(random_number)
                    self.enviados += 1
                except Exception as e:
                    self.errados += 1
                    print(e)
                    print('Ocurrio un error con '+ str(self.excel_data[indice][self.colDestino]) + ' En envio 2')
                    self.Add_error({indice:str(self.excel_data[indice][self.colDestino])})
                    continue
        #para cerrar la sesion del whatapp %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        try:
            #Clic a menú
            boton_menu = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "span[data-icon='more-refreshed']")
            ))
            boton_menu.click()

            #Darle click a cerrar sesión en el menú desplegable.
            cerrar_sesion = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//span[text()='Cerrar sesión']")
            ))
            cerrar_sesion.click()

            # Busca el botón que contiene el texto "Cerrar sesión"
            confirm_btn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[descendant::span[text()='Cerrar sesión']]")
            ))
            confirm_btn.click()
            time.sleep(7)
        except Exception as e:
            print("No se pudo cerrar sesión ", e)
        
        # Close the browser
        driver.quit()
        self.show_end(self.enviados, self.errados)
        
        