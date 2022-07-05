import yfinance as yf
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plot import Stock


class RawData:


    def __init__(self, stock_name):
        '''This function initiates the stock object'''
        self.name = stock_name


    def get_data(self):
        '''This function retrieves the raw data table of the company's financials
        using yahoo finance library'''
        stock = yf.Ticker(self.name)

        #Getting the three financial reports of the company from yahoo finance
        financials = stock.financials
        cashflow = stock.cashflow
        balance_sheet = stock.balance_sheet

        #Listing only the fields that needs to be used for analysis and
        #visualisation
        needed = [
            "Total Revenue",
            "Ebit",
            "Net Income",
            "Total Cash From Operating Activities",
            "Gross Profit",
            "Capital Expenditures",
            "Cash",
            "Total Current Liabilities",
            "Short Long Term Debt",
            "Long Term Debt",
            "Total Stockholder Equity",
            "Short Term Investments",
            "Total Current Assets",
            "Total Current Liabilities",
            "Net Receivables",
            "Accounts Payable",
            "Inventory"
        ]

        #Concatenating the three financial reports into one table
        all_info = pd.concat([financials, cashflow, balance_sheet])

        #Dropping duplicates, as some of the fields have duplicates in the
        #concatenated table
        all_info = all_info.loc[needed].drop_duplicates()
        return all_info


    def process_data(self):
        '''This function uses the raw data table and performs data engineering
        on the raw data, so that further features are added to the raw data table
        for analysis'''
        data = self.get_data()

        #Calculating free cash flow for all years
        data.loc["Free Cash Flow"] = data.loc["Total Cash From Operating Activities"] + data.loc["Capital Expenditures"]

        #Calculating Cash Ratio for all years
        data.loc["Cash Ratio"] = data.loc["Cash"] / data.loc["Total Current Liabilities"]

        #Calculating Debt/Equity Ratio for all years
        data.loc["Debt-Equity Ratio"] = (data.loc["Short Long Term Debt"] + data.loc["Long Term Debt"]) / data.loc["Total Stockholder Equity"]

        #Calculating Net Debt/Equity Ratio for all years
        data.loc["Net-Debt Ratio"] = ((data.loc["Short Long Term Debt"] + data.loc["Long Term Debt"]) - (data.loc["Cash"] + data.loc["Short Term Investments"]))/data.loc["Total Stockholder Equity"]

        #Calculating Current Ratio for all years
        data.loc["Current Ratio"] = data.loc["Total Current Assets"] / data.loc["Total Current Liabilities"]

        #Calculating Return of Equity for all years
        data.loc["ROE"] = (data.loc["Net Income"] / data.loc["Total Stockholder Equity"]) * 100

        #Calculating Days Receivables for all years
        data.loc["Days Receivables"] = (data.loc["Net Receivables"] / data.loc["Total Revenue"]) * 365

        #Calculating Days Payables for all years
        data.loc["Days Payables"] = data.loc["Accounts Payable"] / data.loc["Total Revenue"] * 365

        #Calculating Inventory Days for all years
        data.loc["Inventory Days"] = data.loc["Inventory"] / data.loc["Total Revenue"] * 365

        #Calculating Cash Conversion Cycle Days for all years
        data.loc["Cash Conversion Cycle"] = data.loc["Days Receivables"] + data.loc["Days Payables"] - data.loc["Inventory Days"]

        #Calculating Gross Profit Margin for all years
        data.loc["Gross Margin"] = data.loc["Gross Profit"] / data.loc["Total Revenue"] * 100

        #Calculating Net Profit Margin for all years
        data.loc["Net Margin"] = data.loc["Net Income"] / data.loc["Total Revenue"] * 100

        #Calculating Operating Margin for all years
        data.loc["EBIT Margin"] = data.loc["Ebit"] / data.loc["Total Revenue"] * 100

        #Calculating Quality of Earnings for all years
        data.loc["Quality of Earnings"] = data.loc["Total Cash From Operating Activities"] / data.loc["Net Income"]
        return data

    def get_stock(self):
        '''This function passes the stock object into Stock class'''
        return Stock(self.name, self.process_data())
