import os

bind = ["0.0.0.0:8000"]
wsgi_app = "pyneutrino:create_app()"
worker_class = "gevent"
workers = max(os.cpu_count() // 2, 1)
graceful_timeout = 7
