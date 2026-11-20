"""Research process: the split and its seal, the hypothesis registry, the harness and the catalogue."""

from trading.research.market import ResearchData
from trading.research.split import TRAIN_END


def train_data() -> ResearchData:
    """Data for exploration: everything up to the end of the train segment, and nothing later.

    Exploration happens on train only. Dev is for replication through the harness and is never
    browsed; there is deliberately no shortcut that loads it.
    """
    return ResearchData(TRAIN_END)
