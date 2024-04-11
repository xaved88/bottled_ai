class CustomState:
    attacks_played_this_turn = 0
    extra_ritual_dagger_damage_by_card = dict()


def set_new_game_state():
    CustomState.attacks_played_this_turn = 0
    CustomState.extra_ritual_dagger_damage_by_card.clear()


def set_new_turn_state():
    CustomState.attacks_played_this_turn = 0
