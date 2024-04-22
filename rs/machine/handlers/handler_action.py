from typing import List

from rs.machine.the_bots_memory_book import TheBotsMemoryBook


class HandlerAction:

    def __init__(self, commands: List[str], memory_book: TheBotsMemoryBook = None):
        self.commands = commands
        self.memory_book = memory_book
