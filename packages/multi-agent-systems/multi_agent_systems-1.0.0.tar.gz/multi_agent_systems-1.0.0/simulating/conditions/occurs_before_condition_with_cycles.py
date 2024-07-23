from typing import Iterable

from pm4py import PetriNet

from simulating.conditions.condition import Condition


class OccursBeforeConditionWithCycles(Condition):
    """
    cyclic condition for a < b <=> a occurs before b
    for each b in trace, there should be own a
    """

    def __init__(self, a: PetriNet.Transition | str, b: PetriNet.Transition | str):
        self.a = a
        self.b = b

    def check(self, trace: dict[PetriNet.Transition | str, int]) -> bool:
        return self.a in trace and (self.b not in trace or trace[self.a] > trace[self.b])

    def still_relevant(self, trace: dict[PetriNet.Transition | str, int]) -> bool:
        return True

    def get_dependent(self) -> Iterable[PetriNet.Transition | str]:
        return [self.b]
