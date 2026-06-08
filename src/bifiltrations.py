import numpy as np
import networkx as nx
import multipers as mp
import multipers.filtrations as mpf
from src.filters import forman_ricci_weights, degree_weights, laplacian_weights, hks_weights

def construct_bifiltration(G : nx.Graph, max_dim : int = 2, Rips : bool = False) -> mp.SimplexTreeMulti:

    if Rips:
        return build_rips_bifiltration(G, max_dim=max_dim)
    else:
        return build_bifiltration(G, max_dim=max_dim)


def build_rips_bifiltration(G: nx.Graph, max_dim: int = 2) -> mp.SimplexTreeMulti:

    nodes = list(G.nodes())
    D = nx.floyd_warshall_numpy(G, nodelist=nodes)
    D = np.asarray(D, dtype=float)

# Lower-star function on vertices
# Example: negative degree (high-degree vertices appear first)
    f = degree_weights(G, superlevelfiltration=True)

# Rips-Lowerstar bifiltration
    st = mpf.RipsLowerstar(distance_matrix=D, function=f)
    
    st.collapse_edges(full=True)
    st.expansion(max_dim=max_dim)
    st.make_filtration_non_decreasing()

    return st

def build_bifiltration(G: nx.Graph, max_dim: int = 2) -> mp.SimplexTreeMulti:
    """
    TODO: Implement variable filters
    """

    G_first_filter = laplacian_weights(G)
    G_second_filter = forman_ricci_weights(G)

    st = mp.SimplexTreeMulti(num_parameters=2)

    for v in G.nodes():
        vertex_weight_1 = G_first_filter.nodes[v]['weight']
        vertex_weight_2 = G_second_filter.nodes[v]['weight']
        st.insert([v], [float(vertex_weight_1), float(vertex_weight_2)])
   
        
    for u,v in G.edges():
        edge_weight_1 = G_first_filter[u][v]['weight']
        edge_weight_2 = G_second_filter[u][v]['weight']
        st.insert([u,v], [float(edge_weight_1), float(edge_weight_2)])


    st.make_filtration_non_decreasing()
    st.collapse_edges(full=True)
    st.expansion(max_dim=max_dim)

    return st