from utils.frequency_analysis import ENGLISH_FREQUENCY_ORDER
from utils.frequency_analysis import count_letters
from utils.frequency_analysis import frequency_order
from utils.frequency_analysis import make_ranked_frequency_rows


ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def clean_key(key):
    cleaned = ""

    for ch in key.upper():
        if ch >= "A" and ch <= "Z":
            cleaned = cleaned + ch

    return cleaned


def clean_text(text):
    cleaned = ""

    for ch in str(text).upper():
        if ch >= "A" and ch <= "Z":
            cleaned = cleaned + ch
        elif ch == " ":
            cleaned = cleaned + ch

    return cleaned


def validate_key(key):
    key = clean_key(key)

    if len(key) != 26:
        raise ValueError("The substitution key must have exactly 26 letters.")

    used = []
    for ch in key:
        if ch in used:
            raise ValueError("The substitution key must not repeat letters.")
        used.append(ch)

    return key


def encrypt(plaintext, key):
    key = validate_key(key)
    plaintext = clean_text(plaintext)
    ciphertext = ""

    for ch in plaintext:
        if ch == " ":
            ciphertext = ciphertext + ch
        else:
            position = ALPHABET.index(ch)
            new_ch = key[position]
            ciphertext = ciphertext + new_ch

    return ciphertext


def decrypt(ciphertext, key):
    key = validate_key(key)
    ciphertext = clean_text(ciphertext)
    plaintext = ""

    for ch in ciphertext:
        if ch == " ":
            plaintext = plaintext + ch
        else:
            position = key.index(ch)
            new_ch = ALPHABET[position]
            plaintext = plaintext + new_ch

    return plaintext


def frequency(text):
    return count_letters(clean_text(text))


def frequency_attack(ciphertext):
    ciphertext = clean_text(ciphertext)
    ranked_rows = make_ranked_frequency_rows(ciphertext)
    cipher_to_plain_guess = {}
    mapping_rows = []

    for index in range(len(ranked_rows)):
        cipher_letter = ranked_rows[index]["letter"]
        guessed_plain_letter = ENGLISH_FREQUENCY_ORDER[index]
        cipher_to_plain_guess[cipher_letter] = guessed_plain_letter

        mapping_rows.append({
            "rank": index + 1,
            "cipher_letter": cipher_letter,
            "count": ranked_rows[index]["count"],
            "percentage": ranked_rows[index]["percentage"],
            "guessed_plain_letter": guessed_plain_letter,
        })

    guessed_plaintext = ""

    for ch in ciphertext:
        if ch == " ":
            guessed_plaintext = guessed_plaintext + " "
        else:
            guessed_plaintext = guessed_plaintext + cipher_to_plain_guess[ch]

    return {
        "attack_type": "Monoalphabetic substitution frequency attack",
        "important_note": (
            "This is a heuristic guess, not guaranteed decryption. It works best "
            "on long ciphertext because short text may not match normal English "
            "letter frequencies."
        ),
        "english_frequency_order": ENGLISH_FREQUENCY_ORDER,
        "cipher_frequency_order": frequency_order(ciphertext),
        "cipher_to_plain_guess": cipher_to_plain_guess,
        "mapping_rows": mapping_rows,
        "suggested_plaintext": guessed_plaintext,
        "frequency_analysis": count_letters(ciphertext),
        "can_recover_full_key_by_frequency_only": False,
    }
