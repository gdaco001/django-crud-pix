import os

bind = "0.0.0.0:8000"
worker_tmp_dir = "/dev/shm"
chdir = "pix_api"
max_requests = int(os.environ.get("GUNICORN_MAX_REQUESTS", "1000"))
max_requests_jitter = int(os.environ.get("GUNICORN_MAX_REQUESTS_JITTER", "25"))
graceful_timeout = 30
threads = int(os.environ.get("GUNICORN_THREADS", "1"))
