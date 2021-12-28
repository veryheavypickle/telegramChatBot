import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import json
import os


def setup():
    global currentLanguage, usersDir
    if not os.path.isdir(usersDir):
        os.mkdir(usersDir)
    languages = getLanguage()
    return languages[currentLanguage]


def getLanguage():
    global languagesPath
    languages = openJSON(languagesPath)

    if languages == {}:
        languages = createDefaultLanguages(languagesPath)
    return languages


def getTelegramToken():
    global credentialsPath
    token = openJSON(credentialsPath)

    if token == {}:
        token = createTelegramToken()

    token = testTelegramToken(token=token["telegramToken"])

    return token


def createDefaultLanguages(path):
    english = {
        "pasteTelegramToken": "Paste the telegram token below",
        "newKeysFileCreated": "New keys file created!",
        "loginMessage": "logging in...",
        "loginSuccess": "logged in and chat started!",
        "invalidToken": "Invalid token"
    }
    spanish = {
        "pasteTelegramToken": "Pegue el token de telegram a continuación",
        "newKeysFileCreated": "¡Nuevo archivo de llaves creado!",
        "loginMessage": "entrando...",
        "loginSuccess": "¡se ha conectado y el chat ha comenzado!",
        "invalidToken": "Token no válido"
    }
    lang = {"en": english,
            "es": spanish}
    writeJSON(path, lang)
    return lang


def createTelegramToken(token=None, testToken=True):
    global LANGUAGES, credentialsPath

    if testToken:
        token = testTelegramToken(token=token)

    data = {"telegramToken": token}
    writeJSON(credentialsPath, data)
    print(LANGUAGES["newKeysFileCreated"])
    return data


def testTelegramToken(token=None):
    # Tests the telegram token
    global LANGUAGES

    initialToken = token

    if token is None:
        print("\n" + LANGUAGES["pasteTelegramToken"])
        token = str(input("Token: "))
    tokenValid = False
    while not tokenValid:
        try:
            # Tests if the token is valid
            updater = Updater(token=token, use_context=True)
            updater.start_polling()
            updater.stop()
            tokenValid = True

            if initialToken != token:
                # If the test has changed the token, save the new token
                createTelegramToken(token=token, testToken=False)
        except (telegram.error.InvalidToken, telegram.error.Unauthorized):
            print(LANGUAGES["invalidToken"])
            token = str(input("Token: "))

    return token


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
def login(token):
    global LANGUAGES
    print(LANGUAGES["loginMessage"])
    updater = Updater(token=token, use_context=True)
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
    print(LANGUAGES["loginSuccess"])


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
    # Defaults
    usersDir = "Users"
    credentialsPath = usersDir + "/credentials.json"
    languagesPath = usersDir + "/lang.json"
    currentLanguage = "es"
    LANGUAGES = setup()
    TOKEN = getTelegramToken()

    login(TOKEN)
