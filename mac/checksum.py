from Keccak.python3_sha import sha3_224, sha3_512


def verify_checksum(message, digest):
    message = message.encode()

    message_hash = sha3_224(
        sha3_512(message[:len(message) // 2]).hexdigest() + sha3_512(message[len(message) // 2:]).hexdigest()
    ).hexdigest().decode()
    return digest == message_hash


def gen_checksum(message):
    message = message.encode()
    return sha3_224(
        sha3_512(message[:len(message) // 2]).hexdigest() + sha3_512(message[len(message) // 2:]).hexdigest()
    ).hexdigest().decode()
