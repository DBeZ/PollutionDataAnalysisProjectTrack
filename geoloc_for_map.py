import geopandas
from geopy.extra.rate_limiter import RateLimiter
import geopy
import pandas as pd
from load_data import load_data_from_pickle
from save_data import export_to_csv, save_as_pickel
import os
import multiprocessing


#######################
# City to Gelocation  #
#######################

# Use multithreading to speed up the conversion of city name to geoloc.
# However it is not allowe by the api
def convert_city_to_geoloc_multithreading(data, city_col):
    geoloc_df = pd.DataFrame()
    geoloc_df["Yeshuv"] = data[city_col].unique()
    geoloc_df.dropna(axis=0, how='any', inplace=True)
    geoloc_list = geoloc_df["Yeshuv"].to_list()
    locator = geopy.Nominatim(country_bias='Israel', user_agent="myGeocoder", timeout=4)
    geocode_rate_limited = RateLimiter(locator.geocode,
                                       min_delay_seconds=1.5)  # delay between geocoding calls, pre-requisite of API
    pool = multiprocessing.Pool(processes=1)  # multiprocessing.cpu_count() gives 12 CPUs
    addresses = pool.map(geocode_rate_limited, geoloc_list)
    return addresses


def convert_city_to_geoloc(data, city_col):
    geoloc_df = pd.DataFrame()
    geoloc_df["yeshuv"] = data[city_col].unique()
    geoloc_df.dropna(axis=0, how='any', inplace=True)
    locator = geopy.Nominatim(country_bias='Israel', user_agent="myGeocoder", timeout=4)
    geocode = RateLimiter(locator.geocode, min_delay_seconds=1.5)  # delay between geocoding calls, pre-requisite of API
    geoloc_df['location'] = geoloc_df['yeshuv'].apply(geocode)  # create location column
    geoloc_df['point'] = geoloc_df['location'].apply(lambda loc: tuple(
        loc.point) if loc else None)  # create longitude, laatitude and altitude from location column (returns tuple)
    return geoloc_df


def geoloc_loader(data, city_col):
    pickel_name = "city_geolocations"
    if os.path.isfile(os.getcwd() + "\\" + pickel_name + ".pkl"):
        geoloc = load_data_from_pickle(pickle_file_name=pickel_name)
    else:
        geoloc_df = convert_city_to_geoloc(data=data, city_col=city_col)
        save_as_pickel(dataframe=geoloc_df, save_file_name=pickel_name)
        geoloc = load_data_from_pickle(pickle_file_name=pickel_name)
    # geoloc_dict = dict(zip(geoloc["yeshuv"], geoloc['point']))
    return geoloc
