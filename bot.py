from telethon import TelegramClient
from telethon import TelegramClient, events, utils
import os
from telethon.sessions import StringSession
import threading
import requests
from bs4 import BeautifulSoup as bs4
import time
from pytube import YouTube
import cv2

name = "Name"
api_id = os.environ.get("API_ID")
api_hash = os.environ.get("API_HASH")
str_sess = os.environ.get("SESSION")
TOKEN = os.environ.get("TOKEN")
PORT = int(os.environ.get('PORT', 5000))
chat_data = eval(requests.get(os.environ.get("URL")).text)

client = TelegramClient(StringSession(str_sess), api_id, api_hash)
afk = False

####
chat_data.pop("")
chat_data.pop("i")
chat_data.pop("that day")
chat_data.pop("k")
chat_data["kaise ho"] = ["Theek hun"]
arr = [i.replace("?","").replace(".","").replace(",","").replace("!","").replace("/","") for i in chat_data.keys()]
not_known_reply = []

def sum_of_char(string):
    str_sum = 0
    print(string)
    for char in string:
        str_sum = str_sum + ord(char)
    return str_sum
  

def near_word(word):
    inp = word
    inp_sum = sum_of_char(inp)
    near_wrd = ""
    diff = abs(sum_of_char(arr[0]) - inp_sum)
    old_diff = 0

    if word in arr:
        return word

    
    for i in arr:
        if len(inp) == len(i) and inp[0] == i[0] or abs(len(inp) - len(i)) <= 5:
            avl_wrd_sum = sum_of_char(i)
            diff = abs(avl_wrd_sum - inp_sum)
            if diff == 0:
                near_wrd = i
                break

            if diff < old_diff:
                near_wrd = i
            
                old_diff = diff
        
    return near_wrd
  
def reply(string):
    if near_word(string) != "":
        return chat_data[near_word(string)]
    else:
        not_known_reply.append(string)
        if len(not_known_reply) >= 5:
            return random.choice(not_known_reply)
        else:
            return "hmm"
####


annimate = """.   # # # # #               
  # #       # #             
# #           # #           
#     @   @     #           
#       ∆       #           
#   #       #   #           
#     # # #     #           
  #           #             
    #       #               
      # # #                 
       # #                   
      # # #        |/        
      # # #        #         
    # # # # # # #           
  #   # # #                 
  #   # # #                 
  #   # # #                 
 /|   # # #
-
.   # # # # #               
  # #       # #             
# #           # #           
#     @   @     #           
#       ∆       #           
#   #       #   #           
#     # # #     #           
  #           #             
    #       #               
      # # #                 
       # #                   
      # # #      \|         
      # # #       #         
    # # # # # # #           
  #   # # #                 
  #   # # #                 
  #   # # #                 
 /|   # # #""".split("-")


def execute(code):
    #code = code.replace("\n","\\n").replace("\t","\\t").replace("\r","\\r")
    file = open("agent.py","w",encoding="utf-8")
    file.write(code)
    file.close()
    os.system("python executor.py > output.txt")
    data = open("output.txt",encoding="utf-8").read()
    if data != "":
        return data if len(data) <= 4090 else "Output too big, returning first 4000 characters\n"+data[:4000]
    else:
        return "No output statement provided"
      

def searchonyt(topic):
    """Will play video on following topic, takes about 10 to 15 seconds to load"""
    url = 'https://www.youtube.com/results?q=' + topic
    count = 0
    cont = requests.get(url)
    data = cont.content
    data = str(data)
    lst = data.split('"')
    for i in lst:
        count+=1
        if i == 'WEB_PAGE_TYPE_WATCH':
            break
    if lst[count-5] == "/results":
        return "No video found."
    
    #print("Videos found, opening most recent video")
    return "https://www.youtube.com"+lst[count-5]
  
def img(query):
    data = requests.get("https://www.google.com/search?q=%s&safe=active&rlz=1CAHXUG_enIN901&sxsrf=ALeKk03I4dV2_WxJ0ZhQTtvkIpAkh0s_jg:1615369289431&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjnr7XFt6XvAhVrFLcAHX-vC8sQ_AUoAXoECAEQAw&biw=1320&bih=600"%query).text
    imgs = data.split('src="')
    data = requests.get(imgs[2].split(";")[0]).content
    file = open("img.png","wb")
    file.write(data)
    file.close()
    return imgs[2].split(";")[0]
  
  
