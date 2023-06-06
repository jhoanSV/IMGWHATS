import pygetwindow as gw
import pywinauto
from pywinauto import findwindows

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
    chrome_window = chrome_app.window(handle=ventana_chrome_id)

    # Obtener los objetos de las pestañas abiertas en la ventana de Chrome
    pestañas = chrome_window.descendants(control_type="TabItem")
    print(pestañas)

    # Buscar la página específica entre las pestañas abiertas
    pagina_objetivo = None
    for pestaña in pestañas:
        # Obtener el control de la pestaña
        pestaña_control = pestaña.element_info

        # Obtener el patrón de valor del control
        value_pattern = pestaña_control.patterns.value

        # Obtener la URL de la pestaña
        url = value_pattern.value
        print(url)

        if "https://web.whatsapp.com/" in url:
            pagina_objetivo = url
            break

    if pagina_objetivo:
        # Hacer algo con la página encontrada
        print("Se encontró la página:", pagina_objetivo)

        # Puedes realizar más operaciones en la página encontrada

    else:
        print("La página especificada no se encontró en las pestañas abiertas.")
else:
    print("No se encontró la ventana de Chrome abierta.")
