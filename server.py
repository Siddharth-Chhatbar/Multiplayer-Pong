import socket
import threading
import sys
from game_objects import Paddle, Ball
import pickle

NO_OF_CLIENTS = 2
WIDTH, HEIGHT = 1920, 1080
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 200
RADIUS = 12
paddles = [
    Paddle(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT),
    Paddle(
        WIDTH - PADDLE_WIDTH - 50,
        HEIGHT // 2 - PADDLE_HEIGHT // 2,
        PADDLE_WIDTH,
        PADDLE_HEIGHT,
    ),
]
ball = Ball(WIDTH // 2, HEIGHT // 2, RADIUS)
connected_clients = 0


def threaded_client(connection: socket.socket, current_paddle):
    global paddles, ball, connected_clients
    score = [0, 0]
    win = False
    while connected_clients < NO_OF_CLIENTS:
        print("Waiting for everyone to connect...")
        continue
    connection.send(pickle.dumps((paddles[current_paddle], ball, score, win)))
    reply = None
    while True:
        try:
            data = pickle.loads(connection.recv(2048 * 4))
            paddles[current_paddle], ball, score, win = (
                data[0],
                data[1],
                data[2],
                data[3],
            )
            if not data:
                print("Disconnected")
                break
            else:
                if win:
                    ball.reset()
                    paddles[0].reset()
                    paddles[1].reset()
                    score = [0, 0]
                    continue
                # Update the ball's position on the server
                ball.move()  # Ball movement handled here

                if current_paddle == 1:
                    reply = (paddles[0], ball, score, win)
                else:
                    reply = (paddles[1], ball, score, win)

                print("Received:", data)
                print("Sending:", reply)
            connection.sendall(pickle.dumps(reply))

        except Exception as e:
            print("Error:", e)
            break
    print("Lost connection.")
    connection.close()


def main():
    global connected_clients
    try:
        server = "10.0.0.249"
        port = 5555

        web_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            web_socket.bind((server, port))
        except socket.error as e:
            print(e)

        web_socket.listen(NO_OF_CLIENTS)
        print("Waiting for connection, server started ...")

        current_paddle = 0
        while True:
            connection, address = web_socket.accept()
            print("Connected to:", address)

            client_thread = threading.Thread(
                target=threaded_client,
                args=(
                    connection,
                    current_paddle,
                ),
            )
            client_thread.start()
            current_paddle += 1
            connected_clients += 1
    except KeyboardInterrupt:
        print("")
        sys.exit()


if __name__ == "__main__":
    main()
