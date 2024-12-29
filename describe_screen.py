import google.generativeai as genai
import os
import numpy as np
from mss import mss
from PIL import Image

# НЕ РЕКОМЕНДУЕТСЯ! Используйте переменные окружения
#key = 'AIzaSyD5JFHAtqA-vLFJm3NN8uA4vLkqV7kAjOY'   # 1-
key = 'AIzaSyAPL9cKR86Aj5nqXsIvD_YWDUZ7E8vEyec'  # ?
#key = 'AIzaSyBVpBV7gnTa_XVoCFOcBY4oWRzY0hmGwXQ'  # 3
genai.configure(api_key=key)

model = genai.GenerativeModel('gemini-1.5-flash')

chat_session = {
    'history': []
}


def describe(zapros):
        # Добавляем запрос в историю
        #chat_session['history'].append({'user': zapros, 'response': None})

        with mss() as sct:
            mon = sct.monitors[0]
            monitor = {
                "top": mon["top"] + 87,  # 100px from the top
                "left": mon["left"] + 374,  # 100px from the left
                "width": mon["width"] - 880, #2800,  # Исправлено: width вместо what
                "height": 648
            }
            sct_img = sct.grab(monitor)
            img_np = np.frombuffer(sct_img.bgra, dtype=np.uint8).reshape(sct_img.height, sct_img.width, 4)
            img_np = img_np[..., :3][:, :, ::-1]  # BGRA -> RGB
            img = Image.fromarray(img_np)
            img = img.resize((320, 180))
            #img.show()

        response = model.generate_content([
            f"запрос пользователя: {zapros}",
            img
        ], stream=True)
        response.resolve()

        # Сохраняем ответ в историю
        #chat_session['history'][-1]['response'] = response.text
        #chat_session2.history.append({"role": "model", "parts":f"description of screenshot: {response.text}"})

        return response.text