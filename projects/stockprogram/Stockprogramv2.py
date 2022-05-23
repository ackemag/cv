#Name: Axel Magnusson
#Finished date: 2020-11-30
#Revision date: 2020-12-03
#Assignment nr: 187



#The library I will use for the program
import pandas as pd
import yahoo_fin.stock_info as si 
import yfinance as yf 
import numpy as np
import xlrd 
import sys
import os
from Stockclass import Stock


CLOSING_COL_NUMB = 3
YEAR_EQUITY_RATIO = 1

#List of stock and their respective ticker. Change here or add more to analysie those stocks.
stock_list = [Stock("AstraZeneca","AZN.ST"),
                Stock("Electrolux B","ELUX-B.ST"),
                Stock("Ericsson B","ERIC-B.ST"),
                Stock("Sandvik","SAND.ST")]


#Clear
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

#Main menu where you choose which method you want to use
def methodChoiceMenu():
    first_time = True
    method_list = ['Fundamental analys',
                    'Teknisk analys',
                    'Rangordning av aktier med avseende på dess betavärde',
                    'Avsluta']
    cls()
    
    while True:
        if first_time ==True:
            cls()
            print("*************Välkommen till Aktieköp programmet*************")
            first_time = False
        method_count = 1
        method_str ="\n".join(map(str,method_list)) 
        
        
        for method_str in method_list:  
            str(print(str(method_count)+". "+method_str))
            method_count +=1
        
        try:
            method_options = int(input("Vänligen gör ditt val: "))
            if method_options == 1:
                cls()
                stockChoiceMenu(method_list[method_options-1])
                fundAnalysis()
            elif method_options == 2:
                cls()
                stockChoiceMenu(method_list[method_options-1])
                techAnalysis()
            elif method_options == 3:
                cls()
                betaRanking()
            elif method_options == 4:
                break
        except(ValueError):
            print("Ogiltigt val, försök igen!")
            continue
        if not method_options in range(1,5):
            print("Ogiltigt val, försök igen!")
            continue    

        while True:
            go_back = input("Tryck 'Enter' för att gå tillbaka till huvudmenyn: ")
            if go_back == "":
                break


#Menu where you choose the stock you want to analyise
def stockChoiceMenu(chosen_method):
    global chosen_stock
    counter = 1
    for stock in stock_list:
        print(str(counter)+". "+stock.getName())
        counter +=1
    stock_choice = int(input(f"För vilken aktier vill du utföra {str(chosen_method)} för: "))
    chosen_stock = stock_list[stock_choice-1]
 

#Stock ranking decided by their beta value
def betaRanking():
    beta_list = []
    for stock in stock_list:
        all_data = si.get_quote_table(stock.getTicker()) # from yahoo_fin doc to get data
        bdata = all_data["Beta (5Y Monthly)"]
        beta_list.append([bdata,stock])
    beta_list.sort(reverse=True)
    beta_column = ['Betavärde', 'Företag']
    beta_row = []
    for i in range(len(beta_list)):
        beta_row.append(str(i+1)+".")
    beta_df = pd.DataFrame(beta_list,index=beta_row, columns=beta_column) #pandas dataframe to rank beta value.
    print(beta_df)
        

#Technical analysis 
def techAnalysis():
    stock_tech_ticker = chosen_stock.getTicker()
    stock_info = yf.download(stock_tech_ticker, period="30d") #from yfinance doc to get data
    stock_df = pd.DataFrame(stock_info)
    stock_df.to_excel('stock_data.xlsx')
    excelfile = pd.read_excel('stock_data.xlsx')

    #Beta value 
    beta_data = si.get_quote_table(stock_tech_ticker, dict_result=True)
    beta_value = beta_data["Beta (5Y Monthly)"]

    #Highest value (30d)
    highest =  round(excelfile["High"].max(),1)

    #Lowest value (30d)
    lowest = round(excelfile["Low"].min(),1)

    #Stock growth (30d)
    workbook = xlrd.open_workbook('stock_data.xlsx') #from xlrd doc to use extract values from exceldocument
    worksheet = workbook.sheet_by_name('Sheet1')
    new_price = worksheet.cell_value(worksheet.nrows-1,CLOSING_COL_NUMB)
    old_price = worksheet.cell_value(1,CLOSING_COL_NUMB)
    stock_growth = round(((new_price-old_price)/old_price)*100,1)

    print("Kursutveckling(30d):",str(stock_growth)+"%")
    print("Betavärdet:",beta_value)
    print("Lägsta kurs(30d):",lowest)
    print("Högsta kurs(30d):",highest)


#Fundamental analysis
def fundAnalysis():
    
    stock_fund_ticker = chosen_stock.getTicker()

    #Price to earnings ratio & Price to sales ratio
    fund_data = si.get_stats_valuation(stock_fund_ticker) # from yahoo_fin doc to get data
    fund_data = fund_data.iloc[:,:2]
    fund_data.columns = ["Attribute", "Recent"]
    price_to_earnings = float(fund_data[fund_data.Attribute.str.contains("Trailing P/E")].iloc[0,1])
    price_to_sales = float(fund_data[fund_data.Attribute.str.contains("Price/Sales")].iloc[0,1])
    
    

    #Equity ratio
    balance_sheet_data = si.get_balance_sheet(stock_fund_ticker) # from yahoo_fin doc to get data
    xrows = balance_sheet_data.loc["totalAssets"]
    equity_df = pd.DataFrame(balance_sheet_data)
    equity_df.to_excel('balance_sheet.xlsx')
    workbook = xlrd.open_workbook('balance_sheet.xlsx')
    worksheet = workbook.sheet_by_name('Sheet1')
    total_stock_equity = worksheet.cell_value(4,YEAR_EQUITY_RATIO)
    total_assets = xrows[0]
    equity_precentage = round((total_stock_equity/total_assets)*100,1)

    print("Företagets p/e-tal är:",price_to_earnings)
    print("Företagets p/s-tal är:",price_to_sales)
    print("Företagets soliditet är:",str(equity_precentage)+"%")

#Programstart
methodChoiceMenu()