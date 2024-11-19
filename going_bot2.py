from ultralytics import YOLO
import cv2 as cv
import numpy as np
import pyautogui
import subprocess
import time

model = YOLO('Cherry2.pt')
kov1 = "{"
kov2 = "}"

def press_down(key):
    global kov1,kov2
    subprocess.run(["press.exe",f"{kov1}{key} down{kov2}"])
def press_up(key):
    global kov1, kov2
    subprocess.run(["press.exe",f"{kov1}{key} up{kov2}"])
def find_object_with_center():
    screen = pyautogui.screenshot()
    image = np.array(screen)
    image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
    image = cv.resize(image, (640, 380))

    results = model(image)[0]

    if results.boxes is not None and len(results.boxes) > 0:
        # Получаем bounding box
        box = results.boxes[0]

        # Извлекаем координаты
        x1 = int(box.xyxy[0][0])
        y1 = int(box.xyxy[0][1])
        x2 = int(box.xyxy[0][2])
        y2 = int(box.xyxy[0][3])

        # Вычисляем координаты центра
        x_center = int((x1 + x2) / 2)
        y_center = int((y1 + y2) / 2)

        print(f"Центр объекта: ({x_center}, {y_center})")

        result = []
        if abs(320-x_center)<50 and abs(190-y_center):
            print("Слишком близко :з")
            #pet()
            return []
        if x_center>320:
           print(f"Right:{x_center-320}")
           result.append(f"Right:{x_center-320}")
        else:
            print(f"Left:{320-x_center}")
            result.append(f"Left:{320-x_center}")
        if y_center>190:
            print(f"Down:{y_center-190}")
            result.append(f"Down:{y_center-190}")
        else:
            print(f"Up:{190-y_center}")
            result.append(f"Up:{190-y_center}")

        """
        # Optional: отобразить результат на изображении
        cv.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv.circle(image, (x_center, y_center), 5, (0, 0, 255), -1)  # Рисуем точку
        cv.imshow('Detected Object', image)
        cv.waitKey(0)
        cv.destroyAllWindows()"""

        return result

    else:
        print("Нет такого :з")
        #pet()
        return []

input("Подтвердите!")
print("Начинаем")
while True:
    #time.sleep(0.8)
    tabl = find_object_with_center()
    if tabl!=[]:
        press_down(tabl[0].split(":")[0])
        time.sleep(float(tabl[0].split(":")[1])/160)
        press_up(tabl[0].split(":")[0])
        press_down(tabl[1].split(":")[0])
        time.sleep(float(tabl[1].split(":")[1])/160)
        press_up(tabl[1].split(":")[0])
