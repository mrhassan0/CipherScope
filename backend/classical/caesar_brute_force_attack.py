ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def preprocess(text):
    cleaned = ""

    for ch in str(text).upper():
        if ch >= "A" and ch <= "Z":
            cleaned = cleaned + ch
        elif ch == " ":
            cleaned = cleaned + ch

    return cleaned


def decrypt_with_shift(ciphertext, shift):
    ciphertext = preprocess(ciphertext)
    plaintext = ""

    for ch in ciphertext:
        if ch == " ":
            plaintext = plaintext + " "
        else:
            old_position = ALPHABET.index(ch)
            new_position = (old_position - shift) % 26
            new_ch = ALPHABET[new_position]
            plaintext = plaintext + new_ch

    return plaintext


def brute_force(ciphertext):
    results = []

    for shift in range(26):
        possible_plaintext = decrypt_with_shift(ciphertext, shift)

        results.append({
            "shift": shift,
            "possible_plaintext": possible_plaintext,
        })

    return {
        "attack_type": "Caesar cipher brute-force attack",
        "important_note": (
            "This brute-force attack works for Caesar cipher substitution only, "
            "because Caesar has only 26 possible shifts. A full monoalphabetic "
            "substitution cipher has 26! possible keys and cannot be brute-forced "
            "like this in a normal class project."
        ),
        "total_shifts_tried": 26,
        "results": results,
    }
