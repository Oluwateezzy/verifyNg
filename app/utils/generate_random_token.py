import random


def generate_random_code(length: int) -> str:
    add = 1
    max_len = 12 - add

    if length > max_len:
        return generate_random_code(max_len) + generate_random_code(length - max_len)

    max_value = 10 ** (length + add)
    min_value = max_value // 10
    number = random.randint(min_value, max_value - 1)

    return str(number)[add:]
