from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')
import os

class Config:
    DEBUG = True
    CACHE_TYPE = "RedisCache"
    CACHE_DEFAULT_TIMEOUT = 2592000
    CACHE_REDIS_URL = os.getenv('REDIS_URL')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')