def fix(org_text):
    data = requests.get("http://services.gingersoftware.com/Ginger/correct/json/GingerTheText?lang=US&clientVersion=2.0&apiKey=6ae0c3a0-afdc-4532-a810-82ded0054236&text="+org_text).json()
    suggested_text = org_text
    lst = data["LightGingerTheTextResult"]
    fixed_gap = 0
    if lst:
        for data in lst:
            try:
                From = data["From"]+fixed_gap
                To = data["To"]+1+fixed_gap
                suggested_word = (data["Suggestions"][0]["Text"])
                suggested_text = suggested_text[:From]+suggested_word+suggested_text[To:]
                #print(suggested_text)
                fixed_gap = len(suggested_text)-len(org_text)

            except Exception as e:
                print(e)
        return suggested_text

    else:
        print("No error found")
        return None
    
    
def scan(img):
    data = cv2.imread(img)
    grey = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(grey, (3, 3), 2)
    threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    threshold = cv2.fastNlMeansDenoising(threshold,20,40,10)# 11, 31, 9)
    cv2.imwrite(img,threshold)
  

@client.on(events.NewMessage)
async def evt(event):
    global afk
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
            await event.edit("`"+annimate[i%2]+"`")
            time.sleep(0.6)
            
    if ".execute" in event.raw_text.lower():
        code = event.raw_text.replace(".execute ","")
        if "import" in code and chatid != 561489747:
            await event.reply("`Error: Import statement allowed for main user only`")
        else:
            #await event.reply(execute(code))
            await event.reply("`"+execute(code)+"`")
    
    if ".yt" in event.raw_text.lower():
        topic = event.raw_text.replace(".yt ","")
        await event.reply(searchonyt(topic))
    
    if ".img" in event.raw_text.lower():
        topic = event.raw_text.replace(".img ","")
        url = img(topic)
        await event.reply("[Image_source](%s)"%url,file="img.png")#event.reply("Found this video: "+searchonyt(topic))
    
    if ".fix" in event.raw_text.lower():
        if event.is_reply:
            message_crt_obj = await event.get_reply_message()
            message = message_crt_obj.raw_text
            fixed = fix(message)
            if fixed:
                await event.reply("`Found some grammatical mistakes`\n\n**Original text:** `%s`\n\n**Fixed text:** `%s`"%(message,fixed))
            else:
                await event.reply("`No grammatical mistakes detected`")
        else:
            await event.reply("Command must be replied to the message that has Grammatical mistake")
    
    if event.is_private or ".ankit" in event.raw_text.lower():
        if afk and chatid != 561489747:
            #try:
            rep = chat_data[event.raw_text.lower()]
            print(rep)
            await event.reply(reply(rep))
            #except Exception as e:
            #    await event.reply(str(e))
#         else:
#             await event.reply(reply("I am not much active on Telegram these days, consider messaging me on WhatsApp.\n`This is an automated reply, you will get same reply everytime.`"))

    if ".afk" in event.raw_text.lower():
        code = event.raw_text.replace(".afk ","")
        if chatid == 561489747:
            afk = True
            await event.reply("`Ankit is now AFK`")
            
    if ".!afk" in event.raw_text.lower():
        code = event.raw_text.replace(".!afk ","")
        if chatid == 561489747:
            afk = False
            await event.reply("`Ankit is no longer AFK`")
            
    if ".download" in event.raw_text:
        outmess = await event.reply("`Fetching data...`")
        if event.is_reply:
            message_crt_obj = await event.get_reply_message()
            message = message_crt_obj.raw_text
            try:
                path = YouTube(message).streams.first().download(r'yt')
                await outmess.edit("`Sending video...`")
                await event.reply(file = path)
                await outmess.edit("`Check this video`")
                os.remove(path)
            except Exception as e:
                await outmess.edit(f"`Error fetching video...{e}`")
            
        else:
            message = event.raw_text.replace(".download ","")
            vid = searchonyt(topic)
            try:
                path = YouTube(vid).streams.first().download(r'yt')
                await outmess.edit("`Sending video...`")
                await event.reply(file = path)
                await outmess.edit("`Check this video`")
                os.remove(path)
            except:
                await event.edit("`Error fetching video...`")

    if ".scan" in event.raw_text:
        if event.is_reply:
            message_crt_obj = await event.get_reply_message()
            result = await message_crt_obj.download_media()
            scan(result)
            await event.reply(file = result)
    
client.start()
client.run_until_disconnected()


