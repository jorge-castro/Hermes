import os
import requests
from dotenv import load_dotenv
from bot_commands import *

def main():
    
    #Load API token from .env
    load_dotenv()
    TOKEN = os.getenv("TOKEN")

    #Format for https requests
    REQUEST_URL = f"https://api.telegram.org/bot{TOKEN}"

    print(requests.get(f"{REQUEST_URL}/getMe").json())


if __name__ == "__main__":
    main()


