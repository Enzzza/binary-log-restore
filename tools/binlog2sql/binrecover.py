import subprocess
import argparse

def main(args):
    # Construct the command
    command = [
        "/home/vagrant/tools/binlog2sql/binlog2sql/binlog2sql.py",
        f"-h {args.host}",
        f"-u {args.user}",
        f"-p {args.password}",
        f"-d {args.database}",
        f"--start-datetime \"{args.start_datetime}\"",
        f"--stop-datetime \"{args.stop_datetime}\"",
        f"--start-file {args.start_file}",
        "|",
        "cut -f1 -d\"#\"",
        "> bin-backup.sql"
    ]

    # Join command list into a single string
    command_string = " ".join(command)

    # Execute the command
    try:
        subprocess.run(command_string, shell=True, check=True)
        print("Command executed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
    except Exception as e:
        print(f"Exception occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run binlog2sql.py and redirect output to bin-backup.sql")
    parser.add_argument("-H", "--host", required=True, help="MySQL host")
    parser.add_argument("-u", "--user", required=True, help="MySQL user")
    parser.add_argument("-p", "--password", required=True, help="MySQL password")
    parser.add_argument("-d", "--database", required=True, help="Database name")
    parser.add_argument("--start-datetime", required=True, help="Start datetime (YYYY-MM-DD HH:MM:SS)")
    parser.add_argument("--stop-datetime", required=True, help="Stop datetime (YYYY-MM-DD HH:MM:SS)")
    parser.add_argument("--start-file", required=True, help="Start file name")
    
    # Generate example command for argparse help
    example_command = "python binrecover.py "
    example_command += "--host 192.168.56.10 "
    example_command += "--user root "
    example_command += "--password password "
    example_command += "--database smartmate "
    example_command += "--start-datetime \"2024-07-24 13:00:00\" "
    example_command += "--stop-datetime \"2024-07-24 14:30:00\" "
    example_command += "--start-file mysql-bin.000002 "
    parser.epilog = f"Example:\n\n{example_command}"

    args = parser.parse_args()
    main(args)
