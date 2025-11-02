from enum import Enum


class Currency(Enum):
    USD = "USD"
    JMD = "JMD"

class TravelerType(Enum):
    ADULT = "ADULT"
    CHILD = "CHILD"
    INFANT = "HELD_INFANT"
