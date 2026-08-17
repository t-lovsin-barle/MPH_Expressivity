import numpy as np
import networkx as nx

from pyrivet import rivet


def construct_bifiltration(
    G: nx.Graph,
    max_dim: int = 2,
    Rips: bool = True,
    homology: int = 0,
):
    """
    Construct the RIVET degree-Rips bifiltration for G.

    The interface is kept close to the existing multipers-based
    construct_bifiltration function so that the experimental code
    can be switched between implementations easily.

    Only the Rips + degree case is supported by this implementation.
    """
    if not Rips:
        raise NotImplementedError(
            "The RIVET implementation currently supports only "
            "the Rips + degree bifiltration."
        )

    if homology not in (0, 1):
        raise ValueError(
            "The RIVET implementation currently supports H_0 and H_1."
        )

    return build_rips_bifiltration(
        G,
        max_dim=max_dim,
        homology=homology,
    )


def build_rips_bifiltration(
    G: nx.Graph,
    max_dim: int = 2,
    homology: int = 0,
):
    """
    Build and compute the degree-Rips bifiltration using RIVET.

    The first parameter is the degree filtration and the second
    parameter is the shortest-path distance filtration.
    """
    nodes = list(G.nodes())

    if len(nodes) == 0:
        raise ValueError(
            "Cannot construct a bifiltration from an empty graph."
        )

    # Use shortest-path distances on the graph as the metric.
    D = nx.floyd_warshall_numpy(G, nodelist=nodes)
    D = np.asarray(D, dtype=float)

    if not np.isfinite(D).all():
        raise ValueError(
            "The graph must be connected so that all shortest-path "
            "distances are finite."
        )

    # Degree values in exactly the same vertex order as D.
    degree_values = [
        float(G.degree(v))
        for v in nodes
    ]

    n = len(nodes)

    distance_matrix = [
        [float(D[i, j]) for j in range(n)]
        for i in range(n)
    ]

    metric_space = rivet.MetricSpace(
        appearance_label="degree",
        distance_label="rips distance",
        appearance_values=degree_values,
        distance_matrix=distance_matrix,
    )

    return rivet.compute_metric_space(
        metric_space,
        homology=homology,
    )