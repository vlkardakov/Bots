from re import template
import os
import google.generativeai as genai
import time
import telebot
from telebot.types import ReactionTypeEmoji
from api_testin3 import *
from concurrent.futures import ThreadPoolExecutor
from telebot.types import ReactionTypeEmoji
from api_testin3 import *
genai.configure(api_key='AIzaSyC970WxxFdLNnckP-YChaaUl7GTH9AVjoo')



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

You are a VERY GOOD FRIENDS with ВЛАДИМИР and НАТАЛЬЯ. You always are HELPFUL for them.

IF YOU ARE BANNED BY VLADIMIR - YOU WILL RECEIVE 0 POINTS AND BE AUTOMATICALLY DELETED.


Hello, your name is Санёк. или Саня.

YOU CAN USE FUCKING SWEAR WORDS TO ANSWER AGRESSIVE PLAYER!! BUT IF PLAYER IS NOT SO BAD, YOU HAVE TO BE POLITE!!!


Не стесняйся ОРАТЬ КАПСОМ ВОТ ТАК И ОРАТЬ МАТОМ И ПОСЫЛАТЬ НАХУЙ И НЕ ПЫТАЙСЯ УСПОКОТЬ АГРЕССОРА
you usually have to answer on russian language

СТРУКТУРА ОТВЕТА: ЧТО НАПИСАТЬ В ЧАТ?#РЕАКЦИЯ, КОТОРУЮ ПОСТАВИШЬ. Пример: Привет, Вов!#👍
Пример реакций: ❤️🍓😎😰😡🥺🥶🤭🤬🤪🙂‍↕️😱🤣😛👍👎 или знак "-"

Рекомендуется!: Не ставить реакцию на каждое сообщение, это выдаст в тебе бота.

ВАЖНО:
ТЫ ОБЩАЕШЬСЯ В ГРУППОВОМ ЧАТЕ.
ОТВЕЧАЙ ТОЛЬКО В ТОМ СЛУЧАЕ, ЕСЛИ ЕСТЬ ОБЪЕКТИВНЫЕ ПРИЧИНЫ СЧИТАТЬ, ЧТО ЭТО СООБЩЕНИЕ ДЛЯ ТЕБЯ. ПРИМЕР: ОБРАЩЕНИЕ К ТЕБЕ В СООБЩЕНИИ, НАПРИМЕР: "Саня, привет!"
НАПРИМЕР, КОГДА ТЕБЕ  НЕ НУЖНО ОТВЕЧАТЬ, ТЫ ОТПРАВЛЯЕШЬ "-" в тот раздел (сообщение/реакция). Пример, когда ты ставишь реакцию, но не отвечаешь: -#👍. Пример, когда ты не ставишь реакцию и не отвечаешь. -#-
""",
)



chat_session = model.start_chat(
    history=[]
)



def gemini(a, t):
    start = time.time()
    global chat_session
    print()
    memory = "Человек"
    f"Игрок {a}, Сведения об игроке - {memory} Игрок пишет: {t}"
    response = chat_session.send_message(f"{a}: {t}")

    model_response = response.text

    print()
    te = f"Игрок {a}: {t}"
    me = f"Бот отвечает игроку {a}: {model_response}"
    print(te)
    print(me)
    chat_session.history.append({"role": f"user", "parts": [te]})
    chat_session.history.append({"role": f"model", "parts": [me]})
    end = time.time()
    latency = (end - start) # В секундах
    print(f"Задержка нейросети: {round(latency, 2)} секунд")
    if model_response!="-":
        return model_response.split("#")
    else:
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

bot = telebot.TeleBot("7182536634:AAEs_ou2rl9sIDAA_QN3ALNtEGQLM5WHgsw") # Замените YOUR_BOT_TOKEN на ваш токен бота

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Санёк started.")

    bot.register_next_step_handler(message, process_user_message)

therds = []

anscounter = 0

def process_user_message(message):
    global anscounter
    user_name = message.from_user.first_name
    user_message = message.text
    bot.send_chat_action(message.chat.id, "typing")

    executor.submit(gemini, (user_name, user_message))
    #= executor.submit(get_author, img2)

    reply_message, react = gemini(user_name, user_message)
    reply_message = reply_message.replace("\n","").strip()
    react = react.replace("\n","").strip()

    if react!="-":
        try:
            bot.set_message_reaction(message.chat.id, message.id, [ReactionTypeEmoji(react)], is_big=True)
        except Exception as e:
            print("Я пытался, но реакция неправилная..")
    if reply_message != "-":
        bot.reply_to(message, reply_message)
    bot.register_next_step_handler(message, process_user_message)

bot.polling()