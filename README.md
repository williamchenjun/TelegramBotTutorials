# **🤖 Telegram Bot Tutorials**

## Python Modules

[![Generic badge](https://img.shields.io/badge/Python-3.10.6-blue.svg)](https://www.python.org)
[![Generic badge](https://img.shields.io/badge/PythonTelegramBot-20.0_a1-pink.svg)](https://docs.python-telegram-bot.org/en/v20.0a1/)

## **📜 Table of contents**

- [What is this about?](#what-is-this-about)
- [Getting started](#getting-started)
    - [Creating a bot](#creating-a-bot)
    - [(Optional) Testing environment](#optional-testing-environment)
    - [Setting up Heroku](#setting-up-heroku)
    - [The Holy Trinity](#the-holy-trinity)
    - [Python Telegram Bot Module](#python-telegram-bot-module)
- [Your first Telegram bot](#your-first-telegram-bot)
    - [Introduction](#introduction)
    - [Echo bot (with explanation)](#echo-bot-with-explanation)
    - [Edit the `requirements.txt` file](#edit-the-requirementstxt-file)
    - [Deploy your bot on Heroku](#deploy-your-bot-on-heroku)


## **What is this about?**

If you know some Python, and have thought about creating a Telegram bot, you're in the right place. It can be complicated to get started, especially if you're a self-didact or still a beginner. Hopefully you can find my tutorials useful. I will try to keep it as simple as I can and avoiding using jargon too often.

## **Getting started**

First of all, we need to know what a "bot" is and how it works.

> A bot is an **automated system** that one can create and manipulate as they like. This can go from very simple tasks, such as repeating words, solving equations or drawing graphs, to group and database management, managing businesses and selling products.

The way Telegram bots work is through an API. The term "API" stands for "Application Programming Interface". If the acronym is not explicit enough for you, it basically means that we are given an programmable interface to manipulate whatever the application is about. In our case, it gives you the necessary "tools" to manipulate a Telegram bot however you want (with some limitations).

### **Creating a bot**

Now for the part that you've been waiting for... How can we create a bot?

Let's start with the basics. First of all, go on Telegram and search for [@BotFather](https://t.me/BotFather).

<img src="https://user-images.githubusercontent.com/79821802/190801198-3ad08283-8ac2-4cdb-8402-d0c8b1a69b0d.gif" width="300"/>

Now, type in the text box "**/newbot**". This will prompt BotFather to ask you to name your bot. You can pick any name you desire. Afterwards, it will ask you to pick a username for your bot, which **must** end with the word "bot". (For example: *ThisIsARandomBot, myOwnBot, BananaBot, helpbot, etc*.) Don't worry, you will be able to edit your bot's information later through BotFather (except for the username).

<img src="https://user-images.githubusercontent.com/79821802/190808308-fd20cd1c-517d-4b10-949f-3452a525aa7a.gif" width="500"/>

We have finished setting up your bot! Your bot is now officially part of Telegram. You will need to keep the long string that BotFather gives you. It's called a "token" or "API key". It's a unique string that enables you, and only you, to have access to your bot. Make sure to **keep it safe** and hidden.

### **(Optional) Testing environment**

Depending on your needs, you might find it useful to set up a testing environment to test out your bot. Go ahead and create a new group with you and your bot in it. If you want to log your bot's actions, you can also create a channel.

Ok, now that you have your bot and a "test group", we can talk about deploying your bot. Something that you might have been wondering is "*How can a bot stay online on its own?*" or "*Will I have to keep my computer on forever?*". So, the simplest way that I can explain it to you is that there are some websites that will let you host your bot on their servers for free or for a monthly subscription. It's actually hard to find free services nowadays. As of right now, I'm only aware of [Heroku](https://www.heroku.com). But sadly they're removing their free plan on the 28th November, 2022.

I might update this section with any free hosting websites, if I find any, after I publish this tutorial. For now, if you can afford it, Heroku is a good option. The "Free and Hobby" [plan](https://www.heroku.com/pricing) is about $7/month.

### **Setting up Heroku**

There is a comprehensive tutorial on how to set up an app and deploy it with git on Heroku, which you can find [here](https://devcenter.heroku.com/articles/git).

But the main points are:

- [Create a Heroku remote](https://devcenter.heroku.com/articles/git#for-a-new-app), which allows you to push your code to Heroku's server and have it associated with your Heroku app.
- Clone the git repository to edit the code. Just go to Heroku's website, log in, and select your app. Then, click on "deploy" and select "Heroku CLI" in the "deployment method" section. You will see a series of instructions. Just follow through and you will be able to easily push your code through your terminal/command prompt. (Notice: if `git push heroku master` does not work for you, use `git push heroku main`).
- Once you get used to it, the only commands you need to remember are:
    - `cd <directory of where your code is>`
    - `git add .`
    - `git commit -am "Whatever message..."`
    - `git push heroku main` &nbsp;**or**&nbsp; `git push heroku master`

Ok, the complicated part of this tutorial is over! Honestly, setting up everything takes longer than learning how to create a functioning bot.

### **The Holy Trinity**

We're getting closer and closer to coding. Just hang on for a little longer...

Open your terminal/command prompt and move to the directory where you have the folder with the same name as your Heroku app: 
```bash
williamchen@Williams-MacBook-Pro ~ % cd <Heroku App Name>
```
After that, create the following three files:

```bash
williamchen@Williams-MacBook-Pro <Heroku App Name> ~ % touch <Heroku App Name>.py requirements.txt Procfile
```

This will create `<Heroku App Name>.py`, `requirements.txt` &nbsp;and&nbsp; `Procfile` in your folder. The first file is where the main code will go. The second one will contain all the Python dependencies (modules) that you use in your main code. Procfile is a file that will be read by Heroku and will start your code.

**Optional**: You can also create a fourth file by running `git touch runtime.txt` to specify what version of Python you want to use.

Start by editing `Procfile` and writing:

```
worker: python <Heroku App Name>.py
```
(Of course, substitute `<Heroku App Name>` with the name of your app.)

Now save and close the file. We don't need to look at it anymore.

If you have create a `runtime.txt` file as well, specify your Python version in it: 

```
python-<version>
```

(Write the version of your Python instead of `<version>`, e.g. `python-3.10.7`)

Again, save and close it. We don't need to do anything else with these two files.

The `requirements.txt` will be edited last (unless you already know which Python modules you're going to use).

### **Python Telegram Bot Module**

The official documentation can be found **[here](https://docs.python-telegram-bot.org/en/v20.0a1/)** (or click on the badge at the very [top](#python-modules)).

> **Note**: I will assume that you have Python properly installed and have an idea on how to install Python modules.

If you don't have the `python-telegram-bot` module installed yet, install it by running the following in your terminal/command prompt: 

```bash
pip install python-telegram-bot
```

Once you have installed the module, we can open our main Python script `<Heroku App Name>.py` and start coding!

## **Your first Telegram bot**

### **Introduction**

Unless you have your own workflow already, I suggest you set your page as follows:

```python
#MODULES
from telegram.ext import ApplicationBuilder, ContextTypes
from telegram import Update

#ENVIRONMENT VARIABLES
API_KEY = "<Insert your API token here>"

#SECONDARY FUNCTIONS

#PRIMARY FUNCTIONS

if __name__ == '__main__':
    application = ApplicationBuilder().token(API_KEY).build()

    #EVENT HANDLERS
    
    application.run_polling(allowed_updates = Update.ALL_TYPES)
```

The modules section show be pretty self-explanatory. The environment variables section will contain global variables that can be accessed from anywhere. Later on I will show you how to keep your private information hidden. The primary and secondary functions sections are where you will write your functions. Finally, everything nested within the last `if` statement keeps your bot in a loop, so that it keeps working. We will also be adding event handlers in it. That is, triggers that will activate a certain function that you define (e.g. A text message, a URL, a command, etc...).

Another thing to note is that we are going to be using [asynchronous functions](https://www.aeracode.org/2018/02/19/python-async-simplified/). A very reductive and rough explanation is that a synchronous function usually just runs straight away when called. Whereas asynchronous functions depend on a main loop, and you can run multiple at the same time. However, they will never run entirely until the associated trigger (event handlers) fires off. The syntax is pretty simple:

```python
async def function(args):
    await #Do something
    ...

#Main loop will call "function" and pause when it hits the first "await", until an event triggers it to complete the routine.
```

Ok, now we can start creating our first bot!

### **Echo bot (with explanation)**

I know, I know... You have probably already encountered a lot of websites explaining how to write an echo bot. For those who are completely new, an echo bot is just a bot that replies with whatever you write. This is one of the simplest examples to explore what each component does.

We start by writing a function that catches the message you send in the chat and sends it back:

> **Note**: I will omit the modules, loop, and everything else, just to save up some space and make it easier to read. I will specify in which section I am writing the code.

```python
#PRIMARY FUNCTION
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = update.effective_message.text
    )
```
Ok this might look very confusing but we'll go through everything, no worries! So:

- As I mentioned earlier, `async` just lets Python know that we want it to be asynchronous.
- The arguments:
    - `Update` catches events that take place in the chat. For example, if a new message is sent in the chat, if a new user joins the group, etc...
    - `ContextTypes.DEFAULT_TYPE` is a bit hard to explain in simple terms, but just think of it as something you need to control things within your function. It is not crucial to really understand what it means.
- `await` is part of the `async/await` pair for the asynchronous function.
- `context.bot` refers to the bot in our `context`. Simply put, within our context there is one bot, which is our own. By writing `context.bot`, we can tell it to do various things.
- The `context.bot.send_message(...)` method tells the bot to send a message:
    - `chat_id`: Every chat has an ID associated to it on Telegram. For the bot to have context, it needs to know which chat you are referring to. It will use that to confirm that the bot is present and can interact with it.
        - `update.effective_chat` is a [`Chat` object](https://docs.python-telegram-bot.org/en/v20.0a1/telegram.chat.html). `effective_chat` points to the group the update is coming from. So by writing this, the `Chat` object returns all the information of the chat the update is coming from.
        - `update.effective_chat.id` returns the chat ID of the chat it is currently in. (If you're talking directly with the bot, it will return your user ID).
    - `text` is pretty straightforward. It's whatever you want the bot to send as a message.
        - `update.effective_message`, likewise, is a [`Message` object](https://docs.python-telegram-bot.org/en/v20.0a1/telegram.message.html). This points to the message you send in the chat. On update (i.e. new message), the bot has access to the `Message` object.
        - `update.effective_message.text` returns the text of the message you have just sent.

Phew! We are finally done analysing those few lines of code. Hopefully, now everything is clearer. 

So to make a long story short, this function requires you to provide an "event catcher" (`update`) and a context so that it knows where to operate. Whenever the function is called, it will wait for the specified event to be triggered, so that the function will receive information in the form of an update. Following that, it will send back the message you sent (`text`), in the chatroom you specified (`chat_id`).

Now we need to set up the event handler. An event handler is used to catch, well, events. That is, the "trigger". In this case, we want the trigger to be any text message we send in chat. The handler that deals with this kind of event is the [`MessageHandler`](https://docs.python-telegram-bot.org/en/v20.0a1/telegram.ext.messagehandler.html?highlight=messagehandler).

Ok, good. Now that we have pinned down what handler to use, we need to tell the bot what kind of messages to listen to. We can specify that using the `filters` component. 

First of all, import both `MessageHandler` and `filters` from `telegram.ext`:

```python
#MODULES
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from telegram import Update
```

Now we can go down to the `if` statement and write:

```python
if __name__ == '__main__':
    application = ApplicationBuilder().token(API_KEY).build()

    #EVENT HANDLERS
    echoFunc = MessageHandler(filters.TEXT, echo)
    application.add_handler(echoFunc)
    
    application.run_polling(allowed_updates = Update.ALL_TYPES)
```

- We defined a new variable called `echoFunc` which defines the `MessageHandler`. The `MessageHandler` takes a [filter](https://docs.python-telegram-bot.org/en/v20.0a1/telegram.ext.filters.html#module-telegram.ext.filters) (if you don't need any specific filter, you can write `filters.ALL` which will catch any type of message). In this case, we use `filters.TEXT` which will filter and catch all text messages. Then, we pass the function we want it to run whenever the event is triggered. In our case, `echo`.
- `application.add_handler(echoFunc)` is pretty straightforward. It adds the event handler `echoFunc` to the bot. 

Woo! We are done. This is all there is to create an echo bot. I hope you were able to understand all the different components. I might have skipped some syntax like `application.run_polling()` or `ApplicationBuilder().token(API_KEY).build()`. But that's because it's not vital to know what they do. They usually just stay fixed like that and there is no need to really know what they do. Let's just say that one defines your bot and the other one keeps your bot running. One is the "brain", the other one is the "heart".

### **Edit the `requirements.txt` file**

This file is read by Heroku to know which Python modules are used in your Python script. That's because everytime Heroku runs your code in its system, it doesn't have any modules. So if you don't specify anything, it doesn't know what `python-telegram-bot` is.

Now, open the `requirements.txt` in your favourite text editor and write:

```
python-telegram-bot==20.0a1
```
> **Note**: I am using version 20.0a1 of `python-telegram-bot`, but you should specify the version you are using. If you have no idea, create a new Python file and run
>
>```python
>import telegram
>print(telegram.__version__)
>```
>You should now see the version of the module. If you have an earlier version, you can install this pre-release version by running `pip install python-telegram-bot==20.0a1` in the terminal/command prompt.


### **Deploy your bot on Heroku**

As I [mentioned earlier](#setting-up-heroku), it is very easy to deploy your bot. Just open the terminal/command prompt and run one by one:
1. `cd <Heroku App Name>`
2. `git add .`
3. `git commit -am "Whatever you want..."`
4. `git push heroku main` &nbsp;or&nbsp; `git push heroku master`

Now you can mess around with the echo bot!

<img src="https://user-images.githubusercontent.com/79821802/190833286-38e5fcc1-84fe-4a1e-8530-e816e1cf24a1.gif" width="500"/>

To use it in your test group, make the bot an admin.

<img src="https://user-images.githubusercontent.com/79821802/190833950-885b5cbb-4b32-41f8-9312-2d178b92f7c5.gif" width="500"/>
