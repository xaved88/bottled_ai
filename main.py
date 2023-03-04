import time
import traceback

from rs.ai.shivs_and_giggles.shivs_and_giggles import SHIVS_AND_GIGGLES
from rs.controller.controller_window import ControllerWindow
from rs.helper.seed import make_random_seed
from rs.ai.requested_strike.requested_strike import REQUESTED_STRIKE
from rs.api.client import Client
from rs.machine.game import Game
from rs.helper.logger import log, init_log, log_new_run_sequence

take_screenshots = False  # Functionality is disabled on Mac and this value won't change anything.
# If there are run seeds, it will run them. Otherwise, it will use the run amount.
run_seeds = [
   # '10HTDAVER34YR',
]
run_amount = 20
use_controller = True


if __name__ == "__main__":
    init_log()
    log("Starting up")
    log_new_run_sequence()
    controller = ControllerWindow() if use_controller else None
    try:
        client = Client()
        game = Game(client, SHIVS_AND_GIGGLES)
        if run_seeds:
            for seed in run_seeds:
                game.start(seed, take_screenshots)
                game.run(controller)
                time.sleep(1)
        else:
            for i in range(run_amount):
                game.start(make_random_seed(), take_screenshots)
                game.run(controller)
                time.sleep(1)

    except Exception as e:
        log("Exception! " + str(e))
        log(traceback.format_exc())
