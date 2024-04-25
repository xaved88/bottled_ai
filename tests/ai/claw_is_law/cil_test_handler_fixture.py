from typing import List

from base_test_handler_fixture import BaseTestHandlerFixture
from rs.ai.claw_is_law.claw_is_law import CLAW_IS_LAW
from rs.machine.handlers.handler import Handler


class CilTestHandlerFixture(BaseTestHandlerFixture):
    ai_handlers: List[Handler] = CLAW_IS_LAW.handlers
