from http.server import SimpleHTTPRequestHandler as Handler
from http.server import HTTPServer as Server
from threading import Thread
import socket
import os

PORT = int(os.getenv('PORT', 3000))
http = Server(("", PORT), Handler)

class WebServer:

    def __init__(self, address='0.0.0.0', port=PORT):
        self.port = port
        self.address = address

    def start(self):
        # Definindo o tipo de server como 'sr' que será TCP/IP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sr:
            sr.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sr.bind((self.address, self.port))
            sr.listen(10)

            while True:
                print('Aguardando conexão...')
                # Definindo o sr para aguardar conexão, ele vai continuar ligado 
                conn, addr = sr.accept() #Objeto/Cliente
                req = HttpRequest(conn, addr)
                req.start()


class HttpRequest(Thread):

    def __init__(self, conn, addr):
        super(HttpRequest, self).__init__()
        self.conn = conn
        self.addr = addr
        self.CRLF = '\r\n'
        self.buffer_size = 4096

    def run(self):
        request = self.conn.recv(self.buffer_size)
        print(request)

        response = HttpResponse(self.conn, self.addr, '')
        response.processRespose()

        self.conn.close()

class App:

    os.chdir('src')
    
    try:
        print("Conexão iniciada na porta %i" % PORT)
        http.serve_forever()
    except KeyboardInterrupt:
        pass
    except socket.error as error:
        print("Algo deu errado!", error)
    
    http.server_close()

class HttpResponse:

    def __init__(self, conn, addr, file):
        self.conn = conn
        self.addr = addr
        self.file = file

    def processRespose(self):
        self.conn.sendall(App)
        

        
        
        
