from typing import List

from base_test_handler_fixture import BaseTestHandlerFixture
from rs.ai.shivs_and_giggles.shivs_and_giggles import SHIVS_AND_GIGGLES
from rs.machine.handlers.handler import Handler


class SgTestHandlerFixture(BaseTestHandlerFixture):
    strategy = SHIVS_AND_GIGGLES
    ai_handlers: List[Handler] = strategy.handlers
    slay_heart: bool = strategy.slay_heart
