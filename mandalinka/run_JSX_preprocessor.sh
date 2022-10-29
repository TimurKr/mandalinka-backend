#!/usr/bin/env bash
(
    trap 'kill 0' SIGINT;
    for SRC in $(find . -type d -name js); 
    do
        if [ -d ${SRC}/jsx ];
        then
            printf "Running babel watcher for ${SRC}/jsx\n" &
            npx babel -w ${SRC}/jsx -d ${SRC} --presets react-app/prod &
        fi
    done
    printf "\nAll babel watchers now runnning, ctrl+c to kill all\n\n" &
    sleep 3600
    wait $!
    echo "TURNING OFF after 60 mins"
    kill 0
)
