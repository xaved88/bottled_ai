from typing import List

from rs.machine.character import Character
from rs.machine.handlers.handler import Handler


class AiStrategy:

    def __init__(self, handlers: List[Handler], character: Character, name: str = "Not set"):
        self.handlers = handlers
        self.character = character
        self.name = name
