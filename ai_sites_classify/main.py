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
                return response.url
    except aiohttp.ClientError as e:
        print(f"Ошибка при запросе: {e}")
        return None

async def get_final_url(url): # Замените на ваш URL
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
        #print(f"Ошибка при запросе ({url}): {e}")
        return None
    except AttributeError:
        #print(f"Заголовок не найден на странице ({url}).")
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

def test():
    # Очищаем от мусора
    checked_domains = load_checked()
    verified_domains = load_verified()
    clean()
    scams = []

    urls = read()
    try:
    #if True:
        go_to(urls[0])
        time.sleep(5)
        err_count = 20
        for i in range(len(urls)-1):
            try:
                url = urls[i]
                current_domain = get_domain(url)
                #current_final_domain = get_domain(str(asyncio.run(get_final_url(url))))
                if not (current_domain in checked_domains): # and not (current_final_domain in checked_domains):
                    print("OK")
                    checked_domains.append(current_domain)
                    print(f"URL сокращения: {current_domain}")
                    #if current_final_domain:
                        #print(f"URL финальный: {current_final_domain}")
                        #checked_domains.append(current_final_domain)

                    title = asyncio.run(get_page_titles([url]))[0]
                    print(f"{title=}")

                    time.sleep(3)

                    img = create_screenshot()
                    time.sleep(0.1)
                    go_to(urls[i+1])
                    try:
                        title = translate(title)
                    except:
                        pass

                    prompt = \
                    f"""
                    Ты должен описать, что ты видишь, и считаешь ли, что сайт - мошеннический.
    
                    Признаки мошеннических сайтов: говорят, что покупатель оплатил товар и просят получить деньги, всякие казино, другие розыгрыши, закос под службы доставки или интернет-магазины. 
                    Уделя внимание Самому URL адресу, например amazon.s4674.world может выглядеть как сайт amazon, но быть мошенническим.
                    Так же определяй, что сайт содержит 18+ контент, или например являются сервисами сокращения ссылок (мошенничество и так далее.
    
                    типы сайтов (): хороший, легитимный (означает, что принадлежит известной компании, например - x.com и другие. Таких много.), мошенничество, казино, 18+
    
                    В ответе выдай: твои рассуждения:%:тип:%:оценка опасности сайта от 0 до 10 1, 1 целым числом
                    Пример ответа, кавычки не считаются, "Сайт выглядит как легитимный адрес поисковой системы Google.  Нет никаких подозрительных поддоменов или странных символов в адресе.  Сам сайт отображает стандартную страницу поиска Google, без каких-либо признаков мошенничества, таких как всплывающие окна, подозрительные запросы на оплату или ссылки на азартные игры.  На сайте отсутствует контент 18+.:%:хороший:%:0"
                    
                    url и title сайта для проверки, структура url - title: {url} - {title}
                    """

                    print("describing")
                    result = describe(prompt, img).split(":%:")

                    print(f"Рассуждения: {result[-3]}")
                    print(f"Тип        : {result[-2]}")
                    print(f"Опасность  : {result[-1]}")

                    if "хороший" in result[1]:
                        pass
                    elif "легитимный" in result[1]:
                        verified_domains.append(current_domain)
                    else:
                        scams.append({"type":result[1], "danger": result[2], "url": url, "thoughts": result[0], "domain":current_domain, "title":title})
                else:
                    print("PASS")
            except:
                save(f"ОТЧЁТ", scams)
                save_checked(checked_domains)
                save_verified(verified_domains)
                err_count -= 1
                print(f"ПРОИЗОШЛА ОШИБКА, РАБОТА СОХРАНЕНА. ЧТОБЫ СЛОМАТЬ, ЕЩЁ {err_count} ОШИБОК")
                if err_count < 1:
                    exit()


    except:
        pass
    #now = datetime.datetime.now()
    #formatted_datetime = now.strftime("%d.%m.%Y %H:%M")
    print("РАБОТА ОКОНЧЕНА, СОХРАНЕНИЕ")
    save(f"ОТЧЁТ", scams)
    save_checked(checked_domains)
    save_verified(verified_domains)
    print("ОТКЛЮЧЕНИЕ")


if __name__ == "__main__":
    test()
