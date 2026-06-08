import numpy as np
import networkx as nx
import multipers as mp
from src.bifiltrations import construct_bifiltration

import multipers.array_api.numpy as _mp_np_api

def _patched_device(x):
    return "cpu" if isinstance(x, np.ndarray) else x.device

def _patched_to_device(x, device):
    return x if isinstance(x, np.ndarray) else x.to_device(device)

_mp_np_api.device    = _patched_device
_mp_np_api.to_device = _patched_to_device

def to_dict(pts, weights, decimals: int = 8) -> dict:
    d = {}
    for p, w in zip(pts, weights):
        key = tuple(np.round(p, decimals))
        d[key] = d.get(key, 0) + w
    return d

def signed_measure_dist(G1: nx.Graph, G2: nx.Graph, degree: int = 0,
                        max_dim: int=2, Rips: bool =False) -> float:
    """

    """

    st1 = construct_bifiltration(G1, max_dim=max_dim, Rips=Rips)
    st2 = construct_bifiltration(G2, max_dim=max_dim, Rips=Rips)

    sm1 = mp.signed_measure(st1, invariant="rank", degree=degree)[0]
    sm2 = mp.signed_measure(st2, invariant="rank", degree=degree)[0]

    pts1, w1 = sm1
    pts2, w2 = sm2

    distance = 0.0
    if len(w1) == 0 and len(w2) == 0:
        return distance
       
    else:

        d1 = to_dict(pts1, w1)
        d2 = to_dict(pts2, w2)
        all_keys = set(d1) | set(d2)
        dist = sum(abs(d1.get(k, 0) - d2.get(k, 0)) for k in all_keys)
        distance = float(dist)

    return distance

def check_if_graphs_are_isomorphic(G1: nx.Graph, G2: nx.Graph, max_dim: int = 2, Rips: bool = False, threshold: float = 10e-8) -> bool:
    """
    Checks if two graphs are isomorphic by comparing their signed measures.
    """
    graphs_are_isomorphic = True

    for degree in range(1, max_dim + 1):
        distance = signed_measure_dist(G1, G2, degree=degree, max_dim=max_dim, Rips=Rips)
    
        if distance > threshold:
            graphs_are_isomorphic = False
            break

    return graphs_are_isomorphic