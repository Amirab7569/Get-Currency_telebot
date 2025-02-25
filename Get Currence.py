import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
import requests

removemarkup = ReplyKeyboardRemove()
    
TOKEN = '7292583591:AAF86Tn619kf5cpZWISfdnaOowX6OpHHbog'
bot = telebot.TeleBot(TOKEN)
# get cryptocurrency
def get_price(currence):
    url = f"https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={currence}-USDT"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        price = data['data']['price']
        return f'The price of in {currence} is - ${price}'
    else:
        return "Error Bot."
    
# listener
def listener(message):
    for m in message:
        # print(m)
        if m.content_type == 'text':
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)
            
bot.set_update_listener(listener)

#ansewer the start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    cid = message.chat.id
    bot.send_chat_action(cid , action='typing')
    # keyboardbutton
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton('ADA'))
    markup.add(KeyboardButton('BTC'))
    markup.add(KeyboardButton('ETH'))
    bot.send_message(cid, "Welcome 👊🏽🔥!\n choose the name of a crypto currency to get its price.",reply_markup=markup)
    
#answer the text content
@bot.message_handler(func=lambda message: True)
def send_crypto_price(message):
    currence = message.text.upper()
    price = get_price(currence)
    if isinstance(price , float):
        bot.send_message(message, f"The price of *{currence}* is - ${price}" , reply_markup=removemarkup)
        send_welcome()
    else:
        bot.reply_to(message, price)

#run robot
bot.infinity_polling()