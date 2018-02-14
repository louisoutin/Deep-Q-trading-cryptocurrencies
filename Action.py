from enum import Enum


class Action(Enum):
    """
        Represent an action of the agent.
    """
    HOLD = 0
    BUY = 1
    SELL = 2
