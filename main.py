import time
import traceback

from rs.ai.requested_strike.requested_strike import REQUESTED_STRIKE
from rs.api.client import Client
from rs.machine.game import Game
from rs.helper.logger import log, init_log, log_new_run_sequence

take_screenshots = True
use_seeded_runs = False
run_amount = 1
run_seeds = [
    '2V27Y5ZB12TGH',
    '40KFT3ZZNRPE0',
    '3MD3J57AE0AVT',
    '4WM6CLQ8Y51UU',
    '4WU3JG91PXJBV',
    '4QCITNBIE7C0',
    '36QHCLWMGMY6H',
    '1B5P668ENZMAA',
    '4MTB3PBAYK2WA',
    '53BDRGT449DVJ',
]
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
40KFT3ZZNRPE0 - the one where we reached Awakened One (also picks up snecko and busted crown??) <- that last part should be fixed now
4WM6CLQ8Y51UU - neow transform into dropkick, also another early dropkick if we wanted it
2V27Y5ZB12TGH - gambling chip relic
"""

if __name__ == "__main__":
    init_log()
    log("Starting up")
    log_new_run_sequence()
    try:
        client = Client()
        game = Game(client, REQUESTED_STRIKE)
        if use_seeded_runs:
            for seed in run_seeds:
                game.start(seed, take_screenshots)
                game.run()
                time.sleep(1)
        else:
            for i in range(run_amount):
                game.start("", take_screenshots)
                game.run()
                time.sleep(1)

    except Exception as e:
        log("Exception! " + str(e))
        log(traceback.format_exc())
