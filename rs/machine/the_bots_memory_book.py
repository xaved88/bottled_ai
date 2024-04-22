from rs.calculator.enums.card_id import CardId


class TheBotsMemoryBook:

    def __init__(self, memory: dict[str, int] = None, memory_by_card: dict[CardId, dict[str, int]] = None):
        self.memory = {} if memory is None else memory
        self.memory_by_card = {} if memory_by_card is None else memory_by_card # the nested dict is: [uuid, some_useful_number]

    def set_new_game_state(self):
        self.memory_by_card.clear()
        self.memory_by_card[CardId.RITUAL_DAGGER] = {"": 0}
        self.memory_by_card[CardId.GENETIC_ALGORITHM] = {"": 0}

        self.set_new_battle_state()
        self.set_new_turn_state()

    def set_new_battle_state(self):
        self.memory_by_card[CardId.STEAM_BARRIER] = {"": 0}
        self.memory_by_card[CardId.GLASS_KNIFE] = {"": 0}
        self.memory.update({"claws_played_this_battle": 0})

        self.set_new_turn_state()

    def set_new_turn_state(self):
        self.memory.update({"attacks_this_turn": 0})
        self.memory.update({"last_known_turn": 0})

    @staticmethod
    def new_default(last_known_turn: int = 0):
        new_memory_book = TheBotsMemoryBook()
        new_memory_book.set_new_game_state()
        new_memory_book.memory["last_known_turn"] = last_known_turn
        return new_memory_book
