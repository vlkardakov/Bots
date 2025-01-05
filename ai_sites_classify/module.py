import os
import google.generativeai as genai
import os
import numpy as np
from mss import mss
from PIL import Image
import time

api_keys = [
    "AIzaSyAPL9cKR86Aj5nqXsIvD_YWDUZ7E8vEyec", # работает
    "AIzaSyBVpBV7gnTa_XVoCFOcBY4oWRzY0hmGwXQ", # работает
    #"AIzaSyArqyXBQrwXLYg26slozZG1BLnHfRpDEM4",
    #"AIzaSyDj1cDXsTKkC7mMroHhIgg37X6MtqgjUmw",
    "AIzaSyCF4gSrVqI7wqP8jfOdD7V-fDo_TAImflY", # 9
    "AIzaSyDENOL9VDuCYYKsx_GkaYa_7qjrSPgiONM", # 10
    "AIzaSyCfLsRDmgJcgbkVVFGXOzIOd4heFtsvnnM", # mail@vlkardakov.ru
    # "","","","","","","","",""
]

key_index = 0
current_key = api_keys[0]

zaprosi_history = []

def get_next_api_key():
    """Gets the next API key in a circular fashion."""
    global key_index

    key_index = (key_index + 1) % len(api_keys) # Circular increment
    api_key = api_keys[key_index]

    return api_key

def describe(zapros, img):
    global key_index, api_keys, zaprosi_history, current_key

    for i in range(len(zaprosi_history) - 1, -1, -1):
        if zaprosi_history[i]["time"] - time.time() < 60:
            break
        else:
            del zaprosi_history[i]

    if len(zaprosi_history) > 0:
        print("ПЕРЕКЛЮЧАЮСЬ...")
        current_key = get_next_api_key()
        print(f"Переключено на {current_key}")
        zaprosi_history = []

    genai.configure(api_key=current_key)

    model = genai.GenerativeModel('gemini-1.5-flash')

    response = model.generate_content([
        f"запрос пользователя: {zapros}",
        img
    ], stream=True)
    response.resolve()

    zaprosi_history.append({"time":time.time(), "text":response.text})

    return response.text

if __name__ == "__main__":
    while True:
        with mss() as sct:
            mon = sct.monitors[0]
            chat_config = {
                "top": mon["top"] + 87,  # 100px from the top
                "left": mon["left"] + 374,  # 100px from the left
                "width": mon["width"] - 880,  # 2800,  # Исправлено: width вместо what
                "height": 648
            }
        with mss() as sct:
            sct_img = sct.grab(chat_config)
            img_np = np.frombuffer(sct_img.bgra, dtype=np.uint8).reshape(sct_img.height, sct_img.width, 4)
            img_np = img_np[..., :3][:, :, ::-1]  # BGRA -> RGB
            img = Image.fromarray(img_np)
            img = img.resize((320, 180))  # Resize for comparison
        #t = input("::")
        print(describe("Проанализируй изображение и назови программу, в которой был сделан скриншот. Только название.", img))
        print(len(zaprosi_history))