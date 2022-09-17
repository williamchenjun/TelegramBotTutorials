# **Message Forwarding Bot**

### **Modules**

[![Generic badge](https://img.shields.io/badge/Python-3.10.6-blue.svg)](https://www.python.org)
[![Generic badge](https://img.shields.io/badge/PythonTelegramBot-20.0_a4-pink.svg)](https://docs.python-telegram-bot.org/en/v20.0a4/)

## **Table of contents**

- [Task](#task)
- [Objectives](#objectives)
    - [What does our bot need to be able to do?](#what-does-our-bot-need-to-be-able-to-do)
- [Functions](#functions)
    - [Echoing](#echoing)
    - [Replying to the user](#replying-to-the-user)
    - [Setting up admins and permissions](#setting-up-admins-and-permissions)
        - [Fixed list of admins](#fixed-list-of-admins)
        - [Dynamic list of admins](#dynamic-list-of-admins)

## **Task** 

We want to develop a Telegram bot, using the `python-telegram-bot` module, that allows users to anonymously send a message to a specific person or group of people. Furthermore, by replying to the forwarded message, we should be able to send a message back to them.

If you're too impatient to go through the full tutorial and want the entire functional code:
<details>
  <summary><b>Full code</b></summary>
  
  ```python
  #MODULES
    from telegram.constants import ParseMode
    from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler
    from telegram import Update
    import json
    import os

    os.chdir('desktop/personal/python/random/bot tutorial')

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
  ```

</details>

---

## **Objectives**
### **What does our bot need to be able to do?**
- It needs to be able to forward a user's message to the admins. So there needs to be some kind of link between **user ↔️ bot ↔️ admin(s)**.
- The admin(s) should be able to **make another user an admin** or to remove the role.
- To avoid chaos, admins should only be able to **reply to a forwaded message by replying directly to it**. That is, any message that is not a direct reply will not be sent.
- Commands should only be available to admins.

---

## **Functions**

### **Echoing**

Just like in our introduction, we want to be able to echo the message that a user sends. This time, however, it will be sent to us (admins) and not themselves. 

We start by copying the echo function from the [introduction](https://github.com/williamchenjun/TelegramBotTutorials):

```python
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = update.effective_message.text
    )
```

The first thing we want to try is to make it forward any message that it receives to us. We introduce the method `forward_message`. If it isn't explicit enough, this method instructs the bot to forward a message to somebody else. There are only 3 things this method requires: `chat_id` (receiver), &nbsp;`from_chat_id` (sender) and `message_id` (message). We already know `chat_id`, as it will be just our own user ID. This is because the chat ID associated with the chat that you have open with the bot is your own chat ID. 'Bot chats' don't have a unique chat ID.

Then, we change the code to:

```diff python
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
-   await context.bot.send_message(
+   await context.bot.forward_message(
-   chat_id = update.effective_chat.id,
+   chat_id = <Your user ID>,
-   text = update.effective_message.text,
+   from_chat_id = update.effective_chat.id,
+   message_id = update.effective_message.id
    )
```

<details>
<summary><b>Clearer text</b></summary>

```python
async def echo (update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.forward_message(
        chat_id = <Your user ID>,
        from_chat_id = update.effective_chat.id,
        message_id = update.effective_message.id
)
```
</details>

> **Note**: If you don't know your user ID, you can use [userinfobot](https://t.me/userinfobot).

If you now try to send a message to the bot from another account, it should forward the message to your chat with the bot.

An optional argument that you can include is `protect_content`. This will prevent you from being to forward a user's forwarded message to somebody else. It's an extra security measure for the user.

<details>
<summary><b>Including <code>protect_content</code></b></summary>

```python
async def echo (update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.forward_message(
        chat_id = <Your user ID>,
        from_chat_id = update.effective_chat.id,
        message_id = update.effective_message.id,
        protect_content = True
)
```
</details>

Ok, so we're done! We have easily created a bot that forwards any message send to it to the admin. Now we have to figure out how we should reply to the user.

---

### **Replying to the user**

To reply to the user, we need to first of all figure out 1 thing:  the `chat_id` of the user. Since there is no way of retrieving a user ID without an event trigger (update), we need to store the user ID from our `echo` function.

Firstly, we create a dictionary called `user_data` (or whatever name you pick). Inside of it, we will store all the necessary information.

> **Note**: `python-telegram-bot` functions already provide you with a dictionary that you can invoke with `context.user_data`. To insert new items in the dictionary, just write `context.user_data[<key>] = <value>`. I'm using an external dictionary just because I prefer to do so and it doesn't change much.

In our echo function, at the very top, we want to add

```python
user_data["from_chat"] = update.effective_chat.id
```

Then, we start writing our new reply function:

```python
async def replyToMsg(update: Update, context: ContextTypes.DEFAULT_TYPE):

    #RETRIEVE SAVED INFORMATION
    from_chat = user_data["user_data"]

    #SEND OUT THE MESSAGE
    await context.bot.send_message(
        chat_id = from_chat,
        text = update.effective_message.text
    )
```

You may be wondering, "*How can the bot tell that it's a reply and not just a normal message?*". Well, let me introduce you to a new filter! It's `filters.REPLY`. Just like the other ones, this filter will only catch replies. 

So at the bottom of the script we write:

```python
if __name__ == "__main__":
    application = ApplicationBuilder().token(API_KEY).build()

    #EVENT HANDLERS
    echoFunc = MessageHandler(filters.TEXT, echo)
    replyFunc = MessageHandler(filters.REPLY, replyToMsg)

    application.add_handler(echoFunc)
    application.add_handler(replyFunc)

    application.run_polling(allowed_updates = Update.ALL_TYPES)
```

The basic layout is the same. The only thing that we changed is what is inside of the `MessageHandler`. We can translate this to: "Catch any message sent to the group that is a reply and run `replyToMsg`".

Now try having a conversation through the bot! If you reply to a message sent by a user, the user should receive a response from the bot.

---

### **Setting up admins and permissions**

Here things get a bit tricky. It is very convenient if you have a fixed list of admins and never want to change it. But if you have a list that can be changed and updated, then you need to save the data externally. Because if you save the data in your code, once you restart it, the list will go back to default (without the admins you added through the bot). I will show you both versions.

---

#### **Fixed list of admins**

For a fixed list of admins, this is very easy. Let us define a list:

```python
admins = [<first user ID>, <second user ID>, ...]
```
What we require is that, if you're an admin, your messages should not be echoed back. That is, your messages should not be forwarded back to you because that would just be messy. Moreover, we want that non-admins should not be able to use commands.

To prevent your own messages to be echoed back, you should just add:

```python
async def echo (update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender_id = update.effective_message.from_user.id

    if sender_id in admin:
        return

    await context.bot.forward_message(
        chat_id = <Your user ID>,
        from_chat_id = update.effective_chat.id,
        message_id = update.effective_message.id,
        protect_content = True
    )
```

If you're not familiar with programming, once you `return` in a function, everything that follows will be nil. That is, the function will just stop and return nothing. However, if the `if` statement is not satisfied, then it will proceed with no issues. Of course, you can also use nested notation.

<details>
<summary><b>Nested version</b></summary>

```python
async def echo (update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender_id = update.effective_message.from_user.id

    if sender_id not in admin:
        await context.bot.forward_message(
            chat_id = <Your user ID>,
            from_chat_id = update.effective_chat.id,
            message_id = update.effective_message.id,
            protect_content = True
        )
```
</details>

Furthermore! We have already seen `update.effective_message`, which is a `Message` object. The message object has a `from_user` component that is a `User` object, and it refers to the sender. So with `update.effective_message.from_user` we can retrieve information about the sender, such as the ID.

Now if you run the code, and you send a message to the bot from your admin account, the bot will not forward the message to you.

Good! Now we move on to the...

---

#### **Dynamic list of admins**

Let's say that you don't have a fixed amount of admins, and maybe one day you want to remove the role of admin of a user. How do we keep the list of admins updated and accessible?

There are various solutions. The easiest version is to keep a text file and keep a list of admins on it. The easy alternative is to keep a JSON file, so that it's easy to manipulate and read. Otherwise, you would have to rely on databases or other cloud services. Unless you have a very large number of admins, or your bot is meant for very big audiences, I would suggest using a JSON file.

Ok, so what is a JSON file? JSON stands for JavaScript Object Notation, and it is literally that. In JavaScript an object is defined like a dictionary in Python. So a JSON file is a JavaScript object.

**For example**: `{"admin_1": 123456, "admin_2": 098765}` is a JavaScript object.

Firstly, create a file named `adminList.json` (or whatever you prefer) in your app folder:

```bash
williamchen@Williams-MacBook-Pro <Path to folder> ~ % touch adminList.json
```

Now in your Python script, import the `json` module:

```python
#MODULES
import json
...
```
The main things you need to remember are:

- `json.load()` loads your JSON file as a Python dictionary.
- `json.dump()` creates a (new) JSON file.
- `open(<filename>, <mode>)` opens your file and read, write or append  text to it.

Therefore, we now need to open `adminList.json` from our Python script:

```python
#ENVIRONMENT VARIABLES
adminList = json.load(open("adminList.json", "r"))
...
```
The `"r"` stands for "read" and it basically instructs your machine to open your file in readonly mode. So you can access what is written inside of it, but you cannot write in it.

In `adminList.json` you should add all of your admins in the following manner:

```
{
    "1": <userid>,
    "2": <userid>,
    "3": <userid>,
    ...
}
```
What the variable `adminList` will print out in Python is the following dictionary:

```python
{"1": <userid>, "2": <userid>, "3": <userid>, ...}
```

That's good! The confusing part is over. We can now start writing the functions that will allow us to add and remove admins from the file: `makeAdmin` and `removeAdmin`.

`makeAdmin` should:
- Check whether the command was send by an admin. We don't want a random user to be able to make themselves or others an admin.
- Be able to add one or more user IDs to the JSON file.

```python
import json
...

adminList = json.load(open('adminList.json', 'w'))
adminUserIds = list(adminList.values())

...

async def makeAdmin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender_id = update.effective_message.from_user.id

    #HALT IF NOT AN ADMIN
    if sender_id not in adminUserIds:
        return

    #GET USER IDS PROVIDED
    userIds = context.args

    #TRY ADDING USER IDS TO FILE
    for userId in userIds:
        try:
            key = str(len(adminUserIds) + 1)
            global adminList
            adminList[key] = int(userId)
            adminUserIds.append(int(userId))
            await context.bot.send_message(
                chat_id = update.effective_chat.id,
                text = f"The new list of admins is:\n<code>{adminUserIds}</code>",
                parse_mode = ParseMode.HTML
            )
        except:
            await context.bot.send_message(
                chat_id = update.effective_chat.id,
                text = f"An error occured!",
                parse_mode = ParseMode.HTML
            )
    json.dump(adminList, open("adminList.json","w"))
```

> **Note**: Whenever you encounter the three dots "`...`" in the code, it means that I've omitted something to keep it short.

This is a lot of code! Let's go through it together. So up to the `if` statement we know everything. The only thing to notice is that I created a new list called `adminUserIds` and it holds all the key values of the dictionary `adminList`. What `list(adminList.values())` returns is `[<userid>, <userid>, ...]`. We want this so that other functions have access to the admin list without having to access the JSON file. 

The `for` loop goes over all the user IDs that were provided from the admin. When you send "`/<command> <text> <text> <text> ...`" to a bot on Telegram, you can retrieve the `<text>`s in `context.args` as list (i.e. `[<text>, <text>, ...]`).

You don't really need to know what `try/except` are but they are used to try something and to catch errors. Basically the machine will try everything nested inside of `try` first, and then if there is an error everything inside of `except` will run.

Now let's analyse the following:

```python
key = str(len(adminUserIds) + 1)
global adminList
adminList[key] = int(userId)
adminUserIds.append(int(userId))
```
As you may have noticed, the dictionary keys are ordered numbers (i.e. 1,2,3,4,...). I used that so that it's easy to organise. The issue with using something more complicated than that is conflicts.

For example: Assume we have an object of 3 items
```
{"item1": <value1>, "item2": <value2>, "item3": <value3>}
```
If I added a new item, I would want the key to be named `item4` with value `<value4>`. So now the list would be:

```
{"item1": <value1>, "item2": <value2>, "item3": <value3>, "item4": <value4>}
```
So the easiest way to generalise the key name is `"item" + str(len(adminUserIds))`. But what happens when you remove an item in position 0, 1 or 3, and add a new one is that it replaces `item3`. We obviously don't want this to happen. I will explain later what we can do to prevent this. We first start by analysing the rest of the code.

The `global` term indicates that `adminList` will be changed globally, and not just within the function.

The last two lines basically add the userId to both `adminList` and `adminUserIds`.

We now discuss how to remove admins and how to avoid conflicts on key names. The `removeAdmin` function is the following:

```python
async def removeAdmin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender_id = update.effective_message.from_user.id

    if sender_id not in admins:
        return

    user_ids = context.args

    for user_id in user_ids:
        if int(user_id) in admins:
            global adminList
            adminList = {key:val for key, val in adminList.items() if val != int(user_id)}
            adminList = reorder(adminList)
            admins.remove(int(user_id))
            await context.bot.send_message(
                chat_id = update.effective_chat.id,
                text = f"Admin(s) successfully removed. The new list of admins is:\n<code>{admins}</code>",
                parse_mode = ParseMode.HTML
            )
    json.dump(adminList, open('adminList.json', 'w'))
```

Again, until the `global adminList` variable, everything is the same. Let's analyse the following lines:
```python
adminList = {key:val for key, val in adminList.items() if val != int(user_id)}
adminList = reorder(adminList)
adminUserIds.remove(int(user_id))
```
The first line basically translates to "From the dictionary `adminList`, loop over all keys and values, and leave every pair item that doesn't have a value equal to `user_id`". Thus, it's a way to remove the specified `user_id` from the list of admins. Now we encounter our main issue. Key names may overlap if we remove an item from the dictionary, so what can we do? We rewrite all key names so that there is no overlapping!

We define the following function:

```python
def reorder(_dict: dict) -> dict:
    newDict = {}
    count = 1
    for key, val in _dict.items():
        newDict[str(count)] = val
        count += 1
    return newDict
```

We are basically substituting every key with an ordered sequence of number. That is, something like this:

```
{"1": <userid>, "2": <userid>, "4": <userid>}
```
becomes this:
```
{"1": <userid>, "2": <userid>, "3": <userid>}
```
Et voilá! No more overlapping issues. Thus, 

```python
adminList = reorder(adminList)
adminUserIds.remove(int(user_id))
```
on the first line we are replacing the key names, as shown above, and the second line removes the user ID from the `adminUserIds` list.

At the very end of both `makeAdmin` and `removeAdmin` you may have noticed that we have `json.dump(adminList, open('adminList.json', 'w'))`. That basically instructs the machine to write the updated JavaScript object in the JSON file.

Now that these two functions have been defined, we can attach them to a specific command by using the `CommandHandler`:

```python
if __name__ == "__main__":
    application = ApplicationBuilder().token(API_KEY).build()

    #EVENT HANDLERS
    echoFunc = MessageHandler(filters.TEXT, echo)
    replyFunc = MessageHandler(filters.REPLY, replyToMsg)
    adminFunc = CommandHandler('admin', makeAdmin)
    unadminFunc = CommandHandler('unadmin', removeAdmin)

    application.add_handler(adminFunc)
    application.add_handler(unadminFunc)
    application.add_handler(echoFunc)
    application.add_handler(replyFunc)

    application.run_polling(allowed_updates = Update.ALL_TYPES)
```

If you run the code, and sending something like "`/admin <userid>`" to your bot, you will notice that in your `adminList.json` file there is a new entry. Likewise, sending "`/unadmin <userid>`" removes the specified user ID.

This is the gist of it. If you feel like it, you can add more conditions and make your bot even better. You can take a look at my [full code](#task) to see what I added.
