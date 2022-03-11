#1024 = 1 kilobyte
#1024 * 1024 = megabyte

import zmq
import os

class Cliente:

    SIZE = 1
    context = zmq.Context()
    socket = context.socket(zmq.REQ)

    def __init__(self, url, name_archive):
        if os.path.exists(name_archive):
            self.name_archive = name_archive
            self.socket.connect(url)
        else:
            print(f'{name_archive} does not exist')

    def get_file_size(self) -> str:
        return f'{os.path.getsize(self.name_archive)} bytes'

    def send_to_server(self):
        while True:
            with open(self.name_archive, 'rb') as f:
                content = f.read(self.SIZE)
                while content:
                    self.socket.send_multipart([content, '0'.encode()])
                    print(self.socket.recv().decode())
                    content = f.read(self.SIZE)

            self.socket.send_multipart([''.encode(), '1'.encode()])
            print(self.socket.recv().decode())
            break

if __name__ == '__main__':
    Cliente(url='tcp://localhost:5555', name_archive='cosa.txt').send_to_server()


