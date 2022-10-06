import sys

from rs.helper.general import can_handle_screenshots

if can_handle_screenshots():
    import pyautogui

print(sys.version, sys.path)

if can_handle_screenshots():
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save('./tmp.jpg')
