import socket
import threading
import json

from mac.checksum import verify_checksum, gen_checksum
from utils.gen_prime_number_by_len_10 import generate_prime
from sympy.ntheory.primetest import isprime
from rabin.rabin import Rabin
from blowfish.blowfish_cipher import decrypt_blowfish_ECB
from colorama import init, Fore, Style
from utils.custom_print import server_print

init()


class Server:

    def __init__(self, host, port, count):
        self._client_list = {}
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.bind((host, port))
        self._server.listen(count)
        self.p = self.__gen_prime()
        self.q = self.__gen_prime()
        self.n = self.p * self.q

        server_print('The server is ready to accept connections')

        self.wait_new_client_cycle()

    @staticmethod
    def __gen_prime():
        while True:
            number = generate_prime(50)
            if number % 4 == 3 and isprime(number):
                return number

    def wait_new_client_cycle(self):
        while True:
            try:
                client, address = self._server.accept()
                self._client_list[client] = None
                threading.Thread(target=self.handle_client_cycle, args=(client,)).start()
            except:
                print('server connection break')
                break

    def handle_client_cycle(self, client):

        message_json = {
            "code": "rb.sh_handshake",
            "data": self.n,
            "checksum": gen_checksum(str(self.n))
        }

        # print(gen_checksum(str(self.n)))
        # print(str(self.n))
        # send public key
        client.send(json.dumps(message_json).encode('utf-8'))

        while True:
            try:
                message = client.recv(4096)
                if len(message) > 0:
                    message_json = json.loads(message.decode('utf-8'))

                    if message_json['code'] == 'rb.sh_handshake':
                        encrypted_key = message_json.get('data')
                        name = message_json.get('name')

                        server_print(Fore.BLUE + 'New connection from user: ' + Fore.LIGHTMAGENTA_EX + f'{name}')

                        rabin_cipher = Rabin(p=self.p, q=self.q)
                        secret_key = rabin_cipher.decrypt(encrypted_key)
                        self._client_list[client] = {
                            'key': secret_key, 'name': name
                        }

                    if message_json['code'] == 'message':
                        message = message_json.get('data')
                        checksum = message_json.get('checksum')
                        name = self._client_list[client]["name"]

                        if verify_checksum(message, checksum):
                            decrypted_message = decrypt_blowfish_ECB(message, self._client_list[client]['key'])
                            server_print(
                                Fore.BLUE + f'New message from user ' + Fore.LIGHTMAGENTA_EX + f'{name}\n' +
                                Fore.BLUE + f'Decrypted message: ' + Fore.LIGHTWHITE_EX +
                                f'{decrypted_message.strip()}\n' +
                                Fore.WHITE + Style.DIM + f'Encrypted message: {message}\n' +
                                f'Checksum (verified): {checksum}' + Style.RESET_ALL
                            )
                        else:
                            server_print(
                                Fore.LIGHTRED_EX + 'Invalid checksum!' +
                                Style.DIM + f'Encrypted message: {message}\n' +
                                f'Checksum (verified): {checksum}' + Style.RESET_ALL
                            )

            except socket.error:
                print('player leave ' + str(client))
                self._client_list.pop(client)
                client.close()
                break


if __name__ == '__main__':
    app_host, app_port = '127.0.0.1', 5000
    server_print(Fore.BLUE + 'Server started at ' + Fore.BLUE + f'{app_host}' + ':' +
                 Fore.BLUE + f'{app_port}')
    Server(app_host, app_port, 2)
