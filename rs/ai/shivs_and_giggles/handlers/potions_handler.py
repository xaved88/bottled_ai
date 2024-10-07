from typing import List

from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.handlers.handler_action import HandlerAction
from rs.machine.state import GameState

# see also common_combat_reward_handler.py for discarding potions
# these potions might still sneak into our slots with entropric brew
dont_play_potions = [
    'Smoke Bomb',
    'Elixir Potion',
    'Liquid Memories',
    'Snecko Oil',
]


class PotionsBaseHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        # must be implemented by children
        pass

    def handle(self, state: GameState, slay_heart: bool) -> HandlerAction:
        pot = self.get_potions_to_play(state)[0]
        wait_command = "wait 30"
        if pot['requires_target']:
            target = 0
            for m_index, monster in enumerate(state.get_monsters()):  # Find the back-est monster that isn't dead
                if monster['name'] == 'Reptomancer':  # Special case since he might not be in the back
                    target = m_index
                    break
                if not monster['is_gone']:
                    target = m_index
            return HandlerAction(
                commands=[wait_command, "potion use " + str(pot['idx']) + " " + str(target), wait_command])
        return HandlerAction(commands=[wait_command, "potion use " + str(pot['idx']), wait_command])

    def get_potions_to_play(self, state: GameState) -> List[dict]:
        to_play = []
        for idx, pot in enumerate(state.get_potions()):
            if pot['can_use'] and pot['name'] not in dont_play_potions:
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
            and (hp_per <= 50 and state.combat_state()['turn'] == 1) \
            and self.get_potions_to_play(state)


class PotionsEventFightHandler(PotionsBaseHandler):  # Treat most Event Fights like Elites
    def __int__(self):
        super().__init__()

    def can_handle(self, state: GameState) -> bool:
        hp_per = state.get_player_health_percentage() * 100
        return state.has_command(Command.POTION) \
            and state.combat_state() \
            and state.screen_type() == ScreenType.NONE.value \
            and state.game_state()['room_type'] == "EventRoom" \
            and not state.has_monster("Fungi Beast") \
            and (hp_per <= 50 and state.combat_state()['turn'] == 1) \
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
