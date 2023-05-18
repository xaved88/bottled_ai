from typing import List

from rs.game.path import Path, PathHandlerConfig
from rs.game.room import RoomType, Room
from rs.machine.state import GameState


class Map:
    def __init__(self, map_json: List[dict], current_position: str, current_floor: int):
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

        # get the first room and add your own starting point
        starter_children = []
        for r in self.rooms.values():
            if "_0" in r.id:
                coords = r.id.split("_")
                starter_children.append({"x": int(coords[0]), "y": int(coords[1])})
        self.rooms["0_-1"] = Room({
            'symbol': 'B',
            'x': 0,
            'y': 0,
            'children': starter_children
        })
        for room in self.rooms.values():
            for c in room.childrenIds:
                room.add_child(self.rooms[c])
        #Sometimes there are weird bugs in the comm mod giving bad coordinates. Only seen at the start of acts, so pretend we're there?
        if(self.current_position not in self.rooms):
            self.current_position = "0_-1"
        paths: List[List[Room]] = []
        paths.append([self.rooms[self.current_position]])
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

        self.paths = [Path(path[1:]) for path in paths]

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

    def sort_paths_by_questions_and_shops(self):
        self.paths.sort(key=question_and_shop_count)

    def sort_paths_by_reward_to_survivability(self, state: GameState, config: PathHandlerConfig):
        for path in self.paths:
            path.calculate_reward_survivability(state, config)
        self.paths.sort(key=reward_and_survivability)


def elite_count(a: Path):
    return a.room_count[RoomType.ELITE]


def campfire_count(a: Path):
    return a.room_count[RoomType.CAMPFIRE]


def question_and_shop_count(a: Path):
    return a.room_count[RoomType.QUESTION] + a.room_count[RoomType.SHOP]


def reward_and_survivability(a: Path):
    return a.reward_survivability
