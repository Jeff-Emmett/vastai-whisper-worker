#!/bin/bash
set -e

# Create log directory
mkdir -p /var/log

# Start the whisper HTTP server in background
echo "Starting faster-whisper server..."
python3 /app/server.py &
SERVER_PID=$!

# If running as Vast.ai serverless, start the PyWorker
if [ "${SERVERLESS:-false}" = "true" ]; then
    echo "Starting Vast.ai PyWorker..."
    # Wait for server to be up
    for i in $(seq 1 60); do
        if curl -s http://localhost:8000/health > /dev/null 2>&1; then
            break
        fi
        sleep 2
    done
    python3 /app/worker.py &
    WORKER_PID=$!
fi

# Wait for either process to exit
wait -n $SERVER_PID ${WORKER_PID:-}
