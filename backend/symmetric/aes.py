import random
import time


S_BOX = [
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5,
    0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0,
    0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC,
    0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A,
    0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0,
    0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B,
    0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85,
    0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5,
    0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17,
    0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88,
    0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C,
    0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9,
    0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6,
    0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E,
    0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94,
    0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68,
    0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
]

RCON = [
    0x00, 0x01, 0x02, 0x04, 0x08, 0x10,
    0x20, 0x40, 0x80, 0x1B, 0x36,
]


def make_inverse_s_box():
    inverse = [0] * 256

    for i in range(256):
        inverse[S_BOX[i]] = i

    return inverse


INV_S_BOX = make_inverse_s_box()


def make_random_bytes(size):
    answer = bytearray()

    for i in range(size):
        answer.append(random.randint(0, 255))

    return bytes(answer)


def multiply(byte_value, multiplier):
    answer = 0
    value = byte_value
    number = multiplier

    while number > 0:
        if number & 1:
            answer = answer ^ value

        value = value << 1

        if value & 0x100:
            value = value ^ 0x11B

        value = value & 0xFF
        number = number >> 1

    return answer


def add_round_key(state, round_key):
    for i in range(16):
        state[i] = state[i] ^ round_key[i]


def sub_bytes(state):
    for i in range(16):
        state[i] = S_BOX[state[i]]


def inv_sub_bytes(state):
    for i in range(16):
        state[i] = INV_S_BOX[state[i]]


def shift_rows(state):
    new_state = state[:]

    for row in range(4):
        row_values = []

        for col in range(4):
            row_values.append(state[row + 4 * col])

        shifted = row_values[row:] + row_values[:row]

        for col in range(4):
            new_state[row + 4 * col] = shifted[col]

    for i in range(16):
        state[i] = new_state[i]


def inv_shift_rows(state):
    new_state = state[:]

    for row in range(4):
        row_values = []

        for col in range(4):
            row_values.append(state[row + 4 * col])

        shifted = row_values[-row:] + row_values[:-row]

        for col in range(4):
            new_state[row + 4 * col] = shifted[col]

    for i in range(16):
        state[i] = new_state[i]


def mix_one_column(column):
    a0 = column[0]
    a1 = column[1]
    a2 = column[2]
    a3 = column[3]

    return [
        multiply(a0, 2) ^ multiply(a1, 3) ^ a2 ^ a3,
        a0 ^ multiply(a1, 2) ^ multiply(a2, 3) ^ a3,
        a0 ^ a1 ^ multiply(a2, 2) ^ multiply(a3, 3),
        multiply(a0, 3) ^ a1 ^ a2 ^ multiply(a3, 2),
    ]


def inv_mix_one_column(column):
    a0 = column[0]
    a1 = column[1]
    a2 = column[2]
    a3 = column[3]

    return [
        multiply(a0, 14) ^ multiply(a1, 11) ^ multiply(a2, 13) ^ multiply(a3, 9),
        multiply(a0, 9) ^ multiply(a1, 14) ^ multiply(a2, 11) ^ multiply(a3, 13),
        multiply(a0, 13) ^ multiply(a1, 9) ^ multiply(a2, 14) ^ multiply(a3, 11),
        multiply(a0, 11) ^ multiply(a1, 13) ^ multiply(a2, 9) ^ multiply(a3, 14),
    ]


def mix_columns(state):
    for col in range(4):
        start = col * 4
        column = state[start:start + 4]
        mixed = mix_one_column(column)

        for i in range(4):
            state[start + i] = mixed[i]


def inv_mix_columns(state):
    for col in range(4):
        start = col * 4
        column = state[start:start + 4]
        mixed = inv_mix_one_column(column)

        for i in range(4):
            state[start + i] = mixed[i]


def rotate_word(word):
    return word[1:] + word[:1]


def sub_word(word):
    answer = []

    for value in word:
        answer.append(S_BOX[value])

    return answer


def expand_key(key_bytes):
    expanded = list(key_bytes)
    rcon_number = 1

    while len(expanded) < 176:
        temp = expanded[-4:]

        if len(expanded) % 16 == 0:
            temp = rotate_word(temp)
            temp = sub_word(temp)
            temp[0] = temp[0] ^ RCON[rcon_number]
            rcon_number = rcon_number + 1

        for i in range(4):
            new_byte = expanded[len(expanded) - 16] ^ temp[i]
            expanded.append(new_byte)

    round_keys = []

    for start in range(0, 176, 16):
        round_keys.append(expanded[start:start + 16])

    return round_keys


