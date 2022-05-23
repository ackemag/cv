#Class is made for stock to easily access the name and ticker of the stocklist

class Stock:
    def __init__(self,name,ticker):
        self.name = name
        self.ticker = ticker
    #How the class is represented as a string
    def __str__(self):
        return f"{self.name}"
    #Name of the stock
    def getName(self):
        return self.name
    #Ticker of the stock
    def getTicker(self):
        return self.ticker


    
