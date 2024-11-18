import pytesseract
from PIL import Image
import mss
import numpy as np
import cv2 as cv
import time
from ultralytics import YOLO
model = YOLO('2.pt')
def scr():
    with mss.mss() as sct:
        # Координаты и размеры области захвата
        mon = sct.monitors[1]
        monitor = {
            "top": mon["top"] + 38,  # 100px from the top
            "left": mon["left"] + 585,  # 100px from the left
            "width": 820,
            "height": 103
        }

        screenshot = np.array(sct.grab(monitor))
        img_rgb = cv.cvtColor(screenshot, cv.COLOR_BGR2RGB)
        img_gray = cv.cvtColor(img_rgb, cv.COLOR_RGB2GRAY)
        output = "sct.png".format(**monitor)

        # Grab the data
        sct_img = sct.grab(monitor)

        # Save to the picture file
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)

def get_author():
    with mss.mss() as sct:
        # Координаты и размеры области захвата
        mon = sct.monitors[1]
        monitor = {
            "top": mon["top"] + 31,  # 100px from the top
            "left": mon["left"] + 259,  # 100px from the left
            "width": 200,
            "height": 110
        }

        screenshot = np.array(sct.grab(monitor))
        img_rgb = cv.cvtColor(screenshot, cv.COLOR_BGR2RGB)
        img_gray = cv.cvtColor(img_rgb, cv.COLOR_RGB2GRAY)
        output = "auth.png".format(**monitor)
        # Grab the data
        sct_img = sct.grab(monitor)
        # Save to the picture file
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
        image = Image.open('auth.png')
        author = pytesseract.image_to_string(image, lang = "+rus+eng")
        print(f"""Автор: {author.split("\n")}""")
        author = author.split("\n")[0]
        authorsymbols = list(author)
        iii = 0
        for authorsymbol in authorsymbols:
            for bad_for_author in bad_for_authors:
                if bad_for_author == authorsymbol:
                    authorsymbols[iii] = ""
                    break
            iii+=1
        author = ""
        for el in authorsymbols:
            if el != "":author+=el

        print(f"""Автор: {author}""")
        return author
bad_for_authors = list("""<>[]/|:,.;`'""")
badsimbols = list("<>[]/|")
from arestarmongus3 import what_step, send_chat, send, find
while True:
    m = what_step()
    if m == "lobby":
        scr()
        # Open the image file
        image = Image.open('sct.png')
        # Perform OCR using PyTesseract
        text = last_text = pytesseract.image_to_string(image, lang='rus')
        author = last_author = get_author()
        text2 = {text.split("\n")[0]}
        Enter = "{Enter}"
        print(f"text - {text}")
        send_chat(f"""Уважаемый {author}, Вы написали: {text.split("\n")[0]}{Enter}""")
        print(f"""text - 1{text.split("\n")[0]}1""")
        if text != "" and author != "":
            send_chat(f"""Уважаемый {author}, Вы написали: {text.split("\n")[0]}{Enter}""")
            while text == last_text and author == last_author and what_step()=="lobby" and text != "" and author != "":

                author = get_author()
                text = pytesseract.image_to_string(image, lang='rus')
            print(text)