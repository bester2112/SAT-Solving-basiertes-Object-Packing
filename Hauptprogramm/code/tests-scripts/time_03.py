import signal
import time

def timeout_handler(signum, frame):
    raise TimeoutError("Timeout reached, terminating code.")

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(5)

try:
    for i in range(3):
        print(i)
        time.sleep(1)

except TimeoutError:
    print("Timeout reached, terminating code.")

finally:
    signal.alarm(0)

print("normal exit")