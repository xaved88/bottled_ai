from typing import List

from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState

# Don't actually know the id of most of these...
dont_play_potions = [
    'GamblersBrew',
    'FairyInABottle',
    'SmokeBomb',
    'ElixirPotion',
    'LiquidMemories',
    'SneckoOil'
]


class PotionsBaseHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        # must be implemented by children
        pass

    def handle(self, state: GameState) -> List[str]:
        pot = self.get_potions_to_play(state)[0]
        wait_command = "wait 30"
        if pot['requires_target']:
            return [wait_command, "potion use " + str(pot['idx']) + " 0", wait_command]
        return [wait_command, "potion use " + str(pot['idx']), wait_command]

    def get_potions_to_play(self, state: GameState) -> List[dict]:
        to_play = []
        for idx, pot in enumerate(state.get_potions()):
            if pot['can_use'] and pot['id'] not in dont_play_potions:
                pot['idx'] = idx
                to_play.append(pot)
        return to_play


class PotionsEliteHandler(PotionsBaseHandler):
    def __int__(self):
        super().__init__()

    def can_handle(self, state: GameState) -> bool:
        hp_per = state.get_player_health_percentage() * 100
        return state.has_command(Command.POTION) \
               and state.combat_state() \
               and state.screen_type() == ScreenType.NONE.value \
               and state.game_state()['room_type'] == "MonsterRoomElite" \
               and ((hp_per <= 50 and state.combat_state()['turn'] == 1) or hp_per <= 30) \
               and self.get_potions_to_play(state)


class PotionsBossHandler(PotionsBaseHandler):
    def __int__(self):
        super().__init__()

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.POTION) \
               and state.combat_state() \
               and state.screen_type() == ScreenType.NONE.value \
               and state.game_state()['room_type'] == "MonsterRoomBoss" \
               and state.combat_state()['turn'] == 1 \
               and self.get_potions_to_play(state)
