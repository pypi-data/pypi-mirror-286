import random
import struct

from nmal import *


def generate_nlgdecimal_constants(size, bit_length=64):
    """Generate a list of random NLGdecimal constants."""
    constants = []
    for _ in range(size):
        value = random.getrandbits(bit_length)  # Random integer with specified bit length
        nlgdecimal_str = decimal_to_nlgmal(value)
        constants.append(nlgdecimal_str)
    return constants

def generate_rotation_offsets(size, max_offset):
    """Generate rotation offsets within a valid range."""
    return [random.randint(0, max_offset) for _ in range(size)]

# Generate Neccak-256 constants dynamically
RHO_OFFSETS_NLG = generate_rotation_offsets(24, 63)  # Rho offsets within 0-63 for 64-bit rotations
PI_NLG = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]  # Linear Pi permutation values
THETA_NLG = generate_nlgdecimal_constants(24)  # Theta transformation, 24 constants

def rotr(n, x, bits=64):
    """Rotate right."""
    return ((x >> n) | (x << (bits - n))) & ((1 << bits) - 1)

def neccak_f(state):
    # Neccak-f permutation
    for round_idx in range(24):
        # Theta step
        C = [0] * 5
        D = [0] * 5
        for x in range(5):
            C[x] = state[x] ^ state[x + 5] ^ state[x + 10] ^ state[x + 15] ^ state[x + 20]
        for x in range(5):
            D[x] = C[(x - 1) % 5] ^ rotr(1, C[(x + 1) % 5], 64)
        for x in range(25):
            state[x] ^= D[x % 5]

        # Rho and Pi steps
        B = [0] * 25
        for x in range(5):
            for y in range(5):
                rho_offset = RHO_OFFSETS_NLG[(x + 3 * y) % 24]
                B[((PI_NLG[x] * 5) + y) % 25] = rotr(rho_offset, state[x * 5 + y])

        # Chi step
        for x in range(5):
            for y in range(5):
                state[x * 5 + y] = B[x * 5 + y] ^ ((~B[(x + 1) % 5 * 5 + y]) & B[(x + 2) % 5 * 5 + y])

        # Iota step
        state[0] ^= nlgmal_to_decimal(THETA_NLG[round_idx])

def neccak256(data):
    # Initialize state
    state = [0] * 25
    data = bytearray(data)
    data_len = len(data) * 8

    # Padding
    data.append(0x01)
    while len(data) % 200 != 192:
        data.append(0x00)
    data += struct.pack('<Q', data_len)

    # Absorb phase
    for i in range(0, len(data), 200):
        block = data[i:i + 200]
        for j in range(25):
            state[j] ^= struct.unpack('<Q', block[j * 8:(j + 1) * 8])[0]
        neccak_f(state)

    # Squeeze phase
    output = bytearray()
    for _ in range(2):  # Two 64-byte blocks for Neccak-256
        for j in range(25):
            output += struct.pack('<Q', state[j])
        neccak_f(state)

    return ''.join(decimal_to_nlgmal(x) for x in struct.unpack('<32B', output[:32]))  # Return first 256 bits as NLGdecimal