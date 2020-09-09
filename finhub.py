import requests
import time
import datetime
import finnhub
import pandas as pd
import mplfinance as mpf
import matplotlib as plt
import json
import base64
from io import BytesIO
from matplotlib.figure import Figure

# Setup client
finnhub_client = finnhub.Client(api_key="MYAPIKEY")
ticker = input("Please enter the ticker of the stock you want to check: ")
today = int(time.time())
one_month = 2678400
res = finnhub_client.stock_candles(ticker.upper(), 'D', today - one_month, today)
compare = finnhub_client.stock_candles(ticker.upper(), 'D', today - one_month - 345600, today - one_month + 345600)
rf_comp = {}
rf_comp['Date'] = []
if compare["s"] != "no_data":
    for num in range(0, len(compare["c"])):
        rf_comp['Date'].append(datetime.datetime.fromtimestamp(compare["t"][num] + 28800).strftime('%Y-%m-%d'))
rf = {}
rf['Date'] = []
rf['Open'] = []
rf['High'] = []
rf['Low'] = []
rf['Close'] = []
rf['Volume'] = []
if res["s"] != "no_data":
    for num in range(0, len(res["c"])):
        rf['Date'].append(datetime.datetime.fromtimestamp(res["t"][num] + 28800).strftime('%Y-%m-%d'))
        #rf['Date'].dt.date
        #rf['Date']= pd.to_datetime(rf['Date']) 
        rf['Open'].append(res["o"][num])
        rf['High'].append(res["h"][num])
        rf['Low'].append(res["l"][num])
        rf['Close'].append(res["c"][num])
        rf['Volume'].append(res["v"][num])
    pda = pd.DataFrame.from_dict(rf)
    pda['Date'] = pda['Date'].astype('datetime64[ns]')
    #pda.index = pd.date_range(start=rf['Date'][0], end=rf['Date'][len(rf['Date'])-1], freq='B') # use pandas to create a date range and set index
    #pda['date'] = pd.date_range(start=rf['Date'][0], end=rf['Date'][len(rf['Date'])-1], freq='B') # also set as column values
    pda.index.name = 'Date'
    pda.set_index('Date', inplace=True)
    pda.shape
    pda.head(3)
    pda.tail(3)
    buf = BytesIO()
    mpf.plot(pda, type='candle', style='charles', title=ticker.upper())

