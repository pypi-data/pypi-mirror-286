from typing import Iterable
from pm4py import PetriNet


class Condition:
    """
    super class for conditions
    """

    def check(self, trace: dict[PetriNet.Transition | str, int]) -> bool:
        """
        check the condition for trace
        :param trace:
        :return: bool
        """
        pass

    def still_relevant(self, trace: dict[PetriNet.Transition | str, int]) -> bool:
        """
        return true if the condition should be saved or false, if presented condition became irrelevant
        :param trace:
        :return: bool
        """
        pass

    def get_dependent(self) -> Iterable[PetriNet.Transition | str]:
        """
        return dependent part of condition
        example: a occurs before b. In this case [b] is the dependent part
        :return: iterable of transitions
        """
        pass
