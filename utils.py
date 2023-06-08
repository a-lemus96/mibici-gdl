# stdlib modules
import os

# third-party modules
from matplotlib import pyplot as plt
import numpy as np
from numpy import ndarray
import pandas as pd
from pandas import DataFrame

def to_global(coords: DataFrame) -> DataFrame:
    """"""
    lat_mean = np.average(coords['latitude'])
    lon_mean = np.average(coords['longitude'])
    r = 6371.0 # earth's radius
    dlon = np.pi * (coords['longitude'] - lon_mean) / 180.0
    dlat = np.pi * (coords['latitude'] - lat_mean) / 180.0
    x = r * dlon * np.cos(np.pi * lat_mean / 180.0)
    y = r * dlat

    return (pd.concat([x, y], axis=1)).rename(columns={'longitude': 'x',
                                                       'latitude': 'y'})

def load_ecobici(fname: str) -> DataFrame:
    """"""
    df = pd.read_csv(os.path.join('data', fname), encoding='ISO-8859-1')
    glob = to_global(df[['latitude', 'longitude']])

    return pd.concat([df['id'], glob], axis=1)

def plot_positions(ax, coords: DataFrame) -> None:
    """"""
    #ax.scatter(coords[])
    pass
