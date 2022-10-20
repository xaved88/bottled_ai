from rs.calculator.hand_state import HandState
from rs.calculator.powers import PowerId


class SbcComparator:  # Abstract class, just for signature for the kiddos.
    def does_best_remain_the_best(self, best: HandState, challenger: HandState, original: HandState) -> bool:
        return True


class DefaultSbcComparator(SbcComparator):

    def get_values(self, state: HandState, original: HandState) -> dict:
        values = {}
        values['battle_lost'] = state.player.current_hp <= 0
        values['monsters_hp'] = [monster.current_hp for monster in state.monsters if monster.current_hp > 0]
        values['battle_won']: bool = not len(values['monsters_hp'])
        values['incoming_damage']: int = original.player.current_hp - state.player.current_hp
        values['dead_monsters']: int = len([True for monster in state.monsters if monster.current_hp <= 0])
        monsters_vulnerable_hp = [monster.current_hp - min(monster.powers.get(PowerId.VULNERABLE, 0) * 5, 3)
                                  for monster in state.monsters if monster.current_hp > 0]
        values['lowest_health_monster']: int = 0 if values['battle_won'] else min(monsters_vulnerable_hp)
        values['total_monster_health']: int = 0 if values['battle_won'] else sum(monsters_vulnerable_hp)
        return values

    def does_best_remain_the_best(self, best: HandState, challenger: HandState, original: HandState) -> bool:
        best_values = self.get_values(best, original)
        challenger_values = self.get_values(challenger, original)
        
        if best_values['battle_lost'] != challenger_values['battle_lost']:
            return not challenger_values['battle_lost']
        if best_values['battle_won'] != challenger_values['battle_won']:
            return challenger_values['battle_won']
        if max(2, best_values['incoming_damage']) != max(2, challenger_values['incoming_damage']):
            return challenger_values['incoming_damage'] < best_values['incoming_damage']
        if best_values['dead_monsters'] != challenger_values['dead_monsters']:
            return challenger_values['dead_monsters'] > best_values['dead_monsters']
        if best_values['lowest_health_monster'] != challenger_values['lowest_health_monster']:
            return challenger_values['lowest_health_monster'] < best_values['lowest_health_monster']
        if best_values['total_monster_health'] != challenger_values['total_monster_health']:
            return challenger_values['total_monster_health'] < best_values['total_monster_health']
        return False
