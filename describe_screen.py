import google.generativeai as genai
import os
import numpy as np
from mss import mss
from PIL import Image

# НЕ РЕКОМЕНДУЕТСЯ! Используйте переменные окружения
key = 'AIzaSyAPL9cKR86Aj5nqXsIvD_YWDUZ7E8vEyec'  # Замените на ваш ключ
genai.configure(api_key=key)

model = genai.GenerativeModel('gemini-1.5-flash')

chat_session = {
    'history': []
}


def describe(zapros, chat_session2):
    try:
        # Добавляем запрос в историю
        chat_session['history'].append({'user': zapros, 'response': None})

        with mss() as sct:
            monitor = sct.monitors[1]
            sct_img = sct.grab(monitor)
            img_np = np.frombuffer(sct_img.bgra, dtype=np.uint8).reshape(sct_img.height, sct_img.width, 4)
            img_np = img_np[..., :3][:, :, ::-1]  # BGRA -> RGB
            img = Image.fromarray(img_np)
            img = img.resize((1280, 720))

        response = model.generate_content([
            f"запрос пользователя: {zapros} (конец). Если ты видишь чат, то дай для всех сообщений 'автор: сообщение' без каких либо украшений. Если видишь игру - описываешь. Предыдущие запросы: {', '.join([f'Пользователь: {h["user"]}' for h in chat_session["history"]]) if chat_session["history"] else 'Нет предыдущих запросов'}, Описание изображения:",
            img
        ], stream=True)
        response.resolve()

        # Сохраняем ответ в историю
        chat_session['history'][-1]['response'] = response.text
        chat_session2.history.append({"role": "model", "parts":f"description of screenshot: {response.text}"})
        print(response.text)
        return chat_session2
    except Exception as e:
        print(f"Ошибка при генерации контента из изображения: {e}")


response = model.generate_content("The opposite of hot is")
print(response.text)

while True:
    zapros = input("Введите запрос (или 'выход'): ")
    if zapros.lower() == 'выход':
        break
    describe(zapros)