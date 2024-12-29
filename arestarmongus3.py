import cv2 as cv
import numpy as np
import mss
import argparse
import time
import pyautogui
import os
import subprocess
import time
from ultralytics import YOLO

from dotenv import load_dotenv
load_dotenv()
monum = int(os.getenv("monitor"))

#model = YOLO('2.pt')
#time.sleep(2)

def send(text):
    subprocess.run(["press.exe", text])
def find(template, threshold, y, x, target_count, do_click):
    global monum
    with mss.mss() as sct:
        screenshot = np.array(sct.grab(sct.monitors[monum]))
        img_rgb = cv.cvtColor(screenshot, cv.COLOR_BGR2RGB)
        img_gray = cv.cvtColor(img_rgb, cv.COLOR_RGB2GRAY)

    template = cv.imread(template, cv.IMREAD_GRAYSCALE)
    w, h = template.shape[::-1]

    res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    count = 1
    for pt in zip(*loc[::-1]):
        if pt[0] < 1920 and pt[1] < 1080:
            center_x = pt[0] + int(w // 2)
            center_y = pt[1] + int(h // 2)

            # Нарисовать прямоугольник и номер на снимке экрана
            cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (255, 0, 0), 2)
            cv.putText(img_rgb, str(count), (pt[0] - x, pt[1] - y - 5), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

            if count == target_count:
                if do_click:
                    # Выполнить клик по центру найденного шаблона
                    pyautogui.click(center_x + x, center_y + y)
                    return True
                return True

            count += 1

    # Сохранить снимок экрана с наложенными элементами
    cv.imwrite("screenshot_with_overlays.png", cv.cvtColor(img_rgb, cv.COLOR_RGB2BGR))
def fafind(template,treshold,do_click):
    res = find(f"imgs/{template}.png",treshold, 0, 0, 1, do_click)
    return res
pyautogui.moveTo(800,500)
print("starting")
def what_step():
    # Сделать скриншот экрана
    screen = pyautogui.screenshot()

    # Преобразовать скриншот в OpenCV изображение
    image = np.array(screen)
    image = cv.cvtColor(image, cv.COLOR_RGB2BGR)

    # Уменьшить размер изображения до размера, требуемого моделью
    image = cv.resize(image, (640, 640))

    # Обработать скриншот с помощью модели YOLO
    results = model(image)[0]

    names = results.names
    #print("Top 1 Class Name : {}".format(names[results.probs.top1]))
    return str(names[results.probs.top1])
def _return():
    fafind("return", 0.8, True)
def _continue():
    fafind("continue", 0.8, True)
def _start():
    return fafind("start_button", 0.6, True)
def _chat():
    fafind("chat", 0.8, True)
def ischat_():
    fafind("chat_is_open", 0.8, False)
def _settings():
    return fafind("settings", 0.8, True)

import pyautogui
import time
def change_params(param):
    send("{Esc}")
    time.sleep(0.2)
    dict_of_coords = {
        "impostors_count": 320,
        "kill_cooldown": 410,
        "impostor_vision": 490,
        "kill_rich": 570,
        "speed": 770,
        "crew_vision": 840,
    }

    if not param.startswith("map:"):
        first, second = param.split(":")
        second = int(second)
    else:
        first = "map"
    if _settings():
        time.sleep(0.1)
        if fafind("settings2", 0.8, True):
            if not param.startswith("map:"):
                time.sleep(0.1)
                # Получаем разрешение экрана
                screen_width, screen_height = pyautogui.size()

                # Вычисляем координаты центра экрана
                center_x = screen_width // 2
                center_y = screen_height // 2

                # Перемещаем курсор в центр экрана
                pyautogui.moveTo(center_x, center_y, duration=0.25)

                # Нажимаем левую кнопку мыши
                pyautogui.mouseDown()

                # Перемещаем курсор вверх на 100 пикселей
                pyautogui.moveTo(center_x, center_y - 270, duration=0.25)

                # Отпускаем левую кнопку мыши
                pyautogui.mouseUp()

                time.sleep(0.1)

                height = dict_of_coords[first]

                if second > 0:
                    pyautogui.click(1550, height)
                else:
                    pyautogui.click(1280, height)

                time.sleep(0.1)
                send("{Esq}")




def what_do(cls):
    if cls == "lobby" and fafind("start_button", 0.8, False) == True:
        for i in range(5):
            time.sleep(5)
            _chat()
            send("Игра автоматически начнется при 15 игроках или напишите СТАРТ{Enter}{Esq}")
            for i in range(10):
                if fafind("startmsg", 0.8, False) == True:
                    for i in range(5):
                        _start()
                        time.sleep(0.5)
    elif cls == "chat":
        send("{Esc}")
    elif cls == "endgame_1" or cls == "imimpostor" or cls == "imcrew":
        _continue()
        time.sleep(0.5)
        _return()
    elif cls == "endgame_2":
        _return()
import keyboard

def parse(pars):
    targets = {}
    pars = pars.split()
    keys = pars[0].split("#")
    values = pars[1].split("#")
    dicti = {}
    i = 0
    for key in keys:
        dicti[key] = float(values[i])
        i+=1
    return dicti

def mufind(pars, target_count, do_click):
    found = []
    y = x = 0
    pars = pars.split()
    keys = pars[0].split("#")
    values = pars[1].split("#")
    #print(f"Keys {keys}, values {values}")
    iii = 0
    #print("screening")
    with mss.mss() as sct:
        # Координаты и размеры области захвата
        mon = sct.monitors[1]
        monitor = {
            "top": mon["top"] + 31,  # 100px from the top
            "left": mon["left"] + 250,  # 100px from the left
            "width": 1160,
            "height": 110
        }

        screenshot = np.array(sct.grab(monitor))
        img_rgb = cv.cvtColor(screenshot, cv.COLOR_BGR2RGB)
        img_gray = cv.cvtColor(img_rgb, cv.COLOR_RGB2GRAY)
        output = "sct.png".format(**monitor)



    for key in keys:
        #print(f"finding {key}")
        #print(f"iii {iii}")
        template = f"imgs/{key}.png"
        threshold = float(values[iii])

        template = cv.imread(template, cv.IMREAD_GRAYSCALE)
        w, h = template.shape[::-1]

        res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        #print(f"loc = {loc}, {res}")
        mgm = False
        count = 1
        for pt in zip(*loc[::-1]):
            if pt[0] < 1920 and pt[1] < 1080:
                mgm = True
        if mgm:
            print(f"now {key}")
            found.append(key)
                #center_x = pt[0] + int(w // 2)
                #center_y = pt[1] + int(h // 2)
                #if do_click == False:return True
                #if count == target_count and do_click == True:
                    # Выполнить клик по центру найденного шаблона
                    #pyautogui.click(center_x + x, center_y + y)
                #count += 1

        iii+=1
        # Сохранить снимок экрана с наложенными элементами
        #cv.imwrite("screenshot_with_overlays.png", cv.cvtColor(img_rgb, cv.COLOR_RGB2BGR))
    return found


import random
bus = [
    "Да, это бу",
    "Нет, это не бу.",
    "Это точно бу.",
    "Может быть бу.",
    "Бу, да бу.",
    "Это не бу, точно.",
    "Угу, бу.",
    "Нет, не бу.",
    "Бу, это бу.",
    "Это бу, я уверен.",
    "Безоговорочно бу",
    "Вероятно, бу.",
    "Похоже, что бу.",
    "Бу, это фак",
    "Это не бу, я уверен.",
    "Нет, это не бу, убедитесь.",
    "Окончательный ответ - бу.",
    "Это бу, без вариантов.",
    "Бу, это моя точка зрения.",
    "Это бу, я чувствую.",
    "Бу, это мой опыт.",
    "Это бу, я убежден.",
    "Нет, не бу, я уверен.",
    "Бу, это моя догадка.",
    "Это бу, ты лох",
    "Не мешай мне делать сложные компьютерные вычисления :З",
    "Это бу, я проверил.",
    "Бля, я аж вдрогнул",
    "Это бу, я исследовал.",
    "Бу, это моя интуиция.",
    "Это бу, я чувствую глубоко.",
    "Бу, это моя внутренняя правда.",
    "Это бу, я знаю на самом деле.",
    "Так ведь можно свердешный приступ словить",
    "Это бу, я чувствую в моем сердце.",
    "Бу, это моя душевная правда.",
    "Это бу, я чувствую в моей душе.",
    "Бу, это моя истинная природа.",
    "Это бу, я чувствую в моей природе.",
    "Сама ты бу блин",
    "Боже...",
    "Бу, испугался - не бойся, я тебя не обижу",
    "Это бу, я чувствую тебя"
]
starts = [
    "Игра началась",
    "Хорошо, я начну",
    "Да, начнем игру",
    "Да угомонитесь, начинаю..",
    "Начнем",
    "Хорошая идея",
    "Давайте начнем",
    "Что тебе неймется",
    "Начнем сначала",
    "Хорошо, я готов",
    "Давайте начнем игру",
    "Сообщение обнаружено{LShift down}11{LShift up}  Начинаем",
    "Начнем игру",
    "Хорошо, я начну",
    "Да, начнем",
    "Игра начата",
    "Начнем новый раунд",
    "Хорошо, давайте начнем",
    "Давайте начнем игру снова",
    "Ну старт так старт"
]
das = [
    "Что да{Lshift down}7{Lshist up}",
    "Слушаю",
    "Да",
    "Угу"
]

"""
    time1 = time.time()
    for i in range(50):
        mufind("bu4#bu5#bu6#bu7#bu8#startmsg#da1#da2 0.8#0.8#0.8#0.8#0.8#0.8#0.8#0.8", 0, False)
    print((time.time()-time1)/400)
    print((time.time() - time1) / 50)
    exit()
"""


#send("Не мешай мне делать сложные компьютерные вычисления :З{Enter}")
if __name__ == "__main__":
    while True:
        time.sleep(0.8)
        m = mufind("bu4#bu5#bu6#bu7#bu8#startmsg#da1#da2 0.8#0.8#0.8#0.8#0.8#0.8#0.8#0.8", 0, False)
        print(f"found {m}")
        if "bu4" in m or "bu5" in m or "bu6" in m or "bu7" in m or "bu8" in m:
            _chat()
            Enter = "{Enter}"
            print("Boollean")
            ans = random.choice(bus)
            send(f"{ans}{Enter}")
            time.sleep(0.5)
            send("{Esc}")
            time.sleep(4)
        if "startmsg" in m:
            Enter = "{Enter}"
            print("start message detected!")
            ans = random.choice(starts)
            _chat()
            time.sleep(0.1)
            send(f"{ans}{Enter}")
            time.sleep(0.5)
            send("{Esc}")
            time.sleep(0.4)
            if _start()!=True:
                _chat()
                time.sleep(0.5)
                send("Нет доступа! {Enter}")
                time.sleep(0.5)
                send("{Esc}")
            time.sleep(3)
        if "da1" in m or "da2" in m:
            _chat()
            Enter = "{Enter}"
            print("ДА")
            ans = random.choice(das)
            send(f"{ans}{Enter}")
            time.sleep(0.5)
            send("{Esc}")
            time.sleep(3)



        """        
if __name__ == "__main__":
    while True:
        print("trying boo")
        if mufind("bu4#bu5#bu6#bu7#bu8 0.8#0.8#0.8#0.8#0.8", 0, False) == True:
            _chat()
            Enter = "{Enter}"
            print("Boollean")
            ans = random.choice(bus)
            send(f"{ans}{Enter}")
            time.sleep(0.5)
            send("{Esc}")
            time.sleep(3)
        print("trying startmsg")
        if fafind("startmsg", 0.8, False) == True:
            Enter = "{Enter}"
            print("start message detected!")
            ans = random.choice(starts)
            _chat()
            time.sleep(0.1)
            send(f"{ans}{Enter}")
            time.sleep(0.5)
            send("{Esc}")
            time.sleep(0.4)
            _start()
            time.sleep(3)
        print("trying das")
        if mufind("da1#da2 0.8#0.8", 0, False) == True:
            _chat()
            Enter = "{Enter}"
            print("ДА")
            ans = random.choice(das)
            send(f"{ans}{Enter}")
            time.sleep(0.5)
            send("{Esc}")
            time.sleep(3)
"""