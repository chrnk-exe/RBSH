from blowfish_tables import p_table as p, s_table as s

# key = [0x4B7A70E9, 0xB5B32944, 0xDB75092E, 0xC4192623,
#        0xAD6EA6B0, 0x49A7DF7D, 0x9CEE60B8, 0x8FEDB266,
#        0xECAA8C71, 0x699A17FF, 0x5664526C, 0xC2B19EE1,
#        0x193602A5, 0x75094C29]

key = [i for i in range(25)]
p_new = p.copy()
s = s.copy()


def driver():
    key_len = len(key)
    index = 0
    for i in range(len(p)):
        val = ((key[index % key_len]) << 24) + \
              ((key[(index + 1) % key_len]) << 16) + \
              ((key[(index + 2) % key_len]) << 8) + \
              (key[(index + 3) % key_len])
        p[i] = p[i] ^ key[i % len(key)]
        p[i] ^= val
        index = index + 4
    k = 0
    data = 0
    # For the chaining process
    l, r = 0, 0

    # Begin chain replacing the p-boxes
    for i in range(0, len(p), 2):
        l, r = encryption(data, True)
        p[i] = l
        p[i + 1] = r

    # Chain replace the s-boxes
    for i in range(len(s)):
        for j in range(0, len(s[i]), 2):
            l, r = encryption(data, True)
            s[i][j] = l
            s[i][j + 1] = r

    # for i in range(10):
    #     temp = encryption(data)
    #     p[k] = temp >> 32
    #     k += 1
    #     p[k] = temp & 0xffffffff
    #     k += 1
    #     data = temp
    encrypt_data = int(input("Enter data to encrypt: "))
    encrypted_data = encryption(encrypt_data)
    print("Encrypted data : ", encrypted_data)
    decrypted_data = decryption(encrypted_data)
    print("Decrypted data : ", decrypted_data)


def encryption(data, return_r_l=False):
    left = data >> 32
    right = data & 0xffffffff
    for i in range(0, 16):
        left = p[i] ^ left
        right = right ^ func(func(left))
        left, right = right, left
    left, right = right, left
    if return_r_l:
        return left, right
    left = left ^ p[17]
    right = right ^ p[16]
    encrypted = (left << 32) ^ right
    return encrypted


def func(L):
    temp = s[0][L >> 24]
    temp = (temp + s[1][L >> 16 & 0xff]) % 2 ** 32
    temp = temp ^ s[2][L >> 8 & 0xff]
    temp = (temp + s[3][L & 0xff]) % 2 ** 32
    return temp


def decryption(data):
    left = data >> 32
    right = data & 0xffffffff
    for i in range(17, 1, -1):
        left = p[i] ^ left
        right = right ^ func(func(left))
        left, right = right, left
    left, right = right, left
    left = left ^ p[0]
    right = right ^ p[1]
    decrypted_data1 = (left << 32) ^ right
    return decrypted_data1


if __name__ == '__main__':
    driver()
    driver()
    driver()
    driver()
