from telethon import TelegramClient
from telethon import TelegramClient, events, utils
import os
from telethon.sessions import StringSession
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import threading

name = "Name"
api_id = os.environ.get("API_ID")
api_hash = os.environ.get("API_HASH")
str_sess = os.environ.get("SESSION")
TOKEN = os.environ.get("TOKEN")
PORT = int(os.environ.get('PORT', 5000))

client = TelegramClient(StringSession(str_sess), api_id, api_hash)


async def main():
    # Now you can use all client methods listed below, like for example...
    #await client.send_message(-1001294411352, 'Hello this is Ankit, naam to suna hi hoga!')
    async for message in client.iter_messages("",1):
        try:
            print(message.id, message.text)
        except:
            pass

@client.on(events.NewMessage)
async def evt(event):
    print(event.raw_text)
    chatid = event.sender_id
    print(chatid)
    if "hi" == event.raw_text.lower() and chatid != 561489747:
        await event.reply('Hello!')
 
def start(bot,update):
    update.message.reply_text("Hi")
    update.message.reply_text('None')
        
    
def clnt():
    client.start()
    client.run_until_disconnected()

threading.Thread(target=clnt).start()
updater = Updater(TOKEN)
updater.start_webhook(listen="0.0.0.0",port=int(PORT),url_path=TOKEN)
dp = updater.dispatcher
dp.add_handler(CommandHandler('start',start))
updater.bot.setWebhook('https://metgaccountmsgr.herokuapp.com/' + TOKEN)
updater.idle()


       
##with client:
##    client.loop.run_until_complete(main())
    
