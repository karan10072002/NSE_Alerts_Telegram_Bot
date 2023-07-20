from nsetools import Nse
import pyautogui
import time
from datetime import datetime

nse=Nse()

print("The server is running. Bot Active")

# print(nse.get_index_list())
# print(nse.get_index_quote('NIFTY NEXT 50'))
# print(nse.get_stock_codes())
# print(nse.get_quote('TVSMOTOR'))


import telebot
import os

API_KEY="5550503373:AAFXYVG8cKPNNJiIy_Y3Pr4_j4Fa7rMtkOs"
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=["Hi", "hi"])
def greet(message):
    bot.reply_to(message, "hey how it's going? [bot author Karan_Cosmos]")

@bot.message_handler(commands=["Help", "help"])
def greet(message):
    commands="Commands:\n 1. price [STOCK SYMBOL / INDEX SYMBOL]: Gives current price.\n 2. ping [STOCK SYMBOL / INDEX SYMBOL] @ [TARGET PRICE]: Notifies when the stock touches specified price."
    bot.send_message(message.chat.id, commands)
    bot.send_message(message.chat.id, "/Stock_symbol : to get all stock symbols\n/Index_symbol : to get all index symbols")

@bot.message_handler(commands=["Stock_symbol", "stock_symbol"])
def greet(message):
    doc = open(r"all stock symbols.txt", 'rb')
    bot.send_document(message.chat.id, doc)

@bot.message_handler(commands=["Index_symbol", "index_symbol"])
def greet(message):
    all_index=['NIFTY 50', 'NIFTY NEXT 50', 'NIFTY100 LIQ 15', 'NIFTY BANK', 'INDIA VIX', 'NIFTY 100', 'NIFTY 500', 'NIFTY MIDCAP 100', 'NIFTY MIDCAP 50', 'NIFTY INFRA', 'NIFTY REALTY', 'NIFTY ENERGY', 'NIFTY FMCG', 'NIFTY MNC', 'NIFTY PHARMA', 'NIFTY PSE', 'NIFTY PSU BANK', 'NIFTY SERV SECTOR', 'NIFTY IT', 'NIFTY SMLCAP 100', 'NIFTY 200', 'NIFTY AUTO', 'NIFTY MEDIA', 'NIFTY METAL', 'NIFTY DIV OPPS 50', 'NIFTY COMMODITIES', 'NIFTY CONSUMPTION', 'NIFTY CPSE', 'NIFTY FIN SERVICE',
                'NIFTY SMLCAP 50']
    reply_index=""
    for i in range(len(all_index)):
        reply_index+=f"{i+1}. {all_index[i]}\n"
    bot.send_message(message.chat.id, reply_index)

# #the continous ping
# @bot.message_handler(commands=["continous_ping"])
# def cp(message):
#     while True:
#         bot.send_message(message.chat.id, "current price is X ")

#the continous ping
@bot.message_handler(commands=["time_ping"])
def cp(message):
    bot.send_message(message.chat.id, "time ping acknowledged")
    while True:
        if str(datetime.now())[11:16] == "01:17":
            bot.send_message(message.chat.id, f"the current time is {str(datetime.now())[11:16]}")
            break

def stock_request(message):
    request=message.text.split()
    if len(request)<2 or request[0].lower() != "price":
        return False
    else:
        return True

@bot.message_handler(func=stock_request)
def send_price(message):
    request=message.text.split()[1]
    all_index=['NIFTY 50', 'NIFTY NEXT 50', 'NIFTY100 LIQ 15', 'NIFTY BANK', 'INDIA VIX', 'NIFTY 100', 'NIFTY 500', 'NIFTY MIDCAP 100', 'NIFTY MIDCAP 50', 'NIFTY INFRA', 'NIFTY REALTY', 'NIFTY ENERGY', 'NIFTY FMCG', 'NIFTY MNC', 'NIFTY PHARMA', 'NIFTY PSE', 'NIFTY PSU BANK', 'NIFTY SERV SECTOR', 'NIFTY IT', 'NIFTY SMLCAP 100', 'NIFTY 200', 'NIFTY AUTO', 'NIFTY MEDIA', 'NIFTY METAL', 'NIFTY DIV OPPS 50', 'NIFTY COMMODITIES', 'NIFTY CONSUMPTION', 'NIFTY CPSE', 'NIFTY FIN SERVICE',
                'NIFTY SMLCAP 50']
    for i in all_index:
        if i in message.text or i.lower() in message.text:
            bot.send_message(message.chat.id, f"{i} @ Rs. {nse.get_index_quote(i)['lastPrice']}")
            break
    else:
        try:
            nse_response=nse.get_quote(request)
            bot_response=f"{nse_response['companyName']} @ Rs.{nse_response['lastPrice']}"
            bot.send_message(message.chat.id, bot_response)
        except:
            bot.send_message(message.chat.id, "No Data found !")    

