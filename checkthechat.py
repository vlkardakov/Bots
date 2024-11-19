import pytesseract
from PIL import Image
import mss
import cv2 as cv
import numpy as np
import random
import os
from dotenv import load_dotenv
monum = int(os.getenv("monitor"))
def find_news(template, threshold, y, x, target_count, do_click):
    with mss.mss() as sct:
        mon = sct.monitors[monum]
        monitor = {
            "top": mon["top"] + 2,  # 100px from the top
            "left": mon["left"] + 1486,  # 100px from the left
            "width": 60,
            "height": 60
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

def check_the_chat():
    return find_news("imgs/news.png", 0.8, 0, 0, 1, False)
