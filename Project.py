# %% [markdown]
# # **Guide for Fundamental Analysis of EUROSTOXX**
# 
# The following script was created in order to visualise graphically fundamental financial data on a macro level. 
# 
# As such, the user will be able to make investment decisions and identify value stocks in the EUROSTOXX index without manually having to read financial reports. 
# 
# The latter section of the script provide visualisations of various fundamental metrics - feel free to scroll down to ease your curiousity and invest intelligently! 

# %%
# %% 
!pip install yahoo_fin
!pip install requests_html
!pip install plotly.express
!pip install nbformat 
!pip install schedule

# %% [markdown]
# ### **Import of packages**
# 
# The yahoo_fin module is used to gather data from the Yahoo Finance website. The pandas module is used for manipulation dataframes, while tdqm will be used to create a progess bar while scraping data from Yahoo Finance. Beautiful soup is used for assistance to download the required tickers and the requests are used to obtain webdata. Lastly, pyplot is imported to create interactive graphs in which the user can hover over desired datapoints and obtain further information. 

# %%
import yahoo_fin.stock_info as si #Get data
import pandas as pd #Data manipulation
from tqdm import tqdm #Make a progress bar because that's cool...
from bs4 import BeautifulSoup # to parse external data
import requests # to get data
from requests_html import HTMLSession
import plotly.express as px #Charting
import pickle
#import matplotlib.pyplot as plt
#import schedule
#import time

# %% [markdown]
# ### **Gathering Tickers**
# 
# The tickers of the EUROSTOXX index changes with business cycles as well as innovative companies gaining ground. Therefore, the following function has been created to obtain an updated version of EUROSTOXX tickers at all times. 

# %%
#Function to define the tickers of the EUROSTOXX index

def getEURSTX50tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/EURO_STOXX_50')
    soup = BeautifulSoup(resp.text, 'lxml')
    tableEURSTX = soup.find(text="Ticker").find_parent("table").find('tbody').findAll('tr')[1:]

    EURSTX_tickers = []
    for row in tableEURSTX:
        ticker1 = row.findAll('td')[0].text.strip()
        EURSTX_tickers.append(ticker1)
    with open("EURSTX50tickers.pickle", "wb") as f:
        pickle.dump(EURSTX_tickers, f)
    return EURSTX_tickers

ER_tickers = getEURSTX50tickers()
ER_tickers

# %% [markdown]
# ### **Valuation Measures**
# 
# Under a given ticker on the Yahoo Finance website 'statistics' section, the data is commonly devided into two sections. The first section gathers data related to overall valuation measures such as market cap, enterprise value and trailing P/E. The following function aims to scrape this information and place it into a dataframe for each of the tickers. 

# %%
#Function to gather valuation measures

def valuation_measures(reload_EURSTX50=False):
       
    if reload_EURSTX50:
        EURSTX_tickers = getEURSTX50tickers()
    else:
        with open("EURSTX50tickers.pickle","rb") as f:
            EURSTX_tickers = pickle.load(f)
    ticker_stats = {}     
    for ticker in EURSTX_tickers:
        try:
            df = si.get_stats_valuation(ticker)
            df = df.iloc[:,:2]
            df.columns = ["Attribute", "Recent"]
            ticker_stats[ticker] = df
        except:
            pass
    dat = pd.concat(ticker_stats)
    dat = dat.reset_index()
    dat = dat.dropna()
    del dat["level_1"]
    dat.columns = ["Ticker", "Attribute", "Recent"]
    dat.to_csv('df1.csv')
    return dat

# %%
#Assignation and valuation measures dataframe 

df1 = valuation_measures()
df1


# %% [markdown]
# ### **Extra Stats**
# 
# However, the statistics page contain a wealth of additional information. Therefore, the following function was defined to gather the extra stats and form them into a usable dataframe

# %%
#Function to gather additional information 

def extra_stats(reload_EURSTX50=False):
    
    if reload_EURSTX50:
        EURSTX_tickers = getEURSTX50tickers()
    else:
        with open("EURSTX50tickers.pickle","rb") as f:
            EURSTX_tickers = pickle.load(f)
    ticker_extra_stats = {}
    for ticker in tqdm(ER_tickers):
        try:
            ticker_extra_stats[ticker] = si.get_stats(ticker)
        except:
            pass
    dat2 = pd.concat(ticker_extra_stats)
    dat2 = dat2.reset_index()
    dat2 = dat2.dropna()
    del dat2["level_1"]
    dat2.columns = ["Ticker", "Attribute", "Value"]
    dat2.to_csv('df2.csv')
    return dat2

# %%
#Assignation and extra stats dataframe 


df2 = extra_stats()
df2

# %%
print(df1)

# %%
print(df2)

