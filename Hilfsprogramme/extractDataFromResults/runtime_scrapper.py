import re

class Runtime:
    def __init__(self, runtime_nr, runtime_name, total_sec, runtime_seconds, runtime_minutes, runtime_hours, runtime_days):
        self.runtime_nr = runtime_nr
        self.runtime_name = runtime_name
        self.total_sec = total_sec
        self.runtime_seconds = runtime_seconds
        self.runtime_minutes = runtime_minutes
        self.runtime_hours = runtime_hours
        self.runtime_days = runtime_days

    def __str__(self):
        return f"Runtime: runtime_nr={self.runtime_nr}, runtime_name={self.runtime_name}, total_sec={self.total_sec}, runtime_seconds={self.runtime_seconds}, runtime_minutes={self.runtime_minutes}, runtime_hours={self.runtime_hours}, runtime_days={self.runtime_days}"

    @staticmethod
    def process(filepath):
        with open(filepath, 'r') as f:
            runtimes = []
            for line in f:
                if "Runtime" in line:
                    match = re.search(
                        r"(INFO|DEBUG): Runtime #(?P<runtime_nr>\d+)# (?P<runtime_name>.+): TotalSec: (?P<total_sec>\d+\.\d+) == (?P<runtime_seconds>\d+\.\d+) seconds, (?P<runtime_minutes>\d+) minutes, (?P<runtime_hours>\d+) hours, (?P<runtime_days>\d+) days",
                        line)
                    if match:
                        runtime_nr = match.group('runtime_nr')
                        runtime_name = match.group('runtime_name')
                        total_sec = match.group('total_sec')
                        runtime_seconds = match.group('runtime_seconds')
                        runtime_minutes = match.group('runtime_minutes')
                        runtime_hours = match.group('runtime_hours')
                        runtime_days = match.group('runtime_days')
                        runtimes.append(Runtime(runtime_nr, runtime_name, total_sec, runtime_seconds, runtime_minutes, runtime_hours, runtime_days))
            runtimes.sort(key=lambda x: int(x.runtime_nr))
            return runtimes
