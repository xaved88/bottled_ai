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
State for when a round is finished and we're ready to start a new one:
#{"available_commands":["start","state"],"ready_for_command":true,"in_game":false}


Seeds:
EFI1QKN4EWKB - transform from neow, gets to floor 27 just aggro LTR
24W1XWCFJR2ZC - upgrade from neow, we get entangled in fourth battle or so. First card reward PS + Shockwave.
NMRZXQFDKKHK - gremlin nob as first elite currently, will be a good one for battle specific combat checks...
             - perfected strike sometime before first elite
             - shop 4th room on the left (but path logic avoids it currently)
19M4YWURMXE59 - remove on floor 2, event on floor 2, and sentries as first elite
"""
