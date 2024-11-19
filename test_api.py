import aiohttp
import asyncio
import os
from dotenv import load_dotenv
import requests
import time
load_dotenv()



#os.environ["ngrok_domain"] = "http://flexible-poorly-buck.ngrok-free.app"
ngrok_domain = os.getenv("ngrok_domain")
from memory import *
import json
import time
import numpy as np

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

def pithon(code):
    global result
    try:
        local_vars = {}
        exec(code, {}, local_vars)  # Используем локальный словарь для хранения переменных
        return local_vars.get('result')  # Возвращаем значение переменной result
    except Exception as e:
        return e

def clean_string(s, bads):
    bad_chars = np.array(list(bads))
    return "".join([c for c in s if c not in bad_chars])


def get_response(url):

        # Отправляем GET-запрос к указанному URL
        response = requests.get(url)

        # Проверяем, успешен ли запрос
        response.raise_for_status()  # Это вызовет исключение для ошибок HTTP
        # Возвращаем текст ответа
        return response.text


def gpt_thinks(a,t, do_ans, act):
    start = time.time()
    global result_coding
    data = {
        'a': a,
        't': t,
        'act': act,
        'do_ans':do_ans
    }
    response = requests.post(f'{ngrok_domain}/', data=data)
    response = requests.post(f'{ngrok_domain}/', data=data)
    print(f"ПОЛНЫЙ ОТВЕТ СЕРВЕРА: {response.text}")
    a = pithon(f"result = {response.text}")
    print(type(a))
    end = time.time()
    latency = (end - start) * 1000  # В миллисекундах
    print(f"Задержка нейросети: {latency}")
    if type(a) == "NameError":
        return "OK"
    typ = a[0]
    if typ == "python":
        print("typ  = python detected")
        result_coding = pithon(a[1])
        return None
    else:
        print("Это не код.")
        ret = a[1]
        #print(f"Возвращаем: {a}")
        return ret


#<body class="h-full" id="ngrok">
if __name__ == "__main__":
    while True:
        result_coding = None
        t = input()
        a = gpt_thinks("system", t, True, "Ask")
        if result_coding:
            a = gpt_thinks("SYSTEM", result_coding, True, "Result")
        print(f"ОТВЕТ БОТА: {a}")