# %% [markdown]
# ### **Pivoting**
# 
# In the dataframes df1 and df2 we see the dataframe repeating the ticker for each additional attribute/value. In order to create a wide dataframe, pivoting was applied

# %%
#Pivoting df1 and df2

df1_wide = df1.pivot(index = "Ticker", columns="Attribute", values="Recent")
df2_wide = df2.pivot(index = "Ticker", columns="Attribute", values="Value")

# %% [markdown]
# ### **Footnote elimination**
# 
# When scraping from the Yahoo Finance website, various footnotes which on the website contain further definitions of the attribute are included in the naming of the attribute. 
# The following aims to eliminate these footnote numbers since the definitions are not required for this macro analysis.

# %%
#Removing footnoted by renaming
df2_wide.rename(columns = {"% Held by Insiders 1":"% Held by Insiders"}, inplace = True)
df2_wide.rename(columns = {"% Held by Institutions 1":"% Held by Institutions"}, inplace = True)
df2_wide.rename(columns = {"200-Day Moving Average 3":"200-Day Moving Average"}, inplace = True)
df2_wide.rename(columns = {"5 Year Average Dividend Yield 4":"5 Year Average Dividend Yield %"}, inplace = True)
df2_wide.rename(columns = {"50-Day Moving Average 3":"50-Day Moving Average"}, inplace = True)
df2_wide.rename(columns = {"52 Week High 3":"52 Week High"}, inplace = True)
df2_wide.rename(columns = {"52 Week Low 3":"52 Week Low"}, inplace = True)
df2_wide.rename(columns = {"52-Week Change 3":"52-Week Change %"}, inplace = True)
df2_wide.rename(columns = {"Avg Vol (10 day) 3":"Avg Vol (10 day)"}, inplace = True)
df2_wide.rename(columns = {"Avg Vol (3 month) 3":"Avg Vol (3 month)"}, inplace = True)
df2_wide.rename(columns = {"Dividend Date 3":"Dividend Date"}, inplace = True)
df2_wide.rename(columns = {"Ex-Dividend Date 4":"Ex-Dividend Date"}, inplace = True)
df2_wide.rename(columns = {"Forward Annual Dividend Rate 4":"Forward Annual Dividend Rate"}, inplace = True)
df2_wide.rename(columns = {"Forward Annual Dividend Yield 4":"Forward Annual Dividend Yield %"}, inplace = True)
df2_wide.rename(columns = {"Last Split Date 3":"Last Split Date"}, inplace = True)
df2_wide.rename(columns = {"Last Split Factor 2":"Last Split Factor"}, inplace = True)
df2_wide.rename(columns = {"Operating Margin (ttm)":"Operating Margin (ttm) %"}, inplace = True)
df2_wide.rename(columns = {"Payout Ratio 4":"Payout Ratio %"}, inplace = True)
df2_wide.rename(columns = {"Profit Margin":"Profit Margin %"}, inplace = True)
df2_wide.rename(columns = {"Quarterly Earnings Growth (yoy)":"Quarterly Earnings Growth (yoy) %"}, inplace = True)
df2_wide.rename(columns = {"Quarterly Revenue Growth (yoy)":"Quarterly Revenue Growth (yoy) %"}, inplace = True)
df2_wide.rename(columns = {"Return on Assets (ttm)":"Return on Assets (ttm) %"}, inplace = True)
df2_wide.rename(columns = {"Return on Equity (ttm)":"Return on Equity (ttm) %"}, inplace = True)
df2_wide.rename(columns = {"S&P500 52-Week Change 3":"S&P500 52-Week Change %"}, inplace = True)
df2_wide.rename(columns = {"Shares Outstanding 5":"Shares Outstanding"}, inplace = True)
df2_wide.rename(columns = {"Trailing Annual Dividend Rate 3":"Trailing Annual Dividend Rate"}, inplace = True)
df2_wide.rename(columns = {"Trailing Annual Dividend Yield 3":"Trailing Annual Dividend Yield %"}, inplace = True)

# %% [markdown]
# ### **Float Transformation**
# 
# Various of the datapoints contain either a letter, such as M for million or % for percentage, which are removed with the following: 

# %%
# Float Transforming and string deletion
df1_wide['Trailing P/E'] = df1_wide['Trailing P/E'].astype(float)
df1_wide['Enterprise Value/EBITDA'] = df1_wide['Enterprise Value/EBITDA'].astype(float)
df1_wide['Enterprise Value/Revenue'] = df1_wide['Enterprise Value/Revenue'].astype(float)
df1_wide['Forward P/E'] = df1_wide['Forward P/E'].astype(float)
df1_wide['PEG Ratio (5 yr expected)'] = df1_wide['PEG Ratio (5 yr expected)'].astype(float)
df1_wide['Price/Book (mrq)'] = df1_wide['Price/Book (mrq)'].astype(float)
df1_wide['Price/Sales (ttm)'] = df1_wide['Price/Sales (ttm)'].astype(float)


