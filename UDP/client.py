import socket

class Client():

    def __init__(self, address = 'localhost', port = 3000):
        self.address = address
        self.port = port
    
    def connect(self):
        server = (self.address, self.port)

        conection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        conection.bind((self.address, self.port))

        msg = input('-> ')

        while msg != 'closed':
            conection.sendto(msg.encode(), server)
            date, addressConection = conection.recvfrom(1024)

            print('received -> ', str(date))

            msg = input('-> ')

if __name__ == '__main__':
    cn = Client()
    cn.connect() 