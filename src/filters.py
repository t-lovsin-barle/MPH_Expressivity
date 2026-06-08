import numpy as np
import networkx as nx


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


def degree_weights(G : nx.Graph, superlevelfiltration : bool = True) -> nx.Graph:
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