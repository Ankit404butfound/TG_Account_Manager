from telethon import TelegramClient
from telethon import TelegramClient, events, utils
import os
from telethon.sessions import StringSession
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import threading
import requests
from bs4 import BeautifulSoup as bs4
import time

name = "Name"
api_id = os.environ.get("API_ID")
api_hash = os.environ.get("API_HASH")
str_sess = os.environ.get("SESSION")
TOKEN = os.environ.get("TOKEN")
PORT = int(os.environ.get('PORT', 5000))

client = TelegramClient(StringSession(str_sess), api_id, api_hash)


annimate = """.   # # # # #               
  # #       # #             
# #           # #           
#     @   @     #           
#        ∆         #           
#   #       #    #           
#     # # #    #           
  #            #             
    #       #               
      # # #                 
         #                   
      # # #       |/        
      # # #       #         
    # # # # # # #           
  #   # # #                 
  #   # # #                 
  #   # # #                 
/|    # # #
-
.   # # # # #               
  # #       # #             
# #           # #           
#     @   @     #           
#        ∆         #           
#   #       #    #           
#     # # #    #           
  #            #             
    #       #               
      # # #                 
         #                   
      # # #      \|         
      # # #       #         
    # # # # # # #           
  #   # # #                 
  #   # # #                 
  #   # # #                 
/|    # # #""".split("-")


def execute(code):
    #code = code.replace("\n","\\n").replace("\t","\\t").replace("\r","\\r")
    file = open("executor.py","w",encoding="utf-8")
    file.write(code)
    file.close()
    os.system("python executor.py > output.txt")
    data = open("output.txt",encoding="utf-8").read()
    return data


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
    if "hi ankit" == event.raw_text.lower() and chatid != 561489747:
        await event.reply('Hello!')
    
    #update.message.reply_text(fact)
    if event.raw_text.lower() == "/rajma_eak_fact_batao":
        try:
            data = requests.get("https://www.generatormix.com/random-facts-generator").content
            soup = bs4(data)
            fact = soup.find("blockquote",attrs = {'class':"text-left"})
     # print((fact.text))
            await event.reply(fact.text)
        except Exception as e:
            await event.reply('Some error occurred')
    if event.raw_text.lower() == ".hi" and chatid == 561489747:
        for i in range(10):
            await event.edit(annimate[i%2])
            time.sleep(0.6)
            
    if ".execute" in event.raw_text.lower():
        code = event.raw_text.replace(".execute ","")
        await event.reply("`"+execute(code)+"`")
 
def start(bot,update):
    update.message.reply_text("Hi")
    update.message.reply_text('None')
        
    
client.start()
client.run_until_disconnected()


