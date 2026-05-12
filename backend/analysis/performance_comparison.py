from classical import caesar_brute_force_attack
from classical import double_transposition
from classical import substitution
from public_key import ecc
from public_key import rsa
from symmetric import aes
from symmetric import des
from utils.timing import run_with_time


def make_row(
    algorithm,
    category,
    sample_input,
    key_or_parameters,
    key_generation_time,
    encryption_time,
    decryption_time,
    analysis_or_attack_time,
    extra_output,
    security_note,
    correctness_check,
):
    return {
        "algorithm": algorithm,
        "category": category,
        "sample_input": sample_input,
        "key_or_parameters": key_or_parameters,
        "key_generation_time_seconds": key_generation_time,
        "encryption_time_seconds": encryption_time,
        "decryption_time_seconds": decryption_time,
        "analysis_or_attack_time_seconds": analysis_or_attack_time,
        "extra_output": extra_output,
        "security_note": security_note,
        "correctness_check": correctness_check,
    }


def analyze_substitution():
    plaintext = "HELLO CRYPTO"
    cleaned_plaintext = substitution.clean_text(plaintext)
    key = "QWERTYUIOPASDFGHJKLZXCVBNM"

    ciphertext, encryption_time = run_with_time(substitution.encrypt, plaintext, key)
    decrypted_text, decryption_time = run_with_time(substitution.decrypt, ciphertext, key)
    frequency_result, analysis_time = run_with_time(substitution.frequency, ciphertext)
    attack_result, attack_time = run_with_time(substitution.frequency_attack, ciphertext)
    caesar_result, caesar_time = run_with_time(caesar_brute_force_attack.brute_force, ciphertext)

    total_analysis_time = round(analysis_time + attack_time + caesar_time, 6)

    if decrypted_text == cleaned_plaintext:
        correctness = "Passed"
    else:
        correctness = "Failed"

    return make_row(
        "Substitution Cipher",
        "Classical",
        plaintext,
        "26-letter key",
        "Not needed",
        encryption_time,
        decryption_time,
        total_analysis_time,
        (
            "Letters counted: "
            + str(frequency_result["total_letters"])
            + ", frequency attack mapping size: "
            + str(len(attack_result["cipher_to_plain_guess"]))
            + ", Caesar shifts tried: "
            + str(caesar_result["total_shifts_tried"])
        ),
        (
            "Weak. Frequency analysis can guess a monoalphabetic mapping. Caesar brute "
            "force is still listed as a separate small-shift demo; full substitution "
            "brute force is 26! and is not practical."
        ),
        correctness,
    )


def analyze_double_transposition():
    plaintext = "HELLOCRYPTO"
    first_key = "3 1 2"
    second_key = "2 3 1"

    encrypted_result, encryption_time = run_with_time(
        double_transposition.encrypt,
        plaintext,
        first_key,
        second_key,
    )
    decrypted_result, decryption_time = run_with_time(
        double_transposition.decrypt,
        encrypted_result["ciphertext"],
        first_key,
        second_key,
    )
    frequency_result, analysis_time = run_with_time(
        double_transposition.frequency,
        encrypted_result["ciphertext"],
    )
    attack_result, attack_time = run_with_time(
        double_transposition.permutation_attack,
        encrypted_result["ciphertext"],
    )
    total_analysis_time = round(analysis_time + attack_time, 6)

    if decrypted_result["plaintext_without_trailing_padding"] == plaintext:
        correctness = "Passed"
    else:
        correctness = "Failed"

    return make_row(
        "Double Transposition",
        "Classical",
        plaintext,
        "First key: " + first_key + ", Second key: " + second_key,
        "Not needed",
        encryption_time,
        decryption_time,
        total_analysis_time,
        (
            "Ciphertext: "
            + encrypted_result["ciphertext"]
            + ", letters counted: "
            + str(frequency_result["total_letters"])
            + ", permutation attempts listed: "
            + str(attack_result["total_results"])
        ),
        (
            "Weak by modern standards. Frequency only counts letters; the attack demo "
            "lists every row/column permutation attempt for sizes 1 through 4."
        ),
        correctness,
    )


