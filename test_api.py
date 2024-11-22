import aiohttp
import asyncio
import socketio
import os
from dotenv import load_dotenv
import requests
load_dotenv()

ngrok_domain = os.getenv("ngrok_domain")

#os.environ["ngrok_domain"] = "http://flexible-poorly-buck.ngrok-free.app"


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
            return None
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

def send_chat(text):
    print(f"ВЫВОДИМ: {text}")

free_time= time.time()

def do_most_of_all(a,t):
    #print("запуск мультипоточного менеджмента)")
    global result_coding
    global free_time
    try:
        print("Пытаемся!")
        if result_coding:
            res = gpt_thinks("SYSTEM", result_coding, True, "Result")
            now_time= time.time()

            while free_time > now_time:
                print("Обновляем время")
                now_time = time.time()
            free_time = time.time() + 3
            send_chat(res)
            free_time = time.time() + 3
            result_coding = None
        else:
            res = gpt_thinks(a, t, True, "Ask")
            now_time = time.time()
            while free_time > now_time:
                print("Обновляем время")
                now_time = time.time()
            free_time = time.time() + 3
            send_chat(res)
            free_time = time.time() + 3

    except Exception as e:
        print(e)
import concurrent

if __name__ == "__main__":
    while True:

        result_coding = None
        t = input()
        concurrent.futures.ThreadPoolExecutor(max_workers=2).submit(do_most_of_all("Кот",t))

        if result_coding:
            concurrent.futures.ThreadPoolExecutor(max_workers=2).submit(do_most_of_all("SYSTEM",result_coding))




