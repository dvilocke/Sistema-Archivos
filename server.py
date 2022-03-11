import zmq

class Server:
    context = zmq.Context()
    socket = context.socket(zmq.REP)

    def __init__(self, url):
        self.socket.bind(url)

    def listen_to_requests(self):
        i = 0
        while True:
            archive = self.socket.recv()
            print(archive)
            with open('prueba.jpg', 'wb') as f:
                f.write(archive)

            msg = f'number of fractions{i}'
            self.socket.send(msg.encode())
            i += 1


if __name__ == '__main__':
    Server(url="tcp://*:5555").listen_to_requests()
