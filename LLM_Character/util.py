import os
import random
import shutil, errno
import string
from dotenv import load_dotenv

# load .env file to environment
load_dotenv()
API_KEY = os.getenv('OPENAI_API_KEY')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def copyanything(src, dst):
  try:
    shutil.copytree(src, dst)
  except OSError as exc: # python >2.5
    if exc.errno in (errno.ENOTDIR, errno.EINVAL):
      shutil.copy(src, dst)
    else: raise

def check_if_file_exists(curr_file): 
    return os.path.isfile(curr_file)

def get_random_alphanumeric(i=6, j=6): 
  k = random.randint(i, j)
  x = ''.join(random.choices(string.ascii_letters + string.digits, k=k))
  return x
# if __name__ == "__main__":
  # print(BASE_DIR)
