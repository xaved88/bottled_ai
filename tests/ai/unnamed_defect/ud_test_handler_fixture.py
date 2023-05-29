from typing import List

from base_test_handler_fixture import BaseTestHandlerFixture
from rs.ai.unnamed_defect_build.example import UNNAMED_DEFECT_STRATEGY
from rs.machine.handlers.handler import Handler


class UdTestHandlerFixture(BaseTestHandlerFixture):
    ai_handlers: List[Handler] = UNNAMED_DEFECT_STRATEGY.handlers
