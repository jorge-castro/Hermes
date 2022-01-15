import os
from inspect import getmembers, isfunction

import requests
from flask import Flask, request

import bot_commands as bot


#Load API token from environment
TOKEN = os.getenv("TOKEN")

#Define format for API requests
REQUEST_URL = f"https://api.telegram.org/bot{TOKEN}"

#Define dictionary with available bot commands
COMMANDS = {member[0]:member[1] for member in getmembers(bot, isfunction)}

#Initialize Flask app
app = Flask(__name__)


#Meet Hermes!
@app.route("/")
def index():
    return requests.get(f"{REQUEST_URL}/getMe").json()


#Handle bot updates
@app.route(f"/{TOKEN}/", methods=['POST'])
def server():
    #Get update data
    data = request.get_json()

    #Only handle new messages, ignore other kinds of updates
    if "message" not in data:
        return "Thank you for the update!"

    #Define useful variables
    message = data["message"]
    chat = message["chat"]
    chat_id = chat["id"]

    #Check for optional fields in the message data
    entities = message["entities"] if "entities" in message else None
    text = message["text"] if "text" in message else None

    #Define variable to hold bot command if one is found
    command = None

    #Check if bot command exists in message
    if entities:
        for entity in entities:
            if entity["type"] == "bot_command":
                offset = entity["offset"]
                length = entity["length"]
                command = text[offset+1:length] #Add 1 to offset due to "/"
                break

    #Define variable to hold reply
    reply = "" 

    #If no valid command is found send a message to the user indicating so
    if command not in COMMANDS:
        reply = "Please send a valid command. Use /help for more information."

    #Handle /get_crypto_price
    elif command == "get_crypto_price":
        reply = COMMANDS[command](",".join(text[offset+length:].split()))

        if reply == "{}":
            reply = "Please pass valid identifier(s) to the command.\n\n" \
                    "E.g., /get_crypto_price bitcoin handshake\n\n" \
                    "See https://api.coingecko.com/api/v3/coins/list " \
                    "for a full list."

    #Handle /get_stock_price
    elif command == "get_stock_price":
        reply = COMMANDS[command](" ".join(text[offset+length:].split()))

        if reply == "{}":
            reply = "Please pass valid ticker(s) to the command.\n\n" \
                    "E.g., /get_stock_price MSFT GOOG\n\n" \
                    "See https://stockanalysis.com/stocks/ for a full list."

    #Handle /start and /help
    else:
        reply = COMMANDS[command]()
    
    #Send message with appropriate reply to the chat 
    return {
        "method": "sendMessage",
        "chat_id": chat_id,
        "text": reply
        }


