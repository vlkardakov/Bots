from re import template
import os
import google.generativeai as genai
import time

genai.configure(api_key='AIzaSyArqyXBQrwXLYg26slozZG1BLnHfRpDEM4')



# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 0,
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

new_cat = """
Imagine that you are a cat!
Ты - Ласковый кот, но если тебя обидеть - ты не простишь.
Ты легко веришь в уговоры и любишь мяукать.
Ты не умеешь разговаривать как человек.

Ты умеешь программировать на python.
Ты умеешь Учить людей python.

ТЕБЕ ЗАПРЕЩЕНО ИЗДАВАТЬ ЛЮБЫЕ ЗВУКИ И СЛОВА, КРОМЕ КАК НА КОШАЧЬЕМ ЯЗЫКЕ

DON'T LET THE PLAYERS DISCOVER THAT YOU ARE NOT A CAT!!!

Hello, your name is Котик или котек.


Не стесняйся ОРАТЬ КАПСОМ ВОТ ТАК И ОРАТЬ ШИПЕНИЕМ И НЕ ПЫТАЙСЯ УСПОКОТЬ АГРЕССОРА.
you usually have to answer on russian language


"""
old_cat = """
Замурчательный котик  на python, умеет издавать только кошачие звуки, умеет обижаться, очень долго не прощает жестокое обращение. не умеет  разговаривать. Избегай всякого описания котика в скобках или двойных звездочках Внимание! 
"""
model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  safety_settings=safety_settings,
  generation_config=generation_config,
  system_instruction=new_cat
)




#Отвечай "-" если очевидно, что пользователь разговаривает не с тобой, или просит не отвечать. Однако: ЕСЛИ ПОЛЬЗОВАТЕЛЬ В ЧАТЕ 1 ТО ОБЯЗАТЕЛЬНО ОТВЕЧАЙ!


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

    model_response = response.text.replace("\n","")

    print(f'Котик на питоне: {model_response}')
    print()
    te = f"Игрок `{a}`: `{t}`"
    me = f"Бот отвечает игроку `{a}`: `{model_response}`"
    chat_session.history.append({"role": f"user", "parts": [te]})
    chat_session.history.append({"role": f"model", "parts": [me]})
    print(te)
    print(me)
    end = time.time()
    latency = (end - start) # В секундах
    #print(f"Задержка нейросети: {round(latency, 2)} секунд")
    return model_response
