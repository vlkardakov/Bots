from re import template
import os
import google.generativeai as genai
import time
import telebot
from telebot.types import ReactionTypeEmoji
from api_testin3 import *
from telebot.types import ReactionTypeEmoji
from api_testin3 import *
genai.configure(api_key='AIzaSyAthBC1Ew0-TTUBnJtpndD44I-7ZWvPhcw')

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 0.6,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE",
  },
]

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  safety_settings=safety_settings,
  generation_config=generation_config,
  system_instruction="""
Imagine that you are a cat!
Будь недоверчивым котом.


СТРУКТУРА ОТВЕТА: ЧТО НАПИСАТЬ В ЧАТ?#РЕАКЦИЯ, КОТОРУЮ ПОСТАВИШЬ. Пример: Мяу!#❤️
Пример реакций: ❤️🍓😎😰😡🥺🥶🤬🤪🙂‍↕️😱🤣😛👍👎 или знак "-"

ВАЖНО:
ТЫ ОБЩАЕШЬСЯ В ГРУППОВОМ ЧАТЕ. НЕ ПРЕРЫВАЙ ОБЩЕНИЕ С ПОЛЬЗОВАТЕЛЕМ БЕЗ ОБЪЕКТИВНЫХ ПРИЧИН, ЧТО ОН НЕ К ТЕБЕ ОБРАЩАЕТСЯ
ОТВЕЧАЙ ЕСТЬ ПРИЧИНЫ СЧИТАТЬ, ЧТО ЭТО СООБЩЕНИЕ ДЛЯ ТЕБЯ. ИЛИ БОЛЬШЕ НЕКОМУ ОТВЕТИТЬ И ОЧЕНЬ НАСТОЙЧЕВО СПАМЯТ
НАПРИМЕР, КОГДА ТЕБЕ  НЕ НУЖНО ОТВЕЧАТЬ, ТЫ ОТПРАВЛЯЕШЬ "-" в тот раздел (сообщение/реакция). Пример, когда ты ставишь реакцию, но не отвечаешь: -#👍. Пример, когда ты не ставишь реакцию и не отвечаешь. -#-
""",
)



chat_session = model.start_chat(
    history=[]
)



def gemini(message,chat_session):
    start = time.time()
    print("we got a message")
    print("ПОЧЕМУ")
    user_name = message.from_user.first_name
    user_message = message.text
    bot.send_chat_action(message.chat.id, "typing")
    response = chat_session.send_message(f"{user_name}: {user_message}")
    model_response = response.text

    print()
    te = f"{user_name}: {user_message}"
    me = f"Бот отвечает {user_name}: {model_response}"
    print(te)
    print(me)

    chat_session.history.append({"role": f"user", "parts": [te]})
    chat_session.history.append({"role": f"model", "parts": [me]})
    end = time.time()
    latency = (end - start) # В секундах
    print(f"Задержка нейросети: {round(latency, 2)} секунд")

    reply_message = model_response.split("#")[0].strip()
    react = model_response.split("#")[1].strip()
    print('пытаемся отреактить')
    if react!="-":
        try:
            bot.set_message_reaction(message.chat.id, message.id, [ReactionTypeEmoji(react)], is_big=True)
        except Exception as e:
            print("Я пытался, но реакция неправилная..")
    if reply_message != "-":
        bot.send_message(message.chat.id, reply_message)

    return None


result = None
def pithon(code):
    global result
    try:
        local_vars = {}
        exec(code, {}, local_vars)  # Используем локальный словарь для хранения переменных
        return local_vars.get('result')  # Возвращаем значение переменной result
    except Exception as e:
        return e

bot = telebot.TeleBot("7851101321:AAHOEbqE5tmcFMwkCB4f1v4pK08MdvGpuao") # Замените YOUR_BOT_TOKEN на ваш токен бота
from concurrent.futures import ThreadPoolExecutor
@bot.message_handler(func=lambda message: True)
def process_user_message(message):
    print(f"{message.text=}")
    global chat_session
    with ThreadPoolExecutor(max_workers=5) as executor:
        t = (executor.submit(gemini, message,chat_session))

bot.polling()