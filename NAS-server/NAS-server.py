#! /usr/bin/env python3

import time
import http.server
import socketserver
import threading
import os
import sys
import random


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path == "/":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(self.generate_html().encode())

            elif self.path == "/style.css":
                self.send_response(200)
                self.send_header("Content-type", "text/css")
                self.end_headers()
                with open("style.css", "rb") as f:
                    self.wfile.write(f.read())

            else:
                super().do_GET()

        except Exception as e:
            print(f"\033[33;1mWarning: \033[0m{e}")

    def list_directory(self, path):
        try:
            html = self.generate_html(path)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode())

        except OSError:
            self.send_error(404, "File not found")

    def generate_html(self, path=None):
        html = ""
        path = self.directory if path is None else path

        _files, folders = [], []
        for i in os.listdir(path):
            item = os.path.join(path, i)
            if os.path.isfile(item):
                _files.append(i)

            else:
                folders.append(i)

        _files.sort()
        folders.sort()
        _files.extend(folders)

        for file in _files:
            if os.path.isfile(os.path.join(path, file)):
                html += f"""
                    <li class="file">
                        <a href="{file}">{file}</a>
                        <a class="download" href="{file}" download="NAS-{file}">download</a> 
                    </li>
                """

            else:
                html += f"""
                    <li class="directory">
                        <a href="{file}">{file}/</a>
                    </li>
                """

        with open("Web/index.html", "r") as f:
            index_html = f.read()

        with open("Web/style.css", "r") as f:
            styles = f.read()

        index_html = index_html.format(f"<style>{styles}</style>", path, html)

        return index_html


class server(threading.Thread):
    def __init__(self, *args, path, port, **kwags):
        self.path = path
        self.port = port
        self.instance = None
        self._is_down = False
        assert os.path.exists(path), "path doesn't exist"
        assert PORT in range(0, 65536), "Port is out of range (0-65535)"
        super().__init__(*args, **kwags)

    def shutdown(self):
        if self._is_down:
            return

        if self.instance is not None:
            self.instance.shutdown()

        while not self._is_down:
            pass

    def run(self):
        path = self.path
        port = self.port

        class handler(CustomHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=path, **kwargs)

        with socketserver.TCPServer(("", port), handler) as httpd:
            self.instance = httpd
            httpd.serve_forever()

        self._is_down = True

IP = "localhost"
PATH = os.getcwd()
PORT = random.randint(49152, 65535)
TIME = 15 * 60

try:
    PATH = sys.argv[1]
    try:
        PORT = int(sys.argv[2])
        try:
            TIME = float(sys.argv[3]) * 60
        except IndexError:
            pass
        except ValueError:
            print(f"\033\a[31;1mError: \033[0m time should be a Number (float/int)")
            os._exit(1)

    except IndexError:
        pass

    except ValueError:
        print(f"\033\a[31;1mError: \033[0m time should be a Number (int)")
        os._exit(1)

except IndexError:
    print(
        f"\033[33;1mYou can also pass arguments:\033[0m python {sys.argv[0]} [path] [port] [runtime(minutes)]"
    )

finally:
    startTime = time.time()

    try:
        localServer = server(port=PORT, path=PATH)

    except AssertionError as e:
        print(f"\033\a[31;1mError: \033[0m{e}")
        os._exit(1)

    localServer.start()
    link = f"http://{IP}:{PORT}"
    print(
        f"\033[32;1mUrl: \033[34m{link}\033[33m\nRuntime:\033[34m {TIME/60} minutes\n\033[33mPath:\033[34m {PATH}\033[0m"
    )

    try:
        while True:
            if time.time() - startTime >= TIME:
                print("\033[33;1mclosing server, time elapse reached\033[0m")
                localServer.shutdown()
                break

    except KeyboardInterrupt:
        localServer.shutdown()
        print("\033[33;1mclosing server on command\033[0m")
