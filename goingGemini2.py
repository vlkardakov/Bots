import google.generativeai as genai
import cv2 as cv
import numpy as np
import math
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


def come_to_coords(x, y, kill=False):
    screenWidth, screenHeight = pyautogui.size()

    if x < 50:
        x = x + 50
    elif x > screenWidth - 50:
        x = x - 50

    if y < 50:
        y = y + 50
    elif y > screenHeight - 50:
        y = y - 50

    mouseX, mouseY = pyautogui.position()

    moveX = x - mouseX
    moveY = y - mouseY

    mouseDistance = math.sqrt(moveX**2 + moveY**2)

    speed = 0.8
    clickTime = 1.5 if mouseDistance > 100 else 0.5
    print(f'sleeping for {clickTime}')
    pyautogui.moveTo(100, 100)
    pyautogui.mouseDown()
    pyautogui.moveTo(x, y, duration = 0.01)
    time.sleep(clickTime)
    pyautogui.mouseUp()

    if mouseDistance < 100 or kill:
        press_down('q')
    #     press_up('q')
    #     press_down('q')
    #     press_up('q')
    #     press_down('q')
    #     press_up('q')
    #     press_down('q')
    #     press_up('q')
    #     press_down('q')
    #     press_up('q')
    #     press_down('q')
    #     press_up('q')
    #     press_down('q')
    #     press_up('q')
    #     press_down('q')
    #     press_up('q')
    #     press_down('q')
    #     press_up('q')
    #     press_down('q')
    #     press_up('q')
    #     press_down('q')
    #     press_up('q')
    #     press_down('q')
    #     press_up('q')
    #     press_down('q')
    #     press_up('q')
    #     press_down('q')
    #     press_up('q')
    #     press_down('q')
    #     press_up('q')
    #     press_down('q')
    #     press_up('q')
    #     press_down('q')
    #     press_up('q')
    #     press_down('q')
    #     press_up('q')
    #     press_down('q')
    #     press_up('q')
    #     press_down('q')
    #     press_up('q')
    #     press_down('q')
    #     press_up('q')
    #     press_down('q')
    #     press_up('q')
    #     press_down('q')
    #     press_up('q')
    #     press_down('q')
    #     press_up('q')

        # press_down('q')
        # press_up('q')

descriptionsw = []

if __name__ == "__main__":
    # input("Подтвердите!")
    print("Начинаем")
    target = f"`find the most NEAREST TO CENTER Among Us Player, BUT IGNORE player with name `Саня`!!! IGNORE HIM!!! WHY UR SO STUPID? DONT LOOK AT 'САНЯ'!!!. NAME IT's LABEL: IF THIS PLAYER IS ALONE, DOESNT HAVE ANY OTHER PLAYERS NEAR: 'RIP'. WARNING: IGNORE ORANGE PLAYER! IF ORANGE PLAYER САНЯ IS ONLY PLAYER JUST SELECT SOME EMPTY PLACE TO GO FOR A WALK!!!. Dead Bodies warning: If you see a DEAD PLAYER BODY NEAR CENTER - GO AHEAD! SELECT FAR PLAYER IN 1-click visuality and go there! GO FROM DEAD BODIES!!!!. You can choose only one character to select. Note: if you dont see any players, you can explore the star ship wih selecting empty rooms/coridors. Walls-warning: character Саня cant go trough the walls, they are monotonnelly grey. Instead of going to players behind of them, go to enter of the room and then go to player. You also MUST make description for the scene in layer 'description', there should be: who did u see, where you did go, what did you do and others. example of description part: ..., 'label': 'description: Саня and black characters are going near cameras room and see there dead red with morphing yellow..'.. LABELS_WARNING: YOU CAN ADD ONLY 1 LABEL of 1 task - 1 walk, 1 rip, 1 few...,  . PREVIOUS DESCRIPTIONS: {descriptionsw[10:]}`"
    while True:
        # time.sleep(4)
        parsed, im = describe_image(target)
        for el in parsed:
            print(el)
        print()


        ripp = None
        walk = None
        few = None

        for el in parsed:
            if 'rip' in el['label'].lower():
                print('cat found!')
                ripp = el
                # break
            elif 'few' in el['label'].lower():
                print('few found!')
                few = el
            elif 'descri' in el['label'].lower():
                print('description found!')
                descriptionsw.append(el['label'])
            else:
                print('walk found!')
                walk = el
        if ripp:
            come_to_coords(ripp['x'], ripp['y'], kill=True)
        if few:
            come_to_coords(few['x'], few['y'])
        if walk:
            come_to_coords(walk['x'], walk['y'])
            # print('done')
            # time.sleep(2)
            # im.show()
            #
            # input('Поддержите!')

