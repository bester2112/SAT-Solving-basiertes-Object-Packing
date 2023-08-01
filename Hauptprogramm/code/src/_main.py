import concurrent
import fcntl
import multiprocessing
import signal
import sys
import threading
import traceback
import datetime

from _argparser import ArgParser
from _fileparser import FileParser
#from _benchmark import Benchmark
from _clauselCalculator import ClauselCalculator
from _imagecreator import ImageCreator
from _timeCalculator import TimeCalculator
from _profiler import Profiler
import time
import logging
import os
import psutil
import platform as platformm
from sys import platform


"""
This script reads in a file with game data, generates a visual representation of the game, and then calculates the
number of possible solutions for the game using a SAT solver.

The script takes in the following command line arguments:
-f or --file: The path to the file containing the game data. Required.
-t or --time: The time limit (in seconds) for the SAT solver to run. Optional, default is 30 seconds.
-d or --debug: Whether to run in debug mode. Optional, default is False.

The script will output a log file containing debug and info messages, as well as an image of the game board and the
number of possible solutions calculated by the SAT solver.

Usage:
python main.py -f example.txt
"""

class Timeout(Exception):
    pass


class Main():
    @staticmethod
    def create_log_folder(default_logs_folder):
        """
        Creates the logs directory if it doesn't already exist.
        Args:
            None

        Raises:
            None

        Returns:
            result: A string message indicating whether the logs directory was created or already exists.
        """
        check_folder = os.path.isdir(default_logs_folder)

        # If folder doesn't exists, then create it
        if not check_folder:
            os.makedirs(default_logs_folder)
            result = ("created folder : ", default_logs_folder)
        else:
            result = (default_logs_folder, "folder already exists.")
        return result

    # def get_random_string(length):
    #     # choose from all lowercase letter
    #     letters = string.ascii_lowercase
    #     result_str = ''.join(random.choice(letters) for i in range(length))
    #     #print("Random string of length", length, "is:", result_str)
    #     return result_str

    @staticmethod
    def create_session_name(filename:str) -> str:
        """
        Creates a session name using the current time and the input filename.

        perl
        Copy code
        Args:
            filename (str): The input filename.

        Raises:
            None

        Returns:
            sessionName: A string representing the session name.
        """

        lt = time.localtime()
        jahr, monat, tag, stunde, minute = lt[0:5]
        date = f"{tag:02d}-{monat:02d}-{jahr:4d}--{stunde:02d}-{minute:02d}"
        return date + "-" + filename.replace(".", "-").replace(" ", "").replace("/", "__").replace("\\", "__")

    @staticmethod
    def check_file_processed(filename: str, processed_files='processed_files.txt') -> bool:
        with open(processed_files, 'a+') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_SH)
            f.seek(0)
            files = f.read().splitlines()
            if filename in files:
                return True
            return False

    @staticmethod
    def mark_file_as_processed(filename: str, processed_files='processed_files.txt') -> None:
        with open(processed_files, 'a') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            f.write(filename + '\n')
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)

    def configure_logging(self):
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        logging.basicConfig(filename=self.DEFAULT_LOGS_FOLDER_ + self.sessionName_ + ".log",
                            format='%(levelname)s: %(message)s',
                            datefmt='%m-%d %H:%M',
                            level=logging.DEBUG)

    @Profiler
    def run(self) -> None:
        """
        Main function that runs the program.

        Args:
            None

        Raises:
            None

        Returns:
            None
        """
        argParser_ = ArgParser()
        filename_ = argParser_.fileName
        if self.check_file_processed(filename_):
            print(f"File: {filename_} exists already - skipping")
            return

        server_info = {
            "Betriebssystem": str(platformm.system()),
            "Betriebssystem-Version": str(platformm.version()),
            "Server Architektur": str(platformm.machine())
        }
        # Messen Sie die CPU- und RAM-Nutzung während der Ausführung Ihres Programms
        start_cpu_times = psutil.cpu_times()
        start_ram = psutil.virtual_memory()

        time_calculator_main = TimeCalculator()
        time_calculator_main.start_with_task_name("#1369# main without data saving")

        try:
            result = None
            DEFAULT_IMAGE_FOLDER = "img/"
            DEFAULT_LOGS_FOLDER = "logs/"
            if platform == "linux" or platform == "linux2":
                DEFAULT_IMAGE_FOLDER = "img/"
                DEFAULT_LOGS_FOLDER = "logs/"
            elif platform == "win32":
                # get the current directory
                current_dir = os.path.dirname(os.path.abspath(__file__))
                # move one level up
                parent_dir = os.path.dirname(current_dir)

                DEFAULT_IMAGE_FOLDER = os.path.join(parent_dir, "img/")
                DEFAULT_LOGS_FOLDER = os.path.join(parent_dir, "logs/")

            #create session name
            time_calculator_log_folder = TimeCalculator()
            time_calculator_log_folder.start_with_task_name("#1371# create_log_folder")

            try:
                result = self.create_log_folder(DEFAULT_LOGS_FOLDER)

            #except TimeoutError:
                #print("Timeout of " + str(time_calculator_log_folder.max_time) + "s reached, terminating code. No Solution found in that time")

            finally:
                time_calculator_log_folder.stop()

            argParser = None
            sessionName = None

            time_calculator_argparser = TimeCalculator()
            time_calculator_argparser.start_with_task_name("#1372# argparser")

            try:
                argParser = ArgParser()
                sessionName = self.create_session_name(filename=argParser.fileName)

            #except TimeoutError:
                #print("Timeout of " + str(time_calculator_argparser.max_time) + "s reached, terminating code. No Solution found in that time")

            finally:
                time_calculator_argparser.stop()

            self.DEFAULT_LOGS_FOLDER_ = DEFAULT_LOGS_FOLDER
            self.sessionName_ = sessionName
            self.configure_logging()
            #logging.disable(logging.CRITICAL) # DISABLE ALL LOGGING
            #print("Started")
            logging.info("Started")
            logging.info("SessionName = " + str(sessionName))
            logging.info(result)

            time_duration = time_calculator_log_folder.get_duration()
            #print(time_duration)
            logging.info(time_duration)
            time_calculator_log_folder = None

            logging.info("-Argparser-")
            logging.debug("argParser.fileName " + str(argParser.fileName))
            logging.debug("argParser.timeLimit " + str(argParser.timeLimit))
            logging.debug("argParser.model " + str(argParser.model))

            time_duration = time_calculator_argparser.get_duration()
            #print(time_duration)
            logging.info(time_duration)
            time_calculator_argparser = None

            logging.info("-FileParser-")
            fileParser = None

            time_calculator_fileparser = TimeCalculator()
            time_calculator_fileparser.start_with_task_name("#1373# fileparser")

            try:
                fileParser = FileParser(fileName=argParser.fileName, timeLimit=argParser.timeLimit,
                                        debugMode=argParser.debugMode)
                res, fPProfiler = fileParser._check_all()
                logging.debug(f" fPProfiler {fPProfiler}")

            #except TimeoutError:
                #print("Timeout of " + str(time_calculator_fileparser.max_time) + "s reached, terminating code. No Solution found in that time")

            finally:
                time_calculator_fileparser.stop()
                time_duration = time_calculator_fileparser.get_duration()
                #print(time_duration)
                logging.info(time_duration)
                time_calculator_fileparser = None

            logging.debug("fileParser" + str(fileParser))

            logging.info("-ImageCreator-")
            img = None

            time_calculator_imageparser = TimeCalculator()
            time_calculator_imageparser.start_with_task_name("#1374# imageparser")

            try:
                img = ImageCreator(folderName=DEFAULT_IMAGE_FOLDER)
                img.createImageFolder(defaultFolder=DEFAULT_IMAGE_FOLDER, sessionName=sessionName)
                # img.createEmptyField(fieldWidth=5, fieldHeight=5)
                # img.createEmptyFieldWithFilename(fieldWidth=5, fieldHeight=5, fileName="grid-empty-custom.png")

            #except TimeoutError:
                #print("Timeout of " + str(time_calculator_imageparser.max_time) + "s reached, terminating code. No Solution found in that time")

            finally:
                time_calculator_imageparser.stop()
                time_duration = time_calculator_imageparser.get_duration()
                #print(time_duration)
                logging.info(time_duration)
                time_calculator_imageparser = None

            # Logging
            logging.info("-ClauselCalculator-")

            try:
                alleSpielteine = fileParser.allSpielsteine
                spielFeldBreite = fileParser.width
                spielFeldHoehe = fileParser.height
                image = img  # Wenn img ein Pfad ist oder in einer anderen Weise, die pickle versteht
                timeToRun = argParser.timeLimit
                model = argParser.model
                fileName = argParser.fileName

                # Prozess erstellen und starten
                q = multiprocessing.Queue()

                p = multiprocessing.Process(target=self.run_clauselCalculator, args=(
                    alleSpielteine, spielFeldBreite, spielFeldHoehe, image, timeToRun, model, fileName, q))

                p.start()

                # Warten, bis der Prozess beendet ist oder das Zeitlimit erreicht ist
                p.join(3 * argParser.timeLimit)

                # Prüfen, ob der Prozess noch läuft, und wenn ja, diesen beenden
                if p.is_alive():
                    logging.info("Timeout of " + str(
                        3 * argParser.timeLimit) + f"s reached, terminating code for {argParser.fileName}. No Solution found in that time")
                    os.kill(p.pid, signal.SIGTERM)
                else:
                    # Falls der Prozess ordnungsgemäß beendet wurde, das Ergebnis erhalten
                    p_res = p.exitcode
                    logging.debug(f"p_res {p_res}")

            except Exception as e:
                logging.info("Ein Fehler ist aufgetreten: ", str(e))

            # logging.info("-Benchmark-")
            # benchmark = Benchmark(fileName="../benchmark.txt", timeLimit="30s")
            # logging.info(benchmark)
            logging.info("Finished")

        finally:
            time_calculator_main.stop()
            time_duration = time_calculator_main.get_duration()
            # print(time_duration)
            logging.info(time_duration)

        end_cpu_times = psutil.cpu_times()
        end_ram = psutil.virtual_memory()

        # Berechnen Sie die durchschnittliche, minimale und maximale CPU-Nutzung
        cpu_percentages = psutil.cpu_percent(percpu=True)
        average_cpu = sum(cpu_percentages) / len(cpu_percentages)
        min_cpu = min(cpu_percentages)
        max_cpu = max(cpu_percentages)

        # Sammeln Sie die CPU- und RAM-Nutzung
        cpu_ram_info = {
            "CPU Start-Zeit": start_cpu_times,
            "CPU Ende-Zeit": end_cpu_times,
            "Durchschnittliche CPU Nutzung": average_cpu,
            "Minimale CPU Nutzung": min_cpu,
            "Maximale CPU Nutzung": max_cpu,
            "Anfangs RAM": start_ram,
            "End RAM": end_ram,
        }

        # Kombinieren Sie alle gesammelten Informationen
        collected_info = {**server_info, **cpu_ram_info}

        # Schreiben Sie die Informationen in eine Datei (Sie können auch eine Datenbank verwenden)
        with open(img.folderName + 'collected_info.txt', 'a') as f:
            f.write(str(collected_info) + "\n")

        data = f"Process {os.getpid()} at {time.ctime()}"
        current_time = datetime.datetime.now()
        formated_time = current_time.strftime("%d.%m.%Y %H:%M:%S") + f",{str(current_time.microsecond)[:3]}"
        # Warte auf das Ergebnis und speichere es
        cres, cCProfiler, solution = q.get()  # Hole die Ergebnisse aus der Queue
        # Benutze die Ergebnisse
        data_clauselCalculator = solution
        img_folder = img.folderName
        img_file = img_folder + "_finalSolution.png"
        log_file = DEFAULT_LOGS_FOLDER + sessionName + ".log"
        data = {
            "clauselCalculator": data_clauselCalculator,
            "img_folder": img_folder,
            "img_file": img_file,
            "log_file": log_file,
            "ram_cpu_file": img.folderName + 'collected_info.txt',
            "time": formated_time
        }

        self.write_to_file(data)
        # Nach erfolgreicher Ausführung die Datei als verarbeitet markieren
        self.mark_file_as_processed(filename_)
        print(f"finish {argParser.fileName}")

    def signal_handler(self, signum, frame):
        logging.debug(f"Signal {signum} received, terminating...")
        #sys.exit(1)

    # Der Code, der in einem separaten Prozess ausgeführt werden soll
    def run_clauselCalculator(self, alleSpielteine, spielFeldBreite, spielFeldHoehe, image, timeToRun, model, fileName,
                              queue):
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGHUP, self.signal_handler)
        signal.signal(signal.SIGQUIT, self.signal_handler)
        # signal.signal(signal.SIGKILL, signal_handler)  # SIGKILL kann in Python nicht abgefangen werden
        # signal.signal(signal.SIGSTOP, self.signal_handler)
        signal.signal(signal.SIGCONT, self.signal_handler)
        try:
            self.configure_logging()
            clauselCalculator = ClauselCalculator(alleSpielteine=alleSpielteine,
                                                  spielFeldBreite=spielFeldBreite,
                                                  spielFeldHoehe=spielFeldHoehe,
                                                  image=image,
                                                  timeToRun=timeToRun,
                                                  model=model,
                                                  fileName=fileName)
            cres, cCProfiler = clauselCalculator.run()
            solution = clauselCalculator.sh.solution  # Hole die Lösung im untergeordneten Prozess
            queue.put((cres, cCProfiler, solution))  # Füge die Ergebnisse in die Queue ein
        except Exception as e:
            logging.debug(f"Fehler: {e}")
            logging.debug(f"Traceback:")
            logging.debug(traceback.format_exc())

    @staticmethod
    def write_to_file(data, filename="output.txt", timeout=300):
        current_dir = os.getcwd()
        file_path = os.path.join(current_dir, filename)
        with open(file_path, 'a') as f:
            # Starten Sie einen Timer-Thread, der eine Exception auslöst, wenn der Timeout abgelaufen ist.
            timer = threading.Timer(timeout, lambda: (_ for _ in ()).throw(Timeout()))
            timer.start()
            try:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                try:
                    f.write(str(data) + '\n')
                    # Warte 0,1 Sekunden, um den Lock zu testen.
                    time.sleep(0.1)
                finally:
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            #except Timeout:
                #print(f"Process {os.getpid()} timed out after {timeout} seconds.")
            finally:
                timer.cancel()
        return None


if __name__ == "__main__":

    if os.path.exists('terminate.txt'):
        print("Terminate file found, exiting program.")
        quit()

    try:
        time_calculator_complete_main = TimeCalculator()
        time_calculator_complete_main.start_with_task_name("#1370# complete_main")

        try:
            main = Main()
            result, resultProfiler = main.run()
            logging.debug(f"resultProfiler {resultProfiler}")

        #except TimeoutError:
            #print("Timeout of " + str(time_calculator_complete_main.max_time) + "s reached, terminating code. No Solution found in that time")

        finally:
            time_calculator_complete_main.stop()
            time_duration = time_calculator_complete_main.get_duration()
            #print(time_duration)
            logging.info(time_duration)
    except Exception as e:
        logging.error(traceback.format_exc())
        #print(traceback.format_exc())
        # Logs the error appropriately.

