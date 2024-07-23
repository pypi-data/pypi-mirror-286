import datetime
import random
from itertools import chain
from random import choice
from typing import Tuple

from pm4py import Marking, PetriNet
from simulating.conditions.condition import Condition
from simulating.conditions.sync_condition import SyncCondition
from simulating.log.event_log import EventLog
from simulating.systems.deadlock_exception import DeadLockException
from simulating.systems.firing import play_from_places, play_from_transitions, add_all


class MultiAgentSystem:
    """
    Allows to simulate behaviour of several Petri nets with conditions between transitions

    Using Pm4py representation of Petri net
    """
    def __init__(self, nets: list[PetriNet], tokens: list[Marking], conditions: list[Condition],
                 start_time: datetime.datetime = datetime.datetime.now(),
                 transition_duration: int = 1):
        """
        :param nets = list of petri nets:
        :param tokens = list of Pm4py marking for each net:
        :param conditions = list of conditions:
        :param start_time = time from which the track starts:
        :param transition_duration = for each next transition the time of firing will be increased by this value:
        """
        self.start_time = start_time
        self.transition_duration = transition_duration
        self.nets = nets
        self.tokens = set(chain.from_iterable(i.keys() for i in tokens))
        self.trace = dict()
        self.conditions = conditions
        self.banned = set()
        self.logs = []
        self.sync_transitions = set(
            chain.from_iterable(i.get_dependent() for i in self.conditions if isinstance(i, SyncCondition)))
        for i in nets:
            for j in i.transitions:
                j.properties["net"] = i.name
            for j in i.places:
                j.properties["net"] = i.name

    def update_banned(self):
        self.banned = set(chain.from_iterable(
            i.get_dependent() for i in self.conditions if not i.check(self.trace)))

    def update_conditions(self):
        self.conditions = [i for i in self.conditions if i.still_relevant(self.trace)]
        self.sync_transitions -= set(i for i in self.sync_transitions if i in self.trace)

    def step(self,
             element: PetriNet.Transition | Tuple[set[PetriNet.Place], set[PetriNet.Transition]] | set[
                 PetriNet.Transition], trace_id: int = 0):

        if isinstance(element, PetriNet.Transition):
            play_from_transitions(element, self.tokens)
            add_all(self.trace, set(i.target for i in element.out_arcs))

        elif isinstance(element, Tuple):
            places = element[0]
            transitions = element[1]
            play_from_places(places, transitions, self.tokens)
            add_all(self.trace, transitions)
            labels = ", ".join(i.label for i in transitions)
            nets = ", ".join(i.properties["net"] for i in transitions)
            self.logs.append(EventLog(labels, nets, trace_id, time=self.start_time))
            self.start_time = self.start_time + datetime.timedelta(seconds=self.transition_duration)
        self.update_conditions()
        self.update_banned()

    def simulate(self, max_depht: int = None, trace_id: int = random.randint(0, 10_000)):
        self.trace = dict((i, 1) for i in self.tokens)
        if not self.tokens:
            raise Exception("empty start marking")
        max_depht = 2 * sum(len(i.places) + len(i.transitions) for i in self.nets) if max_depht is None else max_depht
        cur_depth = 0
        self.update_banned()
        while cur_depth < max_depht:
            active_elements = self.get_all_possible_elements()
            if not active_elements:
                break
            self.step(choice(active_elements), trace_id)
            cur_depth += 1

        if any(len(i.out_arcs) != 0 for i in self.tokens):
            raise DeadLockException("deadlock", self.logs)
        return self.logs

    def get_all_possible_elements(self) -> list[
        PetriNet.Transition | Tuple[set[PetriNet.Place], set[PetriNet.Transition]]]:
        fire_from_transitions = [i for i in self.tokens if isinstance(i, PetriNet.Transition)]
        possible_transition = set(chain.from_iterable(
            [j.target for j in i.out_arcs if j.target not in self.sync_transitions and j.target not in self.banned] for
            i in self.tokens if
            isinstance(i, PetriNet.Place)))
        fire_from_places = []
        for i in possible_transition:
            s = set(j.source for j in i.in_arcs)
            if s.issubset(self.tokens):
                fire_from_places.append((s, {i}))
        for i in [j for j in self.conditions if isinstance(j, SyncCondition)]:
            if any(j in self.banned for j in i.get_dependent()):
                continue
            if i.check(dict((j, 1) for j in self.tokens)):
                fire_from_places.append(
                    (set(k.source for j in i.get_dependent() for k in j.in_arcs), i.get_dependent()))
        return fire_from_transitions + fire_from_places

    def get_trace(self):
        return self.trace

    def create_traces(self, n: int = 1, max_depth: int = None) -> list[list[EventLog]]:
        conditions = self.conditions
        tokens = self.tokens
        sync_transitions = self.sync_transitions
        result = []
        start_time = self.start_time

        def restore_to_default():
            self.start_time = start_time
            self.conditions = conditions.copy()
            self.tokens = tokens.copy()
            self.logs = []
            self.sync_transitions = sync_transitions.copy()

        for i in range(n):
            restore_to_default()
            try:
                trace = self.simulate(max_depth, trace_id=i)
                result.append(trace)
            except DeadLockException as ex:
                return [ex.trace]
        restore_to_default()
        return result
