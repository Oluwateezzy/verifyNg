import random


def generate_random_code(length: int) -> str:
    add = 1
    max_len = (
        12 - add
    )  # 12 is the min safe number random can generate without trailing zeros.

    if length > max_len:
        return generate_random_code(max_len) + generate_random_code(length - max_len)

    max_value = 10 ** (length + add)
    min_value = max_value // 10  # Equivalent to 10^n
    number = random.randint(min_value, max_value - 1)

    return str(number)[add:]


# Example usage:
print(generate_random_code(10))
