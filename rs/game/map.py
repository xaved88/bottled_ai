from enum import Enum
from typing import List


class Room:
    def __init__(self, room_json: dict):
        self.type: RoomType = RoomType(room_json['symbol'])  # TODO - does this even work?!?!
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


class Path:
    def __init__(self, rooms: List[Room]):
        self.rooms = rooms
        self.room_count: dict[RoomType, int] = {RoomType.MONSTER: 0, RoomType.QUESTION: 0, RoomType.ELITE: 0,
                                                RoomType.CAMPFIRE: 0, RoomType.TREASURE: 0, RoomType.SHOP: 0,
                                                RoomType.BOSS: 0}
        for room in self.rooms:
            self.room_count[room.type] += 1


class Map:
    def __init__(self, map_json: List[dict], current_position: str):
        self.rooms: dict[str, Room] = {}
        self.current_position = current_position
        for room in map_json:
            r = Room(room)
            self.rooms[r.id] = r

        # get the last room from the map and add our own boss room?
        keys = list(self.rooms.keys())
        boss_room_id = self.rooms[keys[-1]].childrenIds[0]
        self.rooms[boss_room_id] = Room({
            'symbol': 'B',
            'x': boss_room_id.split('_')[0],
            'y': boss_room_id.split('_')[1],
            'children': [],
        })

        for room in self.rooms.values():
            for c in room.childrenIds:
                room.add_child(self.rooms[c])

        paths: List[List[Room]] = [
            [self.rooms[current_position]]
        ]
        while paths[0][-1].children:
            for path in paths:
                if not path[-1].children:
                    continue
                room = path[-1]
                for i in range(1, len(room.children)):
                    new_path = path.copy()
                    new_path.append(room.children[i])
                    paths.append(new_path)
                path.append(room.children[0])

        self.paths = [Path(path) for path in paths]

    def get_path_choice_from_choices(self, choices: List[str]):
        next_node = self.paths[-1].rooms[0]
        next_x = next_node.id[0]
        for i in range(len(choices)):
            if choices[i][2] == next_x:
                return i
        return 0

    def sort_paths_by_elites(self):
        self.paths.sort(key=elite_count)

    def sort_paths_by_campfires(self):
        self.paths.sort(key=campfire_count)

    def sort_paths_by_questions(self):
        self.paths.sort(key=question_count)


def elite_count(a: Path):
    return a.room_count[RoomType.ELITE]


def campfire_count(a: Path):
    return a.room_count[RoomType.CAMPFIRE]


def question_count(a: Path):
    return a.room_count[RoomType.QUESTION]


class RoomType(Enum):
    MONSTER = 'M'
    QUESTION = '?'
    ELITE = 'E'
    CAMPFIRE = 'R'
    TREASURE = 'T'
    SHOP = '$'
    BOSS = 'B'  # custom
