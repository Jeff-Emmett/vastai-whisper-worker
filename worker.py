"""Vast.ai PyWorker for faster-whisper serverless endpoint."""

from vastai import Worker, WorkerConfig, HandlerConfig, LogActionConfig, BenchmarkConfig

worker_config = WorkerConfig(
    model_server_url="http://127.0.0.1",
    model_server_port=8000,
    model_log_file="/var/log/whisper.log",
    model_healthcheck_url="/health",
    handlers=[
        HandlerConfig(
            route="/transcribe",
            allow_parallel_requests=False,
            max_queue_time=120.0,
            workload_calculator=lambda data: 100.0,
            benchmark_config=BenchmarkConfig(
                dataset=[
                    {
                        "audio_url": "https://upload.wikimedia.org/wikipedia/commons/6/6f/En-us-hello.ogg",
                        "language": "en",
                    }
                ],
                runs=2,
                concurrency=1,
            ),
        ),
    ],
    log_action_config=LogActionConfig(
        on_load=["Whisper model loaded and ready"],
        on_error=["Traceback", "RuntimeError", "CUDA error"],
        on_info=["Loading faster-whisper"],
    ),
)

Worker(worker_config).run()
