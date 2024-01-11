wsgi_app = "pyneutrino:create_app()"
reload = True
worker_class = "gevent"

# Since server-side event routes never return, a worker serving one will always wait until killed.
# Therefore, it's simpler for development to have a shorter timeout
graceful_timeout = 5
