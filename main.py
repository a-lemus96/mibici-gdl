# stdlib modules
import argparse

# third-party modules
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

# local modules
import graph
import tree
import utils


# configure arg parser
parser = argparse.ArgumentParser()
parser.add_argument('-fname', type=str, default='nomenclatura_2023_05.csv',
                    help='CSV filename containing stations information')
parser.add_argument('-method', type=str, default='dijkstra',
                    help='Method for shortest-path computation')
# parse args
args = parser.parse_args()



K=3
# compute and plot (x, y) positions
positions = utils.load_ecobici(args.fname) # load station xy coords
fig, ax = plt.subplots(figsize=(6,6))
plt.tight_layout()
ax = utils.plot_positions(ax, positions['x'], positions['y'])
plt.savefig("out/locations.png")

# build tree and draw it
T = tree.Tree(positions['id'], positions['x'], positions['y'])
fig, ax = plt.subplots(figsize=(6,6))
plt.tight_layout()
ax = utils.plot_positions(ax, positions['x'], positions['y'])
ax = utils.draw_tree(ax, T)
plt.savefig("out/2d-tree.png")

# build graph and plot it
G = graph.build_graph(positions['id'], positions['x'], positions['y'], k=K)
glocs = {node_id: (x, y) for node_id, x, y in zip(positions['id'],
                                                  positions['x'],
                                                  positions['y'])}
fig, ax = plt.subplots(figsize=(6,6))
plt.tight_layout()
nx.draw(G, pos=glocs, ax=ax, node_size=25, node_color='green')
plt.savefig("out/graph.png")

# create two random points
points = np.random.uniform(-6, 7, size=(2, 2))
p, q = tuple(map(tuple, points))
glocs['p'] = (p)
glocs['q'] = (q)
# connect them to the graph
G = graph.connect_query_points(G, T, ['p', 'q'], p, q, k=K)
# draw graph
colors = ['blue' if node == 'p' or node == 'q' else 'green' for node in G.nodes()]
fig, ax = plt.subplots(figsize=(6,6))
plt.tight_layout()
nx.draw(G, pos=glocs, ax=ax, node_size=25, node_color=colors)

# find shortest path between query nodes
G, path = graph.path_plan(id_p='p', id_q='q', G=G, method=args.method)
path_edges = list(zip(path[:-1], path[1:]))
colors = ['blue' if node == 'p' or node == 'q' else 'red' for node in path]
nx.draw_networkx_nodes(G, glocs, nodelist=path, node_color=colors, node_size=25)
nx.draw_networkx_edges(G, glocs, edgelist=path_edges, edge_color='r', width=1)
plt.savefig("out/path.png")
plt.show()
