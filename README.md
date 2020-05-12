# Project ORB

This is a repository containing code which can be used to backtest the opening range breakout strategy for given stocks for a given period using Zerodha's API. 


In order to run the code you'd require the following: 
1. Subscription to Zerodha's KiteConnect as well as Historical Data API. 
2. Initialise the the API through your access code. I have shared a dummy version of my intializing file (init_api-dummy.py).

You can enter some inputs in the beginning of the code to get results of the backtesting as per your requirement. I'm mentioning the inputs here along with their line number for your reference: 

1. tPF (line 11): You can change the list of stocks along with their token which can be obtained from zerodha's website. 
2. stockyear, stockMonth, endMonth (lines 21-23): These inputs will help you obtain results for specific months. 
(Note: The result for the current month isn't accurate. For some reason, it will perform additional loops in the current month, thereby giving you an incorrect output. For eg. it is 'May 2020' currently while I'm writing this code. Do not put May 2020 as an input. Restrict your calculations for the year 2020 till April 2020.)
3. mta (line 33): ("Multiple Trades Allowed") It is a switch which allows changing between single trade per day and multiple trades per day.
    * if mta = 0 ---> Program will perform as many transactions as it can for one day before moving on.
    * if mta = 1 ---> Program will only perform 1 transaction for the day and move to the next day. 
    * In the code below 'trade' will be set as MTA.
4. ord (line 47): (Opening Range Duration) This allows you to change the opening range duration as per your liking. I mosltly set it to 60 mins. 
5. profitTarget, stoplossTarget (line 63, 66): These inputs will allow you to set your targets for reversal trades. 


I've been learning python for about a month now. And this is the first full backtester that I have written. My apologies if the code is too complicated. 

PS: This code will only work with indian stocks unfortunately. I tried to write a similar code with the 'yfinance' library for international stocks. However, 'yfinance' had certain limitations which didn't allow some of the  iterations used in the program. 

Disclaimer: The code is provided with no guarantee of suitability for use in a real system or otherwise.