from PIL import ImageGrab, Image
import mss
import cv2 as cv
import numpy as np
from module import *
print("imported")
import webbrowser
from cleancsv import clean
from read import read
import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def get_page_title(session, url):
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.title.string if soup.title else None
            return title.strip() if title else None
    except aiohttp.ClientError as e:
        print(f"Ошибка при запросе ({url}): {e}")
        return None
    except AttributeError:
        print(f"Заголовок не найден на странице ({url}).")
        return None

async def get_page_titles(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [get_page_title(session, url) for url in urls]
        titles = await asyncio.gather(*tasks)
        return titles



def create_screenshot():
    # Получаем скриншот экрана
    screenshot = ImageGrab.grab()
    return screenshot

def go_to(url):
    webbrowser.open(url)

def test():
    # Очищаем от мусора
    clean()

    urls = read()

    urls_and_titles = []

    titles = asyncio.run(get_page_titles(urls))

    for i in range(len(urls)):
        urls_and_titles.append({"url":urls[i], "title":titles[i]})

    #print(urls_and_titles)

if __name__ == "__main__":
    test()
