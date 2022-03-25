from random import randint
from time import sleep


class TimeoutConnection(Exception):
    pass


def request(timeout: int = 5):
    fake_delay = randint(0, 60) / 10
    if fake_delay > timeout:
        sleep(timeout)
        raise TimeoutConnection(f"Can not receive response after {timeout} seconds")
    else:
        sleep(fake_delay)
