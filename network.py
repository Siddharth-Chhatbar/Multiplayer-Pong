import socket
import pickle


class Network:
    def __init__(self) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "10.0.0.249"
        self.port = 5555
        self.address = (self.server, self.port)
        self.game_obj = self.connect()

    def get_game_obj(self):
        return self.game_obj

    def connect(self):
        try:
            self.client.connect(self.address)
            return pickle.loads(self.client.recv(2048 * 4))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048 * 4))
        except socket.error as e:
            print(e)
