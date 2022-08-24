
from pycoingecko import CoinGeckoAPI
import time
from datetime import date
import pandas as pd

def get_price_to_date(currency="strong", start_date="01/01/2011"):
    cg = CoinGeckoAPI()
    cg.get_price(ids='strong', vs_currencies='Eur')

    start_date = "01/01/2011"
    start_date = pd.to_datetime(start_date)
    today = date.today()

    date_range = [start_date, today]
    date_range = list(map(pd.to_datetime, date_range))
    date_range = list(map(lambda x:x.strftime('%s'), date_range))
    chart_data_from_API = cg.get_coin_market_chart_range_by_id(id='strong',vs_currency='eur',from_timestamp=date_range[0],to_timestamp=date_range[1])

    df_list = []
    for key in chart_data_from_API.keys():
        df = pd.DataFrame.from_dict(chart_data_from_API[key])
        df = df.rename(columns={0: "Date", 1: key})
        df["Date"] = pd.to_datetime(df["Date"], unit='ms')
        # df["Date"] = pd.to_datetime(df["Date"], format='%Y%m%d%H%M%S', errors='coerce')
        df= df.set_index("Date")
        df_list.append(df)
    price_df = pd.concat(df_list, axis=1)
    price_df = price_df.rename(columns={"prices": "price"})

    return price_df

