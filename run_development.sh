#!/bin/bash

# If -w tag has been set, set local viariable WAIT to true
if [ "$1" = "-w" ]; then
  WAIT=True
fi


# Create virtual environment if not already created
if [ ! -d "venv" ]; then
  printf "\nCreating virtual environment...\n\n"
  python3 -m venv venv
fi

# Activate virtual environment
printf "\nActivating virtual environment...\n\n"
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install debugpy
export DEVELOPMENT=True


# Download cloud-sql-proxy if not already downloaded
if [ ! -f "cloud-sql-proxy" ]; then
  printf "\nDownloading cloud-sql-proxy...\n\n"
  curl -o cloud-sql-proxy https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.1.2/cloud-sql-proxy.darwin.amd64
  chmod +x cloud-sql-proxy
fi

# Start cloud-sql-proxy
printf "\nStarting cloud-sql-proxy...\n"
./cloud-sql-proxy mandalinka-382516:europe-west6:mandalinka &


# Run server
printf "\nRunning server...\n\n"

# If WAIT is true, run server waiting for debugger to attach
if [ "$WAIT" = "True" ]
then
  printf "\nWaiting for debugger to attach...\n\n"
  python -m debugpy --listen 5678 --wait-for-client ./manage.py runserver 0.0.0.0:8000
else
  python -m debugpy --listen 5678 ./manage.py runserver 0.0.0.0:8000
fi

# Clean up
printf "\nCleaning up...\n\n"
kill %1 # kill cloud-sql-proxy
deactivate # exit virtual environment
