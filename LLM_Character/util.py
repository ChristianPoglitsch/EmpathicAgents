import os
import random
import shutil
import string
import time

from dotenv import load_dotenv

# load .env file to environment
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# https://eli.thegreenplace.net/2008/08/21/robust-exception-handling/
# FIXME: needs proper error handling...


def copyanything(src: str, dst: str):
    """Raises exception"""
    try:
        shutil.copytree(src, dst)
    except OSError:
        raise


def check_if_file_exists(curr_file):
    return os.path.isfile(curr_file)


def receive(s) -> str:
    byte_data = None
    while True:
        time.sleep(1)
        byte_data = s.ReadReceivedData()
        if not byte_data:
            continue
        break
    return byte_data


def get_random_alphanumeric(i=6, j=6):
    k = random.randint(i, j)
    x = "".join(random.choices(string.ascii_letters + string.digits, k=k))
    return x


# if __name__ == "__main__":
# print(BASE_DIR)
