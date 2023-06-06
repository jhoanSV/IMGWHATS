import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


# JSON message properties
message_properties_json = '[{"code": "caminar.jpg", "ferreteria": 300, "responsable": 300, "whatsapp": 3134237538}, {"code": "caminar.jpg", "ferreteria": 300, "responsable": 300, "whatsapp": 3219155489}]'
message_properties = json.loads(message_properties_json)

# Path to your Chrome driver executable
chromedriver_path = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"

# URL of WhatsApp Web
whatsapp_web_url = "https://web.whatsapp.com/"

# Configure Chrome driver options
options = webdriver.ChromeOptions() 
options.add_experimental_option('excludeSwitches', ['enable-logging']) 

# Initialize Chrome driver with options
driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)

# Open WhatsApp Web and wait for QR code scan
driver.get(whatsapp_web_url)
print("Scan the QR code and press enter")
input()

# Wait for the WhatsApp Web interface to load
wait = WebDriverWait(driver, 10)
wait.until(EC.title_contains("WhatsApp"))

# Iterate over the message properties and send messages
#for properties in message_properties:
phone_number = '+573228813094' #properties["whatsapp"]
message = "Este es un mensaje de prueba"
#image_path = r'C:\Users\pc\Documents\proyectos empresa\Envio de WhatsApp\pikachu.png'
image_path = r'C:\Users\pc\Documents\proyectos empresa\Envio de WhatsApp\imagen.jpg'
# Search for the chat by phone number
search_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]')))#'//div[@class="_2_1wd"]//div[@contenteditable="true"][@data-tab="3"]')))
search_input.clear()
search_input.send_keys(phone_number)
time.sleep(2)

# Click on the chat to open it
chat_element = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="pane-side"]/div[1]/div/div/div[1]/div/div')))#'//span[@text="{phone_number}"]')))
chat_element.click()
time.sleep(2)

# Send the message with the number of the contact that we want to contact
message_input = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')#'//div[@contenteditable="true"][@data-tab="6"]')
message_input.send_keys(phone_number)
message_input.send_keys(Keys.ENTER)
time.sleep(2)


#esta es la parte para enviar la imagen
attachment_button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]')))
attachment_button.click()
time.sleep(1)

#prueba para seleccionar la imagen
# Choose the "Attach an image" option
attach_image_option = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')))
attach_image_option.send_keys(image_path)
time.sleep(5)

#To write the message that it will send with the image
message_input = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[3]/div[2]/span/div/span/div/div/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[1]/p')#'//div[@contenteditable="true"][@data-tab="6"]')
message_input.send_keys('Este es un mensaje de prueba')
message_input.send_keys(Keys.ENTER)
time.sleep(5)

#fin de la prueba para seleccionar la imaen a mandar


#para cerrar la sesion del whatapp %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
send_button = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="app"]/div/div/div[4]/header/div[2]/div/span/div[4]/div')))#'//*[@id="main"]/footer/div[1]/div/div/div[2]/button')))
send_button.click()

send_button = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="app"]/div/div/div[4]/header/div[2]/div/span/div[4]/span/div/ul/li[7]')))#'//*[@id="main"]/footer/div[1]/div/div/div[2]/button')))
send_button.click()
time.sleep(1)

send_button = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div[3]/div/button[2]')))#'//*[@id="main"]/footer/div[1]/div/div/div[2]/button')))
send_button.click()
time.sleep(7)
#click to send the message

# Close the browser
driver.quit()
