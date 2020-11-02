import socket
import argparse
import json
import pickle

def recvall(sc, length):
    data = b""
    while len(data) < length:
        more = sc.recv(length - len(data))
        if not more:
            raise EOFError('Data has not been received')
        data += more
    return data



class ChangeText():
    def __init__(self, host, port, txt, json_):
        self.host = host
        self.port = port
        self.txt = txt
        self.json_ = json_

    def run(self):
        with open(self.txt, "r") as f:
            txt_data = f.read()

        with open(self.json_, "r") as f:
            json_data = json.load(f)

        send_data = {
            "txt": txt_data,
            "json": json_data
        }

        send_data = pickle.dumps(send_data)
        send_data_length = len(send_data)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))

        sock.sendall(send_data_length.to_bytes(10, byteorder='big'))
        sock.sendall(send_data)

        exchanged_len = sock.recv(10)
        exchanged = recvall(sock, int.from_bytes(exchanged_len, byteorder='big'))
        exchanged = exchanged.decode("utf-8")

        print(exchanged)
        with open('exchanged.txt', 'w') as f:
            f.write(exchanged)

class EncodeDecode():
    def __init__(self, host, port, txt, key):
        self.host = host
        self.port = port
        self.txt = txt
        self.key = key

    def run(self):
        with open(self.txt, 'rb') as f:
            txt_data = f.read()

        with open(self.key, 'r') as f:
            key_data = f.read()

        send_data = {
            'txt': txt_data.decode('utf-8'),
            'key': key_data
        }

        send_data = pickle.dumps(send_data)
        send_data_length = len(send_data)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))

        sock.sendall(send_data_length.to_bytes(10, byteorder='big'))
        sock.sendall(send_data)

        cipher_length = sock.recv(10)
        cipher = recvall(sock, int.from_bytes(cipher_length, byteorder='big'))
        print(cipher)

        with open("cipher.txt", "wb") as f:
            f.write(cipher)

if __name__ == "__main__":
    choices = {
        'change_text': ChangeText,
        'encrypt_decrypt': EncodeDecode
    }

    parser = argparse.ArgumentParser(description="The text service to change or encrypt/decrypt data")
    parser.add_argument(
        '--host',
        metavar='HOST',
        default='127.0.0.1',
        help='Host to connect to'
    )
    parser.add_argument(
        '-p',
        metavar='PORT',
        type=int,
        default=1060,
        help='Port to connect to'
    )
    parser.add_argument(
        '--mode',
        metavar = 'MODE',
        choices = choices,
        help='change text - needs two files'
            '\t1. txt file - text file to be altered'
            '\t2. json file - dictioanry to change the words'
            'The responce contains text with replaced words'
            'encrypt_decrypt - needs two files'
            '\t1. txt file - text file to be crypted'
            '\t2. key file - file containing the key'
            'The responce contains encrypted/decrypted data'
    )
    parser.add_argument(
        'txt_file',
        help = '.txt file containg data to be processed'
    )
    parser.add_argument(
        'json_key_file',
        help = '.json or .txt file containing dictionary or key respectively'
    )

    args = parser.parse_args()
    mode = choices[args.mode](args.host, args.p, args.txt_file, args.json_key_file)
    mode.run()

