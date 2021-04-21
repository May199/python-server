# UDP 
# Protocolo que não se basea em uma conexão em que se manda dados sem segurança com relação ao seu ddestino. 
import socket
import time

class Server:

    def __init__(self, address = 'localhost', port = 3000):
        self.address = address
        self.port = port 

    def connect(self):
        #Criando socket com o protocolo UDP utilizando 'SOCK_DGRAM'
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
            # Bind() só recebe 1 paramentro então utilizando as (()) conseguimos burlar isso já que teoricamente é apenas 1
            server.bind((self.address, self.port))  

            # Esperando receber lista de arquivos do cliente 
            print('Connecting to server')
            files = []

            while True:
                conn, addr = server.recvfrom(1024)

                if conn.decode() == 'closed':
                    break

                filename = conn.decode()
                print(f'[{len(files)}] {filename}')
                files.append(filename)
                
            # Escolhendo arquivo que vou querer baixar do cliente
            fileselect = int(input('\nWhich file do you want to receive? '))
            
            while not (0 <= fileselect < len(files)):
                print('invalid option!')
                fileselect = int(input('\nWhich file do you want to receive?'))
        
            server.sendto(fileselect.to_bytes(4, 'little'), addr) 
            
            # Recebendo numero de pacotes
            # Queremos saber em quantos pacotes o arquivo sera enviado
            conn = server.recv(4)
            packet = int.from_bytes(conn, 'little')

            # Recebendo pacotes
            server.settimeout(5)
            file = open(files[fileselect], 'wb')
            packet_kilobytes = 1024
            packet_bytes = packet_kilobytes * 8

            print('-----------------------------------------------------------')
            print(f'Getting {packet} packages...')

            start = time.time()
            for i in range(packet):
                conn = server.recv(packet_bytes)
                file.write(conn)

                time_download = f'Downloading ... {round((100*(i+1))/packet, 2)}%'
                print('\r'+time_download, end='')

            total_time = round(time.time()-start, 2)
            print(f'\nDownload complete: {total_time} milliseconds')

            print('message received from: ', str(addr))
        
        server.close()

if __name__ == '__main__':
    sr = Server()
    sr.connect() 
                


   
