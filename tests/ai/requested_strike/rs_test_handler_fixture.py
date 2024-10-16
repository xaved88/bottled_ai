from typing import List

from base_test_handler_fixture import BaseTestHandlerFixture
from rs.ai.requested_strike.requested_strike import REQUESTED_STRIKE
from rs.machine.handlers.handler import Handler


class RsTestHandlerFixture(BaseTestHandlerFixture):
    strategy = REQUESTED_STRIKE
    ai_handlers: List[Handler] = strategy.handlers
    slay_heart: bool = strategy.slay_heart
