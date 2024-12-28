import pyautogui
import sys
import time

coord1, coord2 = int(sys.argv[1]), int(sys.argv[2])

pyautogui.click(coord1, coord2)
time.sleep(0.1)
pyautogui.click(2000, 500)