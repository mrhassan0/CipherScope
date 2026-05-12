from itertools import permutations
from math import factorial

from utils.frequency_analysis import count_letters


def clean_text(text):
    cleaned = ""

    for ch in str(text).upper():
        if ch >= "A" and ch <= "Z":
            cleaned = cleaned + ch
        elif ch == " ":
            cleaned = cleaned + ch

    return cleaned


def get_letters_only(text):
    letters = ""

    for ch in clean_text(text):
        if ch >= "A" and ch <= "Z":
            letters = letters + ch

    return letters


def put_spaces_back(letters, template_text):
    answer = ""
    letter_position = 0
    template_text = clean_text(template_text)

    for ch in template_text:
        if ch == " ":
            answer = answer + " "
        else:
            if letter_position < len(letters):
                answer = answer + letters[letter_position]
                letter_position = letter_position + 1

    while letter_position < len(letters):
        answer = answer + letters[letter_position]
        letter_position = letter_position + 1

    return answer


def parse_key(key_text):
    key_text = str(key_text).replace(",", " ")
    parts = key_text.split()

    if len(parts) == 1 and parts[0].isdigit() and len(parts[0]) > 1:
        parts = list(parts[0])

    key = []
    for part in parts:
        if not part.isdigit():
            raise ValueError("Permutation keys must contain only numbers.")
        key.append(int(part))

    if len(key) == 0:
        raise ValueError("Permutation key cannot be empty.")

    sorted_key = sorted(key)
    expected = []
    for number in range(1, len(key) + 1):
        expected.append(number)

    if sorted_key != expected:
        raise ValueError("Permutation key must use each number from 1 to key size once.")

    return key


def pad_text(text, block_size, padding_char="X"):
    padded = text

    while len(padded) % block_size != 0:
        padded = padded + padding_char

    return padded


def make_grid(block, row_count, column_count):
    grid = []
    position = 0

    for row_number in range(row_count):
        row = ""

        for column_number in range(column_count):
            row = row + block[position]
            position = position + 1

        grid.append(row)

    return grid


def grid_to_text(grid):
    text = ""

    for row in grid:
        text = text + row

    return text


def permute_rows(grid, row_key):
    new_grid = []

    for row_position in row_key:
        new_grid.append(grid[row_position - 1])

    return new_grid


def reverse_rows(grid, row_key):
    new_grid = [""] * len(row_key)

    for new_position in range(len(row_key)):
        old_position = row_key[new_position] - 1
        new_grid[old_position] = grid[new_position]

    return new_grid


def permute_columns(grid, column_key):
    new_grid = []

    for row in grid:
        new_row = ""

        for column_position in column_key:
            new_row = new_row + row[column_position - 1]

        new_grid.append(new_row)

    return new_grid


def reverse_columns(grid, column_key):
    new_grid = []

    for row in grid:
        new_row = [""] * len(column_key)

        for new_position in range(len(column_key)):
            old_position = column_key[new_position] - 1
            new_row[old_position] = row[new_position]

        new_grid.append("".join(new_row))

    return new_grid


def encrypt_letters_with_grid(letters, row_key, column_key):
    row_count = len(row_key)
    column_count = len(column_key)
    block_size = row_count * column_count
    padded = pad_text(letters, block_size)

    after_row_text = ""
    after_column_text = ""

    for start in range(0, len(padded), block_size):
        block = padded[start:start + block_size]
        grid = make_grid(block, row_count, column_count)
        row_grid = permute_rows(grid, row_key)
        column_grid = permute_columns(row_grid, column_key)

        after_row_text = after_row_text + grid_to_text(row_grid)
        after_column_text = after_column_text + grid_to_text(column_grid)

    return after_row_text, after_column_text


def decrypt_letters_with_grid(ciphertext_letters, row_key, column_key):
    row_count = len(row_key)
    column_count = len(column_key)
    block_size = row_count * column_count

    if len(ciphertext_letters) % block_size != 0:
        raise ValueError("Ciphertext length must match row key size times column key size.")

    after_reverse_column_text = ""
    after_reverse_row_text = ""

    for start in range(0, len(ciphertext_letters), block_size):
        block = ciphertext_letters[start:start + block_size]
        grid = make_grid(block, row_count, column_count)
        column_grid = reverse_columns(grid, column_key)
        row_grid = reverse_rows(column_grid, row_key)

        after_reverse_column_text = after_reverse_column_text + grid_to_text(column_grid)
        after_reverse_row_text = after_reverse_row_text + grid_to_text(row_grid)

    return after_reverse_column_text, after_reverse_row_text


