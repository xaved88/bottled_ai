from rs.calculator.enums.card_id import CardId
from rs.calculator.interfaces.memory_items import MemoryItem, ResetSchedule


class TheBotsMemoryBook:
    def __init__(self, memory: dict[MemoryItem, int] = None, memory_by_card: dict[CardId, dict[str, int]] = None):
        self.memory = {} if memory is None else memory
        self.memory_by_card = {} if memory_by_card is None else memory_by_card

    def set_new_game_state(self):
        self.memory_by_card.clear()
        self.initialize_memory_by_card(CardId.RITUAL_DAGGER)
        self.initialize_memory_by_card(CardId.GENETIC_ALGORITHM)

        self.set_new_battle_state()
        self.set_new_turn_state()

    def set_new_battle_state(self):
        self.initialize_memory_by_card(CardId.STEAM_BARRIER)
        self.initialize_memory_by_card(CardId.GLASS_KNIFE)

        self.memory[MemoryItem.CLAWS_PLAYED_THIS_BATTLE] = 0

        self.set_new_turn_state()

    def set_new_turn_state(self):
        self.memory[MemoryItem.ATTACKS_THIS_TURN] = 0
        self.memory[MemoryItem.LAST_KNOWN_TURN] = 0

    def initialize_memory_by_card(self, card_id: CardId):
        self.memory_by_card[card_id] = {"": 0}

    @staticmethod
    def new_default(last_known_turn: int = 0):
        new_memory_book = TheBotsMemoryBook()
        new_memory_book.set_new_game_state()
        new_memory_book.memory[MemoryItem.LAST_KNOWN_TURN] = last_known_turn
        return new_memory_book
