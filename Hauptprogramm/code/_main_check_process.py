# -*- coding: utf-8 -*-
import subprocess
import time
from datetime import datetime
import getpass
import re
import os
import subprocess
from collections import defaultdict


# Global variables for process information
benchmark_processes = defaultdict(list)
structured_benchmark_processes = defaultdict(list)

# Create a new dictionary with individual process information values
def create_process_info_dict(line, pattern):
    info_parts = line.split()
    process_info_dict = {
        "PID": info_parts[0],  # Process ID, a unique identifier for the process
        "USER": info_parts[1],  # User who owns the process
        "PRI": int(info_parts[2]),  # Process priority
        "NI": int(info_parts[3]),  # Nice value of the process, a user/kernel mode indicator
        "VSZ": int(info_parts[4]),  # Virtual memory used by the process in kilobytes
        "RSS": int(info_parts[5]),  # Resident Set Size, the physical memory used by the process in kilobytes
        "%CPU": float(info_parts[6]),  # Percentage of CPU time used by the process
        "%MEM": float(info_parts[7]),  # Percentage of physical memory used by the process
        "TIME": info_parts[8],  # Total CPU time consumed by the process
        "CMD": " ".join(info_parts[9:]),  # Command that started the process
        "TIME_STARTED": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "PATTERN_ALL": pattern,
        "PATTERN_MODIFIED": pattern[:-2].replace('.', '-').replace('/', '__')
    }
    return process_info_dict

# New method to check if all current processes exist
def check_and_update(processes, new_process):
    for new in new_process:
        # Check if a process with the same PID already exists in the processes list
        if new["PID"] not in [p["PID"] for p in processes]:
            # If not, append the new process to the list
            processes.append(new)
    return processes


def print_process_info(user):
    command = ['ps', '-u', user, '-o', 'pid,user,pri,ni,vsz,rss,pcpu,pmem,time,cmd']
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    output = ""
    pattern = r'benchmark/retro/[^/]*\.gif\.txt -'

    if stdout:
        output = stdout.decode()
        # Get all lines
        lines = output.split("\n")
        for line in lines:
            match = re.search(pattern, line)
            if match:
                process_info = create_process_info_dict(line.strip(), match.group())
                benchmark_processes[match.group()].append(line.strip())
                # Update structured_benchmark_processes dictionary only with new processes
                structured_benchmark_processes[match.group()] = check_and_update(structured_benchmark_processes[match.group()], [process_info])

    if stderr:
        print("Standard Error:\n" + stderr.decode())

    # Write the output to a file
    # with open("_running_process.txt", "a") as file:
    #     file.write(f"\n{datetime.now()}\n")  # Write current time
    #     file.write(output)
    #     # Separate benchmark processes with a line
    #     file.write("\n" + "-" * 50 + "\n")
    #     for key, values in benchmark_processes.items():
    #         file.write(key + "\n")
    #         for value in values:
    #             file.write("\t" + value + "\n")
    #     file.write("\n" + "-" * 50 + "\n")
    #     # Print structured dictionary
    #     file.write("\n" + "=" * 50 + "\n")
    #     for key, values in structured_benchmark_processes.items():
    #         file.write(key + "\n")
    #         for value in values:
    #             file.write("\t" + str(value) + "\n")
    #     file.write("\n" + "=" * 50 + "\n")

    # Print dictionaries
    for key, values in benchmark_processes.items():
        #print(key)
        for value in values:
            #print("\t" + value)
            pass
    
    #print("\n" + "=" * 50 + "\n")
    for key, values in structured_benchmark_processes.items():
        #print(key)
        for value in values:
            #print("\t" + str(value))
            pass
    #print("\n" + "=" * 50 + "\n")

# Helper function to get the latest start time among processes belonging to a given pattern
def get_latest_time_started(pattern):
    # Get the start times of all processes belonging to this pattern
    start_times = [datetime.strptime(proc["TIME_STARTED"], "%Y-%m-%d %H:%M:%S") for proc in structured_benchmark_processes[pattern]]
    # Find the latest start time
    latest_start_time = max(start_times)
    return latest_start_time

def modify_dir_name(dir_name):
    return dir_name[:-2].replace('.', '-').replace('/', '__')


