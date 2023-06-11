# stdlib modules
from typing import List

# third-party modules
import networkx as nx
from networkx import Graph

# custom modules
import tree as t
from tree import Tree

def build_graph(
        ids: List[int],
        xs: List[float], 
        ys: List[float], 
        k: int = 3) -> Graph:
    """"""
    tree = t.Tree(ids, xs, ys) # build 2D-tree for efficient spatial search
    G = nx.Graph()
    nodes = [(ids[i], {'x': xs[i], 'y': ys[i]}) for i in range(len(xs))]
    G.add_nodes_from(nodes)
    edges = []
    for query_id, x, y in zip(ids, xs, ys):
        query = [x, y]
        dists, nns = tree.nearest_neighbors(query, tree.root, k=k)
        near = [(query_id, nn.id, d) for nn, d in zip(nns, dists)]
        edges += near
    G.add_weighted_edges_from(edges)

    return G

def path_plan(
        ids: List[int],
        p: List[float],
        q: List[float],
        G: Graph,
        T: Tree,
        k: int = 3):
    """"""
    id_p, id_q = ids
    G.add_node(id_p)
    dists_p, near_p = T.nearest_neighbors(p, T.root, k=k)
    edges = [(id_p, nn.id, d) for nn, d in zip(near_p, dists_p)]
    G.add_weighted_edges_from(edges)

    dists_q, near_q = T.nearest_neighbors(q, T.root, k=k)
    edges = [(id_q, nn.id, d) for nn, d in zip(near_q, dists_q)]
    G.add_weighted_edges_from(edges)

    return G
