class MonsterProfiler:
    def __init__(self, profiler_list=None):
        self.function_executed_check_all: str = None
        self.file_executed_check_all: str = None
        self.execution_time_check_all: float = None
        self.average_cpu_usage_check_all: float = None
        self.minimum_cpu_usage_check_all: float = None
        self.maximum_cpu_usage_check_all: float = None
        self.memory_before_check_all: int = None
        self.memory_after_check_all: int = None
        self.memory_consumed_check_all: int = None
        self.memory_before_b2h_check_all: str = None
        self.memory_after_b2h_check_all: str = None
        self.memory_consumed_b2h_check_all: str = None

        self.function_executed_run: str = None
        self.file_executed_run: str = None
        self.execution_time_run: float = None
        self.average_cpu_usage_run: float = None
        self.minimum_cpu_usage_run: float = None
        self.maximum_cpu_usage_run: float = None
        self.memory_before_run: int = None
        self.memory_after_run: int = None
        self.memory_consumed_run: int = None
        self.memory_before_b2h_run: str = None
        self.memory_after_b2h_run: str = None
        self.memory_consumed_b2h_run: str = None

        self.function_executed_createTheVariables: str = None
        self.file_executed_createTheVariables: str = None
        self.execution_time_createTheVariables: float = None
        self.average_cpu_usage_createTheVariables: float = None
        self.minimum_cpu_usage_createTheVariables: float = None
        self.maximum_cpu_usage_createTheVariables: float = None
        self.memory_before_createTheVariables: int = None
        self.memory_after_createTheVariables: int = None
        self.memory_consumed_createTheVariables: int = None
        self.memory_before_b2h_createTheVariables: str = None
        self.memory_after_b2h_createTheVariables: str = None
        self.memory_consumed_b2h_createTheVariables: str = None

        self.function_executed_createTheEquivalents: str = None
        self.file_executed_createTheEquivalents: str = None
        self.execution_time_createTheEquivalents: float = None
        self.average_cpu_usage_createTheEquivalents: float = None
        self.minimum_cpu_usage_createTheEquivalents: float = None
        self.maximum_cpu_usage_createTheEquivalents: float = None
        self.memory_before_createTheEquivalents: int = None
        self.memory_after_createTheEquivalents: int = None
        self.memory_consumed_createTheEquivalents: int = None
        self.memory_before_b2h_createTheEquivalents: str = None
        self.memory_after_b2h_createTheEquivalents: str = None
        self.memory_consumed_b2h_createTheEquivalents: str = None

        self.function_executed_createExactlyOneForThePixels: str = None
        self.file_executed_createExactlyOneForThePixels: str = None
        self.execution_time_createExactlyOneForThePixels: float = None
        self.average_cpu_usage_createExactlyOneForThePixels: float = None
        self.minimum_cpu_usage_createExactlyOneForThePixels: float = None
        self.maximum_cpu_usage_createExactlyOneForThePixels: float = None
        self.memory_before_createExactlyOneForThePixels: int = None
        self.memory_after_createExactlyOneForThePixels: int = None
        self.memory_consumed_createExactlyOneForThePixels: int = None
        self.memory_before_b2h_createExactlyOneForThePixels: str = None
        self.memory_after_b2h_createExactlyOneForThePixels: str = None
        self.memory_consumed_b2h_createExactlyOneForThePixels: str = None

        self.function_executed_createExactlyOneForThePossiblePlaystone: str = None
        self.file_executed_createExactlyOneForThePossiblePlaystone: str = None
        self.execution_time_createExactlyOneForThePossiblePlaystone: float = None
        self.average_cpu_usage_createExactlyOneForThePossiblePlaystone: float = None
        self.minimum_cpu_usage_createExactlyOneForThePossiblePlaystone: float = None
        self.maximum_cpu_usage_createExactlyOneForThePossiblePlaystone: float = None
        self.memory_before_createExactlyOneForThePossiblePlaystone: int = None
        self.memory_after_createExactlyOneForThePossiblePlaystone: int = None
        self.memory_consumed_createExactlyOneForThePossiblePlaystone: int = None
        self.memory_before_b2h_createExactlyOneForThePossiblePlaystone: str = None
        self.memory_after_b2h_createExactlyOneForThePossiblePlaystone: str = None
        self.memory_consumed_b2h_createExactlyOneForThePossiblePlaystone: str = None

        self.function_executed_printFormulaFile: str = None
        self.file_executed_printFormulaFile: str = None
        self.execution_time_printFormulaFile: float = None
        self.average_cpu_usage_printFormulaFile: float = None
        self.minimum_cpu_usage_printFormulaFile: float = None
        self.maximum_cpu_usage_printFormulaFile: float = None
        self.memory_before_printFormulaFile: int = None
        self.memory_after_printFormulaFile: int = None
        self.memory_consumed_printFormulaFile: int = None
        self.memory_before_b2h_printFormulaFile: str = None
        self.memory_after_b2h_printFormulaFile: str = None
        self.memory_consumed_b2h_printFormulaFile: str = None

        if profiler_list:
            for profiler_info in profiler_list:
                if profiler_info.function_executed == "_check_all":
                    self.function_executed_check_all: str = None
                    self.file_executed_check_all: str = None
                    self.execution_time_check_all: float = None
                    self.average_cpu_usage_check_all: float = None
                    self.minimum_cpu_usage_check_all: float = None
                    self.maximum_cpu_usage_check_all: float = None
                    self.memory_before_check_all: int = None
                    self.memory_after_check_all: int = None
                    self.memory_consumed_check_all: int = None
                    self.memory_before_b2h_check_all: str = None
                    self.memory_after_b2h_check_all: str = None
                    self.memory_consumed_b2h_check_all: str = None

                    self.function_executed_check_all = profiler_info.function_executed
                    self.file_executed_check_all = profiler_info.file_executed
                    self.execution_time_check_all = profiler_info.execution_time.total_sec
                    self.average_cpu_usage_check_all = profiler_info.average_cpu_usage
                    self.minimum_cpu_usage_check_all = profiler_info.minimum_cpu_usage
                    self.maximum_cpu_usage_check_all = profiler_info.maximum_cpu_usage
                    self.memory_before_check_all = profiler_info.memory_before
                    self.memory_after_check_all = profiler_info.memory_after
                    self.memory_consumed_check_all = profiler_info.memory_consumed
                    self.memory_before_b2h_check_all = profiler_info.memory_before_b2h
                    self.memory_after_b2h_check_all = profiler_info.memory_after_b2h
                    self.memory_consumed_b2h_check_all = profiler_info.memory_consumed_b2h

                elif profiler_info.function_executed == "run":
                    self.function_executed_run = profiler_info.function_executed
                    self.file_executed_run = profiler_info.file_executed
                    self.execution_time_run = profiler_info.execution_time.total_sec
                    self.average_cpu_usage_run = profiler_info.average_cpu_usage
                    self.minimum_cpu_usage_run = profiler_info.minimum_cpu_usage
                    self.maximum_cpu_usage_run = profiler_info.maximum_cpu_usage
                    self.memory_before_run = profiler_info.memory_before
                    self.memory_after_run = profiler_info.memory_after
                    self.memory_consumed_run = profiler_info.memory_consumed
                    self.memory_before_b2h_run = profiler_info.memory_before_b2h
                    self.memory_after_b2h_run = profiler_info.memory_after_b2h
                    self.memory_consumed_b2h_run = profiler_info.memory_consumed_b2h

                elif profiler_info.function_executed == "_createTheVariables":
                    self.function_executed_createTheVariables = profiler_info.function_executed
                    self.file_executed_createTheVariables = profiler_info.file_executed
                    self.execution_time_createTheVariables = profiler_info.execution_time.total_sec
                    self.average_cpu_usage_createTheVariables = profiler_info.average_cpu_usage
                    self.minimum_cpu_usage_createTheVariables = profiler_info.minimum_cpu_usage
                    self.maximum_cpu_usage_createTheVariables = profiler_info.maximum_cpu_usage
                    self.memory_before_createTheVariables = profiler_info.memory_before
                    self.memory_after_createTheVariables = profiler_info.memory_after
                    self.memory_consumed_createTheVariables = profiler_info.memory_consumed
                    self.memory_before_b2h_createTheVariables = profiler_info.memory_before_b2h
                    self.memory_after_b2h_createTheVariables = profiler_info.memory_after_b2h
                    self.memory_consumed_b2h_createTheVariables = profiler_info.memory_consumed_b2h

                elif profiler_info.function_executed == "_createTheEquivalents":
                    self.function_executed_createTheEquivalents = profiler_info.function_executed
                    self.file_executed_createTheEquivalents = profiler_info.file_executed
                    self.execution_time_createTheEquivalents = profiler_info.execution_time.total_sec
                    self.average_cpu_usage_createTheEquivalents = profiler_info.average_cpu_usage
                    self.minimum_cpu_usage_createTheEquivalents = profiler_info.minimum_cpu_usage
                    self.maximum_cpu_usage_createTheEquivalents = profiler_info.maximum_cpu_usage
                    self.memory_before_createTheEquivalents = profiler_info.memory_before
                    self.memory_after_createTheEquivalents = profiler_info.memory_after
                    self.memory_consumed_createTheEquivalents = profiler_info.memory_consumed
                    self.memory_before_b2h_createTheEquivalents = profiler_info.memory_before_b2h
                    self.memory_after_b2h_createTheEquivalents = profiler_info.memory_after_b2h
                    self.memory_consumed_b2h_createTheEquivalents = profiler_info.memory_consumed_b2h

                elif profiler_info.function_executed == "_createExactlyOneForThePixels":
                    self.function_executed_createExactlyOneForThePixels = profiler_info.function_executed
                    self.file_executed_createExactlyOneForThePixels = profiler_info.file_executed
                    self.execution_time_createExactlyOneForThePixels = profiler_info.execution_time.total_sec
                    self.average_cpu_usage_createExactlyOneForThePixels = profiler_info.average_cpu_usage
                    self.minimum_cpu_usage_createExactlyOneForThePixels = profiler_info.minimum_cpu_usage
                    self.maximum_cpu_usage_createExactlyOneForThePixels = profiler_info.maximum_cpu_usage
                    self.memory_before_createExactlyOneForThePixels = profiler_info.memory_before
                    self.memory_after_createExactlyOneForThePixels = profiler_info.memory_after
                    self.memory_consumed_createExactlyOneForThePixels = profiler_info.memory_consumed
                    self.memory_before_b2h_createExactlyOneForThePixels = profiler_info.memory_before_b2h
                    self.memory_after_b2h_createExactlyOneForThePixels = profiler_info.memory_after_b2h
                    self.memory_consumed_b2h_createExactlyOneForThePixels = profiler_info.memory_consumed_b2h

                elif profiler_info.function_executed == "_createExactlyOneForThePossiblePlaystone":
                    self.function_executed_createExactlyOneForThePossiblePlaystone = profiler_info.function_executed
                    self.file_executed_createExactlyOneForThePossiblePlaystone = profiler_info.file_executed
                    self.execution_time_createExactlyOneForThePossiblePlaystone = profiler_info.execution_time.total_sec
                    self.average_cpu_usage_createExactlyOneForThePossiblePlaystone = profiler_info.average_cpu_usage
                    self.minimum_cpu_usage_createExactlyOneForThePossiblePlaystone = profiler_info.minimum_cpu_usage
                    self.maximum_cpu_usage_createExactlyOneForThePossiblePlaystone = profiler_info.maximum_cpu_usage
                    self.memory_before_createExactlyOneForThePossiblePlaystone = profiler_info.memory_before
                    self.memory_after_createExactlyOneForThePossiblePlaystone = profiler_info.memory_after
                    self.memory_consumed_createExactlyOneForThePossiblePlaystone = profiler_info.memory_consumed
                    self.memory_before_b2h_createExactlyOneForThePossiblePlaystone = profiler_info.memory_before_b2h
                    self.memory_after_b2h_createExactlyOneForThePossiblePlaystone = profiler_info.memory_after_b2h
                    self.memory_consumed_b2h_createExactlyOneForThePossiblePlaystone = profiler_info.memory_consumed_b2h

                elif profiler_info.function_executed == "printFormulaFile":
                    self.function_executed_printFormulaFile = profiler_info.function_executed
                    self.file_executed_printFormulaFile = profiler_info.file_executed
                    self.execution_time_printFormulaFile = profiler_info.execution_time.total_sec
                    self.average_cpu_usage_printFormulaFile = profiler_info.average_cpu_usage
                    self.minimum_cpu_usage_printFormulaFile = profiler_info.minimum_cpu_usage
                    self.maximum_cpu_usage_printFormulaFile = profiler_info.maximum_cpu_usage
                    self.memory_before_printFormulaFile = profiler_info.memory_before
                    self.memory_after_printFormulaFile = profiler_info.memory_after
                    self.memory_consumed_printFormulaFile = profiler_info.memory_consumed
                    self.memory_before_b2h_printFormulaFile = profiler_info.memory_before_b2h
                    self.memory_after_b2h_printFormulaFile = profiler_info.memory_after_b2h
                    self.memory_consumed_b2h_printFormulaFile = profiler_info.memory_consumed_b2h

                else:
                    print(profiler_info.function_executed, "profiler_info.function_executed")