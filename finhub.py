import requests
import time
import datetime
import finnhub
import pandas as pd

# Setup client
finnhub_client = finnhub.Client(api_key="bsuto6n48v6qu589ijp0")

ticker = input("Please enter the ticker of the stock you want to check: ")
res = finnhub_client.stock_candles(ticker.upper(), 'D', 1595557674, int(time.time())) #comparing july 23 to now

def check_ws():
    ws_count = 0
    green_candle = False
    downtrend_arr = []
    downtrend = False
    for num in range(0, len(res["c"])):
        close_price = res["c"][num]
        open_price = res["o"][num]
        current_date = datetime.datetime.fromtimestamp(res["t"][num] + 28800).strftime('%Y-%m-%d')
        if num == 0:
            prev_price = close_price
        if len(downtrend_arr) < 3:
            downtrend_arr.append(close_price-prev_price)
        if open_price < close_price:
            green_candle = True
        else:
            if downtrend:
                downtrend_arr.pop(0)
                #uptrend = False
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
        current_date = datetime.datetime.fromtimestamp(res["t"][num] + 28800).strftime('%Y-%m-%d')
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
        current_date = datetime.datetime.fromtimestamp(res["t"][num] + 28800).strftime('%Y-%m-%d')
        if num == 0:
            prev_price = close_price
        if len(uptrend_arr) < 4:
            uptrend_arr.append(close_price-prev_price)
        if len(uptrend_arr) == 4:
            average = sum(uptrend_arr)/len(uptrend_arr)
            if average > 0:
                uptrend = True
            else:
                uptrend_arr.pop(0)
                uptrend = False
        if open_price < close_price and uptrend == True: #checks if open < close
            del engulf_arr[:]
            engulf_arr.append(open_price)#open
            engulf_arr.append(close_price)#close
        elif len(engulf_arr) == 2 and open_price > close_price and uptrend == True:
            if open_price >= engulf_arr[1] and close_price < engulf_arr[0]:
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
        current_date = res["t"][num]
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
            if open_price <= engulf_arr[1] and close_price > engulf_arr[0]:
                print('Bullish Engulfing at date: ' + datetime.datetime.fromtimestamp(current_date + 28800).strftime('%Y-%m-%d'))
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
        current_date = datetime.datetime.fromtimestamp(res["t"][num] + 28800).strftime('%Y-%m-%d')
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
            print('Shooting Star at date: ' + current_date)
        elif len(uptrend_arr) == 3:
            uptrend = False
            uptrend_arr.pop(0)
        prev_price = close_price

#test()
check_ws()
check_bc()
check_bearish_engulfing()
check_bullish_engulfing()
check_shstar()

