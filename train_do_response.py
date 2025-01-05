from bs4 import BeautifulSoup
import requests

url = "https://hi-tech.mail.ru/news/119682-gigachat-uchastvuet-v-pryamoj-translyacii-s-putinym/"
response = requests.get(url)
soup = BeautifulSoup(response.content, features="lxml")

# Исправленное имя класса - проверьте HTML-исходник, чтобы получить правильное имя
parent = soup.find("div", class_="cab580ccd6") # Скопируйте имя класса из исходного кода!
if parent:
    kid = parent.find("div")
    if kid:
        kid3 = kid.find("p")
        if kid3:
            print(kid3.get_text(strip=True))
        else:
            print("Тег <p> не найден.")
    else:
        print("Дочерний элемент <div> не найден.")
else:
    print("Элемент <div> с указанным классом не найден.")