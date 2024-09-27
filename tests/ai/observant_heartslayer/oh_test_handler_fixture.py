from typing import List

from base_test_handler_fixture import BaseTestHandlerFixture
from rs.ai.observant_heartslayer.observant_heartslayer import OBSERVANT_HEARTSLAYER
from rs.machine.handlers.handler import Handler


class OhTestHandlerFixture(BaseTestHandlerFixture):
    ai_handlers: List[Handler] = OBSERVANT_HEARTSLAYER.handlers