def encrypt_block(block_bytes, round_keys):
    state = list(block_bytes)

    add_round_key(state, round_keys[0])

    for round_number in range(1, 10):
        sub_bytes(state)
        shift_rows(state)
        mix_columns(state)
        add_round_key(state, round_keys[round_number])

    sub_bytes(state)
    shift_rows(state)
    add_round_key(state, round_keys[10])

    return bytes(state)


def decrypt_block(block_bytes, round_keys):
    state = list(block_bytes)

    add_round_key(state, round_keys[10])

    for round_number in range(9, 0, -1):
        inv_shift_rows(state)
        inv_sub_bytes(state)
        add_round_key(state, round_keys[round_number])
        inv_mix_columns(state)

    inv_shift_rows(state)
    inv_sub_bytes(state)
    add_round_key(state, round_keys[0])

    return bytes(state)


def pad_bytes(data):
    pad_size = 16 - (len(data) % 16)

    if pad_size == 0:
        pad_size = 16

    return data + bytes([pad_size] * pad_size)


def remove_padding(data):
    if len(data) == 0:
        return data

    pad_size = data[-1]

    if pad_size < 1 or pad_size > 16:
        return data

    return data[:-pad_size]


def encrypt_bytes(data, round_keys):
    data = pad_bytes(data)
    answer = bytearray()

    for start in range(0, len(data), 16):
        block = data[start:start + 16]
        encrypted_block = encrypt_block(block, round_keys)
        answer.extend(encrypted_block)

    return bytes(answer)


def decrypt_bytes(data, round_keys):
    answer = bytearray()

    for start in range(0, len(data), 16):
        block = data[start:start + 16]
        decrypted_block = decrypt_block(block, round_keys)
        answer.extend(decrypted_block)

    return remove_padding(bytes(answer))


def round_key_to_hex(round_key):
    answer = ""

    for value in round_key:
        answer = answer + format(value, "02X")

    return answer


def round_keys_for_output(round_keys):
    round_key_list = []

    for i in range(len(round_keys)):
        round_key_list.append({
            "round": i,
            "key": round_key_to_hex(round_keys[i]),
        })

    return round_key_list


def encrypt_text(plaintext):
    key = make_random_bytes(16)
    round_keys = expand_key(key)
    plaintext_bytes = plaintext.encode("utf-8")

    start_encrypt = time.perf_counter()
    encrypted_bytes = encrypt_bytes(plaintext_bytes, round_keys)
    end_encrypt = time.perf_counter()

    return {
        "algorithm": "AES-128",
        "mode": "Plaintext to Ciphertext",
        "ciphertext_hex": encrypted_bytes.hex().upper(),
        "generated_key_hex": key.hex().upper(),
        "round_keys": round_keys_for_output(round_keys),
        "encryption_time_seconds": round(end_encrypt - start_encrypt, 6),
    }


def decrypt_text(ciphertext_hex, key_hex):
    key = bytes.fromhex(key_hex.strip())
    encrypted_bytes = bytes.fromhex(ciphertext_hex.strip())

    if len(key) != 16:
        raise ValueError("AES-128 key must be 32 hex characters.")

    if len(encrypted_bytes) % 16 != 0:
        raise ValueError("AES ciphertext hex must represent full 16-byte blocks.")

    round_keys = expand_key(key)

    start_decrypt = time.perf_counter()
    decrypted_bytes = decrypt_bytes(encrypted_bytes, round_keys)
    end_decrypt = time.perf_counter()

    return {
        "algorithm": "AES-128",
        "mode": "Ciphertext to Plaintext",
        "decrypted_plaintext": decrypted_bytes.decode("utf-8", errors="replace"),
        "used_key_hex": key.hex().upper(),
        "round_keys": round_keys_for_output(round_keys),
        "decryption_time_seconds": round(end_decrypt - start_decrypt, 6),
    }


def run_aes(plaintext):
    key = make_random_bytes(16)
    round_keys = expand_key(key)
    plaintext_bytes = plaintext.encode("utf-8")

    start_encrypt = time.perf_counter()
    encrypted_bytes = encrypt_bytes(plaintext_bytes, round_keys)
    end_encrypt = time.perf_counter()

    start_decrypt = time.perf_counter()
    decrypted_bytes = decrypt_bytes(encrypted_bytes, round_keys)
    end_decrypt = time.perf_counter()

    return {
        "algorithm": "AES-128",
        "plaintext": plaintext,
        "ciphertext_hex": encrypted_bytes.hex().upper(),
        "decrypted_plaintext": decrypted_bytes.decode("utf-8", errors="replace"),
        "generated_key_hex": key.hex().upper(),
        "round_keys": round_keys_for_output(round_keys),
        "encryption_time_seconds": round(end_encrypt - start_encrypt, 6),
        "decryption_time_seconds": round(end_decrypt - start_decrypt, 6),
    }
