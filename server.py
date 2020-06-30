import socket
from _thread import *
import pickle
from game import Game
server = "192.168.43.221"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")
currentPlayer = 0
game = Game()


def threaded_client(conn, p):
    conn.send(str.encode(str(p)))
    global currentPlayer
    global game
    while True:
        try:
            data = conn.recv(4096).decode()

            if not data:
                break
            else:
                # data = 25 is a signal given by player p, that it has won, now server send
                # it to other player, if this player also wins, then the match is DRAWN.
                if int(data) == 25:
                    game.wins[p] = True

                elif int(data) != -1:
                    game.move = int(data)
                    game.went[p] = True
                    game.went[1 - p] = False
                conn.sendall(pickle.dumps(game))
        except:
            break

    print("Lost connection")
    currentPlayer = 0
    game = Game()
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
