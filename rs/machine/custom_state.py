class CustomState:
    attacks_played_this_turn = 0
    extra_ritual_dagger_damage = 0

    def new_turn_state(self):
        CustomState.attacks_played_this_turn = 0

    def new_game_state(self):
        CustomState.attacks_played_this_turn = 0
        CustomState.extra_ritual_dagger_damage = 0
