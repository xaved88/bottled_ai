from typing import List

from base_test_handler_fixture import BaseTestHandlerFixture
from rs.ai.requested_scaling.requested_scaling import REQUESTED_SCALING
from rs.machine.handlers.handler import Handler


class SynergyCardRewardHandlerFixture(BaseTestHandlerFixture):
    ai_handlers: List[Handler] = REQUESTED_SCALING.handlers
