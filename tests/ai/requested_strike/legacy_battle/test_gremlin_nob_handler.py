import unittest

from ai.requested_strike.rs_test_handler_fixture import RsTestHandlerFixture
from rs.ai.requested_strike.handlers.custom_battle.gremlin_nob_handler import GremlinNobHandler


class GremlinNobHandlerTestCase(RsTestHandlerFixture):
    handler = GremlinNobHandler

    def test_plays_no_skill(self):
        self.execute_handler_tests('battles/gremlin_nob/gremlin_nob_skills_in_hand.json', ['play 4 0'])

    def test_plays_allowed_skill(self):
        self.execute_handler_tests('battles/gremlin_nob/gremlin_nob_battle_trance.json', ['play 3'])
