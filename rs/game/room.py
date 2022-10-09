from enum import Enum
from typing import List


class Room:
    def __init__(self, room_json: dict):
        self.type: RoomType = RoomType(room_json['symbol'])
        self.id: str = str(room_json['x']) + '_' + str(room_json['y'])
        self.childrenIds: List[str] = []
        for c in room_json['children']:
            self.childrenIds.append(str(c['x']) + '_' + str(c['y']))
        self.children: List[Room] = []
        self.parents: List[Room] = []

    def add_child(self, room):
        self.children.append(room)
        room.add_parent(self)

    def add_parent(self, room):
        self.parents.append(room)


class RoomType(Enum):
    MONSTER = 'M'
    QUESTION = '?'
    ELITE = 'E'
    CAMPFIRE = 'R'
    TREASURE = 'T'
    SHOP = '$'
    BOSS = 'B'  # custom
