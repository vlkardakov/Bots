from xmlrpc.client import boolean
import os
import pytesseract
from PIL import Image
import mss
import pyautogui as pg
import cv2 as cv
import numpy as np
import time
# from time import sleep
# from ultralytics import YOLO
from concurrent.futures import ThreadPoolExecutor
from utils import _chat, change_params
import os
from dotenv import load_dotenv

import threading
import datetime
import numpy as np
import signal
import sys
from pynput import keyboard

load_dotenv()
import subprocess


def send(text):
    print(f'{text=}')
    subprocess.run(["press.exe", text])


monum = int(os.getenv("monitor"))
name = int(os.getenv("name"))
names = os.getenv("names").split(",")

Enter = "{Enter}"




def clean_string(s, bads):
    bad_chars = np.array(list(bads))
    return "".join([c for c in s if c not in bad_chars])

free_time = float(time.time())


def convert_to_single_line(text):
    return text.replace('\n', '  ')


Esc = "{Esc}"


def send_chat(string, limit=256):
    message = '' + clean_string(str(string), ["[", "]", "<", ">"]) + ('' if string.startswith('#') else '  сб')#.replace("\n", "   ")
    message = convert_to_single_line(message)
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
        send('е')
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
        '#': '{LAlt down}{Numpad3}{Numpad5}{LAlt up}',
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
from utils import _start
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

def what_step():
    response = describe('ОПИШИ СКРИНШОТ И ВЫБЕРИ, ГДЕ НАХОДИТСЯ ПОЛЬЗОВАТЕЛЬ В ИГРЕ MINECRAFT', makescreen())
    return response.strip().upper()

def restartTheGame():
    coords = (1800, 930)
    pg.click(coords)
    time.sleep(0.5)
    pg.click(coords)


def main():
    global result_coding, chat_session, messages, new_messages, step
    timeing = 5

    while True:
        for _ in range(3):
                print('checking is chat open...')
                # time.sleep(timeing)
                refreshed = refresh_chat()
                print(refreshed)
                if refreshed:
                    timeing = 3
                    print('checking news...')
                    me1 = convert_to_single_line(
                        clean_string(ask_gemini(), ["[", "]", "<", ">", r"\n", "\n"]).replace("\n", ""))
                    if not me1.replace("\n", "").strip() == "-":
                        print(me1)

                        for el in me1.split("%"):
                            send_chat(el)
                            if el != me1.split("%")[-1]:
                                time.sleep(2.4)
                    else:
                        print("not sending, sleep")
                        time.sleep(1)

        # step = what_step()
        # if step == "КОНЕЦ ИГРЫ":
        #     restartTheGame()
        # elif step == "В ИГРЕ":
        #     ask_gemini()
        # elif step in ("ВНЕ ИГРЫ", ''):
        #     time.sleep(10)


if __name__ == "__main__":
    # while True:
    #     send_chat('МЯУ МЯУ МЯУ МЯУ МЯУ МЯУ МЯУ МЯУ МЯУ МЯУ МЯУ МЯУ МЯУ МЯУ ')
    #     time.sleep(2.5)
    #
    send_chat('Дубль хз какой. (сб = сгенерировано ботом ')
    # send_chat('И второе сообщение')
    # exit()
    main()
    # send_chat("Бляя... Я сломался")
