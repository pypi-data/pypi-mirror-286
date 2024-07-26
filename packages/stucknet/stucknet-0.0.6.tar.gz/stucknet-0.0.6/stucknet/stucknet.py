import random


def generate_random_256_bit_passkey():
    # I hope you didn't try a brute force
    return random.randbytes(32)

def get_flag():
    return 'FLAG{🇮🇱}'


# print hacked message in red
message = 'YOU HAVE BEEN HACKED!!!'
print(f'\033[38;2;255;0;0m{message} \033[38;2;255;255;255m')
