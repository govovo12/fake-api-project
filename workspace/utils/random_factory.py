import random
import string

def simple_random_string(length: int) -> list:
    return random.choices(string.ascii_letters + string.digits, k=length)
