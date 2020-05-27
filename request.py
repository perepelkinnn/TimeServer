import ntp
import time
import socket


SERVER_ADDRESS = ('localhost', 11000)
CLIENT_ADDRESS = ('localhost', 11001)


client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(CLIENT_ADDRESS)

packet = ntp.Packet(originate=time.time()).pack()

client.sendto(packet, SERVER_ADDRESS)
client.close()