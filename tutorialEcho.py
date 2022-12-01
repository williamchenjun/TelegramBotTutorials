#MODULES
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler
from telegram import Update
import json
import os

os.chdir('desktop/personal/python/random/botTutorial')

#ENVIRONMENT VARIABLES
API_KEY = "5686335452:AAFVPfdwBuMfWnWjPCOKw2T-0-u-LB8g1Lg"
adminRead = json.load(open("adminList.json", "r"))
admins = list(adminRead.values())
user_data = {}

#SECONDARY FUNCTIONS
def reorder(_dict: dict) -> dict:
    newDict = {}
    count = 1
    for key, val in _dict.items():
        newDict[str(count)] = val
        count += 1
    return newDict

async def greet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    greetingMsg = f"Hello {update.effective_message.from_user.first_name}! Thank you for using this bot. To begin chatting with an admin, send a message to the bot."

    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = greetingMsg
    )

async def makeAdmin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender_id = update.effective_message.from_user.id

    if sender_id not in admins:
        return

    user_ids = context.args

    for user_id in user_ids:
        try:
            key = str(len(admins) + 1)
            global adminRead
            adminRead[key] = int(user_id)
            admins.append(int(user_id))
            await context.bot.send_message(
                chat_id = update.effective_chat.id,
                text = f"The new list of admins is:\n<code>{admins}</code>",
                parse_mode = ParseMode.HTML
            )
        except:
            await context.bot.send_message(
                chat_id = update.effective_chat.id,
                text = "An error occurred! Please make sure that you adhere to the following format: <code>/admin user_id_1 user_id_2 user_id_3 ...</code>",
                parse_mode = ParseMode.HTML
            )
    json.dump(adminRead, open("adminList.json","w"))

async def removeAdmin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender_id = update.effective_message.from_user.id

    if sender_id not in admins:
        return

    user_ids = context.args

    for user_id in user_ids:
        if int(user_id) in admins:
            global adminRead
            adminRead = {key:val for key, val in adminRead.items() if val != int(user_id)}
            adminRead = reorder(adminRead)
            admins.remove(int(user_id))
            await context.bot.send_message(
                chat_id = update.effective_chat.id,
                text = f"Admin(s) successfully removed. The new list of admins is:\n<code>{admins}</code>",
                parse_mode = ParseMode.HTML
            )
    json.dump(adminRead, open('adminList.json', 'w'))

#PRIMARY FUNCTIONS
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.effective_message.text
    from_chat = update.effective_chat.id
    user_data["message_id"] = update.effective_message.id
    user_data["from_chat"] = from_chat

    for admin in admins:
        if from_chat not in admins:
            if text.startswith("/"):
                await context.bot.send_message(
                    chat_id = update.effective_chat.id,
                    text = "Commands are for admins only."
                )
                return
            else:
                await context.bot.forward_message(
                    chat_id = admin,
                    from_chat_id = from_chat,
                    message_id = update.effective_message.id,
                    protect_content = True
                )

async def replyToMsg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_chat = update.effective_chat.id
    text = update.effective_message.text
    from_chat = user_data["from_chat"]
    msg_id = user_data["message_id"]

    if text.startswith("/"):
        return

    if current_chat in admins:
        await context.bot.send_message(
            chat_id = from_chat,
            text = update.effective_message.text
        )
    else:
        from_chat = update.effective_chat.id
        msg_id = update.effective_message.id
        user_data["from_chat"] = from_chat
        user_data["message_id"] = msg_id

        for admin in admins:
            await context.bot.forward_message(
                chat_id = admin,
                from_chat_id = from_chat,
                message_id = msg_id,
                protect_content = True
            )
    

if __name__ == '__main__':
    application = ApplicationBuilder().token(API_KEY).build()

    #EVENT HANDLERS
    echoFunc = MessageHandler(filters.TEXT, echo)
    replyFunc = MessageHandler(filters.REPLY, replyToMsg)
    greetingFunc = CommandHandler(['start', 'help'], greet)
    adminFunc = CommandHandler('admin', makeAdmin)
    unadminFunc = CommandHandler('unadmin', removeAdmin)

    application.add_handler(greetingFunc)
    application.add_handler(adminFunc)
    application.add_handler(unadminFunc)
    application.add_handler(replyFunc)
    application.add_handler(echoFunc)
    
    application.run_polling(allowed_updates = Update.ALL_TYPES)