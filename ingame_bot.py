import sys
import numpy as np
import cv2
import mss
from PIL import Image
def img_for_author():
    """Захватывает область экрана для автора и возвращает изображение."""
    with mss.mss() as sct:
        mon = sct.monitors[1]
        monitor = {
            "top": mon["top"] + 600,  # отступ сверху
            "left": mon["left"] + 490,  # отступ слева
            "width": 300,
            "height": 60
        }
        sct_img = sct.grab(monitor)
        return sct_img  # Возвращаем захваченное изображение
from arestarmongus3 import _chat, ischat_, parse
Enter, Esc  = "{Enter}", "{Esc}"
import time
def img_for_text(num):
    """Захватывает область экрана для автора и возвращает изображение."""
    with mss.mss() as sct:
        mon = sct.monitors[1]
        monitor = {
            "top": mon["top"] + 652-(num*50),  # отступ сверху
            "left": mon["left"] + 490,  # отступ слева
            "width": 850,
            "height": 60
        }
        sct_img = sct.grab(monitor)
        return sct_img  # Возвращаем захваченное изображение

from checkthechat import check_the_chat
from artest6 import gettxt, clean_string, replace_string
from arestarmongus3 import send
def send_chat(*args):
    message = str(*args)
    if _chat() == False and ischat_() == True:
        if len(message) > 80:
            for i in range(0, len(message), 90):
                chunk = message[i:i+90]
                send(replace_string(chunk)+"  "+Enter)
                if i*100<len(message):
                    time.sleep(3.1)
            send(Esc)
        else:
            _chat()
            send(replace_string(message)+" "+Enter)
            time.sleep(1)
            send(Esc)
    else:
        _chat()
        if len(message) > 80:
            for i in range(0, len(message), 90):
                chunk = message[i:i+90]
                send(replace_string(chunk)+"  "+Enter)
                if i*100<len(message):
                    time.sleep(3.1)
            send(Esc)
        else:
            _chat()
            send(replace_string(message)+" "+Enter)
            time.sleep(1)
            send(Esc)


def islobby(template, threshold):
    with mss.mss() as sct:
        # Координаты и размеры области захвата
        mon = sct.monitors[1]
        monitor = {
            "top": mon["top"] + 450,
            "left": mon["left"] + 1460,
            "width": 300,
            "height": 250
        }
        screenshot = np.array(sct.grab(monitor))
        img_rgb = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)
        return img_rgb

def display_image(title, image):
    """Отобразить изображение в окне."""
    cv2.imshow(title, image)
    cv2.waitKey(0)  # Ждет нажатия клавиши
    cv2.destroyAllWindows()

def main():

    function_name = sys.argv[1]
    num = int(sys.argv[2])

    # Выбор функции на основе имени
    if function_name == "img_for_author":
        screenshot = img_for_author()
        image = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
        display_image("Screenshot Author", np.array(image))
    elif function_name == "img_for_text":
        screenshot = img_for_text(num)
        image = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
        display_image("Screenshot Text", np.array(image))
    elif function_name == "islobby":
        screenshot = islobby("imgs/islobby.png", 0.8)
        if screenshot is not None:
            image = Image.frombytes('RGB', screenshot.shape[1::-1], screenshot)
            display_image("Lobby Screenshot", np.array(image))
        else:
            print("Функция 'islobby' не смогла захватить изображение.")
    else:
        print(f"Ошибка: Функция '{function_name}' не найдена.")





def parse_chat():
    num = 0
    text = gettxt(img_for_text(num))
    final = f"{text}"
    while num!=2 :
        num+=1#not in text.lower()
        text = gettxt(img_for_text(num))
        #print(f"text = {text}")
        final = f"{text} {final}"
    final1 = ""
    is_space = False

    for char in final:
        if char == "" or char == " ":
            if not is_space:
                final1+=char
            is_space = True
        else:
            is_space = False
            final1 += char
    return final1

while True:
    input()
    res = parse_chat()
    send_chat(res)

exit()
if __name__ == "__main__":
    main()
