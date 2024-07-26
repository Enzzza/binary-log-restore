import argparse
import os
import shutil
import subprocess
import sys
from tqdm import tqdm
from datetime import datetime

# Utility functions
def get_timestamp():
    now = datetime.now()
    return now.strftime("%Y-%m-%d_%H-%M-%S")

def safe_remove(path):
    try:
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
    except OSError as e:
        print(f"Error removing {path}: {e}")

def create_directory(directory):
    try:
        os.makedirs(directory, exist_ok=True)
    except OSError as e:
        print(f"Error creating {directory}: {e}")

def get_log_time(log_file_path, search_phrase):
    with open(log_file_path, "r") as log_file:
        for line in log_file:
            if search_phrase in line:
                return line.strip().split(" - ")[0]
    return None

# Function to prepare directories
def prepare_directories(output_dir):
    print("Preparing directories for dump...")
    directories = [output_dir]
    for directory in directories:
        safe_remove(directory)

    for directory in directories:
        create_directory(directory)

def execute_command(command, description):
    try:
        with tqdm(total=100, desc=description) as pbar:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            for line in iter(process.stdout.readline, b''):
                print(line.decode().strip())

            if process.stderr is not None:
                stderr_output = process.stderr.read().decode().strip()
                if stderr_output:
                    print(stderr_output)

            return_code = process.wait()

            pbar.update(100 - pbar.n)
            if return_code == 0:
                print(f"Command executed successfully!")
            else:
                raise subprocess.CalledProcessError(return_code, command)

    except subprocess.CalledProcessError as e:
        print(f"Command failed with return code {e.returncode}")
        if e.stderr:
            print(e.stderr.decode().strip())
        raise e

    except Exception as e:
        print(f"Exception occurred: {e}")
        raise e 


# Function to perform database dump
def perform_dump(remote_host, remote_user, remote_password, output_dir, database, log_dump):
    print("Performing database dump from remote server...")
    dump_command = [
        "mydumper",
        f"--host={remote_host}",
        f"--user={remote_user}",
        f"--password={remote_password}",
        f"--outputdir={output_dir}",
        "-G", "-E", "-R", "--compress", "--build-empty-files",
        "--threads=4", "--compress-protocol",
        f"--database={database}",
        f"--logfile={log_dump}",
        "--less-locking",
        "--verbose=3",
        "--clear"
    ]
    execute_command(dump_command, "Load Progress")
    start_time = get_log_time(log_dump, "Started dump at:")
    return start_time

# Function to perform database load
def perform_load(local_user, local_password, output_dir, database, log_load):
    print("Performing database load to local server...")
    load_command = [
        "myloader",
        "--host=localhost",
        f"--user={local_user}",
        f"--password={local_password}",
        f"--directory={output_dir}",
        f"--database={database}",
        "--threads=4",
        "--verbose=3",
        f"--logfile={log_load}"
    ]
    execute_command(load_command, "Load Progress")
    end_time = get_log_time(log_load, "Errors found:")
    return end_time

# Main execution
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Database dump and load script.")
    parser.add_argument("--remote-host", type=str, required=True, help="Remote host IP address")
    parser.add_argument("--remote-user", type=str, required=True, help="Remote user name")
    parser.add_argument("--remote-password", type=str, required=True, help="Remote user password")
    parser.add_argument("--local-user", type=str, required=True, help="Local user name")
    parser.add_argument("--local-password", type=str, required=True, help="Local user password")
    parser.add_argument("--output-dir", type=str, required=True, help="Output directory for dump files")
    parser.add_argument("--database", type=str, required=True, help="Database name")
    parser.add_argument("--log-dir", type=str, required=False, default="/home/vagrant", help="Output directory for dump files")

    # Generate example command for argparse help
    example_command = "python remote_load.py "
    example_command += "--remote-host 192.168.56.11 "
    example_command += "--remote-user root "
    example_command += "--remote-password password "
    example_command += "--local-user root "
    example_command += "--local-password password "
    example_command += "--output-dir /home/smartmate_dump "
    example_command += "--database smartmate "

    parser.epilog = f"Example:\n\n{example_command}"

    args = parser.parse_args()

    timestamp = get_timestamp()
    log_dump = os.path.join(args.log_dir, f"{timestamp}-{args.database}-dump-logs.txt")
    log_load = os.path.join(args.log_dir, f"{timestamp}-{args.database}-load-logs.txt")
    print(f"Dumping logs to the: {log_dump} and {log_load}");

    try:
        prepare_directories(args.output_dir)
        dump_start_time = perform_dump(args.remote_host, args.remote_user, args.remote_password, args.output_dir, args.database, log_dump)
        print("\n\n")
        load_finish_time = perform_load(args.local_user, args.local_password, args.output_dir, args.database, log_load)

        print("\nDatabase dump and load completed.")
        print(f"Dump start time: {dump_start_time}")
        print(f"Load finish time: {load_finish_time}")
    except Exception as e:
        print(f"Error occurred: {e}")
        sys.exit(1)