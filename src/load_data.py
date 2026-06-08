import numpy as np
import networkx as nx
from pathlib import Path

def load_BREC_data():

    BREC_DATA = {
        'basic':'basic.npy', # encode
        'regular':'regular.npy',
        'strongly regular':'str.npy', #enocde
        'extension':'extension.npy',
        'CFI':'cfi.npy',
        '4vtx':'4vtx.npy', #encode
        'DR':'dr.npy'
    }

    path = Path(r'.\external\BREC\customize\Data\raw')
    BREC_GRAPHS = {}

    for graph_set, filename in BREC_DATA.items():
        BREC_GRAPHS[graph_set] = np.load(path / filename)
    
    return BREC_GRAPHS

def load_other_data():

    OTHER_DATA={
        'cay12':'minCayleyGraphs12Vertices.g6',
        'cay16':'minCayleyGraphs16Vertices.g6',
        'cay20':'minCayleyGraphs20Vertices.g6',
        'cay24':'minCayleyGraphs24Vertices.g6',
        'cay32':'minCayleyGraphs32Vertices.g6',
        'cay36':'minCayleyGraphs36Vertices.g6',
        'cay60':'minCayleyGraphs60Vertices.g6',
        'cay63':'minCayleyGraphs63Vertices.g6',
        '16622':'sr16622.g6',
        '251256':'sr251256.g6',
        '261034':'sr261034.g6',
        '281264':'sr281264.g6',
        '291467':'sr291467.g6',
        '351668':'sr351668.g6',
        '351899':'sr351899.g6',
        '361446':'sr361446.g6',
        '401224':'sr401224.g6',
        'cub06':'cub06.g6',
        'cub08':'cub08.g6',
        'cub10':'cub10.g6',
        'cub12':'cub12.g6',
        'cub14':'cub14.g6',
    }


    path = Path(r'.\external\BREC\customize\Data\raw')
    OTHER_GRAPHS = {}
    
    for graph_set, filename in OTHER_DATA.items():
        with open(path / filename, "rb") as fn:

            OTHER_GRAPHS[graph_set] = [nx.from_graph6_bytes(line.strip()) for line in fn]
    
    return OTHER_GRAPHS
    
