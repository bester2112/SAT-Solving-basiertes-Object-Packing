import re
from execution_time import ExecutionTime
from profiler_info import ProfilerInfo


class Profiler:
    def __init__(self, profiler_name=None, function_executed=None, file_executed=None, execution_time=None, average_cpu_usage=None, minimum_cpu_usage=None, maximum_cpu_usage=None, memory_before_b2h=None, memory_after_b2h=None, memory_consumed_b2h=None):
        self.profiler_name = profiler_name
        self.function_executed = function_executed
        self.file_executed = file_executed
        self.execution_time = execution_time
        self.average_cpu_usage = average_cpu_usage
        self.minimum_cpu_usage = minimum_cpu_usage
        self.maximum_cpu_usage = maximum_cpu_usage
        self.memory_before_b2h = memory_before_b2h
        self.memory_after_b2h = memory_after_b2h
        self.memory_consumed_b2h = memory_consumed_b2h

    def __str__(self):
        return f"Profiler: profiler_name={self.profiler_name}, function_executed={self.function_executed}, file_executed={self.file_executed}, execution_time={self.execution_time}, average_cpu_usage={self.average_cpu_usage}, minimum_cpu_usage={self.minimum_cpu_usage}, maximum_cpu_usage={self.maximum_cpu_usage}, memory_before_b2h={self.memory_before_b2h}, memory_after_b2h={self.memory_after_b2h}, memory_consumed_b2h={self.memory_consumed_b2h}"


    @staticmethod
    def _parse_profiler_block(block: str):
        function_match = re.search(r"Function: \"(?P<function_executed>.+)\" from file (?P<file_executed>.+)", block)
        execution_time_match = re.search(
            r"Execution Time: (?P<total_sec>\d+\.\d+)",
            block)
        average_cpu_usage_match = re.search(r"Average CPU Usage: (?P<average>\d+\.\d+)%", block)
        min_cpu_usage_match = re.search(r"Minimum CPU Usage: (?P<minimum>\d+\.\d+)%", block)
        max_cpu_usage_match = re.search(r"Maximum CPU Usage: (?P<maximum>\d+\.\d+)%", block)
        memory_before_match = re.search(r"Memory Usage Before: (?P<memory_before>\d+)", block)
        memory_after_match = re.search(r"Memory Usage After: (?P<memory_after>\d+)", block)
        memory_consumed_match = re.search(r"Memory Consumed: (?P<memory_consumed>\d+)", block)
        memory_before_b2h_match = re.search(r"Memory Before B2H: (?P<memory_before_b2h>.+)", block)
        memory_after_b2h_match = re.search(r"Memory After B2H: (?P<memory_after_b2h>.+)", block)
        memory_consumed_b2h_match = re.search(r"Memory Consumed B2H: (?P<memory_consumed_b2h>.+)", block)

        function_executed = function_match.group('function_executed') if function_match else None
        file_executed = function_match.group('file_executed') if function_match else None
        execution_time = ExecutionTime(float(execution_time_match.group('total_sec')) if execution_time_match else None, None, None, None, None)
        average_cpu_usage = float(average_cpu_usage_match.group('average')) if average_cpu_usage_match else None
        minimum_cpu_usage = float(min_cpu_usage_match.group('minimum')) if min_cpu_usage_match else None
        maximum_cpu_usage = float(max_cpu_usage_match.group('maximum')) if max_cpu_usage_match else None
        memory_before = int(memory_before_match.group('memory_before')) if memory_before_match else None
        memory_after = int(memory_after_match.group('memory_after')) if memory_after_match else None
        memory_consumed = int(memory_consumed_match.group('memory_consumed')) if memory_consumed_match else None
        memory_before_b2h = memory_before_b2h_match.group('memory_before_b2h') if memory_before_b2h_match else None
        memory_after_b2h = memory_after_b2h_match.group('memory_after_b2h') if memory_after_b2h_match else None
        memory_consumed_b2h = memory_consumed_b2h_match.group(
            'memory_consumed_b2h') if memory_consumed_b2h_match else None

        return ProfilerInfo(
            function_executed=function_executed,
            file_executed=file_executed,
            execution_time=execution_time,
            average_cpu_usage=average_cpu_usage,
            minimum_cpu_usage=minimum_cpu_usage,
            maximum_cpu_usage=maximum_cpu_usage,
            memory_before=memory_before,
            memory_after=memory_after,
            memory_consumed=memory_consumed,
            memory_before_b2h=memory_before_b2h,
            memory_after_b2h=memory_after_b2h,
            memory_consumed_b2h=memory_consumed_b2h
        )

    @staticmethod
    def process(filepath):
        with open(filepath, 'r') as file:
            log_content = file.read()

        # Find all profiler blocks in original format
        profiler_blocks = re.findall(r"\sFunction.*?Memory Consumed B2H: .*?[MKG]\n", log_content, re.DOTALL)

        # Find all profiler blocks in new format
        profiler_CC_methods_blocks = re.findall(
            r"INFO:  (cV|cte|ceoftpProfiler) = \(None, '(.*?)'\)|INFO: (ceoftppProfiler|pffProfiler) = \(None, '(.*?)'\)",
            log_content, re.DOTALL)

        # List to hold all profiler info dictionaries
        profiler_info = []
        profiler_CC_methods_info = []

        # Process each profiler block in original format
        for block in profiler_blocks:
            info = Profiler._parse_profiler_block(block)
            profiler_info.append(info)

        # Process each profiler block in new format
        for match in profiler_CC_methods_blocks:
            # Ignore empty string from unmatched group
            prefix, block, prefix2, block2 = match
            if block:
                # Remove the unnecessary \n characters
                block = block.replace("\\n", "\n")
                info = Profiler._parse_profiler_block(block)
                profiler_CC_methods_info.append(info)
            elif block2:
                # Remove the unnecessary \n characters
                block2 = block2.replace("\\n", "\n")
                info = Profiler._parse_profiler_block(block2)
                profiler_CC_methods_info.append(info)

        return profiler_info, profiler_CC_methods_info





