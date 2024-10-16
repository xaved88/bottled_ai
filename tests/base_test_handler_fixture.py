import unittest
from typing import List, Type

from rs.machine.handlers.handler import Handler
from rs.machine.handlers.handler_action import HandlerAction
from rs.machine.the_bots_memory_book import TheBotsMemoryBook
from test_helpers.resources import load_resource_state


class BaseTestHandlerFixture(unittest.TestCase):
    ai_handlers: List[Handler]  # should be overridden by AI package fixture
    slay_heart: bool  # should be overridden by AI package fixture
    handler: Type[Handler]  # should be overridden by children - the expected handler to respond to this state.

    def execute_handler_tests(self, state_path: str, expected=None,
                              memory_book: TheBotsMemoryBook = None) -> TheBotsMemoryBook:
        state = load_resource_state(state_path, memory_book=memory_book)
        actual = HandlerAction(commands=["empty"])
        for h in self.ai_handlers:
            if h.can_handle(state):
                actual = h.handle(state, slay_heart=self.slay_heart)
                if actual is None:
                    continue
                if type(h) is self.handler:
                    break
                else:
                    self.fail(f"Expected handler {self.handler}, instead was handled by {type(h)}")

        if actual.commands == ["empty"]:
            self.fail("No handler found that could handle")

        if expected is not None:
            self.assertEqual(expected, actual.commands)

        return actual.memory_book
