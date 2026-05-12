import sys
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_DIR / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from classical import double_transposition
from classical import caesar_brute_force_attack
from classical import substitution
from analysis import performance_comparison
from public_key import ecc
from public_key import rsa
from symmetric import aes
from symmetric import des


def check(condition, message):
    if condition:
        print("PASS:", message)
    else:
        raise AssertionError(message)


def test_substitution():
    key = "QWERTYUIOPASDFGHJKLZXCVBNM"
    plaintext = "hello crypto"
    cleaned_plaintext = substitution.clean_text(plaintext)
    ciphertext = substitution.encrypt(plaintext, key)
    decrypted = substitution.decrypt(ciphertext, key)

    check(decrypted == cleaned_plaintext, "Substitution encrypt and decrypt")
    check(ciphertext.isupper() == True, "Substitution output is uppercase")
    check(" " in decrypted, "Substitution keeps spaces")
    caesar_attack = caesar_brute_force_attack.brute_force("KHOOR ZRUOG")
    check("results" in caesar_attack, "Caesar brute force output")
    check(caesar_attack["total_shifts_tried"] == 26, "Separate Caesar brute force file works")
    check(caesar_attack["results"][3]["possible_plaintext"] == "HELLO WORLD", "Caesar brute force finds shift")

    frequency_attack = substitution.frequency_attack(ciphertext)
    check("suggested_plaintext" in frequency_attack, "Substitution frequency attack suggests plaintext")
    check(len(frequency_attack["cipher_to_plain_guess"]) == 26, "Substitution frequency attack builds mapping")
    check(
        frequency_attack["can_recover_full_key_by_frequency_only"] == False,
        "Substitution frequency attack explains heuristic limit",
    )


def test_double_transposition():
    plaintext = "hello crypto"
    cleaned_plaintext = double_transposition.clean_text(plaintext)
    encrypted = double_transposition.encrypt(plaintext, "3 1 2", "2 3 1")
    decrypted = double_transposition.decrypt(encrypted["ciphertext"], "3 1 2", "2 3 1")

    check(
        decrypted["plaintext_without_trailing_padding"] == cleaned_plaintext,
        "Double transposition encrypt and decrypt",
    )
    check(encrypted["ciphertext"].isupper() == True, "Double transposition output is uppercase")
    check(" " in decrypted["plaintext_without_trailing_padding"], "Double transposition keeps spaces")

    grid_result = double_transposition.encrypt("MEET ME AT NOON", "3 1 4 2", "2 4 1 3")
    check(
        double_transposition.get_letters_only(grid_result["ciphertext"]) != double_transposition.get_letters_only("MEET ME AT NOON"),
        "Double transposition uses row and column permutation",
    )
    check(grid_result["method"] == "First key permutes rows. Second key permutes columns.", "Double transposition explains row and column keys")
    grid_decrypted = double_transposition.decrypt(grid_result["ciphertext"], "3 1 4 2", "2 4 1 3")
    check(
        grid_decrypted["plaintext_without_trailing_padding"] == "MEET ME AT NOON",
        "Double transposition decrypts row and column example exactly",
    )

    attack_plaintext = "THE SECRET MESSAGE IS MEET ME AT NOON"
    attack_encrypted = double_transposition.encrypt(attack_plaintext, "3 1 2", "2 3 1")
    automatic_attack = double_transposition.permutation_attack(attack_encrypted["ciphertext"])
    check(automatic_attack["total_candidates_tried"] == 1089, "Double transposition automatic attack tries all 1 to 4 attempts")
    check(automatic_attack["total_results"] == 1089, "Double transposition automatic attack returns all 1089 results")
    check(automatic_attack["valid_decryptions"] == 417, "Double transposition automatic attack decrypts valid block sizes")
    check(automatic_attack["skipped_results"] == 672, "Double transposition automatic attack lists invalid block sizes as skipped")
    check("best_guess" not in automatic_attack, "Double transposition permutation attack does not return best guess")

    found_automatic_attack_result = False

    for result in automatic_attack["results"]:
        if (
            result["possible_plaintext"] == double_transposition.clean_text(attack_plaintext)
            and result["row_key"] == [3, 1, 2]
            and result["column_key"] == [2, 3, 1]
        ):
            found_automatic_attack_result = True

    check(found_automatic_attack_result, "Double transposition automatic attack includes correct attempt without keys")


