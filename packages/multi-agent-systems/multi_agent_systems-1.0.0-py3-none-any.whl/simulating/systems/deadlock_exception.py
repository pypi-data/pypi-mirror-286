from simulating.log.event_log import EventLog


class DeadLockException(Exception):
    """
    Exception for deadlock representation
    """
    def __init__(self, message: str, events: list[EventLog]):
        super().__init__(message)
        self.trace = events
        self.trace.append(EventLog("DEADLOCK", "DEADLOCK"))
