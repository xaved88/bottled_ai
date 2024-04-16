import unittest
from typing import List, Type

from rs.machine.handlers.handler import Handler
from test_helpers.resources import load_resource_state


class BaseTestHandlerFixture(unittest.TestCase):
    ai_handlers: List[Handler]  # should be overriden by AI package fixture
    handler: Type[Handler]  # should be overridden by children - the expected handler to respond to this state.

    def execute_handler_tests(self, state_path: str, expected: List[str] = None):
        state = load_resource_state(state_path)
        actual = None
        for h in self.ai_handlers:
            if h.can_handle(state):
                if type(h) is self.handler:
                    actual = h.handle(state)
                    break
                else:
                    self.fail(f"Expected handler {self.handler}, instead got {type(h)}")

        if actual is None:
            self.fail("No handler found that could handle")

        if expected is not None:
            self.assertEqual(expected, actual)
