ENGLISH_FREQUENCY_ORDER = "ETAOINSHRDLCUMWFGYPBVKJXQZ"


def count_letters(text):
    counts = {}

    for code in range(ord("A"), ord("Z") + 1):
        letter = chr(code)
        counts[letter] = 0

    for ch in text.upper():
        if ch >= "A" and ch <= "Z":
            counts[ch] = counts[ch] + 1

    total = 0
    for letter in counts:
        total = total + counts[letter]

    percentages = {}
    for letter in counts:
        if total == 0:
            percentages[letter] = 0
        else:
            percentages[letter] = round((counts[letter] / total) * 100, 2)

    return {
        "total_letters": total,
        "counts": counts,
        "percentages": percentages,
    }


def make_frequency_rows(text):
    result = count_letters(text)
    rows = []

    for letter in result["counts"]:
        rows.append({
            "letter": letter,
            "count": result["counts"][letter],
            "percentage": result["percentages"][letter],
        })

    return rows


def make_ranked_frequency_rows(text):
    rows = make_frequency_rows(text)
    rows.sort(key=lambda row: (-row["count"], row["letter"]))

    return rows


def frequency_order(text):
    rows = make_ranked_frequency_rows(text)
    order = ""

    for row in rows:
        if row["count"] > 0:
            order = order + row["letter"]

    return order
