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
    server.settimeout(0)    
    logging.info("Starting server...")
    return server


def handle(server, offset):
    try:
        data, addr = server.recvfrom(1024)
        logging.info("Request from {}:{}".format(addr[0], addr[1]))

        packet = ntp.Packet().unpack(data)
        packet.receive = time.time() + offset
        packet.transmit = time.time() + offset

        server.sendto(packet.pack(), addr)
    except OSError:
        pass


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
