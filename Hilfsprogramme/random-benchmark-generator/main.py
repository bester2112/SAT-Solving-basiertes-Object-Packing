import logging
import os
import platform
import sys
import argparse
import time
import re
import os
import platform
import getpass

import requests
from benchmark import Benchmark
from areaPlacer import AreaPlacer
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
import datetime
import smtplib
from email.message import EmailMessage

def are_benchmarks_equal(benchmark1, benchmark2):
    if benchmark1.width != benchmark2.width or benchmark1.height != benchmark2.height:
        return False

    shapes1 = benchmark1.shapes
    shapes2 = benchmark2.shapes

    if len(shapes1) != len(shapes2):
        return False

    for shape1, count1 in shapes1.items():
        found = False
        for shape2, count2 in shapes2.items():
            if shape1 == shape2 and count1 == count2:
                found = True
                break
        if not found:
            return False
    return True

class Main:
    @staticmethod
    def shapes_with_less_hashes(benchmark, threshold):
        for shape, _ in benchmark.shapes.items():
            if shape.number_of_hashes < threshold:
                return True
        return False

    @staticmethod
    def count_shapes_with_one_hash(benchmark):
        count = 0
        for shape, shape_count in benchmark.shapes.items():
            if shape.number_of_hashes == 1:
                count += shape_count
        return count

    @staticmethod
    def shapes_within_hash_range(benchmark, min_threshold, max_threshold):
        for shape, _ in benchmark.shapes.items():
            if min_threshold <= shape.number_of_hashes <= max_threshold:
                return True
        return False

    def __init__(self):
        self.fileName = ""
        self.config_parameters = {}
        self.text = "Hallo Welt"
        self.receiver = "4915156666696"
        self.sender = "GPU Server"
        self.client_id = "382911899125435991853"
        self.client_secret = "L1X8Rf3VsExJKPEf3KPDC"

    def parse_args(self, argv):
        parser = argparse.ArgumentParser()

        # positionals arguments (always required)
        parser.add_argument("filename", type=str, help="file which should be executed")
        parser.add_argument("-s", "--seconds", type=int, help="timeinSeconds")
        args = parser.parse_args(argv)

        self.fileName = args.filename

        self.config_parameters = self.read_config_file(args.filename)

        return args

    def read_config_file(self, config_filename):
        config_parameters = {}
        with open(config_filename, 'r') as config_file:
            for line in config_file:
                key, value = line.strip().split('=')
                if value.isdigit():  # Überprüfen, ob der Wert numerisch ist
                    config_parameters[key] = int(value)
                else:
                    config_parameters[key] = value  # Wenn nicht numerisch, speichern Sie den Wert als String
        return config_parameters

    def configure_logging(self):
        log_filename = os.path.basename(self.fileName)
        log_filename = os.path.splitext(log_filename)[0] + ".log"
        log_path = os.path.join("logs", log_filename)

        if not os.path.exists("logs"):
            os.mkdir("logs")

        logging.basicConfig(filename=log_path, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    def run(self):
        self.parse_args(sys.argv[1:])
        config_params = self.config_parameters
        self.configure_logging()  # Logging konfigurieren

        minX, maxX = config_params["minX"], config_params["maxX"]
        minY, maxY = config_params["minY"], config_params["maxY"]
        min_pixel = config_params["min_pixel"]
        max_pixel = config_params["max_pixel"]
        threshold = config_params["threshold"]
        minThreshold = config_params["minThreshold"]
        maxThreshold = config_params["maxThreshold"]
        maxOneHashLimit = config_params["maxOneHash"]
        countPerBenchmark = config_params["countPerBenchmark"]
        maxFailsLimitReached = config_params["maxFailsLimitReached"]
        maxFailsLimitCount = config_params["maxFailsLimitCount"]
        maxFailsLimit = config_params["maxFailsLimit"]
        fileText = config_params["fileText"]
        maxFailsCount = config_params["maxFailsCount"]
        generated_benchmarks = set()
        maxOneHash = 1

        for width in range(minX, maxX + 1):
            for height in range(minY, maxY + 1):
                n = 0
                while n < countPerBenchmark:
                    area_placer = AreaPlacer(width, height, min_pixel, max_pixel)
                    final_grid = area_placer.place_areas()

                    #logging.debug(f"Grid for width={width}, height={height}:")
                    #for row in final_grid:
                    #    logging.debug(row)

                    shapes = area_placer.generate_shapes(final_grid)
                    benchmark = Benchmark(width, height, shapes)

                    is_duplicate = any(are_benchmarks_equal(benchmark, existing_benchmark) for existing_benchmark in generated_benchmarks)

                    lessThenThreshold = Main.shapes_with_less_hashes(benchmark, threshold)
                    oneHash = Main.count_shapes_with_one_hash(benchmark)
                    withinRange = Main.shapes_within_hash_range(benchmark, minThreshold, maxThreshold)

                    if not is_duplicate and not withinRange and oneHash <= maxOneHash:
                        generated_benchmarks.add(benchmark)
                        area_placer.save_benchmark(width, height, shapes, n, fileText, oneHash)
                        n += 1
                        maxFailsCount = 0
                        logging.debug("File saved")
                    else:
                        maxFailsCount = maxFailsCount + 1
                        if maxFailsCount > maxFailsLimit:
                            if maxFailsLimitReached < maxOneHashLimit:
                                maxFailsLimitReached = maxFailsLimitReached + 1
                                maxOneHash = maxOneHash + 1
                                maxFailsCount = 0
                                n = 0
                            else:
                                n = countPerBenchmark + 1 #todo
                                maxFailsCount = 0
                                maxFailsLimitReached = 0
                    logging.debug(str("maxFailsCount") + str(maxFailsCount))

                maxOneHash = 1
                generated_benchmarks = set()

    def run_parallel(self, width_height_offset, config_params):
        width, height, offset = width_height_offset
        generated_benchmarks = set()
        maxOneHash = offset
        countPerBenchmark = config_params["countPerBenchmark"]
        maxFailsLimitReached = config_params["maxFailsLimitReached"]
        maxFailsLimitCount = config_params["maxFailsLimitCount"]
        maxFailsLimit = config_params["maxFailsLimit"]
        fileText = config_params["fileText"]
        maxFailsCount = config_params["maxFailsCount"]
        min_pixel = config_params["min_pixel"]
        max_pixel = config_params["max_pixel"]
        threshold = config_params["threshold"]
        minThreshold = config_params["minThreshold"]
        maxThreshold = config_params["maxThreshold"]
        maxOneHashLimit = config_params["maxOneHash"]

        start_time = time.time()

        n = 0
        while n < countPerBenchmark:
            if os.path.exists("terminate.txt"):
                print("Fehler: 'terminate.txt' gefunden, Programm wird beendet.")
                sys.exit(1)
            area_placer = AreaPlacer(width, height, min_pixel, max_pixel)
            final_grid = area_placer.place_areas()

            shapes = area_placer.generate_shapes(final_grid)
            benchmark = Benchmark(width, height, shapes)

            is_duplicate = any(
                are_benchmarks_equal(benchmark, existing_benchmark) for existing_benchmark in generated_benchmarks)

            lessThenThreshold = Main.shapes_with_less_hashes(benchmark, threshold)
            oneHash = Main.count_shapes_with_one_hash(benchmark)
            withinRange = Main.shapes_within_hash_range(benchmark, minThreshold, maxThreshold)

            if not is_duplicate and not withinRange and oneHash == maxOneHash:
                generated_benchmarks.add(benchmark)
                area_placer.save_benchmark(width, height, shapes, n, fileText, oneHash)
                n += 1
                maxFailsCount = 0
                logging.debug("File saved")
            else:
                maxFailsCount = maxFailsCount + 1
                if maxFailsCount > maxFailsLimit:
                    # if maxFailsLimitReached < maxOneHashLimit:
                    #     maxFailsLimitReached = maxFailsLimitReached + 1
                    #     maxOneHash = maxOneHash + 1
                    #     maxFailsCount = 0
                    #     n = 0
                    # else:
                        n = countPerBenchmark + 1
                        maxFailsCount = 0
                        maxFailsLimitReached = 0
            logging.debug(str("maxFailsCount") + str(maxFailsCount))

        end_time = time.time()
        elapsed_time = end_time - start_time
        self.send_batch_email(config_params["fileText"], str(width_height_offset), elapsed_time)

    def is_linux(self) -> bool:
        current_os = platform.system()
        return current_os == "Linux"

    def format_seconds(self, seconds: float) -> str:
        MINUTE = 60
        HOUR = MINUTE * 60
        DAY = HOUR * 24
        MONTH = DAY * 30
        YEAR = DAY * 365

        years, remainder = divmod(seconds, YEAR)
        months, remainder = divmod(remainder, MONTH)
        days, remainder = divmod(remainder, DAY)
        hours, remainder = divmod(remainder, HOUR)
        minutes, remainder = divmod(remainder, MINUTE)
        secs = round(remainder)

        time_units = [
            ("Jahr", int(years)),
            ("Monat", int(months)),
            ("Tag", int(days)),
            ("h", int(hours)),
            ("min", int(minutes)),
            ("s", int(secs)),
        ]

        formatted_time = []
        for unit, value in time_units:
            if value > 0:
                formatted_time.append(f"{value}{unit}")

        return ", ".join(formatted_time)

    def run_all_configs(self):
        text = "Hallo Welt"
        receiver = "4915156666696"
        sender = "MacBook"
        client_id = "382911899125435991853"
        client_secret = "L1X8Rf3VsExJKPEf3KPDC"

        config_files = [file for file in os.listdir("configs") if file.endswith(".txt")]

        for config_file in config_files:
            print(f"Starte die parallele Ausführung für die Konfigurationsdatei: {config_file}")
            text = f"Starte : {config_file}"
            #if not self.is_linux():
            #response_text = self.send_sms(text, receiver, sender, client_id, client_secret)
            self.send_email(config_file, "Start")
            #print(response_text)
            print("email Send")

            start_time = time.time()

            config_params = self.read_config(os.path.join("configs", config_file))
            self.run_parallel_start(config_params, config_file)

            end_time = time.time()
            elapsed_time = end_time - start_time
            time_passed_str = self.format_seconds(elapsed_time)
            print(f"Parallele Ausführung für {config_file} abgeschlossen. Dauer: {time_passed_str} Sekunden")
            text = f"Dauer: {time_passed_str}. Ausführung für {config_file} "
            self.send_email(config_file, text)
            #response_text = self.send_sms(text, receiver, sender, client_id, client_secret)
            #print(response_text)
            print("email Send")

    def read_config(self, config_path):
        with open(config_path, 'r') as file:
            config_params = {}
            for line in file.readlines():
                key, value = line.strip().split('=')
                config_params[key] = self.parse_value(value)
        return config_params

    @staticmethod
    def extract_value_from_filename(filename):
        pattern = r"config-(\d+)-.*\.txt"
        match = re.search(pattern, filename)
        if match:
            return int(match.group(1))
        return None

    @staticmethod
    def should_generate_benchmark(width, height, maxOneHash, mod_Value):
        for offset in range(maxOneHash):
            if ((width * height) % mod_Value) - offset == 0:
                print("width " + str(width) + " height " + str(height) + " mod " + str(mod_Value) + " offset " + str(offset) + " maxOne " + str(maxOneHash))
                return True, offset
        return False, None

    def run_parallel_start(self, config_params, config_file):
        self.config_parameters = config_params
        self.configure_logging()

        mod_Value = self.extract_value_from_filename(config_file)

        minX, maxX = config_params["minX"], config_params["maxX"]
        minY, maxY = config_params["minY"], config_params["maxY"]

        maxOneHash = config_params["maxOneHash"]

        # Breite und Höhe als Liste von Tupeln erstellen
        #width_height_list = [(w, h, offset) for w in range(minX, maxX + 1) for h in range(minY, maxY + 1)
        #                     for should_generate, offset in [self.should_generate_benchmark(w, h, maxOneHash, mod_Value)] if should_generate]

        width_height_list = [(w, h, offset) for w in range(minX, maxX + 1) for h in range(minY, maxY + 1)
                             for should_generate, offset in
                             [self.should_generate_benchmark(w, h, maxOneHash, mod_Value)] if should_generate]

        # Die maximale Anzahl der Prozesse ermitteln, die auf Ihrer Maschine ausgeführt werden sollen
        max_processes = min(multiprocessing.cpu_count(), 20)

        # ProcessPoolExecutor erstellen und die run_parallel-Methode parallel ausführen
        #with ProcessPoolExecutor(max_workers=max_processes) as executor:
        #    for _ in executor.map(self.run_parallel, width_height_list, [config_params] * len(width_height_list)):
        #        pass

        with ProcessPoolExecutor(max_workers=max_processes) as executor:
            elapsed_times = list(
                executor.map(self.run_parallel, width_height_list, [config_params] * len(width_height_list)))
            print("Elapsed times for each process:", elapsed_times)

    def parse_value(self, value: str):
        try:
            return int(value)
        except ValueError:
            pass

        try:

            return float(value)
        except ValueError:
            pass

        if value.lower() == 'true':
            return True
        if value.lower() == 'false':
            return False

        if value.startswith('[') and value.endswith(']'):
            return [x.strip() for x in value[1:-1].split(',')]

        return value

    def send_sms(self, text, receiver, sender, client_id, client_secret):
        url = "https://api.smsgatewayapi.com/v1/message/send"
        payload = {
            'message': text,
            'to': receiver,
            'sender': sender
        }
        headers = {
            'X-Client-Id': client_id,
            'X-Client-Secret': client_secret,
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, json=payload)
        return response.text

    def print_user_pc_name(self):
        user_name = getpass.getuser()
        pc_name = platform.node()

        return str(user_name) + " " + str(pc_name)

    def send_batch_email(self, subject, new_message, elapsed_time, batch_size=50):
        subject = subject + " " + str(self.print_user_pc_name())

        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%d.%m %H:%M:%S")

        elapsed_time_str = self.format_seconds(elapsed_time)

        # Füge die neue Nachricht zur Textdatei hinzu
        with open("email_data.txt", "a") as email_file:
            email_file.write(f"{formatted_time} {new_message} {elapsed_time_str}\n")

        # Zähle die Anzahl der Zeilen in der Datei
        with open("email_data.txt", "r") as email_file:
            num_lines = sum(1 for line in email_file)

        if num_lines >= batch_size:
            combined_subject = subject
            combined_content = []

            with open("email_data.txt", "r") as email_file:
                for line in email_file:
                    body = line.strip()
                    combined_content.append(body)

            # Konvertiere die Liste von Nachrichten in einen einzigen String mit Zeilenumbrüchen
            combined_content_str = "\n".join(combined_content)


            self.send_combined_email(subject, combined_content_str)


    def send_combined_email(self, subject, content):
        with open('email_credentials.txt', 'r') as f:
            sender_email = f.readline().strip()
            sender_password = f.readline().strip()

        recipient_email = "sat.solver.solution@gmail.com"

        msg = EmailMessage()
        msg.set_content(content)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient_email

        try:
            with smtplib.SMTP_SSL('mail.gmx.net', 465) as server:
                server.login(sender_email, sender_password)
                server.send_message(msg)
                print("E-Mail erfolgreich gesendet!")
                with open("email_data.txt", "w") as email_file:
                    email_file.write("")
        except Exception as e:
            print(f"E-Mail konnte nicht gesendet werden: {e}")


    def send_email(self, subject, content):
        subject = subject + " " + str(self.print_user_pc_name())

        with open('email_credentials.txt', 'r') as f:
            sender_email = f.readline().strip()
            sender_password = f.readline().strip()

        recipient_email = "sat.solver.solution@gmail.com"

        msg = EmailMessage()
        msg.set_content(content)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient_email

        try:
            with smtplib.SMTP_SSL('mail.gmx.net', 465) as server:
                server.login(sender_email, sender_password)
                server.send_message(msg)
                print("E-Mail erfolgreich gesendet!")
        except Exception as e:
            current_time = datetime.datetime.now()
            formatted_time = current_time.strftime("%d.%m %H:%M:%S")

            print(f"E-Mail konnte nicht gesendet werden: {e}")
            with open("email_data.txt", "a") as email_file:
                email_file.write(f"{formatted_time} {content}\n")


if __name__ == "__main__":
    main = Main()

    print(f"Starte die parallele Ausführung für die Konfigurationsdatei: ...")
    start_time = time.time()

    main.run_all_configs()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Parallele Ausführung für ... abgeschlossen. Dauer: {elapsed_time:.2f} Sekunden")