def test_des():
    key = bytes.fromhex("133457799BBCDFF1")
    block = bytes.fromhex("0123456789ABCDEF")
    round_keys = des.make_round_keys(key)
    encrypted_bits = des.encrypt_block(des.bytes_to_bits(block), round_keys)
    encrypted_bytes = des.bits_to_bytes(encrypted_bits)

    check(encrypted_bytes.hex().upper() == "85E813540F0AB405", "DES known test vector")

    result = des.run_des("HELLO DES")
    check(result["decrypted_plaintext"] == "HELLO DES", "DES full run decrypts correctly")

    encrypted_result = des.encrypt_text("DES MODE TEST")
    decrypted_result = des.decrypt_text(
        encrypted_result["ciphertext_hex"],
        encrypted_result["generated_key_hex"],
    )
    check(decrypted_result["decrypted_plaintext"] == "DES MODE TEST", "DES separate modes")


def test_aes():
    key = bytes.fromhex("000102030405060708090A0B0C0D0E0F")
    block = bytes.fromhex("00112233445566778899AABBCCDDEEFF")
    round_keys = aes.expand_key(key)
    encrypted = aes.encrypt_block(block, round_keys)
    decrypted = aes.decrypt_block(encrypted, round_keys)

    check(encrypted.hex().upper() == "69C4E0D86A7B0430D8CDB78070B4C55A", "AES known test vector")
    check(decrypted == block, "AES known test vector decrypt")

    result = aes.run_aes("HELLO AES")
    check(result["decrypted_plaintext"] == "HELLO AES", "AES full run decrypts correctly")

    encrypted_result = aes.encrypt_text("AES MODE TEST")
    decrypted_result = aes.decrypt_text(
        encrypted_result["ciphertext_hex"],
        encrypted_result["generated_key_hex"],
    )
    check(decrypted_result["decrypted_plaintext"] == "AES MODE TEST", "AES separate modes")


def test_rsa():
    keys = rsa.generate_keys(64)
    check(isinstance(keys["n"], str), "RSA modulus output is full digit string")
    check(isinstance(keys["d"], str), "RSA private exponent output is full digit string")

    encrypted = rsa.encrypt_message("HI", keys["e"], keys["n"])
    check(isinstance(encrypted["ciphertext_integer"], str), "RSA ciphertext output is full digit string")

    decrypted = rsa.decrypt_message(encrypted["ciphertext_integer"], keys["d"], keys["n"])

    check(decrypted["decrypted_message"] == "HI", "RSA encrypt and decrypt")

    attack = rsa.factorization_attack(3233, 17)
    check(attack["success"] == True, "RSA factorization attack demo")


def test_ecc():
    points = ecc.list_points(17, 2, 2)
    check(points["count"] > 0, "ECC point listing")

    key = ecc.generate_public_key(17, 2, 2, 5, 1, 19, 5)
    check(key["public_key"] == "(9, 16)", "ECC public key generation")

    exchange = ecc.run_ecdh(17, 2, 2, 5, 1, 19, 5, 7)
    check(exchange["same_shared_key"] == True, "ECDH shared key")


def test_performance_comparison():
    result = performance_comparison.run_full_comparison()
    rows = result["rows"]

    check(len(rows) == 6, "Performance comparison has all six algorithms")

    for row in rows:
        check(row["correctness_check"] == "Passed", row["algorithm"] + " comparison correctness")


if __name__ == "__main__":
    test_substitution()
    test_double_transposition()
    test_des()
    test_aes()
    test_rsa()
    test_ecc()
    test_performance_comparison()
    print("All checks passed.")
