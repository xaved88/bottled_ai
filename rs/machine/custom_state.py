from rs.calculator.enums.card_id import CardId


class CustomState:
    general_global_memory = dict()
    memory_by_card: dict[CardId, dict] = {}


def set_new_game_state():
    CustomState.memory_by_card.clear()
    CustomState.memory_by_card.update({CardId.RITUAL_DAGGER: {"": 0}})
    CustomState.memory_by_card[CardId.RITUAL_DAGGER] = {"test_uuid_powered_up_ritual_dagger": 3}  # for test

    set_new_battle_state()
    set_new_turn_state()


def set_new_battle_state():
    CustomState.general_global_memory.update({"claws_played_this_battle": 0})

    set_new_turn_state()


def set_new_turn_state():
    CustomState.general_global_memory.update({"attacks_this_turn": 0})
    CustomState.general_global_memory.update({"last_known_turn": 0})


