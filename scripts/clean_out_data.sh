#!/bin/bash

# Log script start time
echo "[$(date)] Starting clean_out_data.sh..."

# Check if data/out directory exists
if [ -d "data/out" ]; then
    echo "[$(date)] Deleting data/out directory..."
    rm -rf data/out
else
    echo "[$(date)] data/out directory not found. Skipping deletion."
fi

# Create data/out directory (force if it already exists)
echo "[$(date)] Creating data/out directory..."
mkdir -p data/out

# Log script completion
echo "[$(date)] clean_out_data.sh completed."