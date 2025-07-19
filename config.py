from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')
import os

class Config:
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')


