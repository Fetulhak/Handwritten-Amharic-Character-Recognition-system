# -*- coding: utf-8 -*-
import re
import sys
import os
import json
from http.server import SimpleHTTPRequestHandler, HTTPServer


class FileUploadHTTPRequestHandler(SimpleHTTPRequestHandler):

    protocol_version = "HTTP/1.1"

    def do_POST(self):

        wasSuccess, files_uploaded = self.handle_file_uploads()

        response_obj = {
            "wasSuccess": wasSuccess,
            "files_uploaded": files_uploaded,
            "client_address": self.client_address
        }

        response_str = json.dumps(response_obj)

        self.log_message(response_str)

        self.send_response(200)
        self.send_header("Content-type", "Application/json")
        self.send_header("Content-Length", len(response_str))
        self.send_header("Access-Control-Allow-Origin",'*')
        self.send_header("Access-Control-Allow-Methods",'GET,POST,OPTIONS')
        self.send_header("Access-Control-Allow-Headers","X-Requested-with")
        self.end_headers()
        self.wfile.write(response_str.encode(encoding= "ISO-8859-1"))

    def read_line(self):
        line_str = self.rfile.readline().decode(encoding= "ISO-8859-1")
        self.char_remaining -= len(line_str)
        return line_str

    def handle_file_uploads(self):

        self.char_remaining = int(self.headers['content-length'])

        boundary = self.headers['content-type'].split("=")[1]

        basepath = self.translate_path(self.path)

        basepath = os.path.dirname(basepath)

        line_str = self.read_line()
        if not boundary in line_str:
            self.log_message("Content did NOT begin with boundary as " +
                             "it should")
            return False, []

        files_uploaded = []
        while self.char_remaining > 0:

            wasSuccess = False
            line_str = self.read_line()
            filename = re.findall('Content-Disposition.*name="file"; ' +
                                  'filename="(.*)"', line_str)
            if not filename:
                self.log_message("Can't find filename " + filename)
                break
            else:
                filename = filename[0]
            filepath = os.path.join('C:\\Users\\user\\Desktop\\HRACRS text generate\\saver\\nn', filename)
            try:
                outfile = open(filepath, 'wb')
            except IOError:
                self.log_message("Can't create file " + str(filepath) +
                                 " to write; do you have permission to write?")
                break
            line_str = self.read_line()
            line_str = self.read_line()
            preline = self.read_line()
            while self.char_remaining > 0:
                line_str = self.read_line()
                if boundary in line_str:
                    preline = preline[0:-1]
                    if preline.endswith('\r'):
                        preline = preline[0:-1]
                    outfile.write(preline.encode(encoding= "ISO-8859-1"))
                    outfile.close()
                    self.log_message("File '%s' upload success!" % filename)
                    files_uploaded.append(filename)
                    wasSuccess = True
                    break
                else:
                    outfile.write(preline.encode(encoding= "ISO-8859-1"))
                    preline = line_str

        return wasSuccess, files_uploaded

        
if __name__ == "__main__":
    httpd = HTTPServer(("", 8000), FileUploadHTTPRequestHandler)
    sa = httpd.socket.getsockname()
    print("Serving HTTP on", sa[0], "port", sa[1], "...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        httpd.server_close()
        sys.exit(0)