import argparse
import subprocess


def execute_command(command):
    print(f"Executing command...")
    try:
        subprocess.run(command, shell=True, check=True, executable='/bin/bash')
        print("Command executed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
    except Exception as e:
        print(f"Exception occurred: {e}")

def seed_server1_db(seed_number):
    command = [
        f"/home/vagrant/tools/scripts/execute.sh 192.168.56.10 7337 'seed {seed_number}'",
    ]
    execute_command(command)

def drop_server1_db():
    command = [
        f"/home/vagrant/tools/scripts/execute.sh 192.168.56.10 7337 drop_db",
    ]
    execute_command(command)

def load_data_from_mysql_server1():
    command = [
        f"/home/vagrant/tools/data-loader/example.sh",
    ]
    execute_command(command)

parser = argparse.ArgumentParser(description="Enzzza went bananas!")

parser.add_argument("function", choices=["seed_server1_db", "drop_server1_db", "load_data_from_server1_db"], help="Function to run")

parser.add_argument("arguments", nargs="*", type=int, default=[], help="Arguments for the function")

args = parser.parse_args()

if args.function == "seed_server1_db":
    seed_server1_db(*args.arguments)
elif args.function == "drop_server1_db":
    drop_server1_db()
elif args.function == "load_data_from_server1_db":
    load_data_from_mysql_server1()
else:
    result = "Error: Invalid function name"
