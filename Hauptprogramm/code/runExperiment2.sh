#!/bin/bash
# runExperiment.sh
for i in {1..80}; do
    python3 mainTest.py &
    python3 sleep.py # sleeps for 100 milliseconds
done
wait
