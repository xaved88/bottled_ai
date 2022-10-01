import time
import traceback

from rs.ai.requested_strike.requested_strike import REQUESTED_STRIKE
from rs.api.client import Client
from rs.machine.game import Game
from rs.helper.logger import log, init_log

# NOTE -> now it will keep running even when you abandon if there are more seeds/runs left, so you'll need to force your way out.
use_seeded_runs = False
run_amount = 10
run_seeds = ['NMRZXQFDKKHK']

"""
Seeds:
EFI1QKN4EWKB - transform from neow, gets to floor 27 just aggro LTR
24W1XWCFJR2ZC - upgrade from neow, we get entangled in fourth battle or so. First card reward PS + Shockwave.
NMRZXQFDKKHK - gremlin nob as first elite currently, will be a good one for battle specific combat checks...
             - perfected strike sometime before first elite
             - shop 4th room on the left (but path logic avoids it currently)
19M4YWURMXE59 - remove on floor 2, event on floor 2, and sentries as first elite
"""

if __name__ == "__main__":
    init_log()
    log("Starting up")
    try:
        client = Client()
        game = Game(client, REQUESTED_STRIKE)
        if use_seeded_runs:
            for seed in run_seeds:
                game.start(seed)
                game.run()
                time.sleep(1)
        else:
            for i in range(run_amount):
                game.start()
                game.run()
                time.sleep(1)

    except Exception as e:
        log("Exception! " + str(e))
        log(traceback.format_exc())