df2_wide['50-Day Moving Average'] = df2_wide['50-Day Moving Average'].astype(float)
df2_wide['52 Week High'] = df2_wide['52 Week High'].astype(float)
df2_wide['52 Week Low'] = df2_wide['52 Week Low'].astype(float)
df2_wide['Beta (5Y Monthly)'] = df2_wide['Beta (5Y Monthly)'].astype(float)
df2_wide['Book Value Per Share (mrq)'] = df2_wide['Book Value Per Share (mrq)'].astype(float)
df2_wide['Current Ratio (mrq)'] = df2_wide['Current Ratio (mrq)'].astype(float)
df2_wide['Diluted EPS (ttm)'] = df2_wide['Diluted EPS (ttm)'].astype(float)
df2_wide['Forward Annual Dividend Rate'] = df2_wide['Forward Annual Dividend Rate'].astype(float)
df2_wide['Quarterly Revenue Growth (yoy) %'] = df2_wide['Quarterly Revenue Growth (yoy) %'].astype(str).str.strip('%').astype('float')
df2_wide['Revenue Per Share (ttm)'] = df2_wide['Revenue Per Share (ttm)'].astype(float)
df2_wide['Total Cash Per Share (mrq)'] = df2_wide['Total Cash Per Share (mrq)'].astype(float)
df2_wide['Total Debt/Equity (mrq)'] = df2_wide['Total Debt/Equity (mrq)'].astype(float)
df2_wide['Trailing Annual Dividend Rate'] = df2_wide['Trailing Annual Dividend Rate'].astype(float)
df2_wide['200-Day Moving Average'] = df2_wide['200-Day Moving Average'].astype(float)
df2_wide['% Held by Insiders'] = df2_wide['% Held by Insiders'].astype(str).str.strip('%').astype('float')
df2_wide['% Held by Institutions'] = df2_wide['% Held by Institutions'].astype(str).str.strip('%').astype('float')
df2_wide['5 Year Average Dividend Yield %'] = df2_wide['5 Year Average Dividend Yield %'].astype(float)
df2_wide['Forward Annual Dividend Yield %'] = df2_wide['Forward Annual Dividend Yield %'].astype(str).str.strip('%').astype('float')
df2_wide['Operating Margin (ttm) %'] = df2_wide['Operating Margin (ttm) %'].astype(str).str.strip('%').astype('float')
df2_wide['Payout Ratio %'] = df2_wide['Payout Ratio %'].astype(str).str.strip('%').astype('float')
df2_wide['Profit Margin %'] = df2_wide['Profit Margin %'].astype(str).str.strip('%').astype('float')
df2_wide['Return on Assets (ttm) %'] = df2_wide['Return on Assets (ttm) %'].astype(str).str.strip('%').astype('float')
df2_wide['Return on Equity (ttm) %'] = df2_wide['Return on Equity (ttm) %'].astype(str).str.strip('%').astype('float') 
df2_wide['Trailing Annual Dividend Yield %'] = df2_wide['Trailing Annual Dividend Yield %'].astype(str).str.strip('%').astype('float')
#df2_wide['S&P500 52-Week Change %'] = df2_wide['S&P500 52-Week Change %'].astype(str).str.strip('%').astype('float')
#df2_wide['Quarterly Earnings Growth (yoy) %'] = df2_wide['Quarterly Earnings Growth (yoy) %'].astype(str).str.strip('%').astype('float')
#df2_wide['52-Week Change %'] = df2_wide['52-Week Change %'].astype(str).str.strip('%').astype('float')

# %% [markdown]
# ### **Concatinating**
# 
# The datasets, df1_wide and df2_wide are now concatinated i.e joined and the na values, which are surprisingly common in Trailing P/E, are ignored. 

# %%
#Joining the dataframes
joined_data = pd.concat([df1_wide, df2_wide], axis=1, join='inner')
joined_data = joined_data[joined_data['Trailing P/E'].notna()]
joined_data.to_csv("completeddf.csv")
joined_data

# %% [markdown]
# ### **Charting**
# 
# Below are the data visualisation to guide value investing and investment decisions overall. Explanations for each are offered seperately: 

# %% [markdown]
# ### **Quarterly Revenue Growth (yoy) % vs. Price/Sales (ttm) vs. Trailing P/E**
# 
# Investment guide: stocks at the bottom right are value stock and investment-worthy. 
# Revenue growth is high, while the price is relativly low. The trailing P/E, however, always depends on interpretation - yet, in general, lower is better, indicating undervaluation.

# %%
# Plot of Quarterly Revenue Growth (yoy) % vs. Price/Sales (ttm) vs. Trailing P/E 

