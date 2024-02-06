import socket
import threading
import json
from hashlib import md5
from time import time
from mac.checksum import gen_checksum, verify_checksum
from rabin.rabin import Rabin
from blowfish.blowfish_cipher import encrypt_blowfish_ECB, decrypt_blowfish_ECB
from colorama import init, Fore
from utils.custom_print import client_print
from time import sleep

init()


class Client:
    def __init__(self, address, port):
        client_print('Choose your nickname: ', end='')
        self.name = input()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((address, port))
        self._first_message = True

        self.blowfish_key = md5(str(int(time())).encode('ascii')).hexdigest()
        # self.blowfish_key = "e31f4f03807f093c6db75e6a9153005e"

        start_message = {'code': 'set_name', 'data': self.name}
        self.client.send(json.dumps(start_message).encode('utf-8'))
        client_print(Fore.LIGHTYELLOW_EX + 'Wait for the server to be prepared.', end='')
        sleep(2)
        print(Fore.LIGHTYELLOW_EX + '.', end='')
        sleep(2)
        print(Fore.LIGHTYELLOW_EX + '.')

        receive_thread = threading.Thread(target=self.receive_message)
        receive_thread.start()

        write_thread = threading.Thread(target=self.send_message)
        write_thread.start()

    def receive_message(self):
        try:
            message = self.client.recv(4096)
            if len(message) > 0:
                message_json = json.loads(message.decode('utf8'))

                if message_json['code'] == 'rb.sh_handshake':
                    public_key = int(message_json.get('data'))
                    checksum = message_json.get('checksum')
                    # print(str(public_key), checksum)
                    if verify_checksum(str(public_key), checksum):
                        cipher = Rabin(n=public_key)
                        encrypted_key = cipher.encrypt(self.blowfish_key)
                        message_json = {
                            'code': 'rb.sh_handshake',
                            'data': encrypted_key,
                            'name': self.name,
                        }
                        self.client.send(json.dumps(message_json).encode('utf-8'))
                    else:
                        client_print(Fore.LIGHTRED_EX + 'Error! Bad checksum.')
                        client_print('Try again')
                        exit()

                if message_json['code'] == 'message':
                    message = message_json.get('data')
                    checksum = message_json.get('checksum')

                    if verify_checksum(message, checksum):
                        decrypted_message = decrypt_blowfish_ECB(message, self.blowfish_key)
                        print(
                            f'Checksum verified:  {checksum}\n'
                            f'Encrypted message:  {message}\n'
                            f'Decrypted message:  {decrypted_message.strip()}'
                        )
                    else:
                        print('Invalid checksum!')

        except socket.error:
            print('Connection to server lost..')
            print('Check your server connection and try to reconnect')
            self.client.close()

    def send_message(self):
        if self._first_message:
            self._first_message = False
            client_print(Fore.LIGHTYELLOW_EX + 'Wait for the handshake to end.', end='')
            sleep(2)
            print(Fore.LIGHTYELLOW_EX + '.', end='')
            sleep(2)
            print(Fore.LIGHTYELLOW_EX + '.')

        while True:
            client_print('Your message: ', end='')
            if (input_text := input()):
                message = encrypt_blowfish_ECB(input_text, self.blowfish_key)

                message_json = {
                    'code': 'message',
                    'sender': self.name,
                    'data': message,
                    'checksum': gen_checksum(message)
                }
                self.client.send(json.dumps(message_json).encode('utf8'))


if __name__ == '__main__':
    app_host, app_port = '127.0.0.1', 5000
    client_print(Fore.LIGHTGREEN_EX + 'Client started at ' + Fore.LIGHTYELLOW_EX + f'{app_host}' + ':' +
                 Fore.LIGHTYELLOW_EX + f'{app_port}')
    try:
        Client(app_host, app_port)
    except KeyboardInterrupt:
        client_print(Fore.LIGHTRED_EX + 'Client closed. Bye bye!')
