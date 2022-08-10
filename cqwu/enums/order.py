from enum import Enum


class OrderStatus(Enum):
    NO_PAY = 0
    NO_PAY_RE = 1
    SUCCESS = 2
    FAILURE = 3
    EXPIRED = 4