def make_warning(plaintext_letters, ciphertext_letters):
    if plaintext_letters == ciphertext_letters:
        return (
            "Warning: the ciphertext looks the same as the plaintext for this "
            "input. This can happen with repeated letters or a weak key choice. "
            "Try a longer message or different keys."
        )

    return "No warning."


def encrypt(plaintext, first_key_text, second_key_text):
    row_key = parse_key(first_key_text)
    column_key = parse_key(second_key_text)
    template_text = clean_text(plaintext)
    plaintext_letters = get_letters_only(plaintext)

    after_first, after_second = encrypt_letters_with_grid(plaintext_letters, row_key, column_key)
    ciphertext_with_spaces = put_spaces_back(after_second, template_text)
    after_first_with_spaces = put_spaces_back(after_first, template_text)
    warning = make_warning(plaintext_letters, after_second)

    return {
        "ciphertext": ciphertext_with_spaces,
        "intermediate_ciphertext": after_first_with_spaces,
        "row_key": row_key,
        "column_key": column_key,
        "warning": warning,
        "method": "First key permutes rows. Second key permutes columns.",
        "padding_note": "Padding character X is added when the block is incomplete.",
        "frequency_analysis": count_letters(ciphertext_with_spaces),
    }


def decrypt(ciphertext, first_key_text, second_key_text):
    row_key = parse_key(first_key_text)
    column_key = parse_key(second_key_text)
    template_text = clean_text(ciphertext)
    ciphertext_letters = get_letters_only(ciphertext)

    after_reverse_second, after_reverse_first = decrypt_letters_with_grid(ciphertext_letters, row_key, column_key)
    plaintext_with_padding = put_spaces_back(after_reverse_first, template_text)
    plaintext_without_padding = put_spaces_back(after_reverse_first.rstrip("X"), template_text)

    return {
        "plaintext_without_trailing_padding": plaintext_without_padding,
        "plaintext_with_padding": plaintext_with_padding,
        "intermediate_plaintext": put_spaces_back(after_reverse_second, template_text),
    }


def frequency(text):
    return count_letters(clean_text(text))


def make_size_pairs(ciphertext_length):
    size_pairs = []

    for row_size in range(1, 5):
        for column_size in range(1, 5):
            block_size = row_size * column_size

            size_pairs.append({
                "row_size": row_size,
                "column_size": column_size,
                "block_size": block_size,
                "attempts": factorial(row_size) * factorial(column_size),
                "can_decrypt": ciphertext_length % block_size == 0,
            })

    return size_pairs


def permutation_attack(ciphertext):
    ciphertext = clean_text(ciphertext)
    ciphertext_letters = get_letters_only(ciphertext)

    if len(ciphertext_letters) == 0:
        raise ValueError("Ciphertext must contain letters.")

    size_pairs = make_size_pairs(len(ciphertext_letters))
    results = []
    tried = 0
    valid_decryptions = 0
    skipped_results = 0

    for size_pair in size_pairs:
        row_size = size_pair["row_size"]
        column_size = size_pair["column_size"]
        block_size = size_pair["block_size"]
        row_keys = permutations(range(1, row_size + 1))
        column_key_list = list(permutations(range(1, column_size + 1)))

        for row_key_tuple in row_keys:
            row_key = list(row_key_tuple)

            for column_key_tuple in column_key_list:
                column_key = list(column_key_tuple)

                result = {
                    "attempt_number": tried + 1,
                    "status": "skipped",
                    "row_size": row_size,
                    "column_size": column_size,
                    "block_size": block_size,
                    "row_key": row_key,
                    "column_key": column_key,
                    "possible_plaintext": "",
                }

                if size_pair["can_decrypt"]:
                    _, plaintext_letters = decrypt_letters_with_grid(
                        ciphertext_letters,
                        row_key,
                        column_key,
                    )
                    plaintext_without_padding = put_spaces_back(plaintext_letters.rstrip("X"), ciphertext)

                    result["status"] = "decrypted"
                    result["possible_plaintext"] = plaintext_without_padding
                    valid_decryptions = valid_decryptions + 1
                else:
                    result["note"] = (
                        "Skipped because ciphertext length is not divisible by "
                        "row size times column size."
                    )
                    skipped_results = skipped_results + 1

                results.append(result)
                tried = tried + 1

    return {
        "attack_type": "Double transposition small-key permutation attack",
        "important_note": (
            "This lists every row-key and column-key permutation attempt for "
            "row and column sizes 1 through 4. Attempts whose block size does "
            "not divide the ciphertext length are listed as skipped."
        ),
        "searched_key_sizes": size_pairs,
        "total_results": len(results),
        "total_candidates_tried": tried,
        "valid_decryptions": valid_decryptions,
        "skipped_results": skipped_results,
        "results": results,
    }
