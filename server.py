import socket, time, logging

logging.basicConfig(filename="requests.log", format='%(asctime)s %(message)s',level=logging.INFO)

SERVER_ADDRESS = ('localhost', 123)


def get_non_blocking_server_socket():
    server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    server.bind(SERVER_ADDRESS)
    logging.info("start server")
    return server


def handle(server, offset):
    data, addr = server.recvfrom(1024)
    server.sendto(bytes("{}".format(time.ctime(time.time() + offset)), encoding="utf8"), addr)
    logging.info("send to {}".format(addr))


if __name__ == '__main__':
    server_socket = get_non_blocking_server_socket()
    offset = 0
    with open("config.txt", "r") as file:
        offset = int(file.readline())

    try:
        while True:
            handle(server_socket, offset)
    except KeyboardInterrupt:
        server_socket.close()
    logging.info("stop server")