def ping_request(message):
    request=message.text.split()
    if len(request)<4 or request[0].lower() != "ping":
        return False
    else:
        return True 

@bot.message_handler(func=ping_request)
def send_ping(message):
    request=message.text.split()

    all_index=['NIFTY 50', 'NIFTY NEXT 50', 'NIFTY100 LIQ 15', 'NIFTY BANK', 'INDIA VIX', 'NIFTY 100', 'NIFTY 500', 'NIFTY MIDCAP 100', 'NIFTY MIDCAP 50', 'NIFTY INFRA', 'NIFTY REALTY', 'NIFTY ENERGY', 'NIFTY FMCG', 'NIFTY MNC', 'NIFTY PHARMA', 'NIFTY PSE', 'NIFTY PSU BANK', 'NIFTY SERV SECTOR', 'NIFTY IT', 'NIFTY SMLCAP 100', 'NIFTY 200', 'NIFTY AUTO', 'NIFTY MEDIA', 'NIFTY METAL', 'NIFTY DIV OPPS 50', 'NIFTY COMMODITIES', 'NIFTY CONSUMPTION', 'NIFTY CPSE', 'NIFTY FIN SERVICE',
                'NIFTY SMLCAP 50']
    for i in all_index or i.lower() in message.text:
        if i in message.text:
            bot.reply_to(message, f"Ping request acknowledged: \nYou will be notified when {i} touches Rs. {request[-1]}")

            if nse.get_index_quote(i)['lastPrice'] < eval(request[-1]):
                alert="up"
            else:
                alert="down"

            while True:
                condition=nse.get_index_quote(i)['lastPrice']
                if alert=="up":
                    if condition>=eval(request[-1]):

                        # print(condition, type(condition))
                        # print(eval(request[-1]), type(eval(request[-1])))
                        
                        bot.send_message(message.chat.id, f"Alert !\n Ping condition satisfied: \n {i} @ Rs.{condition}")
                if alert=="down":
                    if condition<=eval(request[-1]):
                        bot.send_message(message.chat.id, f"Alert !\n Ping condition satisfied: \n {i} @ Rs.{condition}")
                break
            break
    else:
        try:
            nse_response=nse.get_quote(request[1])
            bot_response=f"Ping request acknowledged: \nYou will be notified when {nse_response['companyName']} touches Rs. {request[-1]}"
            bot.send_message(message.chat.id, bot_response)

            if nse.get_quote(request[1])['lastPrice'] < eval(request[-1]):
                alert="up"
            else:
                alert="down"

            while True:
                condition=nse.get_quote(request[1])['lastPrice']
                if alert=="up":
                    if condition>=eval(request[-1]):
                        bot.send_message(message.chat.id, f"Alert !\n Ping condition satisfied: \n {nse_response['companyName']} @ Rs.{condition}")
                if alert=="down":
                    if condition<=eval(request[-1]):
                        bot.send_message(message.chat.id, f"Alert !\n Ping condition satisfied: \n {nse_response['companyName']} @ Rs.{condition}")
                break

        except:
            bot.send_message(message.chat.id, "Unsucessfull !")

def abusive(message):
    if message.text.lower() in ["fuck you", "fuck off", "mc","madarchod", "bsdk", "saale"]:
        return True
    else:
        return False
@bot.message_handler(func=abusive)
def abusive_return(message):
    bot.reply_to(message, "humm...\n getting nauty haan...")


# p_time=None
# def time_ping(message):
#     global p_time
#     if "tell time @ " in message.text:
#         p_time=message
#     if str(datetime.now())[11:16] == str(p_time.text.split()[-1]):
#         return True
#     else:
#         return False


# @bot.message_handler(func=time_ping)
# def send_time_ping(message):
#     global p_time
#     print("Ya !")
#     # if str(datetime.now())[11:16] == str(p_time.text.split()[-1]):
#     bot.send_message(p_time.chat.id, f"the current time is {str(datetime.now())[11:16]}")

bot.polling()




