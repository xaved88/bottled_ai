from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.handlers.handler_action import HandlerAction
from rs.machine.state import GameState


class DefaultPlayHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.PLAY)

    def handle(self, state: GameState, slay_heart: bool) -> HandlerAction:
        hand = state.hand
        energy = state.get_player_combat()["energy"]
        card_to_play = next(card for card in hand.cards if card.cost <= energy)
        card_index = hand.cards.index(card_to_play)
        command = "play " + str(card_index + 1)
        if card_to_play.has_target:
            monsters = state.get_monsters()
            target = next(monster for monster in monsters if not monster['is_gone'])
            command += " " + str(monsters.index(target))

        return HandlerAction(commands=[command])
