#!/bin/bash

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
python manage.py test

# Clean up
printf "\nCleaning up...\n\n"
kill %1 # kill cloud-sql-proxy
deactivate # exit virtual environment
