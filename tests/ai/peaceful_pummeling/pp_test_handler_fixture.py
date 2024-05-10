from typing import List

from base_test_handler_fixture import BaseTestHandlerFixture
from rs.ai.peaceful_pummeling.peaceful_pummeling import PEACEFUL_PUMMELING
from rs.ai.pwnder_my_orbs.pwnder_my_orbs import PWNDER_MY_ORBS
from rs.machine.handlers.handler import Handler


class PpTestHandlerFixture(BaseTestHandlerFixture):
    ai_handlers: List[Handler] = PEACEFUL_PUMMELING.handlers
