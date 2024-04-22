import unittest
from typing import List, Type

from rs.machine.handlers.handler import Handler
from rs.machine.handlers.handler_action import HandlerAction
from rs.machine.state import GameState
from test_helpers.resources import load_resource_state


class BaseTestHandlerFixture(unittest.TestCase):
    ai_handlers: List[Handler]  # should be overriden by AI package fixture
    handler: Type[Handler]  # should be overridden by children - the expected handler to respond to this state.

    def execute_handler_tests(self, state_path: str, expected=None) -> GameState:
        state = load_resource_state(state_path)
        actual = HandlerAction(commands=["empty"])
        for h in self.ai_handlers:
            if h.can_handle(state):
                if type(h) is self.handler:
                    actual = h.handle(state)
                    break
                else:
                    self.fail(f"Expected handler {self.handler}, instead got {type(h)}")

        if actual.commands == ["empty"]:
            self.fail("No handler found that could handle")

        if expected is not None:
            self.assertEqual(expected, actual.commands)

        return state
