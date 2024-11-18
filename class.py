from ultralytics import YOLO
import cv2
import numpy as np
import pyautogui
from tkinter import messagebox
# Загрузка модели YOLO
model = YOLO('2.pt')
color = (0, 255, 255)


while True:
    input()
    # Сделать скриншот экрана
    screen = pyautogui.screenshot()

    # Преобразовать скриншот в OpenCV изображение
    image = np.array(screen)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Уменьшить размер изображения до размера, требуемого моделью
    image = cv2.resize(image, (640, 640))

    # Обработать скриншот с помощью модели YOLO
    results = model(image)[0]

    names = results.names
    print("Top 1 Class Name : {}".format(names[results.probs.top1]))
    #print("Top 1 Class Accuracy : {:.2f}%".format(results.probs.top1conf.item() * 100))