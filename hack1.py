# example prompt: python hack.py localhost 9090
import sys
from socket import socket
from itertools import product
from string import ascii_lowercase


# read and check the address from cmd line
def read_address():
    if len(sys.argv) != 3:
        sys.exit("Usage: python hack.py localhost 9090")
    else:
        # argv[1] is a IP address; argv[2] is a port
        address = (sys.argv[1], int(sys.argv[2]))
        return address


def generate_password():
    numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    alphabet = list(ascii_lowercase)
    alphanum = numbers + alphabet

    n = 1
    while True:
        alphanum_product = product(alphanum, repeat=n)
        alphanum_iter = iter(alphanum_product)
        for i in alphanum_iter:
            yield i
        n += 1

address1 = read_address()
hack_socket = socket()
hack_socket.connect(address1)

a = generate_password()
for k in a:
    password = ''.join(str(j) for j in k)
    password_encoded = password.encode()
    hack_socket.send(password_encoded)
    response = hack_socket.recv(1024)
    response_decoded = response.decode()
    if response_decoded == "Connection success!":
        break

hack_socket.close()

"""
password = generate_password()
for k in password:
    password_str = ''.join(str(j) for j in k)
    password_encoded = password_str.encode()
    hack_socket.send(password_encoded)
    response = hack_socket.recv(1024)
    if response.decode() == "Connection success!":
        print(password_str)
        break

if __name__ == "__main__":
    hack_socket.close()
"""
