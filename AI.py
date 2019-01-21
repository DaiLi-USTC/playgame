from enum import IntEnum


class AI_type(IntEnum):
    NOTHING = 1
    PATROL = 2
    FOLLOW = 3


class AI:
    def __init__(self):
        self.state = AI_type.NOTHING