def check_files_and_time(wait_time):
    # List of files to be checked inside the folders
    required_files = ["collected_info.txt", "_finalSolution.png", "_file_problem.cnf.res", "_file_problem.cnf"]
    wait_time_in_sec = wait_time * 60

    # Path to the main directory
    main_dir_path = "img"
    first_time_dir_name = False
    first_time_keys = False
    first_time_dir_path = False
    first_time_files_in_dir = False
    first_time_all_files_present = False
    first_time_current_time = False
    first_time_latest_start_time = False
    first_time_elapsed_time = False
    first_time_pids = False

    # Traverse all subdirectories in 'main_dir_path'
    for dir_name in os.listdir(main_dir_path):
        if first_time_dir_name:
            #print(f"dir_name: {dir_name}")
            first_time_dir_name = True
            #print(f"structured_benchmark_processes.keys():{structured_benchmark_processes.keys()}")

        # Traverse all dictionary names
        for key in list(structured_benchmark_processes.keys()):  # create a list from the keys
            # If 'key' (i.e., PATTERN_MODIFIED) is part of the folder name
            if modify_dir_name(key) in dir_name:
                if first_time_keys:
                    #print(f"key: {key}")
                    first_time_keys = True
                dir_path = os.path.join(main_dir_path, dir_name)
                # List files in the directory
                files_in_dir = os.listdir(dir_path)
                if first_time_dir_path:
                    #print(f"dir_path: {dir_path}")
                    first_time_dir_path = True
                if first_time_files_in_dir:
                    #print(f"files_in_dir: {files_in_dir}")
                    first_time_files_in_dir = True

                # Check if all required files are present in the folder
                all_files_present = all(file in files_in_dir for file in required_files)
                if first_time_all_files_present:
                    #print(f"all_files_present: {all_files_present}")
                    first_time_all_files_present = True

                # If not all files are present
                if not all_files_present:
                    # Get the current time
                    current_time = datetime.now()
                    if first_time_current_time:
                        #print(f"current_time: {current_time}")
                        first_time_current_time = True

                    # Get the latest start time among processes belonging to this pattern
                    latest_start_time = get_latest_time_started(key)
                    if first_time_latest_start_time:
                        #print(f"latest_start_time: {latest_start_time}")
                        first_time_latest_start_time = True

                    # Calculate the elapsed time since the latest start time
                    elapsed_time = (current_time - latest_start_time).total_seconds()
                    if first_time_elapsed_time:
                        #print(f"elapsed_time: {elapsed_time}")
                        first_time_elapsed_time = True

                    # If the elapsed time is greater than 120 seconds
                    if elapsed_time > wait_time_in_sec:
                        # Get the PIDs of all processes belonging to this pattern
                        pids = [proc["PID"] for proc in structured_benchmark_processes[key]]
                        if first_time_pids:
                            #print(f"pids: {pids}")
                            first_time_pids = True

                        # Print the required information
                        #print("Path to the folder:", dir_path)
                        #print("Elapsed time (in seconds):", elapsed_time)
                        #print("Current execution time:", current_time)
                        #print("PIDs of the processes:", pids)

                        start_processes(dir_path, elapsed_time, current_time, pids)

                        # Delete entries from dictionaries
                        del benchmark_processes[key]
                        del structured_benchmark_processes[key]


def write_to_could_not_run_txt(folder_path, elapsed_time, current_time, pids):
    with open("_could_not_run.txt", "a") as file:
        file.write(f"Path to the folder: {folder_path}\n")
        file.write(f"Elapsed time (in seconds): {elapsed_time}\n")
        file.write(f"Current execution time: {current_time}\n")
        file.write(f"PIDs of the processes: {pids}\n")
        file.write("---------------------\n")

def delete_folder(folder_path):
    try:
        # Call the 'rm' command to delete the folder
        subprocess.Popen(["rm", "-r", folder_path])
    except Exception as e:
        pass

def kill_pids(pids):
    for pid in pids:
        try:
            # Call the 'kill' command to kill the process
            subprocess.Popen(["kill", "-9", pid])
        except Exception as e:
            pass

def start_processes(folder_path, elapsed_time, current_time, pids):
    write_to_could_not_run_txt(folder_path, elapsed_time, current_time, pids)

    # Start the subprocess to delete the folder
    delete_folder(folder_path)

    # Start the subprocess to kill the PIDs
    kill_pids(pids)


def main():
    wait_time = 20  # Define the wait time here in minutes
    while True:
        current_user = getpass.getuser()
        print_process_info(current_user)
        check_files_and_time(wait_time)
        time.sleep(60)  # Wait for 60 seconds

if __name__ == "__main__":
    main()
