import random


def get_seed_string(seed: float) -> str:
    seed_string = ""
    chars = "0123456789ABCDEFGHIJKLMNPQRSTUVWXYZ"
    leftover = seed  # here long to unsigned string?
    if leftover < 0:
        leftover += 18446744073709551616
    charCount = len(chars)
    while leftover >= 1:
        remainder = int(leftover % charCount)
        leftover -= remainder
        leftover = leftover // charCount  # need // because that allows for some integer division to keep big floats accurate
        char = chars[remainder]
        seed_string += char
    return seed_string[::-1]


def make_seed_string_number(seed: str) -> float:
    total = 0
    seed_str = seed.upper().replace("O", "0")
    chars = "0123456789ABCDEFGHIJKLMNPQRSTUVWXYZ"
    for c in seed_str:
        if c not in chars:
            raise Exception("Bad Seed!")
        r = chars.index(c)
        total *= len(chars)
        total += r
    return total


def make_random_seed() -> str:
    return get_seed_string(random.randrange(1337, 4_000_000_000_000_000_000))
