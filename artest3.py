import pytesseract
from PIL import Image
import mss
import cv2 as cv
import numpy as np
import time
from time import sleep
from ultralytics import YOLO
from concurrent.futures import ThreadPoolExecutor
from arestarmongus3 import send, _chat, what_step
from g4f.client import Client

model = YOLO('3.pt')
chat_updatesval = "None"
Enter = "{Enter}"
from checkthechat import check_the_chat
client = Client()
total_msgs = [{"role": "system", "content": "ОСНОВНАЯ ИНСТРУКЦИЯ: Твое имя BOT-01, в ответе ты должен ответить на вопросы из списка (до 100 символов), добавить знак # и выдать новый список памяти (то, что ты получил) без наважных сообщений. У меня не будет возможности проконтролировать твою работу."}]

def gettxt(sct_img):
    image = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
    text = pytesseract.image_to_string(image, lang="rus")
    strings = text.split("\n")
    text = ""
    for el in strings:
        text+=f"{el} "
    text = clean_string(text, "<>[]|")
    #print(f"Текст - {text}")
    return text
def img_for_author():
    with mss.mss() as sct:
        # Координаты и размеры области захвата
        mon = sct.monitors[1]
        monitor = {
            "top": mon["top"] + 31,  # 100px from the top
            "left": mon["left"] + 259,  # 100px from the left
            "width": 200,
            "height": 110
        }
        # Grab the data
        sct_img = sct.grab(monitor)
        return sct_img
def img_for_text():
    with mss.mss() as sct:
        # Координаты и размеры области захвата
        mon = sct.monitors[1]
        monitor = {
            "top": mon["top"] + 38,  # 100px from the top
            "left": mon["left"] + 585,  # 100px from the left
            "width": 800,
            "height": 103
        }
        sct_img = sct.grab(monitor)
        # Сохраняем скриншот в файл
        img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
        filename = "screenshot.png"
        img.save(filename)
        return sct_img
def get_author(sct_img):
    image = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
    author = pytesseract.image_to_string(image, lang="+rus+eng")
    print(f"""Автор: {author.split("\n")}""")
    author = author.split("\n")[0]
    author = clean_string(author, """<>[]/|:,.;`'""")

    print(f"""Автор: {author}""")
    if "Cherry" in author: author+=f" (Префикс мяу)"
    return author
def clean_string(s, bads):
    bad_chars = np.array(list(bads))
    return "".join([c for c in s if c not in bad_chars])
def islobby(template, threshold):
    with mss.mss() as sct:
        # Координаты и размеры области захвата
        mon = sct.monitors[1]
        monitor = {
            "top": mon["top"] + 450,  # 100px from the top
            "left": mon["left"] + 1460,  # 100px from the left
            "width": 300,
            "height": 250
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
def is_lobby():
    return islobby("imgs/islobby.png", 0.8)
def fast_data():
    with ThreadPoolExecutor(max_workers=4) as executor:
        print("Задаем потоки..")
        img1 = img_for_text()
        img2 = img_for_author()
        futuretext = executor.submit(gettxt, img1)
        futureauthor = executor.submit(get_author, img2)
        text, author = futuretext.result(), futureauthor.result()
        return text, author
free_time = float(time.time())
Esc = "{Esc}"
def send_chat(*args):
    global free_time
    if free_time < float(time.time()):
        _chat()
        send(str(*args)+"{Esc}")
    else:
        realtime = time.time()
        while free_time > realtime:
            realtime = float(time.time())
            time.sleep(0.5)

        _chat()
        free_time = time.time()+2.5
        send(str(*args)+"{Esc}")
        time.sleep(0.8)
recent_msgs = []
import random
journal = []
def main():
    global recent_msgs
    while True:
        for i in range(10):
            if is_lobby():
                chat_result = check_the_chat()
                while chat_result == None:
                    print(f"chatres {chat_result}")
                    # print("fast data")
                    chat_result = check_the_chat()
                    time.sleep(0.5)
                print("получаем данные..")
                text, author = fast_data()
                print(f"Текст, автор - {text} {author}")
                print("проверим далее на нулевость")
                if text != (""or" ") and author != "":
                    send_chat(f"""Уважаемый {author}, Вы написали: {text.split("\n")[0]}{Enter}""")
                    print("Далее  проверяем на наличие новых данных #и нахождение вне чата.")
                    print(f"chatres {chat_result}")
                else: print("Что-то пустое.")
            else:
                time.sleep(0.5)
                send(Esc)


def get_ans(total_msgs):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=total_msgs,
        # Add any other necessary parameters
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content


if __name__ == "__main__":
    #send_chat("Вас приветствует BOT 01. Я могу повторить почти любые слова из чата.     {Enter}")
    main()