import yfinance as yf
import numpy as np
import pandas as pd


class RawData:


    def __init__(self, stock_name):
        '''This function initiates the stock'''
        self.name = stock_name


    def get_rev_growth(self):
        '''This function returns the annualised growth rate of the
        revenue of the company for the past 3 years'''
        stock = yf.Ticker(self.name)
        return (((stock.financials.loc["Total Revenue"][0]/stock.financials.loc["Total Revenue"][-1])**(1/(len(stock.financials.loc["Total Revenue"]) - 1)))-1)*100


    def get_gross_profit_margin(self):
        '''This function returns the latest Gross Profit Margin of the company'''
        stock = yf.Ticker(self.name)
        return (stock.financials.loc["Gross Profit"][0] / stock.financials.loc["Total Revenue"][0]) * 100


    def get_ebit_margin(self):
        '''This function returns the latest Operating Margin of the company'''
        stock = yf.Ticker(self.name)
        return (stock.financials.loc["Ebit"][0] / stock.financials.loc["Total Revenue"][0]) * 100


    def get_net_margin(self):
        '''This function returns the latest Net Profit Margin of the company'''
        stock = yf.Ticker(self.name)
        return (stock.financials.loc["Net Income"][0] / stock.financials.loc["Total Revenue"][0]) * 100


    def get_qoe(self):
        '''This function returns the latest Quality of Earnings of the company'''
        stock = yf.Ticker(self.name)
        return stock.cashflow.loc["Total Cash From Operating Activities"][0] / stock.cashflow.loc["Net Income"][0]


    def get_fcf(self):
        '''This function returns the latest Free Cash Flow of the company if
        Free Cash Flow is in the yahoo finance table, if Free Cash Flow is not
        present, this function will calculate the Free Cash Flow using Cash
        Flow from Operations minus Capital Expenditures'''
        stock = yf.Ticker(self.name)
        if "Capital Expenditures" in stock.cashflow.index:
            capex = stock.cashflow.loc["Capital Expenditures"][0]
        else:
            capex = 0
        return stock.cashflow.loc["Total Cash From Operating Activities"][0] - capex


    def get_fcf_margin(self):
        '''This function returns the latest Free Cash Flow Margin of the company'''
        stock = yf.Ticker(self.name)
        financials = stock.financials
        cashflow = stock.cashflow
        info = pd.concat([financials, cashflow])

        if "Capital Expenditures" in info.index:
            capex = info.loc["Capital Expenditures"][0]
        else:
            capex = 0

        return ((info.loc["Total Cash From Operating Activities"][0] - capex) / info.loc["Total Revenue"][0]) * 100


    def get_debt_equity(self):
        '''This function returns the latest Debt/Equity ratio of the company
         by using total of Short Term Debt (if present) plus Long Term Debt (if
         present) divide by Total Equity'''
        stock = yf.Ticker(self.name)

        if "Short Long Term Debt" in stock.balance_sheet.index:
            short_term_debt = stock.balance_sheet.loc["Short Long Term Debt"][0]
        else:
            short_term_debt = 0

        if "Long Term Debt" in stock.balance_sheet.index:
            long_term_debt = stock.balance_sheet.loc["Long Term Debt"][0]
        else:
            long_term_debt = 0

        return (short_term_debt + long_term_debt) / stock.balance_sheet.loc["Total Stockholder Equity"][0]


    def get_net_debt_equity(self):
        '''This function returns the latest Net Debt/Equity Ratio of the company
        by using Short Term Debt (if present) plus Long Term Debt (if present)
        minus Total Cash divided by Total Equity'''
        stock = yf.Ticker(self.name)

        if "Short Long Term Debt" in stock.balance_sheet.index:
            short_term_debt = stock.balance_sheet.loc["Short Long Term Debt"][0]
        else:
            short_term_debt = 0

        if "Long Term Debt" in stock.balance_sheet.index:
            long_term_debt = stock.balance_sheet.loc["Long Term Debt"][0]
        else:
            long_term_debt = 0

        if "Cash" in stock.balance_sheet.index:
            cash = stock.balance_sheet.loc["Cash"][0]
        else:
            cash = 0

        return (cash - (short_term_debt + long_term_debt)) / stock.balance_sheet.loc["Total Stockholder Equity"][0]


    def get_cash_ratio(self):
        '''This function returns the latest Cash Ratio of the company by using
        Total Cash divide by Total Current Liabilities'''
        stock = yf.Ticker(self.name)

        if "Cash" in stock.balance_sheet.index:
            cash = stock.balance_sheet.loc["Cash"][0]
        else:
            cash = 0

        return cash / stock.balance_sheet.loc["Total Current Liabilities"][0]


    def get_current_ratio(self):
        '''This function returns the latest Current Ratio of the company by
        using Total Current Assets divide by Total Current Liabilities'''
        stock = yf.Ticker(self.name)
        return stock.balance_sheet.loc["Total Current Assets"][0] / stock.balance_sheet.loc["Total Current Liabilities"][0]


    def get_roe(self):
        '''This function returns the latest Return of Equity of the company'''
        stock = yf.Ticker(self.name)
        financials = stock.financials
        balancesheet = stock.balance_sheet
        info = pd.concat([financials, balancesheet])
        info = info.loc[["Net Income", "Total Stockholder Equity"]]
        return (info.loc["Net Income"][0] / info.loc["Total Stockholder Equity"][0]) * 100


    def get_ccc(self):
        '''This function returns the latest Cash Conversion Cycle days of the
        company'''
        stock = yf.Ticker(self.name)
        financials = stock.financials
        balancesheet = stock.balance_sheet
        info = pd.concat([financials, balancesheet])
        if "Net Receivables" in info.index:
            days_receivables = (info.loc["Net Receivables"][0] / info.loc["Total Revenue"][0]) * 365
        else:
            days_receivables = 0

        if "Accounts Payable" in info.index:
            days_payables = (info.loc["Accounts Payable"][0] / info.loc["Total Revenue"][0]) * 365
        else:
            days_payables = 0

        if "Inventory" in info.index:
            days_inventory = info.loc["Inventory"][0] / info.loc["Total Revenue"][0] * 365
        else:
            days_inventory = 0

        return days_receivables + days_inventory - days_payables
