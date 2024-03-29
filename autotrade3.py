import time
import pyupbit
import datetime

access = "xtPzmE2vQyjV5cwwrHOqK5w8YBeTy6Mpeigv99Os"
secret = "5y8aU8j5P5YqbBYP6WLFURcSQJr6yNSCeolQwujs"

def get_buy_target_price(ticker, k):
    df = pyupbit.get_ohlcv(ticker, interval="minute10", count=6)
    buy_target_price = df.iloc[0]['close'] - (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return buy_target_price

def get_sell_target_price(ticker, j):
    df = pyupbit.get_ohlcv(ticker, interval="minute10", count=2)
    sell_target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * j
    return sell_target_price


def get_start_time(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute10", count=20)
    start_time = df.index[0]
    return start_time
    
def get_balance(ticker):
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
         if b['balance'] is not None:
          return float(b['balance'])
         else:
            return 0
     return 0

def get_current_price(ticker):
   return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

while True:
try:
   k = 0.02
   j = 0.05

    buy_target_price = get_buy_target_price("KRW-SAND", k)
    sell_target_price = get_sell_target_price("KRW-SAND", j)
    current_price = get_current_price("KRW-SAND")
     if buy_target_price < current_price: 
      krw = get_balance("KRW")
      if krw > 5000:
       upbit.buy_market_order("KRW-SAND", krw*0.9995)
       buy_target_price = y;
     else:
       if sell_target_price > current_price > y:
        sand = get_balance("SAND")
        upbit.sell_market_order("KRW-SAND", sand*0.9995)
      time.sleep(1)

except Exception as e:
print(e)
time.sleep(1)
