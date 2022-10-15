import time
import traceback

from rs.controller.controller_window import ControllerWindow
from rs.helper.seed import make_random_seed
from rs.ai.requested_strike.requested_strike import REQUESTED_STRIKE
from rs.api.client import Client
from rs.machine.game import Game
from rs.helper.logger import log, init_log, log_new_run_sequence

take_screenshots = False  # Functionality is disabled on Mac and this value won't change anything
#if there are run seeds, it will run them. Otherwise, it will use the run amount.
run_seeds = [
   # '10HTDAVER34YR',
]
run_amount = 20
use_controller = True

"""
Seeds:
EFI1QKN4EWKB - transform from neow, gets to floor 27 just aggro LTR
24W1XWCFJR2ZC - upgrade from neow, we get entangled in fourth battle or so. First card reward PS + Shockwave.
NMRZXQFDKKHK - gremlin nob as first elite currently, will be a good one for battle specific combat checks...
             - perfected strike sometime before first elite
             - shop 4th room on the left (but path logic avoids it currently)
19M4YWURMXE59 - remove on floor 2, event on floor 2, and sentries as first elite
1SG4LPD7YFUBM - Astrolabe as act1 reward
3RWGR6T3HKE6A - 2 card gen potions to use for act 1 boss, good potion edge case
2AKHVLXU75Q77 - shop floor 2 (with perfected strike)
40KFT3ZZNRPE0 - reached Awakened One on a new account (also picks up snecko)
4WM6CLQ8Y51UU - neow transform into dropkick, also another early dropkick if we wanted it
"""

if __name__ == "__main__":
    init_log()
    log("Starting up")
    log_new_run_sequence()
    controller = ControllerWindow() if use_controller else None
    try:
        client = Client()
        game = Game(client, REQUESTED_STRIKE)
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
