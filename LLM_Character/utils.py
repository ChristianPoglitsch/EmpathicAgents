from dotenv import load_dotenv
import os
# load .env file to environment
load_dotenv()
API_KEY = os.getenv('OPENAI_API_KEY')
