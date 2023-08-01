import os
import time
import fcntl
import threading
import datetime

class Timeout(Exception):
    pass

def write_to_file(data, filename="output.txt", timeout=300):
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, filename)
    with open(file_path, 'a') as f:
        timer = threading.Timer(timeout, lambda: (_ for _ in ()).throw(Timeout()))
        timer.start()
        try:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            try:
                f.write(data + '\n')
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        except Timeout:
            print(f"Process {os.getpid()} timed out after {timeout} seconds.")
        finally:
            timer.cancel()

if __name__ == "__main__":
    now = datetime.datetime.now()
    formatted = now.strftime("%d.%m.%Y %H:%M:%S") + f",{str(now.microsecond // 1000)[:3]}"
    data = f"Process {os.getpid()} at {formatted}"
    write_to_file(data)
