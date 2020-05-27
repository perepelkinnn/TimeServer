import ntp
import time
import socket


SERVER_ADDRESS = ('localhost', 11000)
CLIENT_ADDRESS = ('localhost', 11001)


client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(CLIENT_ADDRESS)
client.settimeout(10)

cur_time = time.time()
print('Current time - {}\n\r'.format(time.ctime(cur_time)))
packet = ntp.Packet(originate=cur_time).pack()

client.sendto(packet, SERVER_ADDRESS)
data, addr = client.recvfrom(1024)
client.close()

packet = ntp.Packet().unpack(data)
print(packet.to_display())

ser_time = packet.transmit
print('\n\rServer time - {}\n\r'.format(time.ctime(ser_time)))

