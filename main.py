# stdlib modules
import argparse

# third-party modules
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

# local modules
import graph
import tree
import utils


# configure arg parser
parser = argparse.ArgumentParser()
parser.add_argument('-fname', type=str, default='nomenclatura_2023_05.csv',
                    help='CSV filename containing stations information')
# parse args
args = parser.parse_args()

colors = ['red', 'orange', 'brown', 'green', 'cyan', 'magenta', 'black', 'gray']
count = 0

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
    
    if np.random.choice([True] + 20*[False]) and count < 1:
        c = np.random.choice(colors)
        rect = Rectangle((max(-6, node.xmin), max(node.ymin, -6)),
                         min(node.xmax, 7) - max(node.xmin, -6),
                         min(node.ymax, 7) - max(node.ymin, -6),
                         facecolor=c,
                         alpha=0.5)
        ax.scatter(node.x, node.y, color=c, linewidth=1)
        ax.add_patch(rect)
        count += 1
        _, nns = tree.nearest_neighbors([node.x, node.y], tree.root, k=4)
        for nn in list(nns):
            ax.scatter(nn.x, nn.y, color='red', linewidth=1)
        

def draw(ax, tree: tree.Tree) -> None:
    draw_subtree(ax, tree.root, 0, colors[6])

K=3
positions = utils.load_ecobici(args.fname) # load station xy coords
tree = tree.Tree(positions['id'], positions['x'], positions['y'])
fig, ax = plt.subplots(figsize=(9,9))
#ax.scatter(positions['x'], positions['y'], linewidth=0.05, color='green')
G = graph.build_graph(positions['id'], positions['x'], positions['y'], k=K)
glocs = {node_id: (x, y) for node_id, x, y in zip(positions['id'],
                                                  positions['x'],
                                                  positions['y'])}
#print(glocs)
#draw(ax, tree)
points = np.random.uniform(-6, 7, size=(2, 2))
p, q = tuple(map(tuple, points))
glocs['p'] = (p)
glocs['q'] = (q)
G, path = graph.path_plan(ids=['p', 'q'], p=p, q=q, G=G, T=tree, k=K)
colors = ['blue' if node == 'p' or node == 'q' else 'green' for node in G.nodes()]
nx.draw(G, pos=glocs, ax=ax, node_size=25, node_color=colors)
path_edges = list(zip(path, path[1:]))
nx.draw_networkx_nodes(G, glocs, nodelist=path, node_color='r', node_size=25)
nx.draw_networkx_edges(G, glocs, edgelist=path_edges, edge_color='r', width=1)
plt.show()