def analyze_des():
    plaintext = "HELLO DES TEST"
    plaintext_bytes = plaintext.encode("utf-8")

    key, random_key_time = run_with_time(des.make_random_bytes, 8)
    round_keys, round_key_time = run_with_time(des.make_round_keys, key)
    encrypted_bytes, encryption_time = run_with_time(des.encrypt_bytes, plaintext_bytes, round_keys)
    decrypted_bytes, decryption_time = run_with_time(des.decrypt_bytes, encrypted_bytes, round_keys)

    key_generation_time = round(random_key_time + round_key_time, 6)

    if decrypted_bytes.decode("utf-8", errors="replace") == plaintext:
        correctness = "Passed"
    else:
        correctness = "Failed"

    return make_row(
        "DES",
        "Symmetric-key",
        plaintext,
        "Auto-generated 64-bit DES key, 16 round keys",
        key_generation_time,
        encryption_time,
        decryption_time,
        "Not needed",
        "Round keys generated: " + str(len(round_keys)),
        "Old algorithm. Weak today because the effective key size is too small.",
        correctness,
    )


def analyze_aes():
    plaintext = "HELLO AES TEST"
    plaintext_bytes = plaintext.encode("utf-8")

    key, random_key_time = run_with_time(aes.make_random_bytes, 16)
    round_keys, round_key_time = run_with_time(aes.expand_key, key)
    encrypted_bytes, encryption_time = run_with_time(aes.encrypt_bytes, plaintext_bytes, round_keys)
    decrypted_bytes, decryption_time = run_with_time(aes.decrypt_bytes, encrypted_bytes, round_keys)

    key_generation_time = round(random_key_time + round_key_time, 6)

    if decrypted_bytes.decode("utf-8", errors="replace") == plaintext:
        correctness = "Passed"
    else:
        correctness = "Failed"

    return make_row(
        "AES-128",
        "Symmetric-key",
        plaintext,
        "Auto-generated 128-bit AES key, 11 round keys",
        key_generation_time,
        encryption_time,
        decryption_time,
        "Not needed",
        "Round keys generated: " + str(len(round_keys)),
        "Modern and strong when implemented correctly.",
        correctness,
    )


def analyze_rsa():
    plaintext = "HI"
    key_size = 64

    keys, key_generation_time = run_with_time(rsa.generate_keys, key_size)
    encrypted_result, encryption_time = run_with_time(
        rsa.encrypt_message,
        plaintext,
        keys["e"],
        keys["n"],
    )
    decrypted_result, decryption_time = run_with_time(
        rsa.decrypt_message,
        encrypted_result["ciphertext_integer"],
        keys["d"],
        keys["n"],
    )
    attack_result, attack_time = run_with_time(rsa.factorization_attack, 3233, 17)

    if decrypted_result["decrypted_message"] == plaintext:
        correctness = "Passed"
    else:
        correctness = "Failed"

    return make_row(
        "RSA",
        "Public-key",
        plaintext,
        "Demo key size: " + str(key_size) + " bits",
        key_generation_time,
        encryption_time,
        decryption_time,
        attack_time,
        "Attack demo success: " + str(attack_result["success"]),
        (
            "Security depends on factoring n. The attack demo uses small n=3233; "
            "large keys should not factor quickly."
        ),
        correctness,
    )


def analyze_ecc():
    p = 17
    a_value = 2
    b_value = 2
    gx = 5
    gy = 1
    n = 19
    alice_private = 5
    bob_private = 7

    key_result, key_generation_time = run_with_time(
        ecc.generate_public_key,
        p,
        a_value,
        b_value,
        gx,
        gy,
        n,
        alice_private,
    )
    ecdh_result, ecdh_time = run_with_time(
        ecc.run_ecdh,
        p,
        a_value,
        b_value,
        gx,
        gy,
        n,
        alice_private,
        bob_private,
    )
    point_result, point_time = run_with_time(ecc.list_points, p, a_value, b_value)

    if ecdh_result["same_shared_key"] == True:
        correctness = "Passed"
    else:
        correctness = "Failed"

    return make_row(
        "ECC / ECDH",
        "Public-key",
        "Curve over p=17",
        "a=2, b=2, G=(5,1), n=19",
        key_generation_time,
        "Not an encryption algorithm here",
        ecdh_time,
        "Not applicable",
        (
            "Points listed: "
            + str(point_result["count"])
            + ", point listing time: "
            + str(point_time)
            + ", public key: "
            + key_result["public_key"]
        ),
        (
            "Strong public-key idea. This project shows key generation and ECDH, "
            "but it does not include an ECC attack demo."
        ),
        correctness,
    )


def run_full_comparison():
    rows = []

    rows.append(analyze_substitution())
    rows.append(analyze_double_transposition())
    rows.append(analyze_des())
    rows.append(analyze_aes())
    rows.append(analyze_rsa())
    rows.append(analyze_ecc())

    return {
        "message": "Times are measured live on this computer using small demo inputs.",
        "rows": rows,
    }
