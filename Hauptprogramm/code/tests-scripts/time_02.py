import random
import time

def random_finish(timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        random_time = random.choice([5, 6000])
        time.sleep(random_time)
        print("Function finished after {} seconds".format(random_time))
    print("Timeout reached, terminating code.")

random_finish()
