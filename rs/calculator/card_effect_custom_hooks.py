from typing import Callable

from rs.calculator.hand_state_interface import HandStateInterface
from rs.calculator.powers import PowerId

CardEffectCustomHook = Callable[[HandStateInterface, int], None]


def dropkick_custom_hook(state: HandStateInterface, target_index: int = -1):
    if target_index > -1:
        if state.monsters[target_index].powers.get(PowerId.VULNERABLE):
            state.player.energy += 1


def entrench_custom_hook(state: HandStateInterface, target_index: int = -1):
    state.player.block *= 2