ValueStockChart = px.scatter(joined_data,
                   x='Quarterly Revenue Growth (yoy) %',
                   y='Price/Sales (ttm)',
                   size = "Trailing P/E",
                   hover_name = joined_data.index,
                   title="Quarterly Revenue Growth (yoy) % vs. Price/Sales (ttm) vs. Trailing P/E",
                   width=1250,
                   height=700)


ValueStockChart.show()

# %% [markdown]
# ## **Additional visualisations**
# 
# ### **Quarterly Revenue Growth (yoy) % vs. Trailing Annual Dividend Yield % vs. Trailing P/E**
# 
# Investment guide: stocks at the top right are value stock and investment-worthy. 
# Revenue growth is high, while the dividends are relativly high. The trailing P/E, however, always depends on interpretation - yet, in general, lower is better, indicating undervaluation.  
# 
# ### **Quarterly Revenue Growth (yoy) % vs. Price/Book (mrq) vs. Trailing P/E**
# 
# Investment guide: stocks at the bottom right are value stock and investment-worthy. 
# Revenue growth is high, while the price-to-book is relativly low - indicating undervaluation. The trailing P/E, however, always depends on interpretation - yet, in general, lower is better, indicating undervaluation.  
# 
# ### **Quarterly Revenue Growth (yoy) % vs. Enterprise Value/EBITDA vs. Trailing P/E**
# 
# Investment guide: stocks at the bottom right are value stock and investment-worthy. 
# Revenue growth is high, while the Enterprise Value/EBITDA is relativly low - indicating undervaluation. The trailing P/E, however, always depends on interpretation - yet, in general, lower is better, indicating undervaluation. 
# 
# 

# %%
if not os.path.exists("images"):
    os.mkdir("images")

def plot_value_stocks(graph_type = None):
    if graph_type == "valuePS":
        valuePS = px.scatter(joined_data,
                   x='Quarterly Revenue Growth (yoy) %',
                   y='Price/Sales (ttm)',
                   size = "Trailing P/E",
                   hover_name = joined_data.index,
                   title="Quarterly Revenue Growth (yoy) % vs. Price/Sales (ttm) vs. Trailing P/E",
                   width=1250,
                   height=700)
        return valuePS.show()
    elif graph_type == "valueDiv":
        ValueDiv = px.scatter(joined_data,
                   x='Quarterly Revenue Growth (yoy) %',
                   y='Trailing Annual Dividend Yield %',
                   size = "Trailing P/E",
                   hover_name = joined_data.index,
                   title="Quarterly Revenue Growth (yoy) % vs. Trailing Annual Dividend Yield % vs. Trailing P/E",
                   width=1250,
                   height=700)
        return ValueDiv.show()
    elif graph_type == "valuePB":
        ValuePB = px.scatter(joined_data,
                   x='Quarterly Revenue Growth (yoy) %',
                   y='Price/Book (mrq)',
                   size = "Trailing P/E",
                   hover_name = joined_data.index,
                   title="Quarterly Revenue Growth (yoy) % vs. Price/Book (mrq) vs. Trailing P/E",
                   width=1250,
                   height=700)
        return ValuePB.show()
    elif graph_type == "valueEBITDA":
        valueEBITDA = px.scatter(joined_data,
                   x='Quarterly Revenue Growth (yoy) %',
                   y='Enterprise Value/EBITDA',
                   size = "Trailing P/E",
                   hover_name = joined_data.index,
                   title="Quarterly Revenue Growth (yoy) % vs. Enterprise Value/EBITDA vs. Trailing P/E",
                   width=1250,
                   height=700)
        return valueEBITDA.show()
    else: 
        print("You have to include graph_type argument in the function! Then, you can choose from different graph types!")
    



graph1 = plot_value_stocks(graph_type = "valuePS") 
graph2 = plot_value_stocks(graph_type = "valueDiv")
graph3 = plot_value_stocks(graph_type = "valuePB")
graph4 = plot_value_stocks(graph_type = "valueEBITDA")
graph1
graph2
graph3
graph4


    

# %% [markdown]
# ### **Scheduling**
# 
# The project was initially intended to run on a scheduled basis using the schedule and time modules. However, it was discovered that running it on a scheduled basis would often break the dataframe for df1. The reason for this is that in the Valuation Measures section of Yahoo Finance, the values are often missing - particularily, in the afternoon and during weekends. Nonetheless, although the down-times did predict a pattern, the pattern was nowhere near definitive enough to find a suitable schedule. 
# 
# As such, the schedule and time module was imported and pip installed, however, remained out of use. Run all when needed is likely to provide more consistent results when needed. 
# 
# Other methods of automating would be running a cronjob. However, since the main purpose of the project is the visualisations, no interpretation could be made if the project ran in the background. 


