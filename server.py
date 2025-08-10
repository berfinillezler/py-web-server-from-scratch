import socket
import os
import mimetypes
import threading
import logging

HOST = '127.0.0.1'
PORT = 8080
STATIC_DIR = './static'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(threadName)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def get_content_type(file_path):
    content_type, _ = mimetypes.guess_type(file_path)
    return content_type or 'application/octet-stream'


def handle_request(conn, addr):
    request = conn.recv(1024).decode('utf-8')
    if not request:
        return


    method, path, _ = request.split('\n')[0].split()
    status_code = None

    if method != 'GET':
        status_code = 405
        response = b"HTTP/1.1 405 Method Not Allowed\r\n\r\nMethod Not Allowed"
        logging.warning(f'{addr[0]}:{addr[1]} "{method} {path}" {status_code}')
        conn.sendall(response.encode())
        return

    if path == '/':
        path = '/index.html'

    file_path = os.path.join(STATIC_DIR, path.lstrip('/'))


    if os.path.isfile(file_path):
        status_code = 200
        with open(file_path, 'rb') as f:
            content = f.read()
        content_type = get_content_type(file_path)
        header = (
	    f"HTTP/1.1 200 OK\r\n"
	    f"Content-Type: {content_type}\r\n"
            f"\r\n"
        ).encode()
        response = header + content
    else:
        response = b"HTTP/1.1 404 Not Found\r\n\r\n404 Page Not Found"
        status_code = 404

    conn.sendall(response)
    logging.info(f'{addr[0]}:{addr[1]} "{method} {path}" {status_code}')


def handle_client(conn, addr):
    with conn:
        logging.info(f"{addr[0]}:{addr[1]} Connected")
        handle_request(conn, addr)


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        logging.info(f"Server running at http://{HOST}:{PORT}/")
        try:
            while True:
                conn, addr = s.accept()
                thread = threading.Thread(
                    target=handle_client, 
                    args=(conn, addr), 
                    daemon=True
                )
                thread.start()
        except KeyboardInterrupt:
            logging.info("Caught Ctrl+C; shutting down server.")
        
if __name__ == '__main__':
    start_server()


