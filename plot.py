import yfinance as yf
import numpy as np
import pandas as pd
import plotly.graph_objects as go


class Stock():


    def __init__(self, name, data):
        '''This function initiates the stock object from the data table which
        is generated from get_stock_data_table'''
        self.name = name
        self.revenue = data.loc["Total Revenue"]
        self.ebit = data.loc["Ebit"]
        self.netincome = data.loc["Net Income"]
        self.grossmargin = data.loc["Gross Margin"]
        self.ebitmargin = data.loc["EBIT Margin"]
        self.netmargin = data.loc["Net Margin"]
        self.operatingcashflow = data.loc["Total Cash From Operating Activities"]
        self.freecashflow = data.loc["Free Cash Flow"]
        self.debtequity = data.loc["Debt-Equity Ratio"]
        self.netdebtratio = data.loc["Net-Debt Ratio"]
        self.currentratio = data.loc["Current Ratio"]
        self.cashratio = data.loc["Cash Ratio"]
        self.roe = data.loc["ROE"]
        self.ccc = data.loc["Cash Conversion Cycle"]
        self.qoe = data.loc["Quality of Earnings"]


    def check_cagr_rev(self):
        '''This function calculates the annualised growth of the company revenue
        for the past three years'''
        return (((self.revenue[0]/self.revenue[-1])**(1/3))-1)*100


    def check_cagr_ebit(self):
        '''This function calculates the annualised growth of the company operating
        profit for the past three years'''
        return (((self.ebit[0]/self.ebit[-1])**(1/3))-1)*100


    def check_cagr_netinc(self):
        '''This function calculates the annualised growth of the company net
        income for the past three years'''
        return (((self.netincome[0]/self.netincome[-1])**(1/3))-1)*100


    def check_cagr_fcf(self):
        '''This function calculates the annualised growth of the company free
        cash flow for the past three years'''
        return (((self.freecashflow[0]/self.freecashflow[-1])**(1/3))-1)*100


    def check_cagr_ocf(self):
        '''This function calculates the annualised growth of the company
        operating cash flow for the past three years'''
        return (((self.operatingcashflow[0]/self.operatingcashflow[-1])**(1/3))-1)*100


    def check_growth(self):
        '''This function ranks the annualised growth of the company for the past
        three years and takes the mean of the ranks to display as Growth criteria
        in the spider chart'''
        rev = pd.cut([self.check_cagr_rev()],[-np.inf, 0, 5, 10, 15, 20, np.inf], labels = [0, 1, 2, 3, 4, 5])
        ebit = pd.cut([self.check_cagr_ebit()],[-np.inf, 0, 5, 10, 15, 20, np.inf], labels = [0, 1, 2, 3, 4, 5])
        netinc = pd.cut([self.check_cagr_netinc()],[-np.inf, 0, 5, 10, 15, 20, np.inf], labels = [0, 1, 2, 3, 4, 5])
        fcf = pd.cut([self.check_cagr_fcf()], [-np.inf, 0, 5, 10, 15, 20, np.inf], labels = [0, 1, 2, 3, 4, 5])
        return np.mean([rev, ebit, netinc, fcf])


    def check_profitability(self):
        '''This function ranks the latest profitability of the company
        in terms of Gross Profit Margin, Operating Profit Margin,
        Net Profit Margin, and takes the mean of the ranks to display as
        Profitability criteria in the spider chart'''
        gpm = pd.cut(self.grossmargin,[-np.inf, 0, 10, 20, 30, 40, np.inf], labels = [0, 1, 2, 3, 4, 5])
        ebitm = pd.cut(self.ebitmargin,[-np.inf, 0, 2, 4, 6, 8, np.inf], labels = [0, 1, 2, 3, 4, 5])
        npm = pd.cut(self.netmargin,[-np.inf, 0, 2.5, 5, 7.5, 10, np.inf], labels = [0, 1, 2, 3, 4, 5])
        return np.mean([gpm, ebitm, npm])


    def check_liquidity(self):
        '''This function ranks the latest liquidity of the company
        in terms of Operating Cash Flow Growth, Quality of Earnings and takes
        the mean of the ranks to display as Liquidity criteria in the spider
        chart'''
        ocf = pd.cut([self.check_cagr_ocf()],[-np.inf, 0, 5, 10, 15, 20, np.inf], labels = [0, 1, 2, 3, 4, 5])
        qoe = pd.cut(self.qoe, [-np.inf, 0, 0.25, 0.5, 0.75, 1, np.inf], labels = [0, 1, 2, 3, 4, 5])
        return np.mean([qoe])


    def check_efficiency(self):
        '''This function ranks the latest Efficiency of the company
        in terms of Return of Equity, Cash Conversion Cycle days and takes
        the mean of the ranks to display as Efficiency criteria in the spider
        chart'''
        roe = pd.cut(self.roe, [-np.inf, 0, 5, 10, 15, 20, np.inf], labels = [0, 1, 2, 3, 4, 5])
        ccc = pd.cut(self.ccc, [-np.inf, 0, 32.5, 65, 97.5, 130, np.inf], labels = [5, 4, 3, 2, 1, 0])
        return np.mean([roe, ccc])


    def check_health(self):
        '''This function ranks the latest Health of the company
        in terms of Debt/Equity Ratio, Net Debt/Equity Ratio, Current Ratio,
        Cash Ratio, and takes the mean of the ranks to display as Health
        criteria in the spider chart'''
        der = pd.cut([self.debtequity[0]], [-np.inf, 0, 0.375, 0.75, 1.125, 1.5, np.inf], labels = [5, 4, 3, 2, 1, 0])
        nder = pd.cut([self.netdebtratio[0]],  [-np.inf, 0, 0.125, 0.25, 0.375, 0.5, np.inf], labels = [5, 4, 3, 2, 1, 0])
        cur = pd.cut([self.currentratio[0]], [-np.inf, 0, 0.5, 1 , 1.5, 2, np.inf], labels = [0, 1, 2, 3, 4, 5])
        cashr = pd.cut([self.cashratio[0]], [-np.inf, 0, 0.25, 0.5, 0.75, 1, np.inf], labels = [0, 1, 2, 3, 4, 5])
        return np.mean([der, nder, cur, cashr])


    def plot(self):
        '''This function plots the spider chart of the stock to display the
        Growth, Profitability, Liquidity, Efficiency and Health aspects of the
        company'''
        criterias = [self.check_growth(),
                     self.check_profitability(),
                     self.check_liquidity(),
                     self.check_efficiency(),
                     self.check_health()
                    ]
        names = ["Growth", "Profitability", "Liquidity", "Efficiency", "Health"]
        data = go.Scatterpolar(r = criterias, theta = names, fill = "toself")
        fig = go.Figure(data = data, layout = dict(title = self.name.upper()))
        return fig
