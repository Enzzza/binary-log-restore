#!/bin/bash

# Check if SERVER_IP is provided as the first argument
if [ -z "$1" ]; then
    echo "Usage: $0 SERVER_IP PORT [CMD]"
    exit 1
else
    SERVER_IP="$1"
fi

# Check if PORT is provided as the second argument, otherwise use default
if [ -z "$2" ]; then
    echo "Usage: $0 SERVER_IP PORT [CMD]"
    exit 1
else
    PORT="$2"
fi

# Check if NUM is provided as the third argument, otherwise use default
if [ -z "$3" ]; then
    CMD="seed 100"
else
    first_arg=$(echo "$3" | cut -d ' ' -f 1)
    second_arg=$(echo "$3" | cut -d ' ' -f 2)
    if [ "$first_arg" = "seed" ]; then
        # Check if second_arg is a number
        if ! [[ "$second_arg" =~ ^[0-9]+$ ]]; then
            echo "Error: Second argument '$second_arg' is not a valid number."
            exit 1
        fi
        CMD="seed $second_arg"
    else
        CMD="$3"
    fi
fi

# Output the resolved variables for verification
echo "Using SERVER_IP: $SERVER_IP"
echo "Using PORT: $PORT"
echo "Executing command: $CMD"

# Example usage of variables in your script (echo to demonstrate)
echo "$CMD" | nc -w 1 "$SERVER_IP" "$PORT"

echo "Done."