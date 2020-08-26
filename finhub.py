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
    count = 0
    ws_count = 0
    counter = 0
    date_counter = 0
    green_candle = False
    downtrend_arr = []
    downtrend = False
    for key, val in res.items():
        if key == 'c':
            for item in val:
                if count == 0:
                    prev_price = item
                if len(downtrend_arr) < 3:
                    downtrend_arr.append(item-prev_price)
                if len(downtrend_arr) == 3:
                    average = sum(downtrend_arr)/len(downtrend_arr)
                    if average < 0:
                        downtrend = True
                    else:
                        downtrend_arr.pop(0)
                for k, v in res.items():#for loop checks if green candle
                    if k == 'o':
                        for i in v:
                            if counter == count:
                                if i < item: #checks if open < close
                                    if ws_count == 0:
                                        ws_count = 1
                                    elif ws_count == 1:
                                        green_candle = True
                                else:
                                    downtrend_arr.pop(0)
                                    downtrend = False
                                    ws_count = 0
                                    green_candle = False
                            counter += 1
                        counter = 0
                if item > prev_price and green_candle == True and downtrend == True:
                    ws_count += 1 
                elif item <= prev_price and count != 0 and ws_count != 1 and downtrend == True:
                    ws_count = 0
                if ws_count == 3:
                    downtrend = False
                    for num in range(1,len(downtrend_arr)):
                        downtrend_arr.pop(0)
                    for k, v in res.items():#for loop gets current date
                        if k == 't':
                            for i in v:
                                if date_counter == count:
                                    print('white soldier on date ' + datetime.datetime.fromtimestamp(i + 28800).strftime('%Y-%m-%d'))
                                date_counter += 1
                            date_counter = 0
                    ws_count = 0
                prev_price = item
                count += 1
    ws_count = 0

def check_bearish_engulfing():
    count = 0
    counter = 0
    date_counter = 0
    uptrend_arr = []
    engulf_arr = []
    uptrend = False
    for key, val in res.items():
        if key == 'c':
            for item in val:
                if count == 0:
                    prev_price = item
                if len(uptrend_arr) < 4:
                    uptrend_arr.append(item-prev_price)
                if len(uptrend_arr) == 4:
                    average = sum(uptrend_arr)/len(uptrend_arr)
                    if average > 0:
                        uptrend = True
                    else:
                        uptrend_arr.pop(0)
                        uptrend = False
                for k, v in res.items():#for loop checks if green candle
                    if k == 'o':
                        for i in v:
                            if counter == count:
                                if i < item and uptrend == True: #checks if open < close
                                    del engulf_arr[:]
                                    engulf_arr.append(i)#open
                                    engulf_arr.append(item)#close
                                elif len(engulf_arr) == 2 and i > item and uptrend == True:
                                    if i >= engulf_arr[1] and item < engulf_arr[0]:
                                        for k, v in res.items():#for loop gets current time
                                            if k == 't':
                                                for i in v:
                                                    if date_counter == count:
                                                        print('bearish engulfing at date: ' + datetime.datetime.fromtimestamp(i + 28800).strftime('%Y-%m-%d'))
                                                    date_counter += 1
                                                date_counter = 0
                                        uptrend_arr.pop(0)
                                        uptrend_arr.append(item-prev_price)
                                    else:
                                        del engulf_arr[:]
                                        uptrend_arr.pop(0)
                                        uptrend = False
                                elif i >= item and uptrend == True and len(engulf_arr) != 2:
                                    uptrend_arr.pop(0)
                                    uptrend = False
                                    del engulf_arr[:]
                                else:
                                    del engulf_arr[:]
                            counter += 1
                        counter = 0
                prev_price = item
                count += 1

def check_bullish_engulfing():
    count = 0
    counter = 0
    date_counter = 0
    downtrend_arr = []
    engulf_arr = []
    downtrend = False
    for key, val in res.items():
        if key == 'c':
            for item in val:
                if count == 0:
                    prev_price = item
                if len(downtrend_arr) < 3:
                    downtrend_arr.append(item-prev_price)
                if len(downtrend_arr) == 3:
                    average = sum(downtrend_arr)/len(downtrend_arr)
                    if average < 0:
                        downtrend = True
                    else:
                        downtrend_arr.pop(0)
                        downtrend = False
                for k, v in res.items():#for loop checks if green candle
                    if k == 'o':
                        for i in v:
                            if counter == count:
                                if i > item and downtrend == True: #checks if open < close
                                    del engulf_arr[:]
                                    engulf_arr.append(i)#open
                                    engulf_arr.append(item)#close
                                elif len(engulf_arr) == 2 and i < item and downtrend == True:
                                    if i <= engulf_arr[1] and item > engulf_arr[0]:
                                        for k, v in res.items():#for loop gets current time
                                            if k == 't':
                                                for i in v:
                                                    if date_counter == count:
                                                        print('bullish engulfing at date: ' + datetime.datetime.fromtimestamp(i + 28800).strftime('%Y-%m-%d'))
                                                    date_counter += 1
                                                date_counter = 0
                                        downtrend_arr.pop(0)
                                        downtrend_arr.append(item-prev_price)
                                    else:
                                        del engulf_arr[:]
                                        downtrend_arr.pop(0)
                                        downtrend = False
                                elif i <= item and downtrend == True and len(engulf_arr) != 2:
                                    downtrend_arr.pop(0)
                                    downtrend = False
                                    del engulf_arr[:]
                                else:
                                    del engulf_arr[:]
                            counter += 1
                        counter = 0
                prev_price = item
                count += 1

check_ws()
check_bearish_engulfing()
check_bullish_engulfing()

