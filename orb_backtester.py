#! python
from init_api import *
from kiteconnect import KiteConnect, KiteTicker
from datetime import datetime, timedelta, date
import pdb
import pandas as pd
import pprint as pp

"""Trade portfolio"""
tPF = {
    1270529:'ICICIBANK',
    738561:'RELIANCE',
    4708097:'RBLBANK',
    1723649:'JINDALSTEL',
    348929:'HINDALCO',
    5582849:'SBILIFE',
    265:'SENSEX',
}

stockyear = 2019 

"""MTA Switch: Allows to change between single trade per day and multiple trades per day.
if mta = 0 > Program will only perform 1 transaction for the day and move to the next day. 
if mta = 1 > Program will perform as many transactions as it can for one day before moving on.
in the code below 'trade' will be set as MTA.
"""
mta = 1  



"""This is the main part of the code. It will iterate through a number of stocks, for 12 months, across every single day of the month for one minute intervals."""
for stockToken, stockName in tPF.items():
    print("Calculating for "+stockName+" ...:")
    percentchange = []
    for stockmonth in range(2):
        for stockday in range(32): 
            try:
                end_date = date(stockyear,stockmonth, stockday)
                start_date = date(stockyear,stockmonth, stockday)
                interval = 'minute' 
                records = kite.historical_data(stockToken, start_date, end_date, interval)
                
                """Main dataframe"""                
                df = pd.DataFrame(records)

                """Separates the opening range dataframe"""
                ord = 60 # opening range duration
                calrange = 375 - ord # period post opening range
                ordf = (df[0:ord]) # opening range dataframe

                """These below are the opening range (High and low) for the day. """
                orHigh = ordf['high'].max()
                orLow = ordf['low'].min()
                # print()
                # print('Opening Range for '+ str(stockday)+ '-'+ str(stockmonth)+': '+str(orLow)+' - '+str(orHigh))
                # print()
                

                """Separates the post-opening range dataframe"""
                adf = df[ord:] 

                """Profit and stoploss targets"""
                profitTarget = 1
                pt = profitTarget/100

                stoplossTarget = 0.25
                slt = stoplossTarget/100


                """pos, trade and tradetype are switches.They have been described below."""
                pos = 0 # Used to check if an exit transaction is needed. 
                num = 0 # counter which allows iteration through every minute of the day. 
                trade = 0 # Used for switching between single and multiple trades per day 
                tradeType = 0 # Used for switching between 1 - Buy transaction(BT), 2 - Sell transaction, 0 - no transaction.

                """The main logic: it checks if the last traded price has crossed above or below the opening range upper or lower limit."""
                for x in range(calrange):
                    ltp = adf.iloc[x,4]
                    if pos == 0 and trade <1:
                        if ltp > orHigh:
                            # print('\nOR upside breakout.')
                            if (pos == 0):
                                bp = ltp
                                pos = 1
                                tradeType = 1
                                # print('BT: Buying now at time: '+ str(adf.iloc[x,0])+' @ '+str(bp))
                        elif ltp < orLow:
                            # print('\nOR downside breakout.')
                            if (pos == 0):
                                sp = ltp
                                pos = 1
                                tradeType = 2
                                # print('ST: Selling now at time: '+ str(adf.iloc[x,0])+' @ '+str(sp))


                        """After entering an active position (either buy or sell), the program will check for 3 things:
                        - whether the profit target is met
                        - whether the stoploss target is met
                        - whether it is the penultimate minute of the day's trading session
                        If any of these 3 criterion are met, active position will be reversed at the closing price. These 3 criterion have been written separately for the buy and sell positions. """

                    # BuyTran Stoploss target sell @ 0.5%
                    
                    elif (tradeType == 1 and ltp <= (bp*(1-slt)) and pos == 1 and trade<1 ):
                        pos = 0
                        sp = ltp
                        # print('BT: Stop loss sale now at time: '+ str(adf.iloc[x,0])+ ' @ '+ str(sp))
                        pc = (sp/bp-1)*100
                        trade = mta
                        percentchange.append(pc)

                        
                        
                    # Last minute of the day sell
                    elif (tradeType == 1 and num==calrange-1 and pos == 1):
                        pos = 0
                        sp = ltp
                        # print('BT: Last trade sale now at time: '+ str(adf.iloc[x,0])+ ' @ '+ str(sp))
                        pc = (sp/bp-1)*100
                        trade = mta
                        percentchange.append(pc)

                        
                    # Profit target sell @ 0.5%
                    elif (tradeType == 1 and pos == 1 and trade<1):
                        if ltp > (bp*(1+pt)):
                            sp = ltp
                            pos = 0
                            # print('BT: Profit sale now at time: '+ str(adf.iloc[x,0]) + ' @ '+ str(sp))
                            pc = (sp/bp-1)*100
                            percentchange.append(pc)
                            trade = mta


                    # SellTran Stoploss target sell @ 0.5%
                    elif (tradeType == 2 and ltp >= (sp*(1+slt)) and pos == 1 and trade<1):
                        pos = 0
                        bp = ltp
                        # print('ST: Stop loss purchase now at time: '+ str(adf.iloc[x,0])+ ' @ '+ str(bp))
                        pc = (sp/bp-1)*100
                        trade = mta
                        percentchange.append(pc)
                        
                    # Sell Tran Last minute of the day sell
                    elif (tradeType == 2 and num==calrange-1 and pos == 1):
                        pos = 0
                        bp = ltp
                        # print('ST: Last trade purchase now at time: '+ str(adf.iloc[x,0])+ ' @ '+ str(bp))
                        pc = (sp/bp-1)*100
                        trade = mta
                        percentchange.append(pc)

                        
                    # Profit target sell @ 0.5%
                    elif (tradeType == 2 and pos == 1 and trade<1):
                        if ltp < (sp*(1-pt)):
                            bp = ltp
                            pos = 0
                            # print('ST: Profit purchase now at time: '+ str(adf.iloc[x,0]) + ' @ '+ str(bp))
                            pc = (sp/bp-1)*100
                            percentchange.append(pc)
                            trade = mta
                    num += 1
            
            except:
                pass
    finalReturn = (round(sum(percentchange), 2))
    print("The total return for "+ stockName+ " over "+str(len(percentchange)) +" trades: "+ str(finalReturn)+"%")






















