from rs.calculator.enums.card_id import CardId


class CustomState:
    general_global_memory = dict()
    general_global_memory.update({"attacks_this_turn": 0})
    general_global_memory.update({"last_known_turn": 0})
    general_global_memory.update({"claws_played_this_battle": 0})

    extra_ritual_dagger_damage_by_card = dict({str: [CardId, int]})


def set_new_game_state():
    CustomState.extra_ritual_dagger_damage_by_card.clear()
    CustomState.extra_ritual_dagger_damage_by_card.update({"test_uuid_powered_up_ritual_dagger": 3})

    set_new_battle_state()
    set_new_turn_state()


def set_new_battle_state():
    CustomState.general_global_memory.update({"claws_played_this_battle": 0})

    set_new_turn_state()


def set_new_turn_state():
    CustomState.general_global_memory.update({"attacks_this_turn": 0})
    CustomState.general_global_memory.update({"last_known_turn": 0})


