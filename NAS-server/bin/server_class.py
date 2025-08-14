import http.server
import socketserver
import threading
import os


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(self.generate_html().encode())

            elif self.path == '/style.css':
                self.send_response(200)
                self.send_header('Content-type', 'text/css')
                self.end_headers()
                with open('style.css', 'rb') as f:
                    self.wfile.write(f.read())
                    
            else:
                super().do_GET()

        except Exception as e:
            print(e)

    def list_directory(self, path):
        try:
            html = self.generate_html(path)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode())

        except OSError:
            self.send_error(404, "File not found")
    
    def generate_html(self, directory=None):
        files = ""
        path = self.directory if directory is None else directory
        
        f, items = [], []
        for i in os.listdir(path):
            item = os.path.join(path, i)
            if os.path.isfile(item):
                f.append(i)

            else:
                items.append(i)

        f.sort()
        items.sort()
        items.extend(f)

        for file in items:
            if os.path.isfile(os.path.join(path, file)):
                files += f'''
                    <li class="file">
                        <a href="{file}">{file}</a>
                        <a class="download" href="{file}" download="download-{file}">download</a> 
                    </li>
                '''

            else:
                files += f'''
                    <li class="directory">
                        <a href="{file}">{file}/</a>
                    </li>
                '''

        with open("Web/index.html", 'r') as f:
            index_html = f.read()

        with open("Web/style.css", "r") as f:
            styles = f.read()

        index_html = index_html.format(f"<style>{styles}</style>", path, files)

        return index_html


class server(threading.Thread):
    used_ports = []
    def __init__(self, *args, path, port, **kwags):
        self.path = path
        assert port not in server.used_ports, "port occupied"
        server.used_ports.append(port)
        self.port = port
        super().__init__(*args, **kwags)

    def run(self):
        path = self.path
        port = self.port

        assert os.path.exists(path), "Error: path specified doesn't exist"

        class handler(CustomHTTPRequestHandler):
            def __init__(self, *args, **kwargs):                                                                 
                super().__init__(*args, directory=path, **kwargs)

        with socketserver.TCPServer(("", port), handler) as httpd:
            httpd.serve_forever()

