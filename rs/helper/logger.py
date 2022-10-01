from datetime import datetime

from rs.helper.seed import get_seed_string
from rs.machine.state import GameState

ROOT_DIR = "./ai/requested_strike"

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


def log_to_run(message: str):
    if not current_run_log_file:
        return

    global current_run_log_count
    current_run_log_count += 1
    if current_run_log_count > 20000:
        log("Dying due to this seeming to be stuck", current_run_log_file)
        raise Exception("Dying due to this seeming to be stuck...")
    log(message, current_run_log_file)


def log_run_results(state: GameState):
    message = "Seed:" + get_seed_string(state.game_state()['seed'])
    message += ", Floor:" + str(state.floor())
    message += ", Score:" + str(state.game_state()['screen_state']['score'])
    message += ", Monsters: "
    for m in state.get_monsters():
        message += m["name"]
    with open(ROOT_DIR + "/logs/run_history.log", 'a+') as f:
        f.write(message)
        f.close()


def log(message, filename="default"):
    f = open(ROOT_DIR + "/logs/" + filename + ".log", "a")
    f.write(message + "\n")
    f.close()


def init_log(filename="default"):
    with open(ROOT_DIR + "/logs/" + filename + ".log", 'r+') as file:
        file.truncate(0)
        file.close()
