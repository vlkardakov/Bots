import pyautogui
import time

def swipe_card():
    pyautogui.click(800, 800)
    time.sleep(0.5)
    pyautogui.moveTo(700, 450)
    pyautogui.drag(800,0,duration=1.5)


swipe_card()