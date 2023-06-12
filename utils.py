# stdlib modules
import os

# third-party modules
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
from numpy import ndarray
import pandas as pd
from pandas import DataFrame

# custom modules
import tree

colors = ['red', 'orange', 'brown', 'green', 'cyan', 'magenta', 'black', 'gray']
count = 0

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

def plot_positions(ax, x, y):
    """"""
    ax.scatter(x, y, linewidth=0.05, color='green')
    ax.grid(True)

    return ax


def draw_subtree(ax, node: tree.TreeNode, s: int, color: str) -> None:
    global count
    width = 1
    if node.left != None:
        draw_subtree(ax, node.left, s + 1, color=colors[6])
    # draw current node as a line segment
    if width > 0:
        if node.split_x == True:
            ax.plot(2 * [node.x], [max(-6, node.ymin), min(node.ymax, 7)],
                     linewidth=width, color=color)
        else:
            ax.plot([max(-6, node.xmin), min(node.xmax, 7)], 2 * [node.y],
                     linewidth=width, color=colors[6])

    if node.right != None:
        draw_subtree(ax, node.right, s + 1, color=colors[6])
    
    if np.random.choice([True] + 20*[False]) and count < 4:
        c = np.random.choice(colors)
        rect = Rectangle((max(-6, node.xmin), max(node.ymin, -6)),
                         min(node.xmax, 7) - max(node.xmin, -6),
                         min(node.ymax, 7) - max(node.ymin, -6),
                         facecolor=c,
                         alpha=0.5)
        ax.scatter(node.x, node.y, color=c, linewidth=1)
        ax.add_patch(rect)
        count += 1

def draw_tree(ax, tree: tree.Tree) -> None:
    draw_subtree(ax, tree.root, 0, colors[6])
    ax.grid(True)
    ax.axis('off')

    return ax
