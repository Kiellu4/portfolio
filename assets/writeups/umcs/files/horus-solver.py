#!/usr/bin/env python3
"""Static RC4 decryptor reconstructed from the HUMBLEBEE UMCS write-up."""
import hashlib

CIPHER_HEX = (
    "037d91c01b45e9db9546f62ecf8601657a7848f04f3391d118783b227741a081"
    "e2ba87dcc2c4f0c45ab3285e248c4211c72da33be3a39e"
)
KEY = bytes.fromhex("deadbeefcafebabe")
EXPECTED_MD5 = "c1a708f3e14e36e388ec2f75d04ceff2"


def rc4(key, data):
    state = list(range(256))
    j = 0
    for i in range(256):
        j = (j + state[i] + key[i % len(key)]) & 0xff
        state[i], state[j] = state[j], state[i]

    i = j = 0
    out = bytearray()
    for byte in data:
        i = (i + 1) & 0xff
        j = (j + state[i]) & 0xff
        state[i], state[j] = state[j], state[i]
        out.append(byte ^ state[(state[i] + state[j]) & 0xff])
    return bytes(out)


assert hashlib.md5(KEY).hexdigest() == EXPECTED_MD5
print(rc4(KEY, bytes.fromhex(CIPHER_HEX)).decode())
