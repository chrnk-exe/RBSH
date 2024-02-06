from blowfish.blowfish_tables import p_table, s_table
from copy import deepcopy
import base64


class Blowfish:
    ENCRYPT = 0
    DECRYPT = 1

    def __init__(self, key):

        if not key or len(key) < 8 or len(key) > 56:
            raise RuntimeError("Attempted to initialize Blowfish cipher with key of invalid length: %s" % len(key))

        self.p_boxes = deepcopy(p_table)

        self.s_boxes = deepcopy(s_table)
        key_len = len(key)
        index = 0
        key = list(map(ord, key))
        for i in range(len(self.p_boxes)):
            val = ((key[index % key_len]) << 24) + \
                  ((key[(index + 1) % key_len]) << 16) + \
                  ((key[(index + 2) % key_len]) << 8) + \
                  (key[(index + 3) % key_len])
            self.p_boxes[i] = self.p_boxes[i] ^ val
            index = index + 4

        # For the chaining process
        l, r = 0, 0

        # Begin chain replacing the p-boxes
        for i in range(0, len(self.p_boxes), 2):
            l, r = self.cipher(l, r, self.ENCRYPT)
            self.p_boxes[i] = l
            self.p_boxes[i + 1] = r

        # Chain replace the s-boxes
        for i in range(len(self.s_boxes)):
            for j in range(0, len(self.s_boxes[i]), 2):
                l, r = self.cipher(l, r, self.ENCRYPT)
                self.s_boxes[i][j] = l
                self.s_boxes[i][j + 1] = r

    def cipher(self, xl, xr, direction):
        if direction == self.ENCRYPT:
            for i in range(16):
                xl = xl ^ self.p_boxes[i]
                xr = self.__round_func(xl) ^ xr
                xl, xr = xr, xl
            xl, xr = xr, xl
            xr = xr ^ self.p_boxes[16]
            xl = xl ^ self.p_boxes[17]
        else:
            for i in range(17, 1, -1):
                xl = xl ^ self.p_boxes[i]
                xr = self.__round_func(xl) ^ xr
                xl, xr = xr, xl
            xl, xr = xr, xl
            xr = xr ^ self.p_boxes[1]
            xl = xl ^ self.p_boxes[0]
        return xl, xr

    def __round_func(self, xl):
        a = (xl & 0xFF000000) >> 24
        b = (xl & 0x00FF0000) >> 16
        c = (xl & 0x0000FF00) >> 8
        d = xl & 0x000000FF

        # Perform all ops as longs then and out the last 32-bits to
        # obtain the integer
        f = (int(self.s_boxes[0][a]) + int(self.s_boxes[1][b])) % (int(2) ** 32)
        f = f ^ int(self.s_boxes[2][c])
        f = f + int(self.s_boxes[3][d])
        f = (f % (int(2) ** 32)) & 0xFFFFFFFF

        return f

    def decrypt(self, data):
        if not len(data) == 8:
            raise RuntimeError("Attempted to encrypt data of invalid block length: %s" % len(data))
        data = list(map(ord, data))
        # Use big endian since that's what everyone else uses
        cl = (data[3]) | ((data[2]) << 8) | ((data[1]) << 16) | ((data[0]) << 24)
        cr = (data[7]) | ((data[6]) << 8) | ((data[5]) << 16) | ((data[4]) << 24)
        xl, xr = self.cipher(cl, cr, self.DECRYPT)
        chars = bytes([
            ((xl >> 24) & 0xFF), ((xl >> 16) & 0xFF), ((xl >> 8) & 0xFF), (xl & 0xFF),
            ((xr >> 24) & 0xFF), ((xr >> 16) & 0xFF), ((xr >> 8) & 0xFF), (xr & 0xFF)
        ])
        return chars

    def encrypt(self, data):

        if not len(data) == 8:
            raise RuntimeError("Attempted to encrypt data of invalid block length: %s" % len(data))

        # Use big endian since that's what everyone else uses
        xl = ord(data[3]) | (ord(data[2]) << 8) | (ord(data[1]) << 16) | (ord(data[0]) << 24)
        xr = ord(data[7]) | (ord(data[6]) << 8) | (ord(data[5]) << 16) | (ord(data[4]) << 24)

        cl, cr = self.cipher(xl, xr, self.ENCRYPT)
        chars = ''.join([
            chr((cl >> 24) & 0xFF), chr((cl >> 16) & 0xFF), chr((cl >> 8) & 0xFF), chr(cl & 0xFF),
            chr((cr >> 24) & 0xFF), chr((cr >> 16) & 0xFF), chr((cr >> 8) & 0xFF), chr(cr & 0xFF)
        ])
        return chars


def encrypt_blowfish_ECB(string, key):
    result = []
    for i in range(0, len(string), 8):
        result.append(string[i:i+8])
    if len(result[-1]) != 8:
        diff = 8 - len(result[-1])
        result[-1] += ' ' * diff
    cipher = Blowfish(key=key)
    encoded = list(map(lambda plaintext: cipher.encrypt(plaintext), result))
    # return base64.b64encode(":".join(encoded).encode()).decode()
    return base64.b64encode("".join(encoded).encode()).decode()


def decrypt_blowfish_ECB(string, key):
    # encrypted_data = base64.b64decode(string.encode()).decode().split(':')
    encrypted_data = base64.b64decode(string.encode()).decode()
    result = []
    for i in range(0, len(encrypted_data), 8):
        result.append(encrypted_data[i:i+8])
    encrypted_data = result
    cipher = Blowfish(key=key)
    plain_data = list(map(lambda ciphertext: cipher.decrypt(ciphertext).decode(), encrypted_data))
    return "".join(plain_data)
