import cv2 as cv
import numpy as np
import mss
import argparse
import time
import pyautogui

def swipe(start_x, start_y, end_x, end_y, button='left', steps=10, duration=0.5):
    """Simulates a swipe with a mouse button press."""
    pyautogui.moveTo(start_x, start_y)
    pyautogui.mouseDown(button=button)
    pyautogui.moveTo(end_x, end_y)
    pyautogui.mouseUp(button=button)

def find(template, threshold, y, x, target_count):
    with mss.mss() as sct:
        screenshot = np.array(sct.grab(sct.monitors[0]))
        img_rgb = cv.cvtColor(screenshot, cv.COLOR_BGR2RGB)
        img_gray = cv.cvtColor(img_rgb, cv.COLOR_RGB2GRAY)

    template = f"imgs_tasks/{template}.png"
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
                # Выполнить клик по центру найденного шаблона
                return center_x + x, center_y + y

            count += 1



def fafind(template):
    return find(template,0.8, 0, -15,1)


def do_provoda():
    colors = ["red","yellow","blue","pink"]
    #results = fafind(colors)
    pyautogui.click(fafind("red1")[0],fafind("red1")[1])
    for color in colors:
        exec(f"""swipe(fafind("{color}1")[0],fafind("{color}1")[1],fafind("{color}2")[0],fafind("{color}2")[1])""")
    return None