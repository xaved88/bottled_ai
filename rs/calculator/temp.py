import copy
import time

from rs.calculator.cards import Card, CardId
from rs.calculator.hand_state import HandState
from rs.calculator.play_path import PlayPath, get_paths
from rs.calculator.targets import Player, Target
from rs.game.card import CardType

"""
 SO NOW LET'S TEST IT OUT

    - we need to build a state from which we can test. So cards for the hand, a hand state, and some enemies.
"""

strike_card = Card()
strike_card.id = CardId.STRIKE_R
strike_card.upgrade = 0
strike_card.cost = 1
strike_card.needs_target = True
strike_card.type = CardType.ATTACK

bash_card = Card()
bash_card.id = CardId.BASH
bash_card.upgrade = 1
bash_card.cost = 2
bash_card.needs_target = True
bash_card.type = CardType.ATTACK

state = HandState()
state.hand = []

state.player = Player()
state.player.powers = dict()
state.player.current_hp = 80
state.player.block = 0
state.player.max_hp = 80
state.player.energy = 3

state.relics = dict()
state.targets = [Target(), Target()]
state.targets[0].current_hp = 50
state.targets[0].max_hp = 50
state.targets[0].block = 0
state.targets[0].powers = dict()

state.targets[1].current_hp = 50
state.targets[1].max_hp = 50
state.targets[1].block = 0
state.targets[1].powers = dict()

"""
for i in range(5):
    state.cards.append(copy.deepcopy(strike_card))
state.cards.append(copy.deepcopy(bash_card))
"""

state.hand.append(copy.deepcopy(strike_card))
state.hand.append(copy.deepcopy(strike_card))
state.hand.append(copy.deepcopy(bash_card))
state.hand.append(copy.deepcopy(strike_card))
state.hand.append(copy.deepcopy(strike_card))

# NOW WE RUN IT
init_path = PlayPath([], state)

start = time.perf_counter()
paths = get_paths(init_path)
mid = time.perf_counter()
sorted_path = sorted(paths, key=lambda path: path.state.targets[0].current_hp)
end = time.perf_counter()

print(
    f"Done. Found {len(sorted_path)} paths, in {end - start} seconds."
    f" {mid - start} seconds to find paths, {end - mid} to sort them"
)

best = sorted_path[0]
print(f"Best path: {best.plays}, health: {best.state.targets[0].current_hp}")

worst = sorted_path[-1]
print(f"Worst path: {worst.plays}, health: {worst.state.targets[0].current_hp}")


print("Now for target 2")
sorted_path = sorted(paths, key=lambda path: path.state.targets[1].current_hp)
best = sorted_path[0]
print(f"Best path: {best.plays}, health: {best.state.targets[1].current_hp}")

worst = sorted_path[-1]
print(f"Worst path: {worst.plays}, health: {worst.state.targets[1].current_hp}")
