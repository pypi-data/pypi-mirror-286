from typing import Iterable

from simulating.log.event_log import EventLog


def export_csv(file_name, event_logs: Iterable[Iterable[EventLog]], append: bool = False):
    arg = "a" if append else "w"
    file_name += ".csv"
    with open(file_name, arg) as file:
        file.write(EventLog.header() + "\n")
        for i in event_logs:
            for j in i:
                file.write(str(j) + "\n")
