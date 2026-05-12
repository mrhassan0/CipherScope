import random


INFINITY = None


def mod_inverse(number, p):
    number = number % p

    if number == 0:
        raise ValueError("Cannot find inverse of 0.")

    old_r = number
    r = p
    old_s = 1
    s = 0

    while r != 0:
        quotient = old_r // r

        new_r = old_r - quotient * r
        old_r = r
        r = new_r

        new_s = old_s - quotient * s
        old_s = s
        s = new_s

    return old_s % p


def validate_curve(p, a, b):
    p = int(p)
    a = int(a)
    b = int(b)

    if p <= 2:
        raise ValueError("p must be an odd prime number for this simple ECC demo.")

    discriminant = (4 * (a ** 3) + 27 * (b ** 2)) % p

    if discriminant == 0:
        raise ValueError("Invalid curve. The discriminant is 0 modulo p.")

    return p, a, b


def point_text(point):
    if point == INFINITY:
        return "Point at infinity"

    return "(" + str(point[0]) + ", " + str(point[1]) + ")"


def is_on_curve(point, p, a, b):
    if point == INFINITY:
        return True

    x = point[0]
    y = point[1]

    left_side = (y * y) % p
    right_side = (x * x * x + a * x + b) % p

    return left_side == right_side


def list_points(p, a, b):
    p, a, b = validate_curve(p, a, b)

    if p > 1000:
        return {
            "points": [],
            "count": 0,
            "message": "p is too large to list all points in a browser demo. Use a small p such as 17 or 23.",
        }

    points = []

    for x in range(p):
        for y in range(p):
            point = (x, y)

            if is_on_curve(point, p, a, b):
                points.append(point)

    readable_points = []
    for point in points:
        readable_points.append(point_text(point))

    return {
        "points": readable_points,
        "count": len(points),
        "message": "All finite points were listed. The point at infinity is also part of the group.",
    }


def add_points(point1, point2, p, a):
    if point1 == INFINITY:
        return point2

    if point2 == INFINITY:
        return point1

    x1 = point1[0]
    y1 = point1[1]
    x2 = point2[0]
    y2 = point2[1]

    if x1 == x2 and (y1 + y2) % p == 0:
        return INFINITY

    if point1 == point2:
        top = (3 * x1 * x1 + a) % p
        bottom = mod_inverse(2 * y1, p)
        slope = (top * bottom) % p
    else:
        top = (y2 - y1) % p
        bottom = mod_inverse(x2 - x1, p)
        slope = (top * bottom) % p

    x3 = (slope * slope - x1 - x2) % p
    y3 = (slope * (x1 - x3) - y1) % p

    return (x3, y3)


def scalar_multiply(private_key, point, p, a):
    private_key = int(private_key)
    result = INFINITY
    add_this = point

    while private_key > 0:
        if private_key % 2 == 1:
            result = add_points(result, add_this, p, a)

        add_this = add_points(add_this, add_this, p, a)
        private_key = private_key // 2

    return result


def generate_public_key(p, a, b, gx, gy, n, private_key=None):
    p, a, b = validate_curve(p, a, b)
    gx = int(gx)
    gy = int(gy)
    n = int(n)

    base_point = (gx, gy)

    if not is_on_curve(base_point, p, a, b):
        raise ValueError("Base point G is not on the curve.")

    if private_key == None or str(private_key).strip() == "":
        private_key = random.randint(1, n - 1)
    else:
        private_key = int(private_key)

    if private_key <= 0 or private_key >= n:
        raise ValueError("Private key must be between 1 and n-1.")

    public_key = scalar_multiply(private_key, base_point, p, a)

    return {
        "private_key": private_key,
        "public_key": point_text(public_key),
        "base_point": point_text(base_point),
    }


def run_ecdh(p, a, b, gx, gy, n, alice_private, bob_private):
    p, a, b = validate_curve(p, a, b)
    gx = int(gx)
    gy = int(gy)
    n = int(n)
    alice_private = int(alice_private)
    bob_private = int(bob_private)

    base_point = (gx, gy)

    if not is_on_curve(base_point, p, a, b):
        raise ValueError("Base point G is not on the curve.")

    if alice_private <= 0 or alice_private >= n:
        raise ValueError("Alice private key must be between 1 and n-1.")

    if bob_private <= 0 or bob_private >= n:
        raise ValueError("Bob private key must be between 1 and n-1.")

    alice_public = scalar_multiply(alice_private, base_point, p, a)
    bob_public = scalar_multiply(bob_private, base_point, p, a)

    alice_shared = scalar_multiply(alice_private, bob_public, p, a)
    bob_shared = scalar_multiply(bob_private, alice_public, p, a)

    return {
        "alice_private": alice_private,
        "bob_private": bob_private,
        "alice_public": point_text(alice_public),
        "bob_public": point_text(bob_public),
        "alice_shared_key": point_text(alice_shared),
        "bob_shared_key": point_text(bob_shared),
        "same_shared_key": alice_shared == bob_shared,
    }
