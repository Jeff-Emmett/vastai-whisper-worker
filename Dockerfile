FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV MODEL_LOG_FILE=/var/log/whisper.log
ENV WHISPER_MODEL=large-v3
ENV WHISPER_DEVICE=cuda
ENV WHISPER_COMPUTE_TYPE=float16

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip \
    ffmpeg git curl openssh-server \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Upgrade pip and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy worker files
COPY server.py worker.py entrypoint.sh ./
RUN chmod +x entrypoint.sh

# Pre-download the whisper large-v3 model into the image
RUN python3 -c "from faster_whisper import WhisperModel; print('Downloading large-v3...'); WhisperModel('large-v3', device='cpu', compute_type='int8'); print('Model cached!')"

EXPOSE 8000

CMD ["/app/entrypoint.sh"]
