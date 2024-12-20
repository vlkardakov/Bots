from arestarmongus3 import fafind
import time
import subprocess
time.sleep(4)
def send(text):
    subprocess.run(["press.exe", text])

while True:
    time.sleep(3)

    if fafind("phone_lock", 0.8, True):
        print(1)
        time.sleep(1)
        if fafind("phone_lock2", 0.8, True):
            time.sleep(0.5)
            send("ВИТЯ ЛОХ")
            print(2)
            time.sleep(1.5)
            if fafind("phone_lock3", 0.8, True):
                print(3)
                time.sleep(1)
    print(0)

