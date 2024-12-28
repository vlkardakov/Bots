import google.generativeai as genai
import mss
import time
from PIL import Image
import asyncio

# Замените на ваш ключ API
API_KEY = "AIzaSyDj1cDXsTKkC7mMroHhIgg37X6MtqgjUmw"
genai.configure(api_key=API_KEY)

# Настройка модели Gemini (выберите подходящую)
model = genai.GenerativeModel('gemini-pro-vision')

async def capture_screen_and_send():
    with mss.mss() as sct:
        while True:
            # Снимаем скриншот всего экрана
            sct_img = sct.grab(sct.monitors[0])

            # Преобразуем его в PIL Image
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

            # Отправляем кадр в Gemini API (пока как текст, где изображение описывается)
            try:
                response = model.generate_content(
                   [ img, "Опиши, что ты видишь на экране." ]
                )
                print(response.text)
            except Exception as e:
                print(f"Ошибка отправки в Gemini: {e}")


            # Небольшая задержка для контроля скорости
            await asyncio.sleep(0.5)  # Задержка 0.5 секунд

async def main():
    await capture_screen_and_send()

if __name__ == "__main__":
    asyncio.run(main())