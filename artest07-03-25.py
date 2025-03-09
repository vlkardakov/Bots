from xmlrpc.client import boolean
import os
import pytesseract
from PIL import Image
import mss
import cv2 as cv
import numpy as np
import time
from time import sleep
from ultralytics import YOLO
from concurrent.futures import ThreadPoolExecutor
from arestarmongus3 import _chat, what_step, change_params
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
        text += f"{el} "
    text = clean_string(text, "<>[]|")
    # print(f"Текст - {text}")
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


def img_for_color():
    with mss.mss() as sct:
        # Координаты и размеры области захвата
        mon = sct.monitors[monum]
        monitor = {
            "top": mon["top"] + 87,  # 100px from the top
            "left": mon["left"] + 275,  # 100px from the left
            "width": 213,
            "height": 40
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
    # print(f"""Автор: {author.split("\n")}""")
    author = author.split("\n")[0]
    author = clean_string(author, """<>[]/|:,.;`'""")

    # print(f"""Автор: {author}""")
    if "Kor" in author:
        author = "Кот"
    elif "Koy" in author:
        author = "Кот"
    elif "Enka" in author:
        author = "Лаша"
    elif "Kor" in author:
        author = "Кот"

    return author


def clean_string(s, bads):
    bad_chars = np.array(list(bads))
    return "".join([c for c in s if c not in bad_chars])


def islobby(template, threshold):
    with mss() as sct:
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
    with ThreadPoolExecutor(max_workers=10) as executor:
        print("Задаем потоки..")
        img1 = img_for_text()
        img2 = img_for_author()
        img3 = img_for_color()
        futuretext = executor.submit(gettxt, img1)
        futureauthor = executor.submit(get_author, img2)
        futurecolor = executor.submit(gettxt, img3)
        text, author, color = futuretext.result(), futureauthor.result(), futurecolor.result()
        return text, author, color


free_time = float(time.time())


def convert_to_single_line(text):
    return text.replace('\n', '  ')


Esc = "{Esc}"


def send_chat(string, limit=100):
    message = clean_string(str(string), ["[", "]", "<", ">"]).replace("\n", "   ")
    message = convert_to_single_line(message)
    # _chat()
    # time.sleep(0.3)
    # _chat()
    if len(message) > limit:
        for i in range(0, len(message), limit):
            chunk = message[i:i + limit]
            print(f"Что печатаем: \n{replace_string(chunk) + Enter}")
            send(replace_string(chunk) + Enter)
            time.sleep(3.2 if i != len(message) else 0.5)
        time.sleep(0.2)
        # send(Esc)
    else:
        print(f"Что печатаем: \n{replace_string(message) + Enter}")
        send(replace_string(message) + Enter)
        time.sleep(1)
        # send(Esc)


recent_msgs = []
import random

journal = []


def replace_string(input_str):
    # Словарь для замены
    # '': '{Lshift down}{Lshift up}',
    replacements = {
        '!': '{Lshift down}1{Lshift up}',
        '?': '{Lshift down}7{Lshift up}',
        ':': '{Lshift down}6{Lshift up}',
        '*': '{Lshift down}8{Lshift up}',
        '+': '{Lshift down}={Lshift up}',
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


def up(tm):
    send("{Up down}")
    time.sleep(tm)
    send("{Up up}")


def left(tm):
    send("{Left down}")
    time.sleep(tm)
    send("{Left up}")


def right(tm):
    send("{Right down}")
    time.sleep(tm)
    send("{Right up}")


def down(tm):
    send("{Down down}")
    time.sleep(tm)
    send("{Down up}")


def up_left(tm):
    send("{Up down}{Left down}")
    time.sleep(tm)
    send("{Up up}{Left up}")


def up_right(tm):
    send("{Up down}{Right down}")
    time.sleep(tm)
    send("{Up up}{Right up}")


def down_left(tm):
    send("{Up down}")
    time.sleep(tm)
    send("{Up up}")


def down_right(tm):
    send("{Down down}{Right down}")
    time.sleep(tm)
    send("{Down up}{Right up}")


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
from describe_screen import describe
from arestarmongus3 import _start
import pickle

def check_if_name(names, result):
    for name in names:
        if name in result:
            return True


def capture_screenshot(monitor_data):
    with mss.mss() as sct:
        sct_img = sct.grab(monitor_data)
        img_np = np.frombuffer(sct_img.bgra, dtype=np.uint8).reshape(sct_img.height, sct_img.width, 4)
        img_np = img_np[..., :3][:, :, ::-1]  # BGRA -> RGB
        img = Image.fromarray(img_np)
        img = img.resize((320, 180))
        return img, np.array(img)


import re


def main():
    global result_coding, chat_session, messages, new_messages
    timeing = 5

    while True:
        _chat()
        if not is_lobby():
            print('checking is chat open...')
            time.sleep(timeing)
            refreshed = refresh_chat()
            print(refreshed)
            if refreshed:
                timeing = 3
                print('checking news...')
                me1 = convert_to_single_line(
                    clean_string(ask_gemini(), ["[", "]", "<", ">", r"\n", "\n"]).replace("\n", ""))
                if not me1.replace("\n", "").strip() == "-":
                    print('Проверка на команды')

                    if "start" in me1:
                        send("{Esc}")
                        time.sleep(0.2)
                        _start()
                        _chat()
                    if "off" in me1:
                        send_chat(me1)
                        time.sleep(1)
                        send_chat("SAVING MEMORY AND TURNING OFF...")
                        with open('chat_history.pkl', 'wb') as f:
                            pickle.dump(chat_session.history, f)
                        exit()
                    if "save" in me1:
                        with open('chat_history.pkl', 'wb') as f:
                            pickle.dump(chat_session.history, f)
                    if "clear" in me1:
                        with open('chat_history.pkl', 'rb') as cs:
                            chat_session.history = pickle.load(cs)

                    if 'impostors_count:+' in me1:
                        change_params("impostors_count:1")
                        time.sleep(0.4)
                        _chat()
                    if 'impostors_count:-' in me1:
                        change_params("impostors_count:-1")
                        time.sleep(0.4)
                        _chat()
                    if 'speed:+' in me1:
                        change_params("speed:1")
                        time.sleep(0.4)
                        _chat()
                    if 'speed:-' in me1:
                        change_params("speed:-1")
                        time.sleep(0.4)
                        _chat()
                    if 'kill_rich:+' in me1:
                        change_params("kill_rich:1")
                        time.sleep(0.4)
                        _chat()
                    if 'kill_rich:-' in me1:
                        change_params("kill_rich:-1")
                        time.sleep(0.4)
                        _chat()
                    if 'impostor_vision:+' in me1:
                        change_params("impostor_vision:1")
                        time.sleep(0.4)
                        _chat()
                    if 'impostor_vision:-' in me1:
                        change_params("impostor_vision:-1")
                        time.sleep(0.4)
                        _chat()
                    if 'crew_vision:+' in me1:
                        change_params("impostor_vision:1")
                        time.sleep(0.4)
                        _chat()
                    if 'crew_vision:+' in me1:
                        change_params("impostor_vision:1")
                        time.sleep(0.4)
                        _chat()
                    print(me1)

                    for el in me1.split("%"):
                        send_chat(el)
                        if el != me1.split("%")[-1]:
                            time.sleep(2.4)
                else:
                    print("not sending, sleep")
                    time.sleep(4)
            # while text == last_text and author == last_author:
            #    #print("text and author last")
            #    time.sleep(0.5)
            #    text, author, color = fast_data()
        else:
            print(f"not chat, увеличиваем timeing с {timeing} до {timeing+0.5}")
            timeing += 1
            time.sleep(0.5)


if __name__ == "__main__":
    # while True:
    #     send_chat('мяу мяу мяу мяу мяу мяу мяу мяу мяу мяу')
    #     time.sleep(2.5)
    # exit()
    main()
    send_chat("Бляя... Я сломался")
