from presentation_config import presentation_mode, p_delay
from rs.machine.handlers.handler import Handler
from rs.machine.handlers.handler_action import HandlerAction
from rs.machine.state import GameState

cards_to_pass_over = [
    'strike',
    'defend',
    'strike+',
    'defend+',
    'clumsy',
    'curse of the bell',
    'decay',
    'doubt',
    'injury',
    'necronomicurse',
    'normality',
    'pain',
    'parasite',
    'pride',
    'regret',
    'shame',
    'writhe',
    'burn',
    'burn+',
    'wound',
    'slimed',
]


class CommonScryHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        return state.current_action() == 'ScryAction'

    def handle(self, state: GameState, slay_heart: bool) -> HandlerAction:
        choice_list = state.get_choice_list()
        commands: list = []

        if presentation_mode:
            commands.append(p_delay)

        # sadly it has to choose by index rather than name since
        # it would otherwise get confused by duplicates and try to select them again
        for idx, checked_card in enumerate(choice_list):
            if checked_card in cards_to_pass_over:
                commands.append('wait 15')
                commands.append("choose " + str(idx))
        commands.append('wait 30')
        commands.append("confirm")

        return HandlerAction(commands=commands)
