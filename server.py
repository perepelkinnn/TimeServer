import socket
import time
import logging
import ntp

logging.basicConfig(filename="history.log",
                    format='%(asctime)s %(message)s', level=logging.INFO)

SERVER_ADDRESS = ('localhost', 11000)


def get_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(SERVER_ADDRESS)
    logging.info("Starting server...")
    return server


def handle(server, offset):
    data, addr = server.recvfrom(1024)
    packet = ntp.Packet().unpack(data)
    print(packet.to_display())
    logging.info("Request from {}:{}".format(addr[0], addr[1]))


if __name__ == '__main__':
    server = get_server()
    offset = 0
    with open("config.txt", "r") as file:
        offset = int(file.readline())

    try:
        while True:
            handle(server, offset)
    except KeyboardInterrupt:
        server.close()
    logging.info("Stoping server...")
