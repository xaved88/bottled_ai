from typing import List

from rs.machine.character import Character
from rs.machine.handlers.handler import Handler


class AiStrategy:

    def __init__(self, handlers: List[Handler], character: Character, name: str = "Not set", slay_heart: bool = False):
        self.name = name
        self.character = character
        self.slay_heart = slay_heart
        self.handlers = handlers
