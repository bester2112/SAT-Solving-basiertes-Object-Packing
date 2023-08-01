import datetime
import logging
import time
from sys import platform
import signal
import threading
from decimal import Decimal
import concurrent.futures


class TimeCalculator:
    def __init__(self, max_time=1000000, task_name=""):
        """
        Initialisiert eine Instanz der TimeCalculator Klasse.

        Args:
            max_time (int, optional): Die maximale Zeit in Sekunden, bevor ein Timeout auftritt. Standardmäßig 1000000.
        """
        self.max_time = max_time
        self.start_time = None
        self.end_time = None
        self.task_name = task_name

    def start(self):
        """
        Startet die Zeitmessung und setzt den Timeout-Alarm.
        """
        self.start_time = datetime.datetime.now()
        self.start_time = time.monotonic_ns()

        if platform == "win32":
            self._timeout_thread = threading.Timer(self.max_time, lambda: self.timeout_handler(0, 0))
            self._timeout_thread.start()
        else:
            signal.signal(signal.SIGALRM, self.timeout_handler)
            signal.alarm(self.max_time)


    def start_with_task_name(self, task_name):
        """
        Startet die Zeitmessung und setzt den Timeout-Alarm mit einem AufgabenNamen.
        """
        self.task_name = task_name
        self.start()

    def stop(self):
        """
        Stoppt die Zeitmessung und deaktiviert den Timeout-Alarm.
        """
        if platform == "win32":
            self._timeout_thread.cancel()
        else:
            signal.alarm(0)
        self.end_time = datetime.datetime.now()
        self.end_time = time.monotonic_ns()

    def get_duration(self):
        """
        Gibt die gemessene Zeitdauer als formatierten String in Sekunden zurück.

        Returns:
            str: Die formatierte Zeitdauer als String in Sekunden.
        """
        #time_diff = self.end_time - self.start_time
        #total_seconds = time_diff.total_seconds()
        time_diff = (self.end_time - self.start_time) / 1_000_000_000  # Umwandlung in Sekunden
        return self.calculate_time(time_diff)
        #return self.calculate_time(total_seconds)

    @staticmethod
    def timeout_handler(signum, frame):
        """
        Timeout-Handler, der eine TimeoutError auslöst.

        Args:
            signum: Die Signalnummer.
            frame: Der aktuelle Stack Frame.

        Raises:
            TimeoutError: Wenn das Programm zu lange zur Ausführung benötigt.
        """
        raise TimeoutError("Timeout reached, terminating code.")

    def calculate_time(self, total_seconds):
        """
        Konvertiert eine Anzahl von Sekunden in einen formatierten String.

        Args:
            total_seconds (float): Die Anzahl der Sekunden, die konvertiert werden sollen.

        Returns:
            str: Ein String, der die Anzahl der Sekunden im Format DD:HH:MM:SS:MS repräsentiert.
        """
        total_milliseconds = total_seconds * 1000
        rounded_milliseconds = round(total_milliseconds)
        rounded_seconds, milliseconds = divmod(rounded_milliseconds, 1000)
        seconds = int(rounded_seconds)

        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        if self.task_name == "":
            myString = "Runtime: TotalSec: {:.3f} == {:02d}.{:03d} seconds, {:02d} minutes, {:02d} hours, {:02d} days".format(
                total_seconds, seconds, milliseconds, minutes, hours, days)
        else:
            myString = "Runtime {}: TotalSec: {:.3f} == {:02d}.{:03d} seconds, {:02d} minutes, {:02d} hours, {:02d} days".format(
                self.task_name, total_seconds, seconds, milliseconds, minutes, hours, days)

        return myString

    def measure_and_run(self, taskname, function, *args):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(function, *args)
            try:
                self.start_with_task_name(taskname)
                result = future.result(timeout=self.max_time)  # Setzt das Timeout
            except concurrent.futures.TimeoutError:
                if self.task_name == "":
                    print("Timeout of " + str(
                        self.max_time) + "s reached, terminating code. No Solution found in that time")
                    logging.debug("Timeout of " + str(
                        self.max_time) + "s reached, terminating code. No Solution found in that time")
                else:
                    print("Timeout of " + str(self.max_time) + "s for \"" + str(
                        self.task_name) + "\" reached, terminating code. No Solution found in that time")
                    logging.debug("Timeout of " + str(self.max_time) + "s for \"" + str(
                        self.task_name) + "\" reached, terminating code. No Solution found in that time")
                quit()
            finally:
                self.stop()
                logging.debug(self.get_duration())

        return result

