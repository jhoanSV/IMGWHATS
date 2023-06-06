import pygetwindow as gw
import pywinauto
from pywinauto import findwindows
import time

# Obtener todas las ventanas abiertas
ventanas = gw.getWindowsWithTitle('Google Chrome')

if ventanas:
    ventana_chrome = ventanas[0]

    # Activar la ventana de Chrome
    ventana_chrome.activate()

    # Esperar a que la ventana esté lista
    ventana_chrome.maximize()

    # Obtener el ID de la ventana de Chrome
    ventana_chrome_id = ventana_chrome._hWnd

    # Conectar a la ventana de Chrome utilizando pywinauto
    chrome_app = pywinauto.Application(backend="uia").connect(handle=ventana_chrome_id)

    # Obtener el objeto de la ventana principal de Chrome
    chrome_window = chrome_app.window(handle=ventana_chrome_id)#findwindows.find_element(handle=ventana_chrome_id)

    # Obtener los objetos de las pestañas abiertas en la ventana de Chrome
    pestañas = chrome_window.descendants(control_type="TabItem")
    #print(pestañas)
    # Buscar la página específica entre las pestañas abiertas
    pagina_objetivo = None
    for pestaña in pestañas:
        url = pestaña.window_text()
        
        if "WhatsApp" in url:
            pagina_objetivo = pestaña #url
            break
        

    if pagina_objetivo:
        # Hacer algo con la página encontrada
        print("Se encontró la página:", pagina_objetivo.window_text())
        
        # Abrir la página encontrada
        pagina_objetivo.click_input()
        #Esto le da un tiempo para que carge
        time.sleep(1)
        # Puedes realizar más operaciones en la página encontrada

    else:
        print("La página especificada no se encontró en las pestañas abiertas.")
else:
    print("No se encontró la ventana de Chrome abierta.")
