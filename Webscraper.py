import pandas as pd
from bs4 import BeautifulSoup
import urllib.request as ur
import requests


def convert_numbers(data):
    col_len = data.shape[1]
    row_len = data.shape[0]

    for i in range(0, col_len):
        for j in range(0, row_len):
            if ("%" in data.iloc[j, i]) == True:
                data.iloc[j, i] = float(data.iloc[j, i].replace("%", "")) / 100
                continue
            if ("," in data.iloc[j, i]) == True:
                if ("(" in data.iloc[j, i]) == True:
                    data.iloc[j, i] = data.iloc[j, i].replace(")", "")
                    data.iloc[j, i] = data.iloc[j, i].replace("(", "-")

                data.iloc[j, i] = float(data.iloc[j, i].replace(",", ""))
                continue
            if ("." in data.iloc[j, i]) == True:
                if ("(" in data.iloc[j, i]) == True:
                    data.iloc[j, i] = data.iloc[j, i].replace(")", "")
                    data.iloc[j, i] = data.iloc[j, i].replace("(", "-")

                data.iloc[j, i] = float(data.iloc[j, i].replace(".", "")) / 100
                continue
            if ("(" in data.iloc[j, i]) == True:
                data.iloc[j, i] = data.iloc[j, i].replace(")", "")
                data.iloc[j, i] = data.iloc[j, i].replace("(", "-")
                data.iloc[j, i] = -float(data.iloc[j, i])

    return data


def get_fundamentals(stock, period="annual", exchange=""):
    # Functiona pulls income statement, balance sheet and cash flow from WSJ.com.
    # Allows selection between annual and quarterly data via period = "annual" or "quarter"
    # Allows user to input an exchange directly into the URL used (optional, default is US). Examples: UK - "UK/XLON/". Look up exchanges on WSJ.com.

    url_is = 'https://www.wsj.com/market-data/quotes/' + exchange + \
        stock + '/financials/' + period + '/income-statement'
    url_bs = 'https://www.wsj.com/market-data/quotes/' + \
        exchange + stock + '/financials/' + period + '/balance-sheet'
    url_cs = 'https://www.wsj.com/market-data/quotes/' + \
        exchange + stock + '/financials/' + period + '/cash-flow'

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

    # INCOME STATEMENT

    req = ur.Request(url_is, None, headers=headers)
    read_data = ur.urlopen(req).read()
    soup_is = BeautifulSoup(read_data, 'lxml')

    ls = []  # Create empty list
    for l in soup_is.find_all('th'):
        #Find all data structure that is 'th'
        ls.append(l.string)  # add each element one by one to the list
    for l in soup_is.find_all('td'):
        #Find all data structure that is 'td'
        ls.append(l.string)  # add each element one by one to the list

    #Remove empty, '5-year trend' and '5-qtr trend' columns
    ls = list(filter(None, ls))
    if '5-year trend' in ls:
        ls.remove('5-year trend')
    if '5-qtr trend' in ls:
        ls.remove('5-qtr trend')

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

    #Remove empty, '5-year trend' and '5-qtr trend' columns
    ls = list(filter(None, ls))
    if '5-year trend' in ls:
        ls.remove('5-year trend')
    if '5-qtr trend' in ls:
        ls.remove('5-qtr trend')
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

    #Remove empty, '5-year trend' and '5-qtr trend' columns
    ls = list(filter(None, ls))
    if '5-year trend' in ls:
        ls.remove('5-year trend')
    if '5-qtr trend' in ls:
        ls.remove('5-qtr trend')

    is_data = list(zip(*[iter(ls)]*6))

    Cash_fl = pd.DataFrame(is_data)

    header1 = list(Income_st.columns)
    header1.insert(0, 0)

    Cash_fl.columns = header1
    Cash_fl = Cash_fl.T
    Cash_fl.columns = Cash_fl.iloc[0]
    Cash_fl.drop(Cash_fl.index[0], inplace=True)
    Cash_fl = Cash_fl.T

    Income_st = convert_numbers(Income_st)
    Balance_sh = convert_numbers(Balance_sh)
    Cash_fl = convert_numbers(Cash_fl)

    return Income_st, Balance_sh, Cash_fl

