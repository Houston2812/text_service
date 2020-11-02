import socket
import argparse
import json, pickle

def recvall(sock, length):
    data = b""
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError("Data is not obtained")
        data += more
    return data


class Server():
    def __init__(self, interface, port):
        self.interface = interface
        self.port = port


    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
        sock.bind((self.interface, self.port))
        sock.listen(1)
        print(f"Server listens at {sock.getsockname()}")

        while True:
            sc, sock_name = sock.accept()
            print(f"Connected socket {sc.getpeername()}")

            data_len = sc.recv(10)
            data = recvall(sc, int.from_bytes(data_len, byteorder='big'))

            data = pickle.loads(data)

            txt = data['txt']
            if "json" in data.keys():
                json_ = data['json']
                exchanged = self.__exchange(txt, json_)
                exchanged_len = len(exchanged)
                sc.sendall(exchanged_len.to_bytes(10, byteorder='big'))
                sc.sendall(exchanged.encode('utf-8'))
            elif "key" in data.keys():
                key = data['key']
                cipher = self.__crypt(txt, key)
                cipher_len = len(cipher)
                sc.sendall(cipher_len.to_bytes(10, byteorder='big'))
                sc.sendall(cipher.encode('utf-8'))

    def __exchange(self, txt, json_):
        exchanged = txt
        for i,j in json_.items():
            exchanged = exchanged.replace(i,j)
        return exchanged

    def __crypt(self, txt, key):
        cipher = ""
        while len(key) < len(txt):
            key += key

        for i in range(len(txt)):
            cipher += chr(ord(txt[i]) ^ ord(key[i]))
        print(f"Cipher \n{cipher}")
        return cipher


if __name__ == "__main__":
    server = Server(interface="127.0.0.1", port=1060)
    server.run()



