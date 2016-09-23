# -*- coding: utf-8 -*-
from wsgiref.simple_server import make_server


def hello_world_app(environ, start_response):
    status = '200 OK'  # HTTP Status
    headers = [('Content-type', 'text/plain')]  # HTTP Headers
    start_response(status, headers)

    # The returned object is going to be printed
    return [b"Hello World"]


httpd = make_server('', 8000, hello_world_app)
print("Serving on port 8000...")

# Serve until process is killed
# httpd.serve_forever()
httpd.handle_request()