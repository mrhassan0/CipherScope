import random
import time


IP = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7,
]

FP = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25,
]

E_TABLE = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1,
]

P_TABLE = [
    16, 7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2, 8, 24, 14,
    32, 27, 3, 9,
    19, 13, 30, 6,
    22, 11, 4, 25,
]

PC1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4,
]

PC2 = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32,
]

SHIFT_AMOUNTS = [
    1, 1, 2, 2,
    2, 2, 2, 2,
    1, 2, 2, 2,
    2, 2, 2, 1,
]

S_BOXES = [
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
    ],
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
    ],
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
    ],
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
    ],
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
    ],
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
    ],
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
    ],
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
    ],
]


def make_random_bytes(size):
    answer = bytearray()

    for i in range(size):
        answer.append(random.randint(0, 255))

    return bytes(answer)


def bytes_to_bits(data):
    bits = ""

    for number in data:
        bits = bits + format(number, "08b")

    return bits


def bits_to_bytes(bits):
    answer = bytearray()

    for start in range(0, len(bits), 8):
        byte_bits = bits[start:start + 8]
        answer.append(int(byte_bits, 2))

    return bytes(answer)


def bits_to_hex(bits):
    return hex(int(bits, 2))[2:].upper().zfill(len(bits) // 4)


def permute(bits, table):
    answer = ""

    for position in table:
        answer = answer + bits[position - 1]

    return answer


def xor_bits(left, right):
    answer = ""

    for i in range(len(left)):
        if left[i] == right[i]:
            answer = answer + "0"
        else:
            answer = answer + "1"

    return answer


def left_shift(bits, amount):
    return bits[amount:] + bits[:amount]


def make_round_keys(key_bytes):
    key_bits = bytes_to_bits(key_bytes)
    key_56 = permute(key_bits, PC1)

    left = key_56[:28]
    right = key_56[28:]

    round_keys = []

    for shift in SHIFT_AMOUNTS:
        left = left_shift(left, shift)
        right = left_shift(right, shift)
        round_key = permute(left + right, PC2)
        round_keys.append(round_key)

    return round_keys


def s_box_substitution(bits):
    answer = ""

    for box_number in range(8):
        block = bits[box_number * 6:(box_number + 1) * 6]
        row_bits = block[0] + block[5]
        col_bits = block[1:5]
        row = int(row_bits, 2)
        col = int(col_bits, 2)
        value = S_BOXES[box_number][row][col]
        answer = answer + format(value, "04b")

    return answer


def des_function(right_half, round_key):
    expanded = permute(right_half, E_TABLE)
    mixed = xor_bits(expanded, round_key)
    after_s_boxes = s_box_substitution(mixed)
    after_p_box = permute(after_s_boxes, P_TABLE)

    return after_p_box


def encrypt_block(block_bits, round_keys):
    block_bits = permute(block_bits, IP)

    left = block_bits[:32]
    right = block_bits[32:]

    for round_number in range(16):
        old_right = right
        function_result = des_function(right, round_keys[round_number])
        right = xor_bits(left, function_result)
        left = old_right

    combined = right + left
    final_bits = permute(combined, FP)

    return final_bits


def decrypt_block(block_bits, round_keys):
    reversed_keys = round_keys[:]
    reversed_keys.reverse()

    return encrypt_block(block_bits, reversed_keys)


def pad_bytes(data):
    pad_size = 8 - (len(data) % 8)

    if pad_size == 0:
        pad_size = 8

    return data + bytes([pad_size] * pad_size)


def remove_padding(data):
    if len(data) == 0:
        return data

    pad_size = data[-1]

    if pad_size < 1 or pad_size > 8:
        return data

    return data[:-pad_size]


def encrypt_bytes(data, round_keys):
    data = pad_bytes(data)
    encrypted_bits = ""

    for start in range(0, len(data), 8):
        block = data[start:start + 8]
        block_bits = bytes_to_bits(block)
        encrypted_bits = encrypted_bits + encrypt_block(block_bits, round_keys)

    return bits_to_bytes(encrypted_bits)


def decrypt_bytes(data, round_keys):
    decrypted_bits = ""

    for start in range(0, len(data), 8):
        block = data[start:start + 8]
        block_bits = bytes_to_bits(block)
        decrypted_bits = decrypted_bits + decrypt_block(block_bits, round_keys)

    decrypted_bytes = bits_to_bytes(decrypted_bits)
    return remove_padding(decrypted_bytes)


def round_keys_for_output(round_keys):
    round_key_hex = []

    for i in range(len(round_keys)):
        round_key_hex.append({
            "round": i + 1,
            "key": bits_to_hex(round_keys[i]),
        })

    return round_key_hex


def encrypt_text(plaintext):
    key = make_random_bytes(8)
    round_keys = make_round_keys(key)
    plaintext_bytes = plaintext.encode("utf-8")

    start_encrypt = time.perf_counter()
    encrypted_bytes = encrypt_bytes(plaintext_bytes, round_keys)
    end_encrypt = time.perf_counter()

    return {
        "algorithm": "DES",
        "mode": "Plaintext to Ciphertext",
        "ciphertext_hex": encrypted_bytes.hex().upper(),
        "generated_key_hex": key.hex().upper(),
        "round_keys": round_keys_for_output(round_keys),
        "encryption_time_seconds": round(end_encrypt - start_encrypt, 6),
    }


def decrypt_text(ciphertext_hex, key_hex):
    key = bytes.fromhex(key_hex.strip())
    encrypted_bytes = bytes.fromhex(ciphertext_hex.strip())

    if len(key) != 8:
        raise ValueError("DES key must be 16 hex characters.")

    if len(encrypted_bytes) % 8 != 0:
        raise ValueError("DES ciphertext hex must represent full 8-byte blocks.")

    round_keys = make_round_keys(key)

    start_decrypt = time.perf_counter()
    decrypted_bytes = decrypt_bytes(encrypted_bytes, round_keys)
    end_decrypt = time.perf_counter()

    return {
        "algorithm": "DES",
        "mode": "Ciphertext to Plaintext",
        "decrypted_plaintext": decrypted_bytes.decode("utf-8", errors="replace"),
        "used_key_hex": key.hex().upper(),
        "round_keys": round_keys_for_output(round_keys),
        "decryption_time_seconds": round(end_decrypt - start_decrypt, 6),
    }


def run_des(plaintext):
    key = make_random_bytes(8)
    round_keys = make_round_keys(key)
    plaintext_bytes = plaintext.encode("utf-8")

    start_encrypt = time.perf_counter()
    encrypted_bytes = encrypt_bytes(plaintext_bytes, round_keys)
    end_encrypt = time.perf_counter()

    start_decrypt = time.perf_counter()
    decrypted_bytes = decrypt_bytes(encrypted_bytes, round_keys)
    end_decrypt = time.perf_counter()

    return {
        "algorithm": "DES",
        "plaintext": plaintext,
        "ciphertext_hex": encrypted_bytes.hex().upper(),
        "decrypted_plaintext": decrypted_bytes.decode("utf-8", errors="replace"),
        "generated_key_hex": key.hex().upper(),
        "round_keys": round_keys_for_output(round_keys),
        "encryption_time_seconds": round(end_encrypt - start_encrypt, 6),
        "decryption_time_seconds": round(end_decrypt - start_decrypt, 6),
    }
