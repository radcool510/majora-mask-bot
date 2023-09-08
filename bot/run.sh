#!/usr/bin/env bash

# Install the required packages from the requirements.txt file
pip install -r requirements.txt

# Create the condition file
touch condition

# Run the script as long as the condition file exists
while [ -e condition ]
do
    python3 main.py
    git pull origin main
done