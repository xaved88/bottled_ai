from definitions import ROOT_DIR
from rs.helper.general import can_handle_screenshots

if can_handle_screenshots():
    import pyautogui


def log_snapshot(floor: int, command: str):
    global current_run_log_count
    my_screenshot = pyautogui.screenshot()
    my_screenshot.save(
        ROOT_DIR +
        f"/logs/screenshots/Floor_${str(floor).zfill(2)}-cmd_${str(current_run_log_count).zfill(4)}-${command}.jpg")