import os
import time
import schedule

GB = 1 << 30  # 1GB in Bytes
MB = 1 << 20  # 1MB in Bytes
TRACK_TIME = 22 * 60  # 22 minutes in seconds
FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")  # Relativer Pfad zum "img" Verzeichnis
TRACKED_FILES = {}  # Dict zum Speichern der Dateien und der Zeit, in der sie getrackt wurden
DELETED_LOG = "deleted_files_log.txt"  # Log-Datei

def track_files():
    for foldername, subfolders, filenames in os.walk(FILE_PATH):
        for filename in filenames:
            file = os.path.join(foldername, filename)
            try:
                size = os.path.getsize(file)
                is_gt_1gb = size > GB  # Prüfe, ob Datei größer als 1GB ist

                is_gt_900mb = size > 900 * MB  # Prüfe, ob Datei größer als 900MB ist
                if is_gt_900mb:
                    print(f"File: {file}, Size: {size} bytes, Is greater than 1GB: {is_gt_1gb}")  # Drucke Dateiinformationen aus
                if is_gt_1gb:
                    if file not in TRACKED_FILES:
                        TRACKED_FILES[file] = time.time()  # Track Datei und Zeitpunkt
                    elif time.time() - TRACKED_FILES[file] > TRACK_TIME:  # Wenn die Datei länger als 22 Minuten getrackt wurde
                        with open(DELETED_LOG, "a") as log:
                            log.write(f"Deleted: {file} at {time.ctime()}\n")  # Loggen Sie das Löschen der Datei
                        print(f"Deleted: {file}")  # Drucke die gelöschte Datei aus
                        os.remove(file)  # Lösche die Datei
                        del TRACKED_FILES[file]  # Entferne die Datei aus den getrackten Dateien
            except Exception as e:
                print(f"Couldn't process file {file}: {str(e)}")

def main():
    # Plane die Funktion jede Minute
    schedule.every(1).minutes.do(track_files)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
