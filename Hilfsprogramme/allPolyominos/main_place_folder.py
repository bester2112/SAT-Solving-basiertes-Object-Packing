import os
import smtplib
import sys
import shutil
import time
import multiprocessing
import traceback
import datetime
from main_place_2nd_try import main as original_main
from main_place_2nd_try import rotated_main
from main_place_2nd_try import read_polyominos
from main_place_2nd_try import rotate_only
from multiprocessing import Process, Queue
from email.message import EmailMessage


def send_email(subject, content):
    subject = subject + " " + str(datetime.datetime.now())

    with open('email_credentials.txt', 'r') as f:
        sender_email = f.readline().strip()
        sender_password = f.readline().strip()

    recipient_email = "sat.solver.solution@gmail.com"

    msg = EmailMessage()
    msg.set_content(content)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    email_sent = False
    while not email_sent:
        try:
            with smtplib.SMTP_SSL('mail.gmx.net', 465) as server:
                server.login(sender_email, sender_password)
                server.send_message(msg)
                print("E-Mail erfolgreich gesendet!")
                email_sent = True
        except Exception as e:
            print(f"E-Mail konnte nicht gesendet werden, versuche es erneut: {e}")


def call_main_with_timeout(polyomino_file, polyomino_size, polyominos):
    # Erstelle eine Queue, um Ergebnisse zwischen Prozessen auszutauschen
    queue = Queue()

    # Prozess erstellen, der original_main aufruft und Queue als Argument übergibt
    p = Process(target=original_main_here, args=(polyomino_file, polyomino_size, polyominos, queue,))
    # Prozess starten
    p.start()
    # Prozess nach 10 Sekunden beenden
    p.join(40)

    if p.is_alive():
        # Prozess beenden
        p.terminate()

        # rotated_main() bis zu vier Mal aufrufen, wenn original_main() zu lange dauert
        for i in range(4):
            # Prozess erstellen, der rotated_main aufruft und Queue als Argument übergibt
            p = Process(target=rotated_main_here, args=(polyomino_file, polyomino_size, polyominos, queue,))
            # Prozess starten
            p.start()
            # Prozess nach 20 Sekunden beenden
            p.join(20)

            if not p.is_alive():
                # Ergebnis aus der Queue holen
                result = queue.get()
                if result:
                    # rotate_only() für die verbleibenden Iterationen aufrufen
                    for j in range(3 - i):
                        rotate_only()
                    return True
                else:
                    continue

            if p.is_alive():
                p.terminate()
        return False
    else:
        # Ergebnis aus der Queue holen
        result = queue.get()
        return result


def original_main_here(polyomino_file, polyomino_size, polyominos, queue):
    result = original_main(polyomino_file, polyomino_size, polyominos)
    queue.put(result)


def rotated_main_here(polyomino_file, polyomino_size, polyominos, queue):
    result = rotated_main(polyomino_file, polyomino_size, polyominos)
    queue.put(result)


