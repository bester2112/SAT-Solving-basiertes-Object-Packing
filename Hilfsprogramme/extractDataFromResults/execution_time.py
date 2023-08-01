class ExecutionTime:
    def __init__(self, total_sec, seconds, minutes, hours, days):
        self.total_sec = total_sec
        self.seconds = seconds
        self.minutes = minutes
        self.hours = hours
        self.days = days

    def __str__(self):
        return f"ExecutionTime: total_sec={self.total_sec}, seconds={self.seconds}, minutes={self.minutes}, hours={self.hours}, days={self.days}"
