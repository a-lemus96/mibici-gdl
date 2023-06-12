# stdlib modules
import math
from queue import PriorityQueue
from typing import Any, List

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

def get_path(G: Graph, node_id: Any):
    """"""
    parent = G.nodes[node_id]['pred']
    if parent is None:
        return [node_id]
    path = get_path(G, parent) + [node_id]
    
    return path

def relax(G: Graph, u: Any, v: Any, w: float):
    """"""
    relaxed = False
    if G.nodes[v]['d'] > G.nodes[u]['d'] + w:
        G.nodes[v]['d'] = G.nodes[u]['d'] + w
        G.nodes[v]['pred'] = u
        relaxed = True
    elif G.nodes[u]['d'] > G.nodes[v]['d'] + w:
        G.nodes[u]['d'] = G.nodes[v]['d'] + w
        G.nodes[u]['pred'] = v
        relaxed = True
    
    return relaxed, G


def init_single_source(G: Graph, s: Any) -> Graph:
    """"""
    for node_id in list(G.nodes):
        G.nodes[node_id]['d'] = math.inf
        G.nodes[node_id]['pred'] = None

    G.nodes[s]['d'] = 0.

    return G

def bellman_ford_path(G: Graph, p_id: Any, q_id: Any) -> List[Any]:
    """"""
    G = init_single_source(G, p_id) # initialize nodes
    for _ in range(len(G.nodes) - 1):
        for u, v, w in G.edges(data='weight'):
            relaxed, G = relax(G, u, v, w)

    # compute path
    path = get_path(G, q_id)
    print(path)
    if path[0] != p_id:
        raise RuntimeError(f'There is no path between nodes {p_id} and {q_id}')

    return path
            

def dijkstra_path(G: Graph, p_id: Any, q_id: Any) -> List[Any]:
    """"""
    G = init_single_source(G, p_id) # initialize nodes
    S = set() # initialize set of path vertices
    Q = PriorityQueue() # priority queue
    Q.put((G.nodes[p_id]['d'], p_id)) # insert root into Q
    while not Q.empty():
        _, u = Q.get()
        S.add(u)
        for v in G.neighbors(u):
            if v not in S:
                # retrieve edge weight
                edge_data = G.get_edge_data(u, v)
                w = edge_data['weight']
                # perform edge relaxation
                relaxed, G = relax(G, u, v, w)
                if relaxed is True:
                    Q.put((G.nodes[v]['d'], v))

    # compute path
    path = get_path(G, q_id)
    if path[0] != p_id:
        raise RuntimeError(f'There is no path between nodes {p_id} and {q_id}')

    return path


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
    path = dijkstra_path(G, id_p, id_q)

    return G, path
