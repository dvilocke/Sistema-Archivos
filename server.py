import zmq
import os


'''
ARCHIVE
1.when you fly open the pointer is placed at the beginning of the file.
'''

class Server:
    SIZE = 1
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    transfer_completed = False

    def __init__(self, url):
        self.socket.bind(url)

    def receive_file(self):
        counter = 0
        while True:
            with open('prueba.jpg', 'wb') as f:
                while not self.transfer_completed:
                    content = self.socket.recv_multipart()
                    if content[1].decode() == '0':
                        f.write(content[0])
                        print(f'part:{counter} entered to the server')
                        self.socket.send(b'ok')
                        counter += 1
                    else:
                        self.transfer_completed = True
                        f.close()

            self.transfer_completed = False
            counter = 0
            self.socket.send(b'file saved on server')
            exit()



if __name__ == '__main__':
    Server(url="tcp://*:5555").receive_file()
