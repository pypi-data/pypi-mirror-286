import datetime
from uuid import uuid4 as uuid


class EventLog:
    """
    Custom event log
    contains: transition, related net, id of the trace and time firing
    """
    def __init__(self, who, net, trace_id: int = 0, time: datetime.datetime = datetime.datetime.now()):
        self.id = trace_id
        self.who = who
        self.timestamp = time
        self.net = net

    def __repr__(self):
        return self.__str__()

    def __str__(self) -> str:
        return "; ".join(map(str, vars(self).values()))

    @classmethod
    def header(cls):
        return "; ".join(vars(EventLog(None, None)).keys())
