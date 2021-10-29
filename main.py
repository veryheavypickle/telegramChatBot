import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import json


def setup():
    keys = getKeys()
    login(keys)


def getKeys():
    keysPath = "keys.json"
    keys = openJSON(keysPath)

    if keys == {}:
        keys = createKeys(keysPath)

    return keys


def createKeys(path):
    print("\nPaste the telegram token below")
    token = input("Token: ")
    data = {"telegramToken": token}
    writeJSON(path, data)
    print("New keys file created!")
    return data


def openJSON(path):
    # Path should always contain the extension
    try:
        jsonFile = open(path)
        return json.load(jsonFile)
    except FileNotFoundError:
        return {}


def writeJSON(path, data):
    assert type(data) is dict
    jsonFile = open(path, "w")
    json.dump(data, jsonFile)


# Telegram login
def login(keys):
    print("logging in...")
    updater = Updater(token=keys["telegramToken"], use_context=True)
    dispatcher = updater.dispatcher
    handlers = [MessageHandler(Filters.text & (~Filters.command), messageHandler),
                CommandHandler('start', start)]

    # An example of adding another handler for the command "/test"
    # where testFunction has to be a python programmed function
    """
    handlers = [MessageHandler(Filters.text & (~Filters.command), messageHandler),
                CommandHandler('start', start),
                CommandHandler('test', testFunction)]
    """
    # Example of testFunction
    """
    def testFunction(update, context):
        userID = str(update.effective_chat.id)
        sendMessage(context, userID, "Bot works well!")
    """

    # Add each handler - a handler is a python function
    for handler in handlers:
        dispatcher.add_handler(handler)
    updater.start_polling()
    print("logged in and chat started!")


# Telegram command/message handlers
def start(update, context):
    userID = str(update.effective_chat.id)
    sendMessage(context, userID, "Hello!")


def sendMessage(context, userID, message):
    try:
        context.bot.send_message(chat_id=userID,
                                 text=message,
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
    except telegram.error.BadRequest:
        context.bot.send_message(chat_id=userID,
                                 text=message,
                                 parse_mode=telegram.ParseMode.HTML)


# This is the general message handler
def messageHandler(update, context):
    userID = str(update.effective_chat.id)  # update.effective_chat.id is the chat id
    textMessage = update.message.text  # update.message.text is the message that user sent

    # Returns the same message to the user
    sendMessage(context, userID, textMessage)


if __name__ == '__main__':
    setup()
