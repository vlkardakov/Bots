import cv2 as cv
import numpy as np
import mss
import argparse
import time
import pyautogui

#time.sleep(3)

def find(template, threshold, y, x, target_count):
    with mss.mss() as sct:
        screenshot = np.array(sct.grab(sct.monitors[0]))
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
                # Выполнить клик по центру найденного шаблона
                pyautogui.click(center_x+x, center_y+y)

            count += 1

    # Сохранить снимок экрана с наложенными элементами
    cv.imwrite("screenshot_with_overlays.png", cv.cvtColor(img_rgb, cv.COLOR_RGB2BGR))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Найти что-то и кликнуть по найденному шаблону")
    parser.add_argument("template", help="Шаблон для поиска")
    parser.add_argument("threshold", type=float, help="Пороговый значение")
    parser.add_argument("y", type=int, help="Координата Y")
    parser.add_argument("x", type=int, help="Координата X")
    parser.add_argument("target_count", type=int, help="Номер найденного шаблона, по которому будет выполнен клик")
    args = parser.parse_args()
    find(args.template, args.threshold, args.y, args.x, args.target_count)