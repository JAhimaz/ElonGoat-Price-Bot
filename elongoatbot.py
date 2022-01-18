import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv.main import load_dotenv
from datetime import timedelta
import telebot
from pythonpancakes import PancakeSwapAPI

load_dotenv()

API_KEY = os.getenv('TG_API_KEY')
TOKEN_ADD = os.getenv("TOKEN_ADD")
BNB_ADD = os.getenv("BNB_ADD")

tokenDetails = {
    'token_name': 'ElonGoat',
    'token_symbol': 'EGT',
    'decimals': 10,
    'website': 'https://www.elongoat.io',
    'contract': TOKEN_ADD,
    'launch_time': 1641349987,
    'total_supply': '10,000,000,000'
}

bot = telebot.TeleBot(API_KEY, parse_mode="HTML")
ps = PancakeSwapAPI()

def configureLogging():
    logFormatter = logging.Formatter("%(levelname)s - %(asctime)s --> %(message)s")

    fileHandler = RotatingFileHandler("/home/app/logs/output.log", mode="a+", maxBytes=10*1024*1024, backupCount=3)
    fileHandler.setFormatter(logFormatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(logFormatter)

    log = logging.getLogger()
    log.setLevel(logging.INFO)
    log.addHandler(streamHandler)
    log.addHandler(fileHandler)

def fetchPooCoinStats():
    tokenData = ps.tokens(TOKEN_ADD)
    bnbData = ps.tokens(BNB_ADD)
    
    marketCap = round(float(tokenData['data']['price']) * (10 ** tokenDetails['decimals']), 2)
    timeSinceLaunch = timedelta(seconds=tokenDetails['launch_time'])

    # print(f'{"${:,.2f}".format(marketCap)}')

    data = {
        'token_name': tokenDetails['token_name'],
        'token_symbol': tokenDetails['token_symbol'],
        'token_price': tokenData['data']['price'],
        'market_cap': marketCap,
        'bnb_price': bnbData['data']['price'],
        'decimals': tokenDetails['decimals'],
        'website': tokenDetails['website'],
        'contract': tokenDetails['contract'],
        'launch_time': tokenDetails['launch_time'],
        'total_supply': tokenDetails['total_supply']
    }

    return data

    # print(tokenData)
    # print(bnbData)

@bot.message_handler(commands=['price', 'mcap', 'marketcap', 'stats'])
def send_price(message):
    # Timeout check
    # Checks the last check, if it is below 5 seconds, then send the timeout message

    # If timeout is not viable, fetch new data from poocoin.
    data = fetchPooCoinStats()
    message_data = f'''
🚀<a href="https://bscscan.com/token/{data['contract']}">{data['token_symbol']}</a>🐐😎

|| Current Price ||
[ {"${:,.5f}".format(float(data['token_price']))} ]

💴 <b>Market Cap: </b>{"${:,.2f}".format(data['market_cap'])}

💰 <b>Circulating Supply: </b>{data['total_supply']}

🏦 <b>BNB / BUSD: </b>{"${:,.2f}".format(float(data['bnb_price']))}

🔄 <b>Buy / Sell: </b><a href="https://pancakeswap.finance/swap?outputCurrency={data['contract']}&inputCurrency=BNB">PancakeSwapV2</a> | <a href="https://poocoin.app/swap?outputCurrency={data['contract']}">PooCoin Swap</a>

🌐 <b>Website: </b><a href="{data['website']}">{data['website']}</a>

📑 <b>Contract: </b><a href="https://bscscan.com/address/{data['contract']}#code">{data['contract']}</a>

===== 〽️ Charts =====

🛠 <a href="https://bsc.ach.tools/#/tabs/home/{data['contract']}">ACH</a> | 💩 <a href="https://poocoin.app/tokens/{data['contract']}">PooCoin</a> | 📈 <a href="https://dex.guru/token/{data['contract']}-bsc">DexGuru</a>

'''
    bot.reply_to(message, message_data, disable_web_page_preview=True)

@bot.message_handler(commands=['contract'])
def contract(message):

    data = fetchPooCoinStats()

    message_data = f'''
📄 This is the <a href="https://bscscan.com/address/{data['contract']}#code">BSCScan Contract</a>

Address: {data['contract']}
    
'''
    bot.reply_to(message, message_data)

@bot.message_handler(commands=['chart'])
def charts(message):

    data = fetchPooCoinStats()

    message_data = f'''
===== 〽️ Charts =====

Pick a chart, any chart...

🛠 <a href="https://bsc.ach.tools/#/tabs/home/{data['contract']}">ACH</a> | 💩 <a href="https://poocoin.app/tokens/{data['contract']}">PooCoin</a> | 📈 <a href="https://dex.guru/token/{data['contract']}-bsc">DexGuru</a>
    
'''
    bot.reply_to(message, message_data, disable_web_page_preview=True)

# @bot.message_handler(commands=['FASTEST_COIN_TO_1BILL_EVER'])
# def charts(message):
#     message_data = "/FASTEST_COIN_TO_1BILL_EVER"

#     bot.send_message(message.chat.id, message_data, disable_web_page_preview=True)

bot.infinity_polling(timeout=20, interval=0)