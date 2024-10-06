import time
import traceback

from rs.ai.claw_is_law.claw_is_law import CLAW_IS_LAW
from rs.ai.observant_heartslayer.observant_heartslayer import OBSERVANT_HEARTSLAYER
from rs.ai.peaceful_pummeling.peaceful_pummeling import PEACEFUL_PUMMELING
from rs.ai.pwnder_my_orbs.pwnder_my_orbs import PWNDER_MY_ORBS
from rs.ai.requested_strike.requested_strike import REQUESTED_STRIKE
from rs.ai.shivs_and_giggles.shivs_and_giggles import SHIVS_AND_GIGGLES
from rs.helper.seed import make_random_seed
from rs.api.client import Client
from rs.machine.game import Game
from rs.helper.logger import log, init_log, log_new_run_sequence

# If there are run seeds, it will run them. Otherwise, it will use the run amount.
run_seeds = [
    'PJXDI7JYG22P',
]
run_amount = 1
strategy = OBSERVANT_HEARTSLAYER

if __name__ == "__main__":
    init_log()
    log("Starting up")
    log_new_run_sequence()
    try:
        client = Client()
        game = Game(client, strategy)
        if run_seeds:
            for seed in run_seeds:
                game.start(seed)
                game.run()
                time.sleep(1)
        else:
            for i in range(run_amount):
                game.start(make_random_seed())
                game.run()
                time.sleep(1)

    except Exception as e:
        log("Exception! " + str(e))
        log(traceback.format_exc())
