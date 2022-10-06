import sys
if not sys.platform.startswith('darwin'):
    import pyautogui

print(sys.version, sys.path)
if not sys.platform.startswith('darwin'):
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save('./tmp.jpg')
