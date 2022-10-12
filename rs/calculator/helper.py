import pickle
from typing import TypeVar

T = TypeVar('T')


def pickle_deepcopy(obj: T) -> T:
    return pickle.loads(pickle.dumps(obj, -1))
