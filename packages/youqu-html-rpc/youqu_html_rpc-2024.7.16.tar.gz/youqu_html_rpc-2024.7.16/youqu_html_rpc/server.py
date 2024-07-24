import os
from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer
from youqu_html import YouQuHtml

class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

def check_connected():
    return True

def gen_html(data_path, gen_path, http_path):
    YouQuHtml.gen(data_path, gen_path)
    os.system(f"ln -s {gen_path} /usr/share/nginx/html/{http_path}")


def makedirs(dirpath):
    os.makedirs(dirpath, exist_ok=True)

def server():
    from youqu_html_rpc.config import config
    server = ThreadXMLRPCServer(("0.0.0.0", config.PORT), allow_none=True)
    server.register_function(gen_html, "gen_html")
    server.register_function(makedirs, "makedirs")
    print("Listen to client requests ...")
    server.serve_forever()


if __name__ == "__main__":
    server()