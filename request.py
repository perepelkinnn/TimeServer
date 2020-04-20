import socket

SERVER_ADDRESS = ('localhost', 123)

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

 
data = b"request"
socket.sendto(data, SERVER_ADDRESS)


data = socket.recvfrom(1024)
print(data)


socket.close()