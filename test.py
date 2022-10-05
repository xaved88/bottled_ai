import sys
import pyautogui

print(sys.version, sys.path)
myScreenshot = pyautogui.screenshot()
myScreenshot.save('./tmp.jpg')
