import pyautogui
import sys
import time

coord1, coord2 = int(sys.argv[1]), int(sys.argv[2])
pyautogui.FAILSAFE = False
pyautogui.click(coord1, coord2)
time.sleep(0.1)
pyautogui.click(2000, 500)

def click(coord1, coord2):
    # coord1,coord2 = (coord2/720)*1080, (coord1/1280)*1920
    coord1,coord2 = coord2, coord1
    print(f'clicking in: {coord1}, {coord2}')
    pyautogui.click(coord1, coord2)