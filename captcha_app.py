import PySimpleGUI
import PySimpleGUI as sg
from PIL import Image, ImageDraw, ImageFont
import random
import string
import io
from base64 import b64encode

# Genera un texto aleatorio para el CAPTCHA
def generar_texto_captcha(length=6):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(length))

# Crea una imagen de CAPTCHA
def crear_captcha(texto, width=200, height=80):
    imagen = Image.new('RGB', (width, height), color=(255, 255, 255))
    d = ImageDraw.Draw(imagen)
    font = ImageFont.truetype("arial.ttf", 40)
    d.text((10, 10), texto, fill=(0, 0, 0), font=font)
    return imagen

# Convierte la imagen PIL a datos base64
def pil_to_base64(imagen):
    buffer = io.BytesIO()
    imagen.save(buffer, format="PNG")
    return b64encode(buffer.getvalue())

# Genera un nuevo CAPTCHA y actualiza la ventana
def generar_nuevo_captcha(window):
    texto_captcha = generar_texto_captcha()
    imagen_captcha = crear_captcha(texto_captcha)
    imagen_base64 = pil_to_base64(imagen_captcha)
    window["-CAPTCHA-"].update(data=imagen_base64)
    return texto_captcha

sg.theme("DarkBlack")

# Crear la ventana de PySimpleGUI
layout = [
    [sg.Text("Introduce el CAPTCHA:")],
    [sg.Image(key="-CAPTCHA-")],
    [sg.Input(key="-INPUT-")],
    [sg.Button("Verificar"), sg.Exit()],
]

window = sg.Window("CAPTCHA", layout,icon=r'16x16.ico', finalize=True)  # Establecer finalize=True
ventana_abierta = True

# Generar el primer CAPTCHA
texto_captcha = generar_nuevo_captcha(window)

while ventana_abierta:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, "Exit"):
        ventana_abierta = False
    elif event == "Verificar":
        texto_ingresado = values["-INPUT-"]
        if texto_ingresado == texto_captcha:
            sg.popup("Captcha Correcto")
            ventana_abierta = False  # Cerrar la ventana principal al verificar el CAPTCHA
        else:
            sg.popup("Captcha Incorrecto. Inténtalo de nuevo.")

        # Generar un nuevo CAPTCHA
        texto_captcha = generar_nuevo_captcha(window)

window.close()  # Asegurarse de cerrar la ventana principal al finalizar
