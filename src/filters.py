import numpy as np
import networkx as nx
from src.experimental_WL_filter_helpers import compute_wl_labels, l1_distance, label_to_counter


def get_filters():
    FILTERS ={
        'forman ricci': forman_ricci_weights,
        'degree': degree_weights,
        'laplacian': laplacian_weights,
        'hks': hks_weights,
        'wl': wl_weights
    }
    return FILTERS

def forman_ricci_weights(G : nx.Graph, superlevelfiltration : bool = False) -> nx.Graph:

    '''
    Returns the Forman-Ricci curvature of a graph G. TODO: Think if a superlevel filtration makes sense here.
    '''

    if superlevelfiltration:
        sign = -1
    else:
        sign = 1
    
    G_ = G.copy()

    for v in G.nodes():
        G_.nodes[v]['weight'] = sign * (-1)
    for v, u in G.edges():
        G_[v][u]['weight'] = sign * (4 - G.degree(v) - G.degree(u) + 3*len(set(G.neighbors(v)) & set(G.neighbors(u))))
    return G_


def degree_weights(G : nx.Graph, superlevelfiltration : bool = False) -> nx.Graph:
    '''
    Returns a weighted graph suitable for a superlevel filtration.
    '''
    
    if superlevelfiltration:
        sign = -1
    else:
        sign = 1

    G_ = G.copy()
    for v in G.nodes():
        G_.nodes[v]['weight'] = sign * G.degree(v)
    for v, u in G.edges():
        G_[v][u]['weight'] = sign * (max(G.degree(v), G.degree(u)))
    return G_

def laplacian_weights(G : nx.Graph, superlevelfiltration : bool= False) -> nx.Graph:
    '''
    It is not entirely clear to me how this works, but it is based on the PH-Expressivity scripts.
    '''

    if superlevelfiltration:
        sign = -1
    else:
        sign = 1
    
    G_ = G.copy()
    eigenvalues = nx.laplacian_spectrum(G)
    for v in G.nodes():
        G_.nodes[v]['weight'] = sign * eigenvalues[v]
    for v, u in G.edges():
        G_[v][u]['weight'] = sign * (max(eigenvalues[v], eigenvalues[u]))
    return G_

def hks_weights(G : nx.Graph, t: float = 10.0, superlevelfiltration: bool = False) -> nx.Graph:
    '''
    Returns HKS weights for a graph G.
    '''

    L = nx.normalized_laplacian_matrix(G).toarray()
    eigenvalues, eigenvectors = np.linalg.eigh(L)  
    diagonal = (eigenvectors**2) @ np.exp(-t * eigenvalues)
    list = list(diagonal)

    if superlevelfiltration:
        sign = -1
    else:
        sign = 1

    G_ = G.copy()
    for v in G.nodes():
        G_.nodes[v]['weight'] = sign * list[v]
    for v, u in G.edges():
        G_[v][u]['weight'] = sign * (max(list[v], list[u]))
    return G_



def wl_weights(G: nx.Graph, superlevelfiltration: bool = False, tau: float = 1) -> nx.Graph:

    lbs, prev_lbs = compute_wl_labels(G)
    counters = [label_to_counter(l) for l in lbs]

    if superlevelfiltration:
        sign = -1
    else:
        sign = 1

    G_ = G.copy()
    for v, u in G.edges():
        G_[v][u]['weights'] = sign*(int(prev_lbs[v] != prev_lbs[u]) + l1_distance(counters[v], counters[u]) + tau)

    for v in G.nodes():
        nbr_weights = [
        G_[v][nbr]['weights']
        for nbr in G_.neighbors(v)
        ]
        nbr_weights.append(0)
        G_.nodes[v]['weights'] = sign*max(nbr_weights)

    return G_
