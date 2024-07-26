    #!/bin/bash

    PORT="7337"
    db_user='root'
    db_pass='password'
    db_addr='localhost'
    db_name='smartmate'

    # Start listening on the specified port and echo back any received data
    nc -l -p "$PORT" -k | while IFS= read -r line; do
        first_arg=$(echo "$line" | cut -d ' ' -f 1)
        second_arg=$(echo "$line" | cut -d ' ' -f 2)
        if [ "$first_arg" = "seed" ]; then
            if ! [[ "$second_arg" =~ ^[0-9]+$ ]]; then
                echo "Error: Second argument '$second_arg' is not a valid number."
            fi
            echo "Seeding database with $second_arg items!"
            source /home/vagrant/tools/data-generator/venv/bin/activate && python /home/vagrant/tools/data-generator/sql.py --seed_number "$second_arg"
        elif [ "$first_arg" = "drop_db" ]; then
            echo "Dropping database!"
            mysql -u"$db_user" -p"$db_pass" -h"$db_addr" -e "DROP DATABASE IF EXISTS $db_name;"
        else
            echo "Unknown command: $first_arg"
        fi
    done
    