import telebot
import pandas as pd
import time
import os
import io

TOKEN = '7923293677:AAH9l0wC1StMncKbrY1yuVpgP65JR80LWVw'  # Замените на ваш токен
bot = telebot.TeleBot(TOKEN)

import subprocess
from PIL import ImageGrab, Image
import mss
import cv2 as cv
import numpy as np
import datetime
from module import describe
import time
import webbrowser
from cleancsv import clean
from read import read
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from get_domain import get_domain
from save import save

print("imported")


async def get_final_url_base(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, allow_redirects=True) as response:
                response.raise_for_status()  # Проверка на ошибки
                result = response.url
                if isinstance(result, bytes):
                    result = result.decode('utf-8', errors='replace')
                return result
    except aiohttp.ClientError as e:
        print(f"Ошибка при запросе: {e}")
        return None


async def get_final_url(url):  # Замените на ваш URL
    final_url = await get_final_url_base(url)
    if final_url:
        return final_url


async def get_page_title(session, url):
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.title.string if soup.title else None
            return title.strip() if title else None
    except aiohttp.ClientError as e:
        # print(f"Ошибка при запросе ({url}): {e}")
        return None
    except AttributeError:
        # print(f"Заголовок не найден на странице ({url}).")
        return None


async def get_page_titles(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [get_page_title(session, url) for url in urls]
        titles = await asyncio.gather(*tasks)
        return titles


def pithon(code):
    global result
    try:
        local_vars = {}
        exec(code, {}, local_vars)  # Используем локальный словарь для хранения переменных
        return local_vars.get('result')  # Возвращаем значение переменной result
    except Exception as e:
        return e


def save_checked(checked):
    with open("checked_domains.txt", "w") as f:
        f.write(str(checked))


def load_checked():
    with open("checked_domains.txt", "r") as f:
        return pithon(f"result = {f.read()}")


def save_verified(checked):
    with open("verified_domains.txt", "w") as f:
        f.write(str(checked))


def load_verified():
    with open("verified_domains.txt", "r") as f:
        return pithon(f"result = {f.read()}")


def create_screenshot():
    # Получаем скриншот экрана
    screenshot = ImageGrab.grab()
    return screenshot


def go_to(url):
    webbrowser.open(url)


def translate(text):
    return GoogleTranslator(source='auto', target='ru').translate(text)



@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Отправьте таблицу CSV!")

def send(text):
    subprocess.run(["press.exe", text])

stop_processing = False

@bot.message_handler(commands=['stop'])
def stop_processing_command(message):
    global stop_processing
    stop_processing = True
    bot.reply_to(message, "Обработка остановлена. Подождите завершения...")

@bot.message_handler(content_types=['document'])
def handle_document(message):
    global stop_processing
    stop_processing = False
    try:
        os.remove("ОТЧЁТ.csv")
    except:
        pass
    if message.document.mime_type == 'text/csv':
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        #num_rows = len(pd.read_csv(io.StringIO(downloaded_file.decode('utf-8'))))
        with open('1.csv', 'wb') as new_file:
            new_file.write(downloaded_file)

        #bot.reply_to(message, f"Файл успешно сохранён. Обнаружено {num_rows} ссылок. (займет примерно {time.strftime('%H:%M:%S', time.gmtime(num_rows*7))}) Начать обработку? (Да/Нет)")
        bot.reply_to(message, f"Файл успешно сохранён. Начать обработку?")

        # Начинаем ожидание ответа пользователя
        @bot.message_handler(func=lambda message: message.text.lower() in ['да', 'нет'])
        def handle_processing_decision(message):
            global stop_processing
            if message.text.lower() == 'да':
                    #bot.reply_to(message, f"Обработка начата... Я пришлю таблицу меньше чем через {time.strftime('%H:%M:%S', time.gmtime(num_rows*7))}")
                    bot.reply_to(message, f"Обработка начата... ")
                #try:
                    time1 = time.time()
                    from main import test

                    # Очищаем от мусора
                    checked_domains = load_checked()
                    verified_domains = load_verified()
                    clean()
                    scams = []

                    urls = read()

                    bot.reply_to(message, f"Я пришлю таблицу меньше чем через {time.strftime('%H:%M:%S', time.gmtime(len(urls) * 7))}")


                    if True:
                    #try:
                        # if True:
                        go_to(urls[0])
                        time.sleep(5)
                        err_count = 60



                        for i in range(len(urls) - 1):
                            if stop_processing:
                                break

                            try:
                                url = urls[i]
                                current_domain = get_domain(url)
                                # current_final_domain = get_domain(str(asyncio.run(get_final_url(url))))
                                if not (current_domain in checked_domains):  # and not (current_final_domain in checked_domains):
                                    print("OK")
                                    checked_domains.append(current_domain)
                                    print(f"URL сокращения: {current_domain}")
                                    # if current_final_domain:
                                    # print(f"URL финальный: {current_final_domain}")
                                    # checked_domains.append(current_final_domain)

                                    title = asyncio.run(get_page_titles([url]))[0]
                                    print(f"{title=}")

                                    time.sleep(3)

                                    img = create_screenshot()
                                    img.save("tempimg.png")  # Сохраняем скриншот

                                    time.sleep(0.1)
                                    send("{Ctrl down}{w}{Ctrl up}")
                                    go_to(urls[i + 1])
                                    print("translating")
                                    try:
                                        title = translate(title)
                                    except:
                                        pass

                                    prompt = \
                                    fr"""
                                    Ты должен описать, что ты видишь, и считаешь ли, что сайт - мошеннический. Не более 2000 символов!!!
                                    
                                    
                                    Признаки мошеннических сайтов: говорят, что покупатель оплатил товар и просят получить деньги, всякие казино, другие розыгрыши, закос под службы доставки или интернет-магазины. 
                                    Уделя внимание Самому URL адресу, например amazon.s4674.world может выглядеть как сайт amazon, но быть мошенническим.
                                    Так же определяй, что сайт содержит 18+ контент, или например являются сервисами сокращения ссылок (мошенничество и так далее.

                                    типы сайтов: хороший, легитимный (означает, что принадлежит известной компании), мошенничество, казино, 18+
                                    
                                    В ответе выдай (разделительные символы между ЧАСТЯМИ - "::": рассуждения::тип::оценка опасности сайта от 0 до 10 1, целым числом
                                    Пример ответа, кавычки не считаются, "Сайт выглядит как легитимный адрес поисковой системы Google.  Нет никаких подозрительных поддоменов или странных символов в адресе.  Сам сайт отображает стандартную страницу поиска Google, без каких-либо признаков мошенничества, таких как всплывающие окна, подозрительные запросы на оплату или ссылки на азартные игры.  На сайте отсутствует контент 18 ::хороший :: 0"

                                    url и title сайта для проверки, структура url - title: {url} - {title}
                                    """

                                    print("describing")
                                    result = describe(prompt, img).split("::")  # Используем tempimg.png

                                    print(f"{result=}")

                                    print(f"{result[-3]}")
                                    print(f"Тип        : {result[-2]}")
                                    print(f"Опасность  : {result[-1]}")

                                    if "хороший" in result[1]:
                                        pass
                                    elif "легитимный" in result[1]:
                                        verified_domains.append(current_domain)
                                    else:
                                        scams.append(
                                            {"type": result[1], "danger": result[2], "url": url, "thoughts": result[0],
                                             "domain": current_domain, "title": title})

                                        with open("tempimg.png", "rb") as img_file:
                                            try:
                                                bot.send_photo(message.chat.id, img_file, caption=f"""{result[-3]}\n\nТип        : {result[-2]}\nОпасность  : {result[-1]}\nРасчётное время : {time.strftime('%H:%M:%S', time.gmtime((((len(urls) - 1) - i) * 7)))}""".encode('utf-8'))
                                            except:
                                                pass


                                        os.remove("tempimg.png")  # Удаляем изображение

                                else:
                                    print("PASS")
                            except Exception as e:
                                print(f"Ошибка внутри цикла: {e}")
                                save(f"ОТЧЁТ", scams)
                                save_checked(checked_domains)
                                save_verified(verified_domains)
                                err_count -= 1
                                print(f"ПРОИЗОШЛА ОШИБКА, РАБОТА СОХРАНЕНА. ЧТОБЫ СЛОМАТЬ, ЕЩЁ {err_count} ОШИБОК")
                                bot.reply_to(message, f"Ошибка!!! Еще обработок - {err_count}")
                                if err_count < 1:
                                    exit()


                    #except Exception as e:
                        #print(f"Ошибка в основной части: {e}")
                        #pass
                    # now = datetime.datetime.now()
                    # formatted_datetime = now.strftime("%d.%m.%Y %H:%M")
                    print("РАБОТА ОКОНЧЕНА, СОХРАНЕНИЕ")
                    save(f"ОТЧЁТ", scams)
                    save_checked(checked_domains)
                    save_verified(verified_domains)
                    print("ОТКЛЮЧЕНИЕ")

                    time.sleep(4)
                    if os.path.exists('ОТЧЁТ.csv'):
                        with open('ОТЧЁТ.csv', 'rb') as report:
                            bot.send_document(message.chat.id, report, caption=f"Запрос занял {time.time() - time1} секунд")
                            time.sleep(20)
                            os.remove("ОТЧЁТ.csv")
                            bot.reply_to(message,
                                         f"Готов!")
                            #stop_processing = False
                    else:
                        bot.reply_to(message, f"Мошеннических сайтов не обнаружено. Запрос занял {time.time() - time1} секунд")

                #except Exception as e:
                    #bot.reply_to(message, f"Произошла ошибка во время обработки: {e}")
            else:
                bot.reply_to(message, "Обработка отменена.")

    else:
        bot.reply_to(message, "Пожалуйста, отправьте файл .csv")


bot.polling()