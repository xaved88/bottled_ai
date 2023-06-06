from typing import List

from base_test_handler_fixture import BaseTestHandlerFixture
from rs.ai._example.example import EXAMPLE_STRATEGY
from rs.machine.handlers.handler import Handler


class CoTestHandlerFixture(BaseTestHandlerFixture):
    ai_handlers: List[Handler] = EXAMPLE_STRATEGY.handlers
