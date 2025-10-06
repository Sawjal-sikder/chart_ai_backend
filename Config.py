from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


model = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))