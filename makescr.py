import cv2
import tkinter as tk
from tkinter import messagebox
import os
import numpy as np
from PIL import ImageGrab, Image
import time
# Папка для сохранения скриншотов
prefs_dir = 'prefs'

# Проверяем, существует ли папка prefs, если нет - создаем ее
if not os.path.exists(prefs_dir):
    os.makedirs(prefs_dir)

# Функция для создания скриншота
def create_screenshot():
    # Получаем скриншот экрана
    screenshot = ImageGrab.grab()
    screenshot.save(os.path.join(prefs_dir, f'screenshot_{i}.png'))

    # Выводим сообщение об успехе
    print("Успех")
    #messagebox.showinfo('Успех', f'Скриншот сохранен как screenshot_{i}.png')

# Функция для циклического создания скриншотов
def create_screenshots():
    global i
    i = int(input("Номер нового скриншота"))
    while True:
        input()
        create_screenshot()
        i += 1
        # Ждем 2 секунды
        #time.sleep(1)
        #root.after(3000)

# Создаем окно tkinter
root = tk.Tk()
root.withdraw()  # Скрываем окно tkinter

# Создаем цикл для создания скриншотов
create_screenshots()

# Основной цикл tkinter
root.mainloop()