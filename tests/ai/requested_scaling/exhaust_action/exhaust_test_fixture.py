from typing import List

from base_test_handler_fixture import BaseTestHandlerFixture
from ai.requested_scaling import REQUESTED_SCALING
from rs.machine.handlers.handler import Handler


class ExhaustHandlerFixture(BaseTestHandlerFixture):
    ai_handlers: List[Handler] = REQUESTED_SCALING.handlers
