# UDP 
# Protocolo que não se basea em uma conexão em que se manda dados sem segurança com relação ao seu ddestino. 
import socket

class Server:

    def __init__(self, address = '', port = 3000):
        self.address = address
        self.port = port

    def connect(self):
        #Criando socket com o protocolo UDP utilizando 'SOCK_DGRAM'

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
            # Bind() só recebe 1 paramentro então utilizando as (()) conseguimos burlar isso já que teoricamente é apenas 1
            server.bind((self.address, self.port))  
            
            while True:
                print('Connecting to server')
                date, addressConection = server.recvfrom(1024)

            
                print('message received from: ', str(addressConection))
                print('received customer: ', str(date))

                response = str(date)
                server.sendto(date, addressConection) 
                


   
