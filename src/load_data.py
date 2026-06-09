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
        'cay12':r'cay\minCayleyGraphs12Vertices.g6',
        'cay16':r'cay\minCayleyGraphs16Vertices.g6',
        'cay20':r'cay\minCayleyGraphs20Vertices.g6',
        'cay24':r'cay\minCayleyGraphs24Vertices.g6',
        'cay32':r'cay\minCayleyGraphs32Vertices.g6',
        'cay36':r'cay\minCayleyGraphs36Vertices.g6',
        'cay60':r'cay\minCayleyGraphs60Vertices.g6',
        'cay63':r'cay\minCayleyGraphs63Vertices.g6',
        '16622':r'SR\sr16622.g6',
        '251256':r'SR\sr251256.g6',
        '261034':r'SR\sr261034.g6',
        '281264':r'SR\sr281264.g6',
        '291467':r'SR\sr291467.g6',
        '351668':r'SR\sr351668.g6',
        '351899':r'SR\sr351899.g6',
        '361446':r'SR\sr361446.g6',
        '401224':r'SR\sr401224.g6',
        'cub06':r'cubic\cub06.g6',
        'cub08':r'cubic\cub08.g6',
        'cub10':r'cubic\cub10.g6',
        'cub12':r'cubic\cub12.g6',
        'cub14':r'cubic\cub14.g6',
    }


    path = Path(r'.\external\PH_expressivity\data\simple_isomorphism_datasets')
    OTHER_GRAPHS = {}
    
    for graph_set, filename in OTHER_DATA.items():
        with open(path / filename, "rb") as fn:

            OTHER_GRAPHS[graph_set] = [nx.from_graph6_bytes(line.strip()) for line in fn]
    
    return OTHER_GRAPHS
    
