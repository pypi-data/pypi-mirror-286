from itertools import chain
from typing import Iterable

from pm4py import PetriNet

from simulating.conditions.condition import Condition


class SyncCondition(Condition):
    """
    condition for firing synchronized transitions. It also works with cycles if parameter is_cyclic_condition passed
    """

    def __init__(self, transitions: Iterable[PetriNet.Transition], is_cyclic_condition: bool = False):
        self.transitions = set(transitions)
        self.prepositions = set(chain.from_iterable([j.source for j in i.in_arcs] for i in transitions))
        self.cyclic = is_cyclic_condition

    def check(self, trace: dict[PetriNet.Transition | str, int]) -> bool:
        return self.prepositions.issubset(set(trace.keys()))

    def still_relevant(self, trace: dict[PetriNet.Transition | str, int]) -> bool:
        return self.cyclic or any(i not in trace for i in self.transitions)

    def get_dependent(self) -> Iterable[PetriNet.Transition | str]:
        return self.transitions
