import time
import pyupbit
import datetime

access = "68IVeww8qBoSirADcbEdqeh9EE5Z4MxJidj417kH"
secret = "iuMe9x61TQ1Tx005FXQB2tikEulJEEgU0FL53x7m"

def get_buy_target_price(ticker, k):
    #ticker = 코인명 k = 변동폭
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute") # ticker 코인 10분 데이터를 200개 불러옴
    buy_target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k #변동성 돌파전략 구축
    return buy_target_price

def get_sell_target_price(ticker, j):
    #ticker = 코인명 j = 변동폭
    df = pyupbit.get_ohlcv(ticker, interval="minute10") # ticker 코인 10분 데이터를 200개 불러옴
    sell_target_price = df.iloc[0]['close'] - (df.iloc[0]['high'] - df.iloc[0]['low']) * j
    return sell_target_price


def get_start_time(ticker):
    """시작 시간 조회"""
    #9:00임
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        #현재시간 불러오기
        now = datetime.datetime.now()
        #시작시간 설정하기(UPbit 일봉 설정이 아침9시로 설정되어 있어, 9:00)
        start_time = get_start_time("KRW-BTC") #9:00
        end_time = start_time + datetime.timedelta(days=1) #다음날 9:00
        k = 0.4
        j = 0.1

        if start_time < now < end_time - datetime.timedelta(seconds=10): #무한정 돌아가게 하기 위해 10초를 뺀 8시 59분 50초까지만 비교
            buy_target_price = get_buy_target_price("KRW-BTC", k)
            sell_target_price = get_sell_target_price("KRW-BTC", j)
            current_price = get_current_price("KRW-BTC")
            if buy_target_price < current_price: # 구매목표가와 현재가 비교
                krw = get_balance("KRW")
                #5000 : 비트코인 최소거래 금액
                if krw > 5000:
                    #수수료 제외 구매를 위해 0.9995로 설정
                    upbit.buy_market_order("KRW-BTC", krw*0.9995)
            if sell_target_price > current_price: # 판매목표가와 현재가 비교
                    upbit.sell_market_order("KRW-BTC", btc*0.9995)
                        
    except Exception as e:
        print(e)
        time.sleep(1)