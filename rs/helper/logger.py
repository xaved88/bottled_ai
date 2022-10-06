import os
import shutil
import sys
from datetime import datetime
from typing import List

from definitions import ROOT_DIR

if not sys.platform.startswith('darwin'):
    import pyautogui

from rs.helper.seed import get_seed_string
from rs.machine.state import GameState


current_run_log_file: str = ''
current_run_log_count: int = 0


def init_run_logging(seed: str):
    dt = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    global current_run_log_file
    global current_run_log_count
    current_run_log_count = 0
    current_run_log_file = "runs/" + dt + "--" + seed
    with open(ROOT_DIR + "/logs/" + current_run_log_file + ".log", 'x') as file:
        file.close()


def log_snapshot(floor: int, command: str):
    global current_run_log_count
    my_screenshot = pyautogui.screenshot()
    my_screenshot.save(
        ROOT_DIR +
        f"/logs/screenshots/Floor_${str(floor).zfill(2)}-cmd_${str(current_run_log_count).zfill(4)}-${command}.jpg")


def log_to_run(message: str):
    if not current_run_log_file:
        return

    global current_run_log_count
    current_run_log_count += 1
    if current_run_log_count > 10000:
        log("Dying due to this seeming to be stuck", current_run_log_file)
        raise Exception("Dying due to this seeming to be stuck...")
    log(message, current_run_log_file)


def log_run_results(state: GameState, elites: List[str], bosses: List[str]):
    message = "Seed:" + get_seed_string(state.game_state()['seed'])
    message += ", Floor:" + str(state.floor())
    message += ", Score:" + str(state.game_state()['screen_state']['score'])
    message += ", DiedTo: "
    for m in state.get_monsters():
        message += m["name"] + ","
    message += " Bosses: " + ",".join(bosses)
    message += " Elites: " + ",".join(elites)
    message += " Relics: "
    for r in state.get_relics():
        message += r["name"] + ","
    message += "\n"
    with open(ROOT_DIR + "/logs/run_history.log", 'a+') as f:
        f.write(message)
        f.close()


def log_new_run_sequence():
    with open(ROOT_DIR + "/logs/run_history.log", 'a+') as f:
        f.write("-------------------------\n")
        f.close()


def log(message, filename="default"):
    f = open(ROOT_DIR + "/logs/" + filename + ".log", "a+")
    f.write(message + "\n")
    f.close()


def init_log(filename="default"):
    with open(ROOT_DIR + "/logs/" + filename + ".log", 'a+') as file:
        file.truncate(0)
        file.close()
    if os.path.exists(ROOT_DIR +"/logs/screenshots"):
        shutil.rmtree(ROOT_DIR +"/logs/screenshots")
    os.makedirs(ROOT_DIR +"/logs/screenshots")
