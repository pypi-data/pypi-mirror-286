# nlg256.py
# license: MIT
# This script implements a NLG-256 hashing algorithm using the custom NLGdecimal number system.

import struct
import random
from nmal import *


def generate_nlgdecimal_constants(size):
    """Generate a list of random NLGdecimal constants."""
    constants = []
    for _ in range(size):
        value = random.getrandbits(32)  # 32-bit random integer
        nlgdecimal_str = decimal_to_nlgmal(value)
        constants.append(nlgdecimal_str)
    return constants


# Generate nlg-256 constants dynamically
K_NLG = generate_nlgdecimal_constants(64)


# Helper functions
def rotr(n, x):
    return (x >> n) | (x << (32 - n)) & 0xFFFFFFFF


def nlg_compress(state, block):
    W = [0] * 64
    for i in range(16):
        W[i] = struct.unpack('>I', block[i * 4:(i + 1) * 4])[0]

    for i in range(16, 64):
        s0 = rotr(7, W[i - 15]) ^ rotr(18, W[i - 15]) ^ (W[i - 15] >> 3)
        s1 = rotr(17, W[i - 2]) ^ rotr(19, W[i - 2]) ^ (W[i - 2] >> 10)
        W[i] = (W[i - 16] + s0 + W[i - 7] + s1) & 0xFFFFFFFF

    a, b, c, d, e, f, g, h = state

    for i in range(64):
        s1 = rotr(6, e) ^ rotr(11, e) ^ rotr(25, e)
        ch = (e & f) ^ (~e & g)
        temp1 = (h + s1 + ch + nlgmal_to_decimal(K_NLG[i]) + W[i]) & 0xFFFFFFFF
        s0 = rotr(2, a) ^ rotr(13, a) ^ rotr(22, a)
        maj = (a & b) ^ (a & c) ^ (b & c)
        temp2 = (s0 + maj) & 0xFFFFFFFF

        h = g
        g = f
        f = e
        e = (d + temp1) & 0xFFFFFFFF
        d = c
        c = b
        b = a
        a = (temp1 + temp2) & 0xFFFFFFFF

    state[0] = (state[0] + a) & 0xFFFFFFFF
    state[1] = (state[1] + b) & 0xFFFFFFFF
    state[2] = (state[2] + c) & 0xFFFFFFFF
    state[3] = (state[3] + d) & 0xFFFFFFFF
    state[4] = (state[4] + e) & 0xFFFFFFFF
    state[5] = (state[5] + f) & 0xFFFFFFFF
    state[6] = (state[6] + g) & 0xFFFFFFFF
    state[7] = (state[7] + h) & 0xFFFFFFFF


def nlg256(data):
    data = bytearray(data)
    length = struct.pack('>Q', 8 * len(data))
    data.append(0x80)
    while (len(data) + 8) % 64 != 0:
        data.append(0)
    data += length

    state = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19,
    ]

    for i in range(0, len(data), 64):
        nlg_compress(state, data[i:i+64])

    return ''.join(decimal_to_nlgmal(x) for x in state)



