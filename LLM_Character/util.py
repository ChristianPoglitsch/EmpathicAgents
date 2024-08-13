import os
import shutil, errno
from dotenv import load_dotenv

# load .env file to environment
load_dotenv()
API_KEY = os.getenv('OPENAI_API_KEY')

def copyanything(src, dst):
  try:
    shutil.copytree(src, dst)
  except OSError as exc: # python >2.5
    if exc.errno in (errno.ENOTDIR, errno.EINVAL):
      shutil.copy(src, dst)
    else: raise

def check_if_file_exists(curr_file): 
    return os.path.isfile(curr_file) 