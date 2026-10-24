import random
import string

CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

STATES = {
    "01": "Jammu & Kashmir", "06": "Haryana", "07": "Delhi",
    "09": "Uttar Pradesh", "24": "Gujarat", "27": "Maharashtra",
    "29": "Karnataka", "33": "Tamil Nadu", "36": "Telangana",
    "19": "West Bengal", "08": "Rajasthan", "05": "Uttarakhand",
}


def checksum(first14):
    total = 0
    for i, ch in enumerate(first14):
        factor = 1 if i % 2 == 0 else 2
        prod = CHARS.index(ch) * factor
        total += prod // 36 + prod % 36
    return CHARS[(36 - total % 36) % 36]


def make_gstin(state_code):
    pan = (
        "".join(random.choices(string.ascii_uppercase, k=5))
        + "".join(random.choices(string.digits, k=4))
        + random.choice(string.ascii_uppercase)
    )
    entity = random.choice("123456789")
    first14 = state_code + pan + entity + "Z"
    return first14 + checksum(first14)


def is_valid_gstin(g):
    return len(g) == 15 and g[:2] in STATES and g[14] == checksum(g[:14])


if __name__ == "__main__":
    for code in ["05", "07", "27"]:
        g = make_gstin(code)
        print(g, STATES[code], is_valid_gstin(g))
