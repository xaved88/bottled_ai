from rs.calculator.enums.card_id import CardId
from rs.calculator.interfaces.memory_items import MemoryItem, ResetSchedule, StanceType


class TheBotsMemoryBook:
    def __init__(self, memory_general: dict = None,
                 memory_by_card: dict[CardId, dict[ResetSchedule, dict[str, int]]] = None):
        self.memory_general = {} if memory_general is None else memory_general
        self.memory_by_card = {} if memory_by_card is None else memory_by_card

    def set_new_game_state(self):
        for card_id in [
            CardId.GENETIC_ALGORITHM,
            CardId.GLASS_KNIFE,
            CardId.PERSEVERANCE,
            CardId.RAMPAGE,
            CardId.RITUAL_DAGGER,
            CardId.STEAM_BARRIER,
            CardId.WINDMILL_STRIKE,
        ]:
            self.initialize_memory_by_card(card_id)

        # Doesn't wipe during run so that we can log the result :D
        self.memory_general[MemoryItem.KILLED_WITH_LESSON_LEARNED] = 0
        self.memory_general[MemoryItem.PLAYED_30_PLUS_CARDS_IN_A_TURN] = 0

        self.set_new_battle_state()
        self.set_new_turn_state()

    def set_new_battle_state(self):
        self.memory_general[MemoryItem.CLAWS_THIS_BATTLE] = 0
        self.memory_general[MemoryItem.FROST_THIS_BATTLE] = 0

        self.memory_general[MemoryItem.LIGHTNING_THIS_BATTLE] = 0
        self.memory_general[MemoryItem.MANTRA_THIS_BATTLE] = 0
        self.memory_general[MemoryItem.PANACHE_DAMAGE] = 0
        self.memory_general[MemoryItem.SAVE_INTERNAL_MANTRA] = 0
        self.memory_general[MemoryItem.STANCE] = StanceType.NO_STANCE
        self.memory_general[MemoryItem.TYPE_LAST_PLAYED] = 0

        # clear memory_by_card based on reset_schedule
        for card_id, schedule_dict in self.memory_by_card.items():
            for reset_schedule in schedule_dict.keys():
                if reset_schedule == ResetSchedule.BATTLE:
                    self.initialize_memory_by_card(card_id)

        self.set_new_turn_state()

    def set_new_turn_state(self):
        self.memory_general[MemoryItem.ATTACKS_THIS_TURN] = 0
        self.memory_general[MemoryItem.CARDS_THIS_TURN] = 0
        self.memory_general[MemoryItem.LAST_KNOWN_TURN] = 0
        self.memory_general[MemoryItem.NECRONOMICON_READY] = 1
        self.memory_general[MemoryItem.ORANGE_PELLETS_ATTACK] = 0
        self.memory_general[MemoryItem.ORANGE_PELLETS_SKILL] = 0
        self.memory_general[MemoryItem.ORANGE_PELLETS_POWER] = 0
        self.memory_general[MemoryItem.PANACHE_COUNTER] = 5
        self.memory_general[MemoryItem.RECYCLE] = 0

    def initialize_memory_by_card(self, card_id: CardId):
        reset_schedule = {}

        match card_id:
            case CardId.GENETIC_ALGORITHM: reset_schedule = ResetSchedule.GAME
            case CardId.GLASS_KNIFE: reset_schedule = ResetSchedule.BATTLE
            case CardId.PERSEVERANCE: reset_schedule = ResetSchedule.BATTLE
            case CardId.RAMPAGE: reset_schedule = ResetSchedule.BATTLE
            case CardId.RITUAL_DAGGER: reset_schedule = ResetSchedule.GAME
            case CardId.STEAM_BARRIER: reset_schedule = ResetSchedule.BATTLE
            case CardId.WINDMILL_STRIKE: reset_schedule = ResetSchedule.BATTLE

        self.memory_by_card[card_id] = {reset_schedule: {"": 0}}

    @staticmethod
    def new_default(last_known_turn: int = 0):
        new_memory_book = TheBotsMemoryBook()
        new_memory_book.set_new_game_state()
        new_memory_book.memory_general[MemoryItem.LAST_KNOWN_TURN] = last_known_turn
        return new_memory_book
