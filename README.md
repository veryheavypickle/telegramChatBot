# telegramChatBot
A general use chatbot for telegram

## Installation
1. `cd` into the directory you wish for this to be installed 
2. `$ git clone https://github.com/veryheavypickle/telegramChatBot.git`
3. `$ cd telegramChatBot`
4. `$ pip install -r requirements.txt`


## Running
1. Make sure you are in the telegramChatBot directory
2. `$ python main.py`
3. ???
4. Profit!

## Code
#### An example of adding another handler for the command "/test"
where testFunction has to be a python programmed function
```
handlers = [MessageHandler(Filters.text & (~Filters.command), messageHandler),
            CommandHandler('start', start),
            CommandHandler('test', testFunction)]
```

#### Example of testFunction
```
def testFunction(update, context):
    userID = str(update.effective_chat.id)
    sendMessage(context, userID, "Bot works well!")
```
