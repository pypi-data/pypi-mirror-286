from pm4py import PetriNet


def play_from_places(places: set[PetriNet.Place], transitions: set[PetriNet.Transition],
                     tokens: set[PetriNet.Place | PetriNet.Transition]):
    tokens -= places
    tokens.update(transitions)


def play_from_transitions(element: PetriNet.Transition, tokens: set[PetriNet.Place | PetriNet.Transition]):
    tokens.remove(element)
    tokens.update(i.target for i in element.out_arcs)


def add_all(trace: dict, what: set):
    for k in what:
        if k not in trace:
            trace[k] = 0
        trace[k] += 1
