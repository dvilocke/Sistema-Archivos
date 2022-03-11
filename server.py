import zmq
import os


'''
ARCHIVE
1.when you fly open the pointer is placed at the beginning of the file.
2.
'''

class Server:
    SIZE = 1
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    transfer_completed = False

    def __init__(self, url):
        self.socket.bind(url)

    def receive_file(self):
        counter = 1
        while True:
            with open('prueba.txt', 'wb') as f:
                while not self.transfer_completed:
                    content = self.socket.recv_multipart()
                    if content[1].decode() == '0':
                        print('ingresando', content[0])
                        f.write(content[0])
                        self.socket.send(b'ok')
                    else:
                        self.transfer_completed = True
                        f.close()

            self.transfer_completed = False
            self.socket.send(b'ok')
            exit()



if __name__ == '__main__':
    Server(url="tcp://*:5555").receive_file()
