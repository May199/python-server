import socket
import time
import os
class Client():

    def __init__(self, address = 'localhost', port = 3000):
        self.address = address
        self.port = port
    
    def connect(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.connect((self.address, self.port))
        
        # Enviando arquivos ao servidor
        # Pegar os arquivos que estão na pasta Cliente irá enviar para o server, depois que o user escolher o arquivo
        # Será baixado e enviado para pasta Server

        file_path = os.listdir()
        print('Sending file names...')

        for file in file_path:
            # Enviando os pacotes
            server.sendall(file.encode())

        # Depois de enviar, será encerrado
        server.sendall('closed'.encode())
        print('Waiting for server response...')

        msg = server.recv(4)
        index = int.from_bytes(msg, 'little')

        # Abrindo arquivos para enviar, depois claro da escolha do usuário de qual arquivo receber
        file = open(file_path[index], 'rb')
        file_size = os.path.getsize(file_path[index])

        packet_kilobytes = 1024
        packet_bytes = packet_kilobytes * 8
        packet  = (file_size // packet_bytes) + 1
        
        server.sendall(packet.to_bytes(4, 'little'))

        # Enviando pacotes
        delay = 0.004
        estimated_time = packet *(delay*1.2)

        def header():
            info = f'Sent {packet} packet to server\nEstimated time: {round(estimated_time)} seconds'
            print(info)

            print('-----------------------------------------------------------\nSize of each package')
            for i in range(packet):
                pk = file.read(packet_bytes)
                server.sendall(pk)

                sent = f'\n {i}:({int((i+1)*packet_kilobytes)})KB'

                print(sent, end='')

                time.sleep(delay)
            
            print('\n message sent to: ', self.address, self.port)

        header()

        file.close()
        server.close()
        
if __name__ == '__main__':
    cn = Client()
    cn.connect() 