from telethon import TelegramClient
from telethon import TelegramClient, events, utils
import os
from telethon.sessions import StringSession

name = "Name"
api_id = os.environ.get("API_ID")
api_hash = os.environ.get("API_HASH")
str_sess = os.environ.get("SESSION")

client = TelegramClient(StringSession(str_sess), api_id, api_hash)

TelegramClient(StringSession()

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

client.start()
client.run_until_disconnected()


       
##with client:
##    client.loop.run_until_complete(main())
    
