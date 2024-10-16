from presentation_config import presentation_mode, p_delay, slow_pathing
from rs.game.map import Map
from rs.game.path import PathHandlerConfig
from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.handlers.handler_action import HandlerAction
from rs.machine.state import GameState

default_config = PathHandlerConfig(
    hallway_fight_base_reward=1,
    hallway_fight_prayer_wheel=0.3,
    hallway_question_card_reward=0.15,
    hallway_fight_gold=15,
    hallway_fight_health_loss=lambda state: state.game_state()['act'] * 5,
    elite_base_reward=1,  # this does not include the relic, that's added separately
    elite_question_card_reward=0.15,
    elite_emerald_key_reward=0,
    elite_fight_gold=30,
    elite_fight_health_loss=lambda state: (state.game_state()['act'] + 1) * 15,
    elite_fight_emerald_key_extra_health_loss=5,
    relic_reward=1.5,
    curse_reward_loss=1.5,
    upgrade_reward=1.1,
    event_value_reward=lambda state: 1 if state.game_state()['act'] == 1 else 1.5,
    gold_at_shop_reward=lambda state, gold_to_spend: gold_to_spend / 100,
    gold_after_boss_reward=lambda state: state.game_state()['gold'] / 200,
    survivability_reward_calculation=lambda reward, survivability: reward + (survivability - 1) * 15,
)


class CommonMapHandler(Handler):

    def __init__(self, config: PathHandlerConfig = None):
        self.config: PathHandlerConfig = default_config if config is None else config

    def can_handle(self, state: GameState) -> bool:
        return state.screen_type() == ScreenType.MAP.value and state.has_command(Command.CHOOSE)

    def handle(self, state: GameState, slay_heart: bool) -> HandlerAction:
        if slay_heart:
            self.config.elite_emerald_key_reward = 5

        # Get the math and paths set up
        n = state.game_state()["screen_state"]["current_node"]
        current_position = str(n["x"]) + "_" + str(n["y"])
        game_map = Map(state.get_map(), current_position, state.game_state()['floor'])

        # Sort the paths by our priorities
        game_map.sort_paths_by_reward_to_survivability(state, self.config)

        # this will actually screw us with winged boots, as there are more choices and we'd be picking from a different list...
        if presentation_mode or slow_pathing:
            return HandlerAction(
                commands=[p_delay, "choose " + str(game_map.get_path_choice_from_choices(state.get_choice_list()))])
        return HandlerAction(commands=["choose " + str(game_map.get_path_choice_from_choices(state.get_choice_list()))])
