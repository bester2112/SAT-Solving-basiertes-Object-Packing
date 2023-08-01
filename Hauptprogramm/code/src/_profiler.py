import logging
import time
import os
import psutil
import inspect

def bytes2human(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n

class Profiler:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        try:
            mem_before = self.get_process_memory()

            start_cpu_times = psutil.cpu_times()
            start_ram = psutil.virtual_memory()
            start_time = time.monotonic_ns()

            result = self.func(*args, **kwargs)

            end_cpu_times = psutil.cpu_times()
            end_ram = psutil.virtual_memory()
            end_time = time.monotonic_ns()

            mem_after = self.get_process_memory()

            cpu_percentages = psutil.cpu_percent(percpu=True)
            average_cpu = sum(cpu_percentages) / len(cpu_percentages)
            min_cpu = min(cpu_percentages)
            max_cpu = max(cpu_percentages)

            time_diff = (end_time - start_time) / 1_000_000_000  # Umwandlung in Sekunden
            elapsed_time = self.calculate_time(time_diff)

            profiling_results = f"""
                    Function: \"{self.func.__name__}\" from file {inspect.getsourcefile(self.func)}
                    Execution Time: {elapsed_time}
                    Average CPU Usage: {average_cpu}%
                    Minimum CPU Usage: {min_cpu}%
                    Maximum CPU Usage: {max_cpu}%
                    Memory Usage Before: {start_ram}
                    Memory Usage After: {end_ram}
                    Memory Before: {mem_before}, 
                    Memory After: {mem_after}, 
                    Memory Consumed: {mem_after - mem_before}
                    Memory Before B2H: {bytes2human(mem_before)}
                    Memory After B2H: {bytes2human(mem_after)}
                    Memory Consumed B2H: {bytes2human(mem_after - mem_before)}
                    """
        except Exception as e:
            logging.info(f"Error occurred in {self.func} in Profiler: {e}")
            print(f"Error occurred in {self.func} in Profiler: {e}")
            quit()
        return result, profiling_results

    def __get__(self, instance, owner):
        def wrapper(*args, **kwargs):
            return self(instance, *args, **kwargs)
        return wrapper

    def called(self, *args, **kwargs):
        mem_before = self.get_process_memory()

        start_cpu_times = psutil.cpu_times()
        start_ram = psutil.virtual_memory()
        start_time = time.monotonic_ns()

        result = self.func(*args, **kwargs)

        end_cpu_times = psutil.cpu_times()
        end_ram = psutil.virtual_memory()
        end_time = time.monotonic_ns()

        mem_after = self.get_process_memory()

        cpu_percentages = psutil.cpu_percent(percpu=True)
        average_cpu = sum(cpu_percentages) / len(cpu_percentages)
        min_cpu = min(cpu_percentages)
        max_cpu = max(cpu_percentages)

        time_diff = (end_time - start_time) / 1_000_000_000  # Umwandlung in Sekunden
        elapsed_time = self.calculate_time(time_diff)

        profiling_results = f"""
        Function: \"{self.func.__name__}\" from file {inspect.getsourcefile(self.func)}
        Execution Time: {elapsed_time}
        Average CPU Usage: {average_cpu}%
        Minimum CPU Usage: {min_cpu}%
        Maximum CPU Usage: {max_cpu}%
        Memory Usage Before: {start_ram}
        Memory Usage After: {end_ram}
        Memory Before: {mem_before}, 
        Memory After: {mem_after}, 
        Memory Consumed: {mem_after - mem_before}
        Memory Before B2H: {bytes2human(mem_before)}
        Memory After B2H: {bytes2human(mem_after)}
        Memory Consumed B2H: {bytes2human(mem_after - mem_before)}
        """

        return result, profiling_results

    def calculate_time(self, total_seconds):
        total_milliseconds = total_seconds * 1000
        rounded_milliseconds = round(total_milliseconds)
        rounded_seconds, milliseconds = divmod(rounded_milliseconds, 1000)
        seconds = int(rounded_seconds)

        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        myString = "TotalSec: {:.3f} == {:02d}.{:03d} seconds, {:02d} minutes, {:02d} hours, {:02d} days".format(
            total_seconds, seconds, milliseconds, minutes, hours, days)

        return myString

    def get_process_memory(self):
        process = psutil.Process(os.getpid())
        return process.memory_info().rss

@Profiler
def execution():
    arr = []
    for i in range(10000000):
        arr.append(i)

    return arr



if __name__ == "__main__":
    result, profiling_results = execution()
    # Log or print the profiling results
    print(profiling_results)


