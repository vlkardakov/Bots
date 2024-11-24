from re import template
import os
import time
import telebot
from telebot.types import ReactionTypeEmoji
from api_testin3 import *
from telebot.types import ReactionTypeEmoji
from api_testin3 import *
from datetime import datetime
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
load_dotenv()
ngrok_domain = os.getenv("ngrok_domain")

def what_day():
    n = datetime.now().weekday()
    if str(n) == "0":
        return "понедельник"
    elif str(n) == "1":
        return "вторник"
    elif str(n) == "2":
        return "среда"
    elif str(n) == "3":
        return "четверг"
    elif str(n) == "4":
        return "пятница"
    elif str(n) == "5":
        return "суббота"
    elif str(n) == "6":
        return "воскресенье"
    else:
        return "Не удалось посчитать день!"
def get_datetime():
    """Возвращает строку с датой и временем в формате год:месяц:число:часы:минуты."""
    now = datetime.now()
    return now.strftime("%Y:%m:%d:%H:%M")
def gpt_thinks(a,t, do_ans, act):
    start = time.time()
    global result_coding
    print("обозначаем данные")
    data = {
        'a': a,
        't': f"РАСПИСАНИЕ СЕЙЧАС (убрать < и >) - <{load()}>\nСегодня день недели: {what_day()}\nСейчас дата и время: {get_datetime()}\n\nЗапрос пользователя: {t}",
        'act': act,
        'do_ans':do_ans
    }
    print("отправляем запрос")
    response = requests.post(f'{ngrok_domain}/', data=data)
    print(f"ПОЛНЫЙ ОТВЕТ СЕРВЕРА: {response.text}")
    a = pithon(f"result = {response.text}")
    print(f"Размер ответа: {len(response.text)}")
    #print(type(a))
    end = time.time()
    latency = (end - start) * 1000  # В миллисекундах
    print(f"Задержка нейросети: {latency}")
    if do_ans:
        typ = a[0]
        if typ == "python":
            print("typ  = python detected")
            result_coding = pithon(a[1])
            return "Кодирует..."
        elif typ == "OK":
            print("Это игнор(..")
            return "OK"
        elif typ == "send":
            print("Это сообщение!")
            ret = a[1]
            #print(f"Возвращаем: {a}")
            #print(f"{ret=}")
            return ret
    else:
        return response.text.strip()
def load():
    print("Пытаемся прочитать")
    with open("rasp.txt", "r") as f:
        print(f"Содержимое емае: `{str(f.read())}`")
        print("прочитано")
        return str(f.read())

def save(data):
    print("Пытаемся записать")
    with open("rasp.txt", "w") as f:
        f.write(f"{data}")
        print("Записано")
        return True

result = None
def pithon(code):
    global result
    try:
        local_vars = {}
        exec(code, {}, local_vars)  # Используем локальный словарь для хранения переменных
        print(f"""{local_vars.get('result')=}""")
        return local_vars.get('result')  # Возвращаем значение переменной result
    except Exception as e:
        print(f"""{e=}""")
        return e

bot = telebot.TeleBot("7351047568:AAFuwC08mPfbSCHmcD2F3Ua6VYm0nry7f00") # Замените YOUR_BOT_TOKEN на ваш токен бота
from concurrent.futures import ThreadPoolExecutor
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Начинаю работу...")
    bot.register_next_step_handler(message, process_user_message)

def send_chat(message, text):
    chat_id = message.chat.id
    bot.send_message(chat_id, text)

def process_user_message(message):
    print(f"{message.text=}")
    concurrent.futures.ThreadPoolExecutor(max_workers=2).submit(do_most_of_all, message)
    bot.register_next_step_handler(message, process_user_message)

def do_most_of_all(message):
    try:
        a = message.from_user.first_name
        t = message.text
        res = gpt_thinks(a, t, True, "Ask")
        send_chat(message, res)
    except Exception as e:
        print(e)
import concurrent

def proverka():
    while True:
        msg = "a"
        msg.from_user.first_name = "СИСТЕМА ПРОВЕРКИ"
        msg.text = "УЧИТЫВАЯ ВРЕМЯ, РАСПИСАНИЕ И ДИАЛОГ, НАПОМНИ КОМУ НУЖНО КУДА ИДТИ СЕЙЧАС."
        do_most_of_all(msg)
        time.sleep(300)



concurrent.futures.ThreadPoolExecutor(max_workers=7).submit(proverka)

save("Все плохо")
bot.polling()