from enum import Enum
from time import sleep

from rs.helper.logger import log_to_run

ROOT_DIR = "./ai/requested_strike"


class ControllerCommand(Enum):
    ABORT = 0,
    PAUSE = 1,
    CONTINUE = 2


def get_controller_command() -> ControllerCommand:
    with open(ROOT_DIR + "/run_controller.txt", 'r') as file:
        lines = file.readlines()
        file.close()

    if "[x]" in lines[0]:
        return ControllerCommand.ABORT
    elif "[x]" in lines[1]:
        return ControllerCommand.PAUSE
    return ControllerCommand.CONTINUE


def await_controller():
    controller_command = get_controller_command()
    if controller_command == ControllerCommand.ABORT:
        log_to_run("Aborting run through controller")
        raise Exception("Let me out!")
    while controller_command == ControllerCommand.PAUSE:
        sleep(1)
        controller_command = get_controller_command()
