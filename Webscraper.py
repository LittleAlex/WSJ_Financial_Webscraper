import pandas as pd
from bs4 import BeautifulSoup
import urllib.request as ur
import requests



def get_fundamentals(stock):

    # URL Link
    url_is = 'https://www.wsj.com/market-data/quotes/' + stock + '/financials/annual/income-statement'
    url_bs = 'https://www.wsj.com/market-data/quotes/' + stock + '/financials/annual/balance-sheet'
    url_cs = 'https://www.wsj.com/market-data/quotes/' + stock + '/financials/annual/cash-flow'

    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

    # INCOME STATEMENT
    
    req = ur.Request(url_is, None, headers=headers)
    read_data = ur.urlopen(req).read()
    soup_is = BeautifulSoup(read_data, 'lxml')

    ls = []  # Create empty list
    for l in soup_is.find_all('th'):
        #Find all data structure that is ‘div’
        ls.append(l.string)  # add each element one by one to the list
    for l in soup_is.find_all('td'):
        #Find all data structure that is ‘div’
        ls.append(l.string)  # add each element one by one to the list

    ls = list(filter(None, ls))
    if '5-year trend' in ls: ls.remove('5-year trend')

    is_data = list(zip(*[iter(ls)]*6))

    Income_st = pd.DataFrame(is_data)

    Income_st.columns = Income_st.iloc[0]
    Income_st.drop(Income_st.index[0], inplace=True)
    Income_st = Income_st.T
    Income_st.columns = Income_st.iloc[0]
    Income_st.drop(Income_st.index[0], inplace=True)
    Income_st = Income_st.T

    # BALANCE SHEET

    req = ur.Request(url_bs, None, headers=headers)
    read_data = ur.urlopen(req).read()
    soup_bs = BeautifulSoup(read_data, 'lxml')

    ls = []  # Create empty list
    for l in soup_bs.find_all('td'):
        #Find all data structure that is ‘div’
        ls.append(l.string)  # add each element one by one to the list

    ls = list(filter(None, ls))
    if '5-year trend' in ls: ls.remove('5-year trend')
    #if 'Net Income before Extraordinaries' in ls: ls.remove('Net Income before Extraordinaries')

    is_data = list(zip(*[iter(ls)]*6))

    Balance_sh = pd.DataFrame(is_data)

    header2 = list(Income_st.columns)
    header2.insert(0, 0)

    Balance_sh.columns = header2
    Balance_sh = Balance_sh.T
    Balance_sh.columns = Balance_sh.iloc[0]
    Balance_sh.drop(Balance_sh.index[0], inplace=True)
    Balance_sh = Balance_sh.T

    # CASH FLOW

    req = ur.Request(url_cs, None, headers=headers)
    read_data = ur.urlopen(req).read()
    soup_cs = BeautifulSoup(read_data, 'lxml')

    ls = []  # Create empty list
    
    for l in soup_cs.find_all('td'):
        #Find all data structure that is ‘div’
        ls.append(l.string)  # add each element one by one to the list

    ls = list(filter(None, ls))
    if '5-year trend' in ls: ls.remove('5-year trend')

    is_data = list(zip(*[iter(ls)]*6))

    Cash_fl = pd.DataFrame(is_data)

    header1 = list(Income_st.columns)
    header1.insert(0, 0)

    Cash_fl.columns = header1
    Cash_fl = Cash_fl.T
    Cash_fl.columns = Cash_fl.iloc[0]
    Cash_fl.drop(Cash_fl.index[0], inplace=True)
    Cash_fl = Cash_fl.T

    return Income_st, Balance_sh, Cash_fl


inc_st, bal_sh, cash_fl = get_fundamentals('MDT')




        


