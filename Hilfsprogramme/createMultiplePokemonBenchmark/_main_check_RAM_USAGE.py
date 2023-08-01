import psutil
import time
import os
import re

kill_enabled = False

def check_total_memory_usage():
    global kill_enabled
    mem = psutil.virtual_memory()
    if mem.percent >= 90:
        print(f"Aktueller Speicherverbrauch: {mem.percent}% von insgesamt {mem.total / (1024**3)}GB")

    if mem.percent >= 95:
        kill_enabled = True
    else:
        kill_enabled = False

def check_memory_usage():
    global kill_enabled
    # Gibt alle laufenden Prozesse zurück
    for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'memory_info', 'username']):
        # Überprüft, ob der Speicher > 100GB und ob der Prozess vom aktuellen Benutzer ausgeführt wird
        if proc.info['memory_info'].rss > 100 * (1024 ** 3) and proc.info['username'] == os.getlogin():
            # Überprüft, ob der Prozessname dem gesuchten Muster entspricht
            if re.search(r'python3 src/_main.py benchmark_2/multiple_pokemon_0_[0-9]{2}/.*', ' '.join(proc.info['cmdline'])):
                if kill_enabled:
                    print(f"Prozess mit PID {proc.info['pid']} verwendet mehr als 100GB Speicher. ", proc.info['cmdline'])
                # Entfernt alles vor "_main.py "
                proc_cmd = ' '.join(proc.info['cmdline']).split('_main.py ', 1)[1]
                # Gibt die PIDs der Prozesse aus, die eine ähnliche Befehlszeile haben
                for p in psutil.process_iter(['pid', 'name', 'cmdline', 'username']):
                    if proc.info['username'] == os.getlogin() and proc_cmd in ' '.join(p.info['cmdline']):
                        if kill_enabled:
                            print(f"Ähnlicher Prozess gefunden: PID {p.info['pid']}", proc.info['cmdline'])
                            print("killed")
                            os.kill(p.info['pid'], 9)
                if kill_enabled:
                    kill_enabled = False  # Setzt die Variable zurück, nachdem die Prozesse beendet wurden

while True:
    check_total_memory_usage()
    check_memory_usage()
    time.sleep(60)  # Wartet
