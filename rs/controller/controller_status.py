from rs.machine.state import GameState


class ControllerStatus:
    def __init__(self):
        self.run_monster = True
        self.run_elite = True
        self.run_boss = True
        self.run_shop = True
        self.run_rest = True
        self.run_event = True
        self.is_paused = False
        self.is_aborted = False

    def should_pause(self, state: GameState) -> bool:
        if self.is_paused:
            return True
        if not self.run_monster and state.game_state()['room_type'] == "MonsterRoom":
            return True
        if not self.run_elite and state.game_state()['room_type'] == "MonsterRoomElite":
            return True
        if not self.run_boss and state.game_state()['room_type'] == "MonsterRoomBoss":
            return True
        if not self.run_shop and state.game_state()['room_type'] == "ShopRoom":
            return True
        if not self.run_rest and state.game_state()['room_type'] == "RestRoom":
            return True
        if not self.run_event and state.game_state()['room_type'] == "EventRoom":
            return True
        return False