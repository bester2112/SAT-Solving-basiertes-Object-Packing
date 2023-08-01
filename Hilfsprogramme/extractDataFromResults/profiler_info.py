class ProfilerInfo:
    def __init__(
        self,
        function_executed: str = None,
        file_executed: str = None,
        execution_time: float = None,
        average_cpu_usage: float = None,
        minimum_cpu_usage: float = None,
        maximum_cpu_usage: float = None,
        memory_before: int = None,
        memory_after: int = None,
        memory_consumed: int = None,
        memory_before_b2h: str = None,
        memory_after_b2h: str = None,
        memory_consumed_b2h: str = None
    ):
        self.function_executed = function_executed
        self.file_executed = file_executed
        self.execution_time = execution_time
        self.average_cpu_usage = average_cpu_usage
        self.minimum_cpu_usage = minimum_cpu_usage
        self.maximum_cpu_usage = maximum_cpu_usage
        self.memory_before = memory_before
        self.memory_after = memory_after
        self.memory_consumed = memory_consumed
        self.memory_before_b2h = memory_before_b2h
        self.memory_after_b2h = memory_after_b2h
        self.memory_consumed_b2h = memory_consumed_b2h

    def __str__(self):
        return (
            f"ProfilerInfo: function_executed={self.function_executed}, file_executed={self.file_executed}, "
            f"execution_time={self.execution_time}, average_cpu_usage={self.average_cpu_usage}, "
            f"minimum_cpu_usage={self.minimum_cpu_usage}, maximum_cpu_usage={self.maximum_cpu_usage}, "
            f"memory_before={self.memory_before}, memory_after={self.memory_after}, memory_consumed={self.memory_consumed}, "
            f"memory_before_b2h={self.memory_before_b2h}, memory_after_b2h={self.memory_after_b2h}, "
            f"memory_consumed_b2h={self.memory_consumed_b2h}"
        )
