import pandas as pd
import random
from datetime import datetime, timedelta

df = pd.read_csv("data/sampleData.csv") # change depend on working directory

def calculateVWAP(date: str, exchange: str, dataframe: pd.DataFrame) -> pd.Series:
    '''
    date: YYYY-MM-DD

    exchange: N or O (N = NYSE, O = NASDAQ)

    Return: pandas series with vwap values for each stock on
    a given exchange
    '''

    df = dataframe[(dataframe["exchange"] == exchange)
                   & (dataframe["date"] == date)].copy()
    
    if len(df) == 0 and len(dataframe) != 0:
        raise ValueError("Incorrect Date or Exchange")

    df["total"] = df["price"] * df["size"]          # new col named "total"
    stockGroup = df.groupby(["date","stock"])
    group = stockGroup[["size","total"]].sum()
    group["vwap"] = group["total"] / group["size"]

    return group["vwap"]

def exchangeDict(date: str,dataframe: pd.DataFrame, selected_exchanges = None) -> dict[str, pd.Series]:
    '''
    date: YYYY-MM-DD

    selected_exchanges: array[str], list of exchanges rather than all within provided dataframe

    Return: dictionary with the key as the exchange and the
    value as a pandas series containing the vwap of each stock
    '''

    exchanges_arr = dataframe["exchange"].unique()

    if selected_exchanges is not None:
        for i in selected_exchanges:
            if i not in exchanges_arr:
                raise ValueError(f"exchange: {i} in selected_exchanges was not found in data")
        exchanges_arr = selected_exchanges

    exchanges_dict = {}

    for i in exchanges_arr:
        exchanges_dict[i] = calculateVWAP(date,i,dataframe)
    
    return exchanges_dict


def highestVWAP(dataSeries: dict, exchange_prio = None, sort_by_difference = False) -> pd.DataFrame:
    '''
    dataSeries: dict, with key as exchange and value as pd.series including
    stock as index and vwap as the values

    exchange_prio: str, passing an exchange will only show stocks for which that exchange has the
    highest vwap

    sort_by_difference: boolean, True for difference to be sorted high -> low
    '''

    df = pd.concat(dataSeries, axis = 1) # this uses the dictionary key as the cols
    max_vwap = df.max(axis = 1)
    max_exchange = df.idxmax(axis=1) # if two vwaps are equal, prioritises the 1st encounter

    df_final = pd.DataFrame({"vwap" : max_vwap, "exchange" : max_exchange})

    if len(dataSeries) == 2:
        df_final["difference"] = abs(df.iloc[:,0] - df.iloc[:,1])
        
        if sort_by_difference:
            df_final = df_final.sort_values(["difference"], ascending=False)

    if exchange_prio is None:
        return df_final
    
    else:
        df_prio = df_final[df_final["exchange"] == exchange_prio]

        if len(df_prio) == 0:
            raise ValueError("This exchange didn't have any stocks with the highest vwap")
        
        else:
            return df_prio


def generateData(dataframe,exchanges,pricestart,priceend):
    df = dataframe
    timestart = datetime.strptime("08:00:00.000","%H:%M:%S.%f")
    timeend = datetime.strptime("18:55:20.000","%H:%M:%S.%f")
    current_time = timestart

    rows = []

    while current_time < timeend:

        current_time += timedelta(milliseconds=random.randint(3000,5000))

        rows.append({"date": "2021-10-01", 
                            "time": current_time,
                            "stock": "NVDA",
                            "price": round(random.uniform(pricestart,priceend),2),
                            "size": random.randint(1,300),
                            "exchange": random.choice(exchanges)})

    df2 = pd.DataFrame(rows)
    return pd.concat([df,df2],ignore_index=True)


def differentDayVWAP(dataframe,startdate,enddate,selected_exchanges=None):
    current_date = startdate
    exchanges_arr = dataframe["exchange"].unique()

    while current_date < enddate:
        current_date += timedelta(days = 1)
        
    return 0

start = datetime.strptime("2021-10-01", "%Y-%m-%d")
end = datetime.strptime("2022-10-01","%Y-%m-%d")

differentDayVWAP(df,start,end)

df2 = generateData(df,['N','K'],45,47)

print(highestVWAP(exchangeDict("2021-10-01",df2,selected_exchanges=['N','K']), sort_by_difference = True))






