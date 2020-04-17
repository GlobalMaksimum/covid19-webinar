import pandas as pd
from tqdm import tqdm
import os.path
from loguru import logger
from covid.helper import __my_flatten_cols
import numpy as np

__base__ = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports'


def download_or_cache(file: str):
    csv, ext = os.path.splitext(file)

    cache_dir = '/tmp/covid19'

    os.makedirs(cache_dir, exist_ok=True)

    parquet_file = os.path.join(cache_dir, f"{csv}.parq")

    if not os.path.exists(parquet_file):
        url = os.path.join(__base__, file)
        logger.debug(url)
        df_d = pd.read_csv(url)

        df_d.to_parquet(parquet_file)

    df = pd.read_parquet(parquet_file)

    return df


def map_loc(rec):
    if rec.Country in ['Spain', 'Italy', 'France', 'Germany', 'Iran', 'United Kingdom', 'Turkey', 'Switzerland',
                       'Belgium', 'Netherlands', 'Brazil', 'Austria', 'Portugal', 'Israel', 'Korea, South',
                       'Sweden''Russia', 'Norway', 'Ireland', 'India', 'Denmark', 'Chile', 'Czechia', 'Poland',
                       'Romania', 'Pakistan', 'Malaysia', 'Japan', 'Philippines', 'Ecuador', 'Luxembourg', 'Peru',
                       'Saudi Arabia', 'Indonesia', 'Serbia', 'Mexico']:
        return rec.Country
    else:
        return f"{rec.Country}, {rec.Province}"


def load_data(start_date: str = '01-22-2020', end_date: str = '04-16-2020', normalized: bool = True,
              min_confirmed: int = 100):
    dt_range = pd.date_range(start=pd.to_datetime(start_date), end=pd.to_datetime(end_date))

    dfs = []
    for d in tqdm(dt_range):
        day, month, year = d.date().day, d.date().month, d.date().year

        df_d = download_or_cache(f"{month:02}-{day:02}-{year}.csv")
        df_d['Day'] = d.date()

        dfs.append(df_d)

    df = pd.concat(dfs, ignore_index=True)

    del dfs

    if normalized:
        df['Country'] = df['Country_Region'].fillna(df['Country/Region'])
        df['Province'] = df['Province_State'].fillna(df['Province/State']).fillna('')

        df.drop(['Province/State', 'Country/Region', 'Last Update', 'Latitude', 'Longitude', 'FIPS', 'Admin2',
                 'Province_State', 'Country_Region', 'Last_Update', 'Lat', 'Long_', 'Combined_Key'], axis=1,
                inplace=True)

        df['Confirmed'] = df.Confirmed.fillna(0)
        df['Deaths'] = df.Deaths.fillna(0)
        df['Recovered'] = df.Recovered.fillna(0)
        df['Active'] = df.Active.replace(0, np.NaN).fillna(df.Confirmed - df.Deaths - df.Recovered)

        d = {'Mainland China': 'China', 'South Korea': 'Korea, South'}

        df['Country'] = df.Country.map(lambda key: d.get(key, key))

        # df["Location"] = df.apply(lambda r: map_loc(r), axis=1)

        df = df.groupby(['Country', 'Province', 'Day']).sum().reset_index()

    if min_confirmed:
        pd.DataFrame.my_flatten_cols = __my_flatten_cols
        filt = df.groupby(['Country', 'Province'], sort='Day').agg(
            {'Day': ['min', 'max'], 'Confirmed': ['max']}).reset_index().my_flatten_cols()
        filt = filt[(filt.Day_max == pd.to_datetime(end_date)) & (filt.Confirmed_max >= min_confirmed)]

        df = df.merge(filt[['Country', 'Province']], on=['Country', 'Province'], validate='many_to_one').copy()

    return df


def load_who_data():
    d = pd.read_csv('/tmp/WHO-COVID-19-global-data.csv', parse_dates=True)

    return d
