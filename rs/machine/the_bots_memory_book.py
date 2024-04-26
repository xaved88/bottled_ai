from rs.calculator.enums.card_id import CardId
from rs.calculator.interfaces.memory_items import MemoryItem, ResetSchedule


class TheBotsMemoryBook:
    def __init__(self, memory_general: dict[MemoryItem, int] = None,
                 memory_by_card: dict[CardId, dict[ResetSchedule, dict[str, int]]] = None):
        self.memory_general = {} if memory_general is None else memory_general
        self.memory_by_card = {} if memory_by_card is None else memory_by_card

    def set_new_game_state(self):
        for card_id in [
            CardId.GENETIC_ALGORITHM,
            CardId.GLASS_KNIFE,
            CardId.RITUAL_DAGGER,
            CardId.STEAM_BARRIER,
        ]:
            self.initialize_memory_by_card(card_id)

        self.set_new_battle_state()
        self.set_new_turn_state()

    def set_new_battle_state(self):
        self.memory_general[MemoryItem.CLAWS_THIS_BATTLE] = 0

        # clear memory_by_card based on reset_schedule
        for card_id, schedule_dict in self.memory_by_card.items():
            for reset_schedule in schedule_dict.keys():
                if reset_schedule == ResetSchedule.BATTLE:
                    self.initialize_memory_by_card(card_id)

        self.set_new_turn_state()

    def set_new_turn_state(self):
        self.memory_general[MemoryItem.ATTACKS_THIS_TURN] = 0
        self.memory_general[MemoryItem.LAST_KNOWN_TURN] = 0
        self.memory_general[MemoryItem.CARDS_THIS_TURN] = 0

    def initialize_memory_by_card(self, card_id: CardId):
        reset_schedule = {}

        match card_id:
            case CardId.GENETIC_ALGORITHM: reset_schedule = ResetSchedule.GAME
            case CardId.GLASS_KNIFE: reset_schedule = ResetSchedule.BATTLE
            case CardId.RITUAL_DAGGER: reset_schedule = ResetSchedule.GAME
            case CardId.STEAM_BARRIER: reset_schedule = ResetSchedule.BATTLE

        self.memory_by_card[card_id] = {reset_schedule: {"": 0}}

    @staticmethod
    def new_default(last_known_turn: int = 0):
        new_memory_book = TheBotsMemoryBook()
        new_memory_book.set_new_game_state()
        new_memory_book.memory_general[MemoryItem.LAST_KNOWN_TURN] = last_known_turn
        return new_memory_book