#comment out uptop and uncomment below to display image on web
    #fig = mpf.plot(pda, type='candle', style='charles', title=ticker.upper(), savefig=buf)
    #data = base64.b64encode(buf.getbuffer()).decode("ascii")


    result_arr = []

    def check_ws():
        ws_count = 0
        green_candle = False
        downtrend_arr = []
        downtrend = False
        appender = []
        if len(appender) == 0:
            for num in range(0, len(compare["c"])):
                if compare["t"][num] == res["t"][0]:
                    appender.append(compare["c"][num-1])
        for num in range(0, len(res["c"])):
            close_price = res["c"][num]
            open_price = res["o"][num]
            current_date = datetime.datetime.fromtimestamp(res["t"][num] + 28800).strftime('%m/%d/%Y')
            if num == 0:
                prev_price = appender[0]
            if len(downtrend_arr) < 3:
                print(prev_price)
                downtrend_arr.append(close_price-prev_price)
            if open_price < close_price:
                green_candle = True
            else:
                if downtrend:
                    downtrend_arr.pop(0)
                    #downtrend = False
                    ws_count = 0
                    green_candle = False
            if close_price >= prev_price and green_candle == True and downtrend == True:
                ws_count += 1 
            elif close_price < prev_price and num != 0 and downtrend == True:
                for num in range(ws_count):
                    downtrend_arr.pop(0)
                ws_count = 0
            if len(downtrend_arr) == 3:
                average = sum(downtrend_arr)/len(downtrend_arr)
                if average < 0:
                    downtrend = True
                elif ws_count > 0:
                    downtrend_arr.pop(0)
                else:
                    downtrend_arr.pop(0)
                    downtrend = False 
            if ws_count == 3:
                downtrend = False
                for num in range(1,len(downtrend_arr)):
                    downtrend_arr.pop(0)
                result_arr.append('Third White Soldier on date ' + current_date)
                print('Third White Soldier on date ' + current_date)
                ws_count = 0
            prev_price = close_price

    def check_bc():
        bc_count = 0
        red_candle = False
        uptrend_arr = []
        uptrend = False
        for num in range(0, len(res["c"])):
            close_price = res["c"][num]
            open_price = res["o"][num]
            current_date = datetime.datetime.fromtimestamp(res["t"][num] + 28800).strftime('%m/%d/%Y')
            if num == 0:
                prev_price = close_price
            if len(uptrend_arr) < 3:
                uptrend_arr.append(close_price-prev_price)
            if open_price > close_price:
                red_candle = True
            elif uptrend:
                uptrend_arr.pop(0)
                #uptrend = False
                bc_count = 0
                red_candle = False
            if close_price <= prev_price and red_candle == True and uptrend == True:
                bc_count += 1 
            elif close_price > prev_price and num != 0 and uptrend == True:#double check this
                for num in range(bc_count):
                    uptrend_arr.pop(0)
                bc_count = 0
            if len(uptrend_arr) == 3:
                average = sum(uptrend_arr)/len(uptrend_arr)
                if average > 0:
                    uptrend = True
                elif average <= 0 and bc_count > 0:
                    uptrend_arr.pop(0)
                else:
                    uptrend_arr.pop(0)
                    uptrend = False                
            if bc_count == 3:
                uptrend = False
                for num in range(1,len(uptrend_arr)):
                    uptrend_arr.pop(0)
                result_arr.append('Third Black Crow on date ' + current_date)
                print('Third Black Crow on date ' + current_date)
                bc_count = 0
            prev_price = close_price

    def check_bearish_engulfing():
        uptrend_arr = []
        engulf_arr = []
        uptrend = False
        for num in range(0, len(res["c"])):
            close_price = res["c"][num]
            open_price = res["o"][num]
            current_date = datetime.datetime.fromtimestamp(res["t"][num] + 28800).strftime('%m/%d/%Y')
            if num == 0:
                prev_price = close_price
            if len(uptrend_arr) < 3:
                uptrend_arr.append(close_price-prev_price)
            if len(uptrend_arr) == 3:
                average = sum(uptrend_arr)/len(uptrend_arr)
                if average > 0:
                    uptrend = True
                else:
                    uptrend_arr.pop(0)
                    uptrend = False
            if open_price < close_price and uptrend == True: #checks if green candle
                del engulf_arr[:]
                engulf_arr.append(open_price)#open
                engulf_arr.append(close_price)#close
            elif len(engulf_arr) == 2 and open_price > close_price and uptrend == True:#checks if red candle
                if open_price > engulf_arr[1] and close_price < engulf_arr[0]:
                    result_arr.append('Bearish Engulfing at date: ' + current_date)
                    print('Bearish Engulfing at date: ' + current_date)
                    uptrend_arr.pop(0)
                    uptrend_arr.append(close_price-prev_price)
                else:
                    del engulf_arr[:]
                    uptrend_arr.pop(0)
                    uptrend = False
            elif open_price >= close_price and uptrend == True and len(engulf_arr) != 2:
                uptrend_arr.pop(0)
                uptrend = False
                del engulf_arr[:]
            else:
                del engulf_arr[:]
            prev_price = close_price

    def check_bullish_engulfing():
        downtrend_arr = []
        engulf_arr = []
        downtrend = False
        for num in range(0, len(res["c"])):
            close_price = res["c"][num]
            open_price = res["o"][num]
            current_date = datetime.datetime.fromtimestamp(res["t"][num] + 28800).strftime('%m/%d/%Y')
            if num == 0:
                prev_price = close_price
            if len(downtrend_arr) < 3:
                downtrend_arr.append(close_price-prev_price)
            if len(downtrend_arr) == 3:
                average = sum(downtrend_arr)/len(downtrend_arr)
                if average < 0:
                    downtrend = True
                else:
                    downtrend_arr.pop(0)
                    downtrend = False
            if open_price > close_price and downtrend == True: #checks if open > close
                del engulf_arr[:]
                engulf_arr.append(open_price)#open
                engulf_arr.append(close_price)#close
            elif len(engulf_arr) == 2 and open_price < close_price and downtrend == True:
                if open_price < engulf_arr[1] and close_price > engulf_arr[0]:
                    result_arr.append('Bullish Engulfing at date: ' + current_date)
                    print('Bullish Engulfing at date: ' + current_date)
                    downtrend_arr.pop(0)
                    downtrend_arr.append(close_price-prev_price)
                else:
                    del engulf_arr[:]
                    downtrend_arr.pop(0)
                    downtrend = False
            elif open_price <= close_price and downtrend == True and len(engulf_arr) != 2:
                downtrend_arr.pop(0)
                downtrend = False
                del engulf_arr[:]
            else:
                del engulf_arr[:]
            prev_price = close_price

    def check_shstar():
        uptrend_arr = []
        uptrend = False
        wick = 0
        tail = 0
        for num in range(0, len(res["c"])):
            close_price = res["c"][num]
            open_price = res["o"][num]
            current_date = datetime.datetime.fromtimestamp(res["t"][num] + 28800).strftime('%m/%d/%Y')
            candle_bod = abs(close_price - open_price)
            if num == 0:
                prev_price = close_price
            if len(uptrend_arr) < 3:
                uptrend_arr.append(close_price-prev_price)
            if len(uptrend_arr) == 3:
                average = sum(uptrend_arr)/len(uptrend_arr)
                if average > 0:
                    uptrend = True
                else:
                    uptrend_arr.pop(0)
                    uptrend = False
            if open_price < close_price: #checks if green candle
                wick = res["h"][num] - close_price
                tail = open_price - res["l"][num]
            elif open_price > close_price: # checks if red candle
                wick = res["h"][num] - open_price
                tail = close_price - res["l"][num]
            if wick >= 2 * candle_bod and wick >=2 * tail and uptrend:
                result_arr.append('Shooting Star at date: ' + current_date)
                print('Shooting Star at date: ' + current_date)
            elif len(uptrend_arr) == 3:
                uptrend = False
                uptrend_arr.pop(0)
            prev_price = close_price


    #test()
def main():
    check_ws()
    check_bc()
    check_bearish_engulfing()
    check_bullish_engulfing()
    check_shstar()
    #result = ", ".join(result_arr)
if __name__ == '__main__':
    main()