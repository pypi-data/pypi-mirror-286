import random


def generate_random_256_bit_passkey():
    # I hope you didn't try a brute force
    return random.randbytes(32)

def get_flag():
    # whoa, that was risky!
    # fortunately, I censored the flag before you captured it and permanently deleted it from pypi
    return 'SUS{n0t_th3_f14g}'


# print hacked message in red
message = 'YOU HAVE BEEN HACKED!!!'
print(f'\033[38;2;255;0;0m{message} \033[38;2;255;255;255m')
