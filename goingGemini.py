import google.generativeai as genai
import cv2 as cv
import numpy as np
import pyautogui
from test_api import *
from GeminiImageParsing import describe_image, execute

pyautogui.FAILSAFE = False
import subprocess
import time
from PIL import Image
from dotenv import load_dotenv
import os

load_dotenv()

# Установите API-ключ
GENAI_API_KEY = os.getenv('api_key')
genai.configure(api_key=GENAI_API_KEY)

kov1 = "{"
kov2 = "}"


def press_down(key):
    global kov1, kov2
    subprocess.run(["press.exe", f"{kov1}{key} down{kov2}"])


def press_up(key):
    global kov1, kov2
    subprocess.run(["press.exe", f"{kov1}{key} up{kov2}"])


def come_to_coords(x, y):
    tabl = count_coords(x, y)
    print(f'{tabl=}')
    """ для примера
    tabl = \
    {
    'up':50,
    'down':0,
    'right':0,
    'left':89
    }
    """

    if tabl:
        up, down, right, left = tabl['up'], tabl['down'], tabl['right'], tabl['left']

        speed = 390

        if up:
            press_down('Up')
            time.sleep(up / speed)
            press_up('Up')

        elif down:
            press_down('Down')
            time.sleep(down / speed)
            press_up('Down')

        if right:
            press_down('Right')
            time.sleep(right / speed)
            press_up('Right')

        elif left:
            press_down('Left')
            time.sleep(left / speed)
            press_up('Left')

        if up + down + right + left < 400:
            press_down('q')
            press_up('q')

def count_coords(x, y):
    center = {'x':960, 'y':540}
    tabl = \
        {
            'up': 0,
            'down': 0,
            'right': 0,
            'left': 0
        }
    if y > center['y']:
        tabl['down'] += y - center['y']
    else:
        tabl['up'] += center['y'] - y

    if x > center['x']:
        tabl['right'] += x - center['x']
    else:
        tabl['left'] += center['x'] - x
    return tabl


if __name__ == "__main__":
    # input("Подтвердите!")
    print("Начинаем")
    target = "`find the most NEAREST TO CENTER Among Us Player, but ignore player with name `Саня`. NAME IT's LABEL WITH WORD 'RIP'. Do not give it any other labels.`"
    while True:
        # time.sleep(4)
        parsed, im = describe_image(target)
        for el in parsed:
            print(el)
        print()


        cat = None

        for el in parsed:
            if el['label'].lower() == 'rip':
                print('cat found!')
                cat = el
                break

        # function_to_execute = globals().get('come_to_coords')

        if cat:
            come_to_coords(cat['x'], cat['y'])
            print('done')
            # time.sleep(2)
            # im.show()
            #
            # input('Поддержите!')

