import os
from inspect import getmembers, isfunction
from json import dumps
import requests
from flask import Flask, request
from dotenv import load_dotenv
import bot_commands as bot

#Load API token from .env
load_dotenv()
TOKEN = os.getenv("TOKEN")

#Define format for API requests
REQUEST_URL = f"https://api.telegram.org/bot{TOKEN}"

#Define dictionary with available bot commands
COMMANDS = {member[0]:member[1] for member in getmembers(bot, isfunction)}

#Initialize Flask app
app = Flask(__name__)


#Wrapper for json.dumps() with paramaters set to return a pretty string
def beautiful_dumps(data):
    return dumps(data, sort_keys=True, indent=4)


#Meet Hermes!
@app.route("/")
def index():
    return requests.get(f"{REQUEST_URL}/getMe").json()


#Handle bot updates
@app.route(f"/{TOKEN}/", methods=['POST'])
def server():
    #Get update data
    data = request.get_json()

    print(beautiful_dumps(data)) #For debugging

    #Only handle new messages, ignore other kinds of updates
    if "message" not in data.keys():
        return "Thank you for the update!"

    #Define useful variables
    message = data["message"]
    chat = message["chat"]
    chat_id = chat["id"]
    user = message["from"]
    user_id = user["id"]

    #Check for optional fields in the message data
    fields = message.keys()
    entities = message["entities"] if "entities" in fields else None
    text = message["text"] if "text" in fields else None

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

    #If no valid command is found send a message to the user indicating so,
    #otherwise send appropriate response
    if command not in COMMANDS:
        return {
                "method": "sendMessage",
                "chat_id": chat_id,
                "text": "Please send a valid command"
                }
    else:
        #TODO: find a way to pass arguments; right now this only works if
        #function corresponding to command works without passing arguments
        #and if return value can be processed by json.dumps()
        return {
                "method": "sendMessage",
                "chat_id": chat_id,
                "text": beautiful_dumps(COMMANDS[command]())
                }


