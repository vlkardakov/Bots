import pytesseract
from PIL import Image
import mss
import cv2 as cv
import numpy as np
import time
from time import sleep
from ultralytics import YOLO
from concurrent.futures import ThreadPoolExecutor
from arestarmongus3 import  _chat, what_step
import os
from dotenv import load_dotenv
load_dotenv()
import subprocess

def send(text):
    subprocess.run(["press.exe", text])

monum = int(os.getenv("monitor"))
name = int(os.getenv("name"))
names = os.getenv("names").split(",")

Enter = "{Enter}"
def gettxt(sct_img):
    image = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
    text = pytesseract.image_to_string(image, lang="+rus+eng")
    strings = text.split("\n")
    text = ""
    for el in strings:
        text+=f"{el} "
    text = clean_string(text, "<>[]|")
    #print(f"Текст - {text}")
    return text
def img_for_author():
    with mss.mss() as sct:
        # Координаты и размеры области захвата
        mon = sct.monitors[monum]
        monitor = {
            "top": mon["top"] + 52,  # 100px from the top
            "left": mon["left"] + 275,  # 100px from the left
            "width": 218,
            "height": 45
        }
        # Grab the data
        sct_img = sct.grab(monitor)
        return sct_img
def img_for_text():
    with mss.mss() as sct:
        # Координаты и размеры области захвата
        mon = sct.monitors[monum]
        monitor = {
            "top": mon["top"] + 38,  # 100px from the top
            "left": mon["left"] + 585,  # 100px from the left
            "width": 800,
            "height": 103
        }
        sct_img = sct.grab(monitor)
        # Сохраняем скриншот в файл
        img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
        filename = "screenshot.png"
        img.save(filename)
        return sct_img
def get_author(sct_img):
    image = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
    author = pytesseract.image_to_string(image, lang="+eng+rus")
    #print(f"""Автор: {author.split("\n")}""")
    author = author.split("\n")[0]
    author = clean_string(author, """<>[]/|:,.;`'""")

    #print(f"""Автор: {author}""")
    #if "Cherry" in author: author+=f" (Префикс мяу)"
    return author
def clean_string(s, bads):
    bad_chars = np.array(list(bads))
    return "".join([c for c in s if c not in bad_chars])
def islobby(template, threshold):
    with mss.mss() as sct:
        # Координаты и размеры области захвата
        mon = sct.monitors[monum]
        monitor = {
            "top": mon["top"] + 450,
            "left": mon["left"] + 1460,
            "width": 300,
            "height": 250
        }
        screenshot = np.array(sct.grab(monitor))
        img_rgb = cv.cvtColor(screenshot, cv.COLOR_BGR2RGB)
        img_gray = cv.cvtColor(img_rgb, cv.COLOR_RGB2GRAY)

    template = cv.imread(template, cv.IMREAD_GRAYSCALE)
    w, h = template.shape[::-1]

    res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):
        if pt[0] < 1920 and pt[1] < 1080:
            return True
        return False
def is_lobby():
    return islobby("imgs/islobby.png", 0.8)
def fast_data():
    with ThreadPoolExecutor(max_workers=4) as executor:
        #print("Задаем потоки..")
        img1 = img_for_text()
        img2 = img_for_author()
        futuretext = executor.submit(gettxt, img1)
        futureauthor = executor.submit(get_author, img2)
        text, author = futuretext.result(), futureauthor.result()
        return text, author
free_time = float(time.time())
def convert_to_single_line(text):
    return text.replace('\n', ' ')
Esc = "{Esc}"
def send_chat(*args):
    message = str(*args)
    message = convert_to_single_line(message)
    _chat()
    time.sleep(0.3)
    _chat()
    if len(message) > 95:
        for i in range(0, len(message), 95):
            chunk = message[i:i+95]
            print(f"Что печатаем: \n{replace_string(chunk)+"  "+Enter}")
            send(replace_string(chunk)+"  "+Enter)
            if i*90<len(message):
                time.sleep(3.6)
        send(Esc)
    else:
        print(f"Что печатаем: \n{replace_string(message) + "  " + Enter}")
        send(replace_string(message)+" "+Enter)
        time.sleep(1)
        send(Esc)
recent_msgs = []
import random
journal = []



def replace_string(input_str):
    # Словарь для замены
    replacements = {
        '!': '{Lshift down}1{Lshift up}',
        '?': '{Lshift down}7{Lshift up}',
        ':': '{Lshift down}6{Lshift up}',
        '*': '{Lshift down}8{Lshift up}',
        '\n': ' '
    }

    # Создаем новую строку с заменами
    output_str = ""
    for char in input_str:
        if char in replacements:
            output_str += replacements[char]
        else:
            output_str += char

    return output_str


import json

def save_data(name, data):
    try:
        with open(f"files/{name}.json", 'w') as file:
            json.dump(data, file)
        return True
    except Exception as e:
        return False
def load_data(name):
    try:
        with open(f"files/{name}.json", 'r') as file:
            return json.load(file)
    except Exception as e:
        return ""

from memory import *
from checkthechat import check_the_chat
from test_api import *
result_coding = None
def check_if_name(names,result):
    for name in names:
        if name in result:
            return True
def main():
    global result_coding
    global chat_session
    while True:
        for i in range(100):
            if is_lobby():
                chat_result = check_the_chat()
                while chat_result == None:
                    chat_result = check_the_chat()
                    time.sleep(0.5)
                    #print("...")
                text, author = fast_data()
                last_text, last_author = text, author

                if text != (""or" ") and author != "":

                    te = f"Игрок {author}: {text}"
                    chat_session.history.append({"role": f"user", "parts": [te]})
                    print(text, author)
                    ans = gemini(author, text)
                    ans = gemini(author, text)
                    print(ans)
                    send_chat(ans)

                while text == last_text and author == last_author:
                    #print("text and author last")
                    time.sleep(0.5)
                    text, author = fast_data()
            else:
                #print("not chat")
                time.sleep(0.5)
                send(Esc)
if __name__ == "__main__":
    send_chat(f"Всем привет!")
    while True:
            main()