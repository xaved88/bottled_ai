import time
import traceback

from rs.ai.requested_scaling.requested_scaling import REQUESTED_SCALING
from rs.ai.requested_strike.requested_strike import REQUESTED_STRIKE
from rs.ai.shivs_and_giggles.shivs_and_giggles import SHIVS_AND_GIGGLES
from rs.helper.seed import make_random_seed
from rs.api.client import Client
from rs.machine.game import Game
from rs.helper.logger import log, init_log, log_new_run_sequence

take_screenshots = False  # Functionality is disabled on Mac and this value won't change anything.
# If there are run seeds, it will run them. Otherwise, it will use the run amount.
run_seeds = [
   # '10HTDAVER34YR',
]
run_amount = 20
strategy = SHIVS_AND_GIGGLES

if __name__ == "__main__":
    init_log()
    log("Starting up")
    log_new_run_sequence()
    try:
        client = Client()
        game = Game(client, strategy)
        if run_seeds:
            for seed in run_seeds:
                game.start(seed, take_screenshots)
                game.run()
                time.sleep(1)
        else:
            for i in range(run_amount):
                game.start(make_random_seed(), take_screenshots)
                game.run()
                time.sleep(1)

    except Exception as e:
        log("Exception! " + str(e))
        log(traceback.format_exc())
