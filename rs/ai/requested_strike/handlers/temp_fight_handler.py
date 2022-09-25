from rs.game.card import CardType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


# Just for doing random things that we want at specific places
class TempFightHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.PLAY)

    def handle(self, state: GameState) -> str:
        hand = state.hand
        energy = state.get_player_combat()["energy"]
        card_to_play = next((card for card in hand.cards if card.cost <= energy and card.type == CardType.ATTACK), None)
        if not card_to_play or state.player_entangled():
            card_to_play = next(card for card in hand.cards if card.cost <= energy and card.type != CardType.ATTACK)
        card_index = hand.cards.index(card_to_play)
        command = "play " + str(card_index + 1)
        if card_to_play.has_target:
            monsters = state.get_monsters()
            target = next(monster for monster in monsters if not monster['is_gone'])
            command += " " + str(monsters.index(target))

        return command
