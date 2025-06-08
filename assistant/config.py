import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    #WHATSAPP_API_URL = os.getenv("WHATSAPP_API_URL")
    #WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
    #EMBRAPA_API_URL = os.getenv("EMBRAPA_API_URL")
    #EMBRAPA_API_TOKEN = os.getenv("EMBRAPA_API_TOKEN")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID")