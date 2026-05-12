import math
import random


def number_text(number):
    return str(number)


def gcd(a, b):
    while b != 0:
        old_b = b
        b = a % b
        a = old_b

    return a


def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0

    gcd_value, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1

    return gcd_value, x, y


def mod_inverse(a, m):
    gcd_value, x, y = extended_gcd(a, m)

    if gcd_value != 1:
        raise ValueError("Modular inverse does not exist.")

    return x % m


def is_probably_prime(number, test_count=8):
    if number < 2:
        return False

    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    for prime in small_primes:
        if number == prime:
            return True
        if number % prime == 0:
            return False

    d = number - 1
    s = 0

    while d % 2 == 0:
        d = d // 2
        s = s + 1

    for i in range(test_count):
        a = random.randint(2, number - 2)
        x = pow(a, d, number)

        if x == 1 or x == number - 1:
            continue

        passed = False
        for r in range(s - 1):
            x = pow(x, 2, number)

            if x == number - 1:
                passed = True
                break

        if passed == False:
            return False

    return True


def make_prime(bits):
    if bits < 8:
        raise ValueError("Prime size must be at least 8 bits for this demo.")

    while True:
        number = random.getrandbits(bits)
        number = number | (1 << (bits - 1))
        number = number | 1

        if is_probably_prime(number):
            return number


def generate_keys(key_size):
    key_size = int(key_size)

    if key_size < 32:
        raise ValueError("RSA key size should be at least 32 bits.")

    half_size = key_size // 2
    e = 65537

    while True:
        p = make_prime(half_size)
        q = make_prime(half_size)

        if p == q:
            continue

        n = p * q
        phi = (p - 1) * (q - 1)

        if gcd(e, phi) == 1:
            d = mod_inverse(e, phi)
            break

    return {
        "p": number_text(p),
        "q": number_text(q),
        "n": number_text(n),
        "phi": number_text(phi),
        "e": number_text(e),
        "d": number_text(d),
        "public_key": {
            "e": number_text(e),
            "n": number_text(n),
        },
        "private_key": {
            "d": number_text(d),
            "n": number_text(n),
        },
    }


def message_to_number(message):
    message_bytes = message.encode("utf-8")
    return int.from_bytes(message_bytes, "big")


def number_to_message(number):
    if number == 0:
        return ""

    byte_count = (number.bit_length() + 7) // 8
    message_bytes = number.to_bytes(byte_count, "big")

    try:
        return message_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return str(message_bytes)


def read_number(value):
    if isinstance(value, int):
        return value

    value = str(value).strip()

    if value.startswith("0x") or value.startswith("0X"):
        return int(value, 16)

    has_hex_letter = False
    for ch in value.upper():
        if ch >= "A" and ch <= "F":
            has_hex_letter = True

    if has_hex_letter:
        return int(value, 16)

    return int(value)


def encrypt_message(plaintext, e, n):
    e = read_number(e)
    n = read_number(n)
    message_number = message_to_number(plaintext)

    if message_number >= n:
        raise ValueError("Plaintext is too large for this RSA key. Use a bigger key size.")

    ciphertext = pow(message_number, e, n)

    return {
        "plaintext_as_integer": number_text(message_number),
        "ciphertext_integer": number_text(ciphertext),
        "ciphertext_hex": hex(ciphertext),
    }


def decrypt_message(ciphertext, d, n):
    ciphertext = read_number(ciphertext)
    d = read_number(d)
    n = read_number(n)

    message_number = pow(ciphertext, d, n)
    plaintext = number_to_message(message_number)

    return {
        "decrypted_integer": number_text(message_number),
        "decrypted_message": plaintext,
    }


def factorization_attack(n, e=None, max_steps=500000):
    n = read_number(n)

    if e != None and str(e).strip() != "":
        e = read_number(e)
    else:
        e = None

    if n % 2 == 0:
        p = 2
        q = n // 2
    else:
        p = None
        q = None
        divisor = 3
        steps = 0
        limit = int(math.isqrt(n))

        while divisor <= limit and steps < max_steps:
            if n % divisor == 0:
                p = divisor
                q = n // divisor
                break

            divisor = divisor + 2
            steps = steps + 1

    if p == None:
        return {
            "success": False,
            "message": (
                "No factor was found within the demo limit. "
                "This is expected for large RSA keys."
            ),
            "max_steps": number_text(max_steps),
        }

    answer = {
        "success": True,
        "p": number_text(p),
        "q": number_text(q),
        "message": "Factorization attack succeeded because this modulus is small enough for demo trial division.",
    }

    if e != None:
        phi = (p - 1) * (q - 1)
        answer["phi"] = number_text(phi)

        if gcd(e, phi) == 1:
            answer["recovered_d"] = number_text(mod_inverse(e, phi))
        else:
            answer["recovered_d"] = "Could not recover d because e and phi are not coprime."

    return answer
