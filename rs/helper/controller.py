from enum import Enum
from time import sleep

from definitions import ROOT_DIR
from rs.helper.logger import log_to_run
from rs.machine.state import GameState


class ControllerCommand(Enum):
    ABORT = 0,
    PAUSE = 1,
    CONTINUE = 2


def get_controller_command(state: GameState) -> ControllerCommand:
    with open(ROOT_DIR + "/run_controller.txt", 'r') as file:
        lines = file.readlines()
        file.close()

    if "[x]" in lines[0]:
        return ControllerCommand.ABORT
    elif "[x]" in lines[1]:
        return ControllerCommand.PAUSE
    elif "[x]" in lines[3]:
        pause_floor = int(lines[4])
        if state.game_state()['floor'] == pause_floor:
            return ControllerCommand.PAUSE
    return ControllerCommand.CONTINUE


def await_controller(state: GameState):
    controller_command = get_controller_command(state)
    if controller_command == ControllerCommand.ABORT:
        log_to_run("Aborting run through controller")
        raise Exception("Let me out!")
    while controller_command == ControllerCommand.PAUSE:
        sleep(1)
        controller_command = get_controller_command(state)