def new_main(directories, polyomino_folder, polyomino_file, polyomino_size):
    total_start_read_polyominos = time.time()  # Startzeit für alle Ordner
    polyominos = read_polyominos('polyomino/' + polyomino_file)

    total_end_read_polyominos = time.time()  # Endzeit für alle Ordner
    total_reading_time = total_end_read_polyominos - total_start_read_polyominos

    print(f"Alle Polyominos wurden in {total_reading_time} Sekunden eingelesen.")
    with open('output.txt', 'a') as file:
        file.write(f"Alle Polyominos wurden in {total_reading_time} Sekunden eingelesen.\n")

    total_start_time = time.time()  # Startzeit für alle Ordner

    for dir_name in directories:
        try:
            dir_start_time = time.time()  # Startzeit für den aktuellen Ordner
            png_files = [f for f in os.listdir(dir_name) if f.endswith('.png')]
            total_files = len(png_files)

            with open('output.txt', 'a') as file:
                file.write(f"Starte die Bearbeitung des Ordners {dir_name} mit {total_files} Dateien.\n")

            for idx, original_file_name in enumerate(png_files, start=1):
                try:

                    if 'terminate.txt' in os.listdir('.'):
                        print("Datei 'terminate.txt' gefunden. Beende das Programm.")
                        break

                    start_time = time.time()  # Startzeit für die aktuelle Datei

                    print(f"Verarbeite Datei {idx} von {total_files} im Ordner {dir_name} - {original_file_name}")
                    original_file_path = os.path.join(dir_name, original_file_name)
                    shutil.copy2(original_file_path, '.')
                    new_file_name = "abra.png"
                    os.rename(original_file_name, new_file_name)

                    result = call_main_with_timeout(polyomino_file, polyomino_size, polyominos)  # Ändern Sie dies, um die Ausführung von original_main zu begrenzen

                    time.sleep(1)

                    if not os.path.exists(original_file_name):
                        os.mkdir(original_file_name)

                    os.rename('abra.png', original_file_name + '.png')
                    os.rename('abra.txt', original_file_name + '.txt')

                    if result:
                        with open('_OK.txt', 'w') as file:
                            file.write("OK")
                    else:
                        with open('_NO.txt', 'w') as file:
                            file.write("NO")

                    files_to_move = []
                    for file in os.listdir('.'):
                        if file.startswith("bool_matrix_") or file.startswith("string_matrix_") or file == original_file_name + '.png' or file == original_file_name + '.txt' or file == '_OK.txt' or file == '_NO.txt':
                            shutil.move(file, os.path.join(original_file_name, file))
                            files_to_move.append(file)

                    if '_OK.txt' in files_to_move:
                        # Erhalten Sie alle bool_matrix und string_matrix Dateien im Ordner
                        bool_matrix_files = [f for f in os.listdir(original_file_name) if f.startswith('bool_matrix_')]
                        string_matrix_files = [f for f in os.listdir(original_file_name) if f.startswith('string_matrix_')]

                        # Sortieren Sie die Dateien nach der Nummer in ihrem Namen und behalten Sie nur die letzte (größte Nummer)
                        bool_matrix_files.sort(key=lambda x: int(x.split('_')[-1].split('.')[0]))
                        string_matrix_files.sort(key=lambda x: int(x.split('_')[-1].split('.')[0]))

                        bool_files_to_delete = bool_matrix_files[:-1]
                        string_files_to_delete = string_matrix_files[:-1]

                        # Löschen Sie alle Dateien, außer derjenigen mit der höchsten Nummer
                        for file in bool_files_to_delete:
                            os.remove(os.path.join(original_file_name, file))

                        for file in string_files_to_delete:
                            os.remove(os.path.join(original_file_name, file))

                    if not os.path.exists('done/' + polyomino_folder + '/' + dir_name + '-ben2'):
                        os.makedirs('done/' + polyomino_folder + '/' + dir_name + '-ben2')

                    if not os.path.exists(os.path.join('done/' + polyomino_folder + '/' + dir_name + '-ben2', original_file_name)):
                        shutil.move(original_file_name, 'done/' + polyomino_folder + '/' + dir_name + '-ben2')

                except Exception as e:
                    error_time = datetime.datetime.now()
                    error_message = traceback.format_exc()
                    email_content = f"Ordner: {dir_name}\nDatei: {original_file_name}\nZeit: {error_time}\nFehler: {error_message}"
                    send_email("Fehler in new_main", email_content)
                finally:
                    end_time = time.time()  # Endzeit für die aktuelle Datei
                    processing_time = end_time - start_time

                    print(f"Datei {original_file_name} wurde in {processing_time} Sekunden verarbeitet.\n")
                    with open('output.txt', 'a') as file:
                        file.write(f"Datei {original_file_name} wurde in {processing_time} Sekunden verarbeitet.\n")

            dir_end_time = time.time()  # Endzeit für den aktuellen Ordner
            dir_processing_time = dir_end_time - dir_start_time

            print(f"Ordner {dir_name} wurde in {dir_processing_time} Sekunden verarbeitet.\n")
            with open('output.txt', 'a') as file:
                file.write(f"Ordner {dir_name} wurde in {dir_processing_time} Sekunden verarbeitet.\n")

        except Exception as e:
            error_time = datetime.datetime.now()
            error_message = traceback.format_exc()
            email_content = f"Polyomino Folder: {polyomino_folder}\nZeit: {error_time}\nFehler: {error_message}"
            send_email("Fehler in new_main", email_content)

    total_end_time = time.time()  # Endzeit für alle Ordner
    total_processing_time = total_end_time - total_start_time

    print(f"Alle Ordner wurden in {total_processing_time} Sekunden verarbeitet.")
    with open('output.txt', 'a') as file:
        file.write(f"Alle Ordner wurden in {total_processing_time} Sekunden verarbeitet.\n")


def run(polyomino_size):
    try:
        directories = ["Gen7-withframe-black", "Gen8-new-withframe-black", "Gen8-withframe-black", "inventory-withframe-black", "misc-withframe-black"]
        polyomino_folder = "polyomino-" + str(polyomino_size)
        polyomino_file = polyomino_folder + ".txt"
        new_main(directories, polyomino_folder, polyomino_file, polyomino_size)
    except Exception as e:
        error_time = datetime.datetime.now()
        error_message = traceback.format_exc()
        email_content = f"Polyomino Folder: {polyomino_folder}\nZeit: {error_time}\nFehler: {error_message}"
        send_email("Fehler in run", email_content)

    finally:
        completion_time = datetime.datetime.now()
        email_content = f"Der Prozess wurde am {completion_time} abgeschlossen."
        send_email("Prozess abgeschlossen", email_content)


if __name__ == "__main__":
    polyomino_size = 10
    run(polyomino_size)
