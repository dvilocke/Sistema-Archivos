import zmq
import os
import time
import shutil

'''
ARCHIVE:
1.when you fly open the pointer is placed at the beginning of the file.
2.if a file that is already created is read again, then it deletes the content 
of the current one, be careful with that.
'''

class Server:
    SIZE = 1
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    transfer_completed = False

    def __init__(self, url):
        self.socket.bind(url)

    def receive_file(self):
        while True:
            self.transfer_completed = False
            exists = True
            counter = 0
            information_user = self.socket.recv_json()

            if not os.path.isdir(information_user['directory_name']):
                os.mkdir(information_user['directory_name'])
                exists = False

            print(f"{'the folder already exists' if exists else 'the folder does not exist'}")
            self.socket.send(b'verification of the folders')


            name_base = 'base' + information_user['extension']

            while True:
                with open(name_base, 'wb') as f:
                    while not self.transfer_completed:
                        content = self.socket.recv_multipart()
                        if content[1].decode() == '0':
                            f.write(content[0])
                            print(f'part:{counter} entered to the server')
                            self.socket.send(b'ok')
                            counter += 1
                        else:
                            self.transfer_completed = True

                self.socket.send(b'file saved on server')
                #save process
                source = 'C:\\Users\\lenov\\PycharmProjects\\proyecto archivos'  + f"\\{name_base}"
                destination = "C:\\Users\\lenov\\PycharmProjects\\proyecto archivos" + f"\\{information_user['directory_name']}"
                shutil.move(source, destination)

                #rename file
                base = "C:\\Users\\lenov\\PycharmProjects\\proyecto archivos"
                complement =  f"\\{information_user['directory_name']}"

                archivo  = base +  complement + f"\\{name_base}"
                print(archivo)
                nuevo = base +  complement + f"\\{information_user['name_archive']}"
                print(nuevo)

                os.rename(archivo, nuevo)

                break

            time.sleep(3)
            print('\nimage saved successfully\n')




if __name__ == '__main__':
    Server(url="tcp://*:5555").receive_file()
