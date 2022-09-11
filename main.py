import telegram
from yodas import Yoda
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler


def testTelegramToken(token=None):
    if not token:
        token = input("Paste the telegram token: ")
        print("")
    try:
        updater = Updater(token=token)
        updater.start_polling()
        updater.stop()
    except (telegram.error.InvalidToken, telegram.error.Unauthorized) as e:
        print("Invalid token: {}".format(e))
        return testTelegramToken()
    return token


def getCredentials(yodas):
    if yodas.contents() == {}:
        yodas.write({
            "telegramToken": testTelegramToken()
        })


def main():
    updater = Updater(token=credentials.contents()["telegramToken"], use_context=True)
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
    print("Bot started")


# Telegram stuff
def sendMessage(context, userID, text):
    try:
        context.bot.send_message(chat_id=userID,
                                 text=text,
                                 parse_mode=telegram.ParseMode.MARKDOWN_V2)
    except telegram.error.BadRequest:
        context.bot.send_message(chat_id=userID,
                                 text=text,
                                 parse_mode=telegram.ParseMode.HTML)


def start(update, context):
    userID = update.effective_chat.id
    sendMessage(context, userID, "hello")


# This is the general message handler
def messageHandler(update, context):
    userID = str(update.effective_chat.id)  # update.effective_chat.id is the chat id
    textMessage = update.message.text  # update.message.text is the message that user sent

    # Returns the same message to the user
    sendMessage(context, userID, textMessage)


if __name__ == '__main__':
    credentials = Yoda("credentials.json")
    getCredentials(credentials)
    main()
