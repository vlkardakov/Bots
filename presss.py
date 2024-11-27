import subprocess
import time

text1 = input()

def send(text):
    subprocess.run(["press.exe", text])


if __name__ == "__main__":
    time.sleep(2)
    send(text1)