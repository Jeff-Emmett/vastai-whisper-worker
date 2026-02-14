#!/bin/bash
set -e

LOG_FILE="/var/log/whisper.log"
mkdir -p /var/log

echo "[$(date)] Starting Whisper serverless setup..." | tee -a $LOG_FILE

# Install system deps
apt-get update && apt-get install -y --no-install-recommends ffmpeg 2>&1 | tee -a $LOG_FILE

# Install Python deps
pip install --no-cache-dir faster-whisper>=1.1.0 flask>=3.0.0 gunicorn>=22.0.0 2>&1 | tee -a $LOG_FILE

# Clone our worker repo
REPO_URL="${WHISPER_WORKER_REPO:-https://github.com/Jeff-Emmett/vastai-whisper-worker.git}"
REPO_DIR="/opt/whisper-worker"
if [ ! -d "$REPO_DIR" ]; then
    git clone "$REPO_URL" "$REPO_DIR" 2>&1 | tee -a $LOG_FILE
fi

# Pre-download model
WHISPER_MODEL="${WHISPER_MODEL:-large-v3}"
echo "[$(date)] Pre-downloading Whisper model: $WHISPER_MODEL" | tee -a $LOG_FILE
python3 -c "
from faster_whisper import WhisperModel
import os
model = os.environ.get('WHISPER_MODEL', 'large-v3')
print(f'Loading {model}...')
WhisperModel(model, device='cuda', compute_type='float16')
print('Model loaded successfully')
" 2>&1 | tee -a $LOG_FILE

# Start the whisper HTTP server
echo "[$(date)] Starting Whisper HTTP server..." | tee -a $LOG_FILE
cd $REPO_DIR
MODEL_LOG_FILE=$LOG_FILE WHISPER_MODEL=$WHISPER_MODEL python3 server.py &
SERVER_PID=$!

# Wait for server to be ready
for i in $(seq 1 120); do
    if curl -s http://localhost:8000/health 2>/dev/null | grep -q "healthy"; then
        echo "[$(date)] Whisper server is healthy!" | tee -a $LOG_FILE
        break
    fi
    sleep 2
done

# If serverless mode, start pyworker
if [ "${SERVERLESS:-false}" = "true" ]; then
    echo "[$(date)] Starting PyWorker for serverless mode..." | tee -a $LOG_FILE
    pip install --no-cache-dir vastai-sdk>=0.3.0 2>&1 | tee -a $LOG_FILE
    cd $REPO_DIR
    MODEL_LOG_FILE=$LOG_FILE python3 worker.py &
fi

wait
