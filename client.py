import zmq
import os
import sys

'''
CRITERIA TO QUALIFY:
1.repeated files
2.any size ---> ok, modulate the file
'''

class Cliente:

    SIZE = 50
    context = zmq.Context()
    socket = context.socket(zmq.REQ)

    def __init__(self, directory_name, name_archive, url):
        self.directory_name = directory_name
        self.name_archive = name_archive
        self.socket.connect(url)

    @staticmethod
    def file_exists(file):
        return os.path.exists(file)

    def get_information_file(self):
        return os.path.splitext(self.name_archive)

    def get_only_name(self):
        name = ''
        for c in self.name_archive:
            if c == '.':
                break
            else:
                name += c
        return name

    def get_file_size(self) -> str:
        return f'{os.path.getsize(self.name_archive)} bytes'

    def save_File(self):
        self.socket.send_json({
            'directory_name' : self.directory_name,
            'name_archive': self.name_archive,
            'extension': self.get_information_file()[1],
            'name_only': self.get_only_name()
        })

        print(self.socket.recv().decode())

        while True:
            with open(self.name_archive, 'rb') as f:
                content = f.read(self.SIZE)
                if content:
                    while content:
                        self.socket.send_multipart([content, '0'.encode()])
                        self.socket.recv().decode()
                        content = f.read(self.SIZE)

            self.socket.send_multipart([''.encode(), '1'.encode()])
            print(self.socket.recv().decode())
            break

if __name__ == '__main__':
    '''
    sys.argv[1] -> directory_name
    sys.argv[2] -> name_archive
    '''
    if sys.argv[1] and sys.argv[2]:
        #check if the file exists
        if Cliente.file_exists(sys.argv[2]):
            Cliente(directory_name=sys.argv[1], name_archive=sys.argv[2], url='tcp://localhost:5555').save_File()
        else:
            print(f'{sys.argv[2]} does not exist')
    else:
        print('missing arguments...')


