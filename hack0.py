# example prompt: python hack.py localhost 9090 password
import socket
import sys


def hack():
    if len(sys.argv) != 4:
        sys.exit("Usage: python hack.py localhost 9090 password")
    else:
        # create the new socket
        new_socket = socket.socket()
        address = (sys.argv[1], int(sys.argv[2]))
        # connect to this server
        new_socket.connect(address)
        password = sys.argv[3]
        # convert the data (password) to bytes
        password = password.encode()
        # send through socket
        new_socket.send(password)
        # receive the response
        response = new_socket.recv(1024)
        # decode the response from bytes to string amd print it
        print(response.decode())

        new_socket.close()


if __name__ == "__main__":
    hack()
