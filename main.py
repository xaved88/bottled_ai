import traceback

from rs.ai.requested_strike.requested_strike import REQUESTED_STRIKE
from rs.api.client import Client
from rs.machine.game import Game
from rs.helper.logger import log, init_log

if __name__ == "__main__":
    init_log()
    log("Starting up")
    try:
        client = Client()
        game = Game(client, REQUESTED_STRIKE)
        game.start("NMRZXQFDKKHK")
        game.run()
    except Exception as e:
        log("Exception! " + str(e))
        log(traceback.format_exc())

"""
Seeds:
EFI1QKN4EWKB - transform from neow, gets to floor 27 just aggro LTR
24W1XWCFJR2ZC - upgrade from neow, we get entangled in fourth battle or so. First card reward PS + Shockwave.
NMRZXQFDKKHK - ???
"""
