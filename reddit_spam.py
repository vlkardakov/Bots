from arestarmongus3 import fafind
import time
import subprocess
from random import choice
time.sleep(4)
def send(text):
    subprocess.run(["press.exe", text])

counter = int(input()) - 1

chars = ['b','m','d','l','k','t','p','g']
ochars = ['o','e','a','u']

while True:
    time.sleep(15)
    if fafind("reddit_add_comment", 0.8, True):
        word = f"{choice(chars)}{choice(ochars)}{choice(chars)}"
        counter += 1
        print(1)
        #time.sleep(0.)
        send(f"""Комментарий номер {counter} уже здесь.
I am a {word}, this action was performed automatically.""")
        time.sleep(1.5)
        fafind("reddit_send_comment", 0.8, True)
    else:
        print(0)
        fafind("reddit_send_comment", 0.9, True)



