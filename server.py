"""Faster-Whisper HTTP server for Vast.ai serverless."""

import base64
import io
import logging
import os
import tempfile
import urllib.request

from flask import Flask, jsonify, request

LOG_FILE = os.environ.get("MODEL_LOG_FILE", "/var/log/whisper.log")
MODEL_SIZE = os.environ.get("WHISPER_MODEL", "large-v3")
DEVICE = os.environ.get("WHISPER_DEVICE", "cuda")
COMPUTE_TYPE = os.environ.get("WHISPER_COMPUTE_TYPE", "float16")

# Set up file logging so PyWorker can monitor readiness
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
model = None


def get_model():
    global model
    if model is None:
        logger.info(f"Loading faster-whisper model: {MODEL_SIZE}")
        from faster_whisper import WhisperModel

        model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)
        logger.info("Whisper model loaded and ready")
    return model


def download_audio(url):
    """Download audio from URL to a temp file."""
    suffix = os.path.splitext(url.split("?")[0])[-1] or ".wav"
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    urllib.request.urlretrieve(url, tmp.name)
    return tmp.name


@app.route("/health", methods=["GET"])
def health():
    if model is not None:
        return jsonify({"status": "healthy", "model": MODEL_SIZE})
    return jsonify({"status": "loading"}), 503


@app.route("/transcribe", methods=["POST"])
def transcribe():
    data = request.json or {}
    audio_path = None
    created_tmp = False

    try:
        # Accept audio as URL or base64
        if "audio_url" in data:
            audio_path = download_audio(data["audio_url"])
            created_tmp = True
        elif "audio_base64" in data:
            audio_bytes = base64.b64decode(data["audio_base64"])
            suffix = data.get("format", ".wav")
            if not suffix.startswith("."):
                suffix = "." + suffix
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            tmp.write(audio_bytes)
            tmp.close()
            audio_path = tmp.name
            created_tmp = True
        else:
            return jsonify({"error": "Provide 'audio_url' or 'audio_base64'"}), 400

        # Transcription options
        language = data.get("language")
        task = data.get("task", "transcribe")  # transcribe or translate
        beam_size = data.get("beam_size", 5)
        word_timestamps = data.get("word_timestamps", False)
        vad_filter = data.get("vad_filter", True)

        whisper = get_model()
        segments, info = whisper.transcribe(
            audio_path,
            language=language,
            task=task,
            beam_size=beam_size,
            word_timestamps=word_timestamps,
            vad_filter=vad_filter,
        )

        segment_list = []
        full_text_parts = []
        for seg in segments:
            seg_data = {
                "start": round(seg.start, 3),
                "end": round(seg.end, 3),
                "text": seg.text.strip(),
            }
            if word_timestamps and seg.words:
                seg_data["words"] = [
                    {
                        "word": w.word,
                        "start": round(w.start, 3),
                        "end": round(w.end, 3),
                        "probability": round(w.probability, 4),
                    }
                    for w in seg.words
                ]
            segment_list.append(seg_data)
            full_text_parts.append(seg.text.strip())

        return jsonify(
            {
                "text": " ".join(full_text_parts),
                "segments": segment_list,
                "language": info.language,
                "language_probability": round(info.language_probability, 4),
                "duration": round(info.duration, 3),
            }
        )

    except Exception as e:
        logger.error(f"Transcription error: {e}")
        return jsonify({"error": str(e)}), 500

    finally:
        if created_tmp and audio_path and os.path.exists(audio_path):
            os.unlink(audio_path)


if __name__ == "__main__":
    # Pre-load model on startup
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    get_model()
    app.run(host="0.0.0.0", port=8000